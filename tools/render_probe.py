# -*- coding: utf-8 -*-
"""Render a known colour, capture it back, and compare. Ground truth for capture.

    python tools/render_probe.py
    python tools/render_probe.py --colour 200 40 120 --tolerance 2

Every other capture test asserts SHAPE: the frame is the right size, the pitch is
at least width * 4, a crop matches the same region of a full frame. None of them
asserts the frame contains what was on the screen. A capture path that returned
the previous frame, or one offset by a row, or a stale buffer, would pass all of
them.

This closes that. It creates a window and a swap chain through these bindings,
clears the back buffer to a colour chosen not to occur on a desktop, presents,
then captures that rectangle and compares the pixels.

It is also the only thing in this repository that renders, which matters for a
second reason: F-60 was ten parameters declared as a scalar where the SDK
declares an array - `const FLOAT ColorRGBA[4]` bound as one float - and every one
of them is on the rendering path. Nothing that only captures can reach them.

Deliberately not a triangle. A cleared render target proves the path and costs
nothing; drawing geometry would need HLSL bytecode compiled at build time, and
that is how the deleted sample application ended up carrying 180 kB of DXBC.
"""
import argparse
import ctypes
import sys
import time
from ctypes import wintypes

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from Direct3D.Capture import CaptureOptions, DesktopCapture, enumerate_outputs  # noqa: E402
from Direct3D.PyIdl.d3d11 import (                                             # noqa: E402
    ID3D11RenderTargetView, ID3D11Resource, ID3D11Texture2D,
)
from Direct3D.PyIdl.dxgi import DXGI_SWAP_CHAIN_DESC                           # noqa: E402
from Direct3D.PyIdl.functions import D3D11CreateDeviceAndSwapChain             # noqa: E402

_user32 = ctypes.WinDLL("user32")
_kernel32 = ctypes.WinDLL("kernel32")
_dwmapi = ctypes.WinDLL("dwmapi")

_user32.DefWindowProcW.restype = ctypes.c_ssize_t
_user32.DefWindowProcW.argtypes = [wintypes.HWND, ctypes.c_uint,
                                   ctypes.c_size_t, ctypes.c_ssize_t]
_user32.CreateWindowExW.restype = wintypes.HWND

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, wintypes.HWND, ctypes.c_uint,
                             ctypes.c_size_t, ctypes.c_ssize_t)

#: DwmGetWindowAttribute. GetWindowRect includes the invisible resize border and
#: would put the rectangle outside the monitor.
DWMWA_EXTENDED_FRAME_BOUNDS = 9

CLASS_NAME = "pyDXGID3DRenderProbe"

#: SetWindowPos. The probe window has to be VISIBLE, not merely created: Desktop
#: Duplication captures the composed desktop, and the compositor does not
#: recompose a window that nothing can see. A covered probe keeps showing
#: whatever was last composited there, which reads exactly like a stale capture
#: and is not one.
HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_SHOWWINDOW = 0x0040
WS_EX_TOPMOST = 0x00000008

#: PeekMessage. A window that never pumps its queue is a window Windows decides
#: is not responding, and DWM stops recomposing it - it freezes the last image
#: it had. Capture then keeps returning that frozen frame, which looks exactly
#: like a stale capture and is nothing of the kind.
#:
#: It does not bite in a script that renders and exits inside a second. It bites
#: hard in a test fixture that lives for the length of a suite, which is how it
#: was found.
PM_REMOVE = 0x0001

#: A colour unlikely to appear on a desktop by accident, so a match means the
#: capture found THIS window rather than something behind it.
DEFAULT_COLOUR = (33, 196, 92)


class WNDCLASS(ctypes.Structure):
    _fields_ = [("style", ctypes.c_uint), ("lpfnWndProc", WNDPROC),
                ("cbClsExtra", ctypes.c_int), ("cbWndExtra", ctypes.c_int),
                ("hInstance", wintypes.HINSTANCE), ("hIcon", wintypes.HICON),
                ("hCursor", wintypes.HANDLE), ("hbrBackground", wintypes.HBRUSH),
                ("lpszMenuName", wintypes.LPCWSTR),
                ("lpszClassName", wintypes.LPCWSTR)]


