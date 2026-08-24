# -*- coding: utf-8 -*-
"""Desktop Duplication, as an iterator.

    with DesktopCapture(CaptureOptions(output=0)) as capture:
        for frame in capture:
            process(frame.array)

Everything the C++ sample spreads across three classes lives inside that loop:
``AcquireNextFrame``, the cursor-only skip, the staging copy, ``Map``, the
delivery, ``Unmap``, ``ReleaseFrame``, and the rebuild after the duplication is
invalidated.

Nothing is allocated per frame. The staging texture, the two SDK structures and
the ``Frame`` object are created once and reused, so a steady-state loop does no
allocation at all - which the test suite asserts rather than trusting.
"""
import ctypes
import time

import comtypes

from Direct3D.PyIdl.d3d11 import (
    D3D11_BOX, D3D11_CPU_ACCESS_READ, D3D11_MAP_READ,
    D3D11_MAPPED_SUBRESOURCE, D3D11_TEXTURE2D_DESC, D3D11_USAGE_STAGING,
    ID3D11Resource, ID3D11Texture2D,
)
from Direct3D.PyIdl.d3dcommon import D3D_DRIVER_TYPE_UNKNOWN
from Direct3D.PyIdl.dxgi import IDXGIResource
from Direct3D.PyIdl.dxgi1_2 import (
    DXGI_OUTDUPL_FRAME_INFO, IDXGIOutput1, IDXGIOutputDuplication,
)
from Direct3D.PyIdl.functions import D3D11CreateDevice
from Direct3D.PyIdl.status import (
    DXGI_ERROR_ACCESS_LOST, DXGI_ERROR_DEVICE_REMOVED,
    DXGI_ERROR_UNSUPPORTED, DXGI_ERROR_WAIT_TIMEOUT, AccessLost, name_of,
    raise_for,
)

from Direct3D.Capture.enumerate import resolve_output
from Direct3D.Capture.frame import Frame
from Direct3D.Capture.options import CaptureOptions

#: DXGI_FORMAT_B8G8R8A8_UNORM. Desktop Duplication delivers this and only this.
_FORMAT_B8G8R8A8_UNORM = 87

#: Progressive back-off between rebuild attempts, in seconds. The C++ sample
#: calls this DYNAMIC_WAIT and it was never ported (F-02). Without it, a display
#: that stays unavailable - a fullscreen-exclusive game, a locked session -
#: turns the rebuild into a spin loop that pins a core.
_REBUILD_BACKOFF = (0.0, 0.01, 0.05, 0.1, 0.25, 0.5)


def _value(constant):
    return constant.value if hasattr(constant, "value") else constant


def _hresult(exc):
    return exc.hresult & 0xFFFFFFFF


class DesktopCapture(object):
    """A duplicated output, delivering frames until you stop asking.

    Use it as a context manager. The device, the duplication and the staging
    texture are COM objects with real lifetimes; leaving the ``with`` block
    drops them in the right order.

    Not thread-safe, and deliberately so. An ``ID3D11DeviceContext`` is not
    free-threaded, and pretending otherwise would produce corruption that
    appears only under load. Capture on one thread and hand frames across.
    """

    def __init__(self, options=None):
        self.options = options if options is not None else CaptureOptions()
        if not isinstance(self.options, CaptureOptions):
            raise TypeError("options must be a CaptureOptions, not %s"
                            % type(self.options).__name__)

        self.output = resolve_output(self.options.output)
        left, top, right, bottom = self.options.region_within(self.output)
        self.width = right - left
        self.height = bottom - top
        self._crop = (left, top, right, bottom)
        self._cropping = (self.width != self.output.width
                          or self.height != self.output.height)

        #: Rebuilds performed since construction. A capture that has been
        #: running for hours across screen locks will have a nonzero count and
        #: nothing is wrong; a count climbing every second means the display is
        #: unavailable and the loop is not going to recover on its own.
        self.rebuilds = 0
        #: Frames skipped because only the cursor moved.
        self.skipped = 0
        #: AcquireNextFrame timeouts. Not errors: the desktop was simply idle.
        self.timeouts = 0

        self._device = None
        self._context = None
        self._duplication = None
        self._staging = None
        self._closed = False

        # Reused across frames. Allocating these per iteration is the whole
        # difference between a loop that does no work and one that does.
        self._info = DXGI_OUTDUPL_FRAME_INFO()
        self._mapped = D3D11_MAPPED_SUBRESOURCE()
        self._box = D3D11_BOX()
        self._box.left, self._box.top, self._box.front = left, top, 0
        self._box.right, self._box.bottom, self._box.back = right, bottom, 1
        self._frame = None
        self._mapped_now = False

        self._open()

    # ---------------------------------------------------------- lifecycle --
    def _open(self):
        """Device on the adapter that owns this output, then duplicate it."""
        self._device, _level, self._context = D3D11CreateDevice(
            adapter=self.output.adapter._adapter,
            driver_type=D3D_DRIVER_TYPE_UNKNOWN)

        output1 = self.output._output.QueryInterface(IDXGIOutput1)
        duplication = ctypes.POINTER(IDXGIOutputDuplication)()
        try:
            output1.DuplicateOutput(self._device, ctypes.byref(duplication))
        except comtypes.COMError as exc:
            code = _hresult(exc)
            if code == DXGI_ERROR_UNSUPPORTED:
                raise_for(code,
                          "DuplicateOutput on %s. This usually means a "
                          "fullscreen-exclusive application owns the display, "
                          "or the desktop is not composited. Setting the game "
                          "to borderless windowed is the fix."
                          % self.output.device_name)
            raise_for(code, "DuplicateOutput on %s" % self.output.device_name)
        self._duplication = duplication

        texture = ctypes.POINTER(ID3D11Texture2D)()
        desc = D3D11_TEXTURE2D_DESC()
        ctypes.memset(ctypes.byref(desc), 0, ctypes.sizeof(desc))
        desc.Width, desc.Height = self.width, self.height
        desc.MipLevels = desc.ArraySize = 1
        desc.Format = _FORMAT_B8G8R8A8_UNORM
        desc.SampleDesc.Count = 1
        desc.Usage = _value(D3D11_USAGE_STAGING)
        desc.CPUAccessFlags = _value(D3D11_CPU_ACCESS_READ)
        self._device.CreateTexture2D(ctypes.byref(desc), None,
                                     ctypes.byref(texture))
        self._staging = texture.QueryInterface(ID3D11Resource)

    def _rebuild(self):
        """Tear down and reopen after the duplication was invalidated.

        A mode change, a resolution change, a session lock, a UAC prompt on the
        secure desktop, or a fullscreen-exclusive application taking the display
        all raise DXGI_ERROR_ACCESS_LOST, and all of them are recoverable. The
        device survives; only the duplication and the staging texture do not.
        """
        if self.options.max_rebuilds is not None \
                and self.rebuilds >= self.options.max_rebuilds:
            # DXGIError takes the HRESULT first and the context second - it
            # formats the code into the message itself. Passing a bare string
            # gets as far as `value & 0xFFFFFFFF` before failing.
            raise AccessLost(
                DXGI_ERROR_ACCESS_LOST,
                "the duplication was lost again after %d rebuild(s) and "
                "max_rebuilds=%d is exhausted"
                % (self.rebuilds, self.options.max_rebuilds))

        delay = _REBUILD_BACKOFF[min(self.rebuilds, len(_REBUILD_BACKOFF) - 1)]
        if delay:
            time.sleep(delay)
        self.rebuilds += 1

        self._release_frame_objects()
        self._duplication = None
        self._staging = None
        self._device = None
        self._context = None
        self._open()

    def _release_frame_objects(self):
        if self._mapped_now:
            try:
                self._context.Unmap(self._staging, 0)
            except Exception:                 # already gone with the device
                pass
            self._mapped_now = False
        if self._frame is not None:
            self._frame.expire()
            self._frame = None

    def close(self):
        """Idempotent. Called for you when the ``with`` block exits."""
        if self._closed:
            return
        self._release_frame_objects()
        # comtypes releases on __del__; calling Release() here would be a
        # double-free, which is F-52 and cost an afternoon once already.
        self._duplication = None
        self._staging = None
        self._context = None
        self._device = None
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()
        return False

    # ----------------------------------------------------------- iterating --
    def __iter__(self):
        return self

    def __next__(self):
        return self.grab()

    next = __next__                                   # for the older protocol

    def grab(self):
        """Block until a frame arrives, then return it.

        The Frame is valid until the next call. Copy inside the loop if it needs
        to outlive that.
        """
        if self._closed:
            raise RuntimeError("this DesktopCapture is closed")

        # Whatever the previous iteration handed out is now void.
        self._release_frame_objects()

        while True:
            resource = ctypes.POINTER(IDXGIResource)()
            lost = False
            try:
                self._duplication.AcquireNextFrame(
                    self.options.timeout_ms, ctypes.byref(self._info),
                    ctypes.byref(resource))
            except comtypes.COMError as exc:
                code = _hresult(exc)
                if code == DXGI_ERROR_WAIT_TIMEOUT:
                    # Not an error. The desktop did not change within the
                    # timeout, so there is nothing to deliver yet.
                    self.timeouts += 1
                    continue
                if code == DXGI_ERROR_DEVICE_REMOVED:
                    raise_for(code,
                              "the graphics device was removed or reset. This "
                              "is not recoverable by rebuilding; the process "
                              "has to create a new device.")
                if code != DXGI_ERROR_ACCESS_LOST:
                    raise_for(code, "AcquireNextFrame on %s"
                              % self.output.device_name)
                if self.options.on_access_lost == "raise":
                    raise_for(code, "AcquireNextFrame on %s"
                              % self.output.device_name)
                # Rebuild *after* leaving the handler, never inside it. While an
                # exception is being handled its traceback holds every frame on
                # the failing call stack alive, and those frames hold COM
                # pointers - including, sometimes, the duplication being
                # replaced. DXGI permits exactly one duplication per output per
                # process, so calling DuplicateOutput with the old one still
                # referenced fails with E_INVALIDARG. Setting a flag and acting
                # on it below costs one local and removes the whole class of
                # problem.
                lost = True

            if lost:
                self._rebuild()
                continue

            if self.options.skip_unchanged and self._info.LastPresentTime == 0:
                # Only the cursor moved; the desktop image is unchanged. This is
                # the cheapest optimisation in the loop, and on an idle desktop
                # it is most of the frames (constraint C-1).
                self.skipped += 1
                self._duplication.ReleaseFrame()
                continue

            try:
                return self._deliver(resource)
            except Exception:
                self._duplication.ReleaseFrame()
                raise

    def _deliver(self, resource):
        """Staging copy, Map, and a Frame over the mapped pages."""
        source = (resource.QueryInterface(ID3D11Texture2D)
                  .QueryInterface(ID3D11Resource))

        if self._cropping:
            self._context.CopySubresourceRegion(
                self._staging, 0, 0, 0, 0, source, 0, ctypes.byref(self._box))
        else:
            self._context.CopyResource(self._staging, source)

        self._context.Map(self._staging, 0, _value(D3D11_MAP_READ), 0,
                          ctypes.byref(self._mapped))
        self._mapped_now = True

        # ReleaseFrame as soon as the pixels are ours. Holding the frame longer
        # blocks the desktop from composing the next one.
        self._duplication.ReleaseFrame()

        self._frame = Frame(
            width=self.width,
            height=self.height,
            pitch=self._mapped.RowPitch,
            pointer=self._mapped.pData,
            timestamp_qpc=self._info.LastPresentTime,
            accumulated=self._info.AccumulatedFrames)
        return self._frame

    def __repr__(self):
        return "<DesktopCapture %s %dx%d%s rebuilds=%d%s>" % (
            self.output.device_name, self.width, self.height,
            " cropped" if self._cropping else "", self.rebuilds,
            " CLOSED" if self._closed else "")