class Probe(object):
    """A window, a swap chain, and a render target view. Closes cleanly.

    The WNDPROC must outlive the window - if Python collects the callback while
    Windows still holds a pointer to it, the next message dispatched is a jump
    into freed memory. It is kept on the instance for exactly that reason.
    """

    def __init__(self, width=480, height=360):
        self.width, self.height = width, height
        self._proc = WNDPROC(self._window_proc)
        self.hwnd = self._make_window()
        (self.swapchain, self.device,
         self.feature_level, self.context) = self._make_swapchain()
        self.rtv = self._make_render_target()

    @staticmethod
    def _window_proc(hwnd, message, wparam, lparam):
        return _user32.DefWindowProcW(hwnd, message, wparam, lparam)

    def _make_window(self):
        cls = WNDCLASS()
        ctypes.memset(ctypes.byref(cls), 0, ctypes.sizeof(cls))
        cls.lpfnWndProc = self._proc
        cls.hInstance = _kernel32.GetModuleHandleW(None)
        cls.lpszClassName = CLASS_NAME
        cls.hCursor = _user32.LoadCursorW(None, ctypes.c_wchar_p(32512))
        _user32.RegisterClassW(ctypes.byref(cls))   # already registered is fine
        self._class = cls                           # keep it alive too

        hwnd = _user32.CreateWindowExW(
            WS_EX_TOPMOST, CLASS_NAME, "pyDXGID3D render probe",
            0x00CF0000,                             # WS_OVERLAPPEDWINDOW
            80, 80, self.width, self.height,
            None, None, cls.hInstance, None)
        if not hwnd:
            raise OSError("CreateWindowExW failed: %d" % ctypes.get_last_error())
        _user32.ShowWindow(hwnd, 5)                 # SW_SHOW
        _user32.UpdateWindow(hwnd)
        self._raise(hwnd)
        return hwnd

    @staticmethod
    def _raise(hwnd):
        """Put the window on top and keep it there.

        Re-asserted before every sample rather than only at creation, because
        anything appearing later - a console from a subprocess, a notification -
        covers it, and a covered window's new frames never reach the desktop.
        """
        _user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                             SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

    def _make_swapchain(self):
        desc = DXGI_SWAP_CHAIN_DESC()
        ctypes.memset(ctypes.byref(desc), 0, ctypes.sizeof(desc))
        desc.BufferDesc.Width = self.width
        desc.BufferDesc.Height = self.height
        desc.BufferDesc.Format = 87                 # B8G8R8A8_UNORM
        desc.BufferDesc.RefreshRate.Numerator = 60
        desc.BufferDesc.RefreshRate.Denominator = 1
        desc.SampleDesc.Count = 1
        desc.BufferUsage = 0x20                     # RENDER_TARGET_OUTPUT
        desc.BufferCount = 2
        desc.OutputWindow = self.hwnd
        desc.Windowed = 1
        desc.SwapEffect = 0                         # DISCARD
        return D3D11CreateDeviceAndSwapChain(desc)

    def _make_render_target(self):
        back = ctypes.POINTER(ID3D11Texture2D)()
        self.swapchain.GetBuffer(0, ID3D11Texture2D._iid_, ctypes.byref(back))
        rtv = ctypes.POINTER(ID3D11RenderTargetView)()
        self.device.CreateRenderTargetView(
            back.QueryInterface(ID3D11Resource), None, ctypes.byref(rtv))
        return rtv

    def pump(self):
        """Drain the message queue. Not optional - see PM_REMOVE above."""
        message = wintypes.MSG()
        while _user32.PeekMessageW(ctypes.byref(message), None, 0, 0, PM_REMOVE):
            _user32.TranslateMessage(ctypes.byref(message))
            _user32.DispatchMessageW(ctypes.byref(message))

    def clear(self, rgb):
        """Clear to an 8-bit RGB triple and present.

        ClearRenderTargetView takes four floats. Before F-60 it was declared as
        one, and this call was impossible to make.
        """
        self.pump()
        colour = (ctypes.c_float * 4)(rgb[0] / 255.0, rgb[1] / 255.0,
                                      rgb[2] / 255.0, 1.0)
        self.context.ClearRenderTargetView(self.rtv, colour)
        self.swapchain.Present(1, 0)

    def bounds(self):
        """The window's visible rectangle in desktop coordinates."""
        rect = wintypes.RECT()
        if _dwmapi.DwmGetWindowAttribute(
                wintypes.HWND(self.hwnd),
                ctypes.c_uint(DWMWA_EXTENDED_FRAME_BOUNDS),
                ctypes.byref(rect), ctypes.sizeof(rect)) != 0:
            _user32.GetWindowRect(self.hwnd, ctypes.byref(rect))
        return (rect.left, rect.top, rect.right, rect.bottom)

    def close(self):
        self.rtv = None
        self.swapchain = None
        self.context = None
        self.device = None
        if self.hwnd:
            _user32.DestroyWindow(self.hwnd)
            self.hwnd = None

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()
        return False


def sample(probe, rgb, output=None, span=32, frames=8):
    """Clear to `rgb`, capture the middle of the window, return what came back.

    Returns (captured_rgb, region). The clear is repeated inside the capture
    loop because the first frames after DuplicateOutput can predate it.
    """
    outputs = enumerate_outputs()
    if not outputs:
        raise RuntimeError("no attached display")
    if output is None:
        output = outputs[0]

    left, top, right, bottom = probe.bounds()
    centre_x, centre_y = (left + right) // 2, (top + bottom) // 2
    region = (max(centre_x - span, output.left), max(centre_y - span, output.top),
              min(centre_x + span, output.right), min(centre_y + span, output.bottom))

    probe._raise(probe.hwnd)
    for _ in range(3):
        probe.clear(rgb)
        time.sleep(0.02)

    options = CaptureOptions(output=output, region=region, timeout_ms=1000)
    with DesktopCapture(options) as capture:
        for _ in range(frames):
            probe.clear(rgb)
            frame = capture.grab()
        view = frame.memoryview
        middle = frame.pitch * (frame.height // 2) + (frame.width // 2) * 4
        got = (view[middle + 2], view[middle + 1], view[middle])
    return got, region


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--colour", type=int, nargs=3, metavar=("R", "G", "B"),
                        default=list(DEFAULT_COLOUR))
    parser.add_argument("--tolerance", type=int, default=4,
                        help="per channel; the desktop compositor is not lossless")
    args = parser.parse_args()

    wanted = tuple(args.colour)
    print("pyDXGID3D - render a known colour, capture it back")
    print("=" * 52)
    print()

    try:
        with Probe() as probe:
            print("  window and swap chain created, feature level 0x%X"
                  % probe.feature_level.value)
            got, region = sample(probe, wanted)
    except Exception as exc:
        print("  could not run: %s" % exc)
        return 1

    print("  sampled region  : %r" % (region,))
    print("  rendered RGB    : %s" % (wanted,))
    print("  captured RGB    : %s" % (got,))

    drift = max(abs(a - b) for a, b in zip(got, wanted))
    print("  worst channel   : %d" % drift)
    print()
    if drift <= args.tolerance:
        print("  MATCH. The frame contains what was drawn, not merely a frame of")
        print("  the right shape - which is the first thing in this project to")
        print("  check capture against ground truth.")
        return 0
    print("  DIFFERENT. Something is between the window and the capture: another")
    print("  window on top, a colour profile, or a scaling factor. Move the probe")
    print("  window to an empty area and try again.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
