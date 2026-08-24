# -*- coding: utf-8 -*-
"""Which monitors can be captured, and which GPU owns each one.

Enumeration walks factory -> adapter -> output, and every ``Output`` keeps a
reference to the adapter it came from. That is not tidiness: ``DuplicateOutput``
fails if the device was created on a different adapter than the one driving the
display, which is the *normal* situation on a hybrid laptop. The panel hangs off
the integrated GPU while games run on the discrete one, so a device created on
"the best adapter" cannot duplicate the only output there is.

Keeping the pair together makes constraint C-4 a fact of the data structure
rather than something the caller has to remember.
"""
import ctypes

import comtypes

from Direct3D.PyIdl.dxgi import (
    DXGI_ADAPTER_DESC1, DXGI_OUTPUT_DESC, IDXGIAdapter1, IDXGIOutput,
)
from Direct3D.PyIdl.functions import CreateDXGIFactory1

#: DXGI_MODE_ROTATION, as words rather than integers.
ROTATION = {0: "unspecified", 1: "none", 2: "90", 3: "180", 4: "270"}

#: DXGI_ADAPTER_FLAG_SOFTWARE. WARP and the Basic Render Driver set it; they
#: have no outputs, so they never appear here, but the flag is worth surfacing
#: on the adapter record.
_ADAPTER_FLAG_SOFTWARE = 0x2


def _value(constant):
    """ctypes enum instance or plain int, either way an int."""
    return constant.value if hasattr(constant, "value") else constant


class Adapter(object):
    """One GPU."""

    __slots__ = ("index", "description", "vendor_id", "device_id", "luid",
                 "dedicated_video_memory", "shared_system_memory",
                 "is_software", "_adapter")

    def __init__(self, index, adapter, desc):
        self.index = index
        self.description = desc.Description
        self.vendor_id = desc.VendorId
        self.device_id = desc.DeviceId
        self.luid = (desc.AdapterLuid.HighPart, desc.AdapterLuid.LowPart)
        self.dedicated_video_memory = desc.DedicatedVideoMemory
        self.shared_system_memory = desc.SharedSystemMemory
        self.is_software = bool(desc.Flags & _ADAPTER_FLAG_SOFTWARE)
        self._adapter = adapter

    def __repr__(self):
        return "<Adapter %d %r %.0f MB>" % (
            self.index, self.description,
            self.dedicated_video_memory / 1048576.0)


class Output(object):
    """One monitor, and the adapter driving it."""

    __slots__ = ("index", "device_name", "left", "top", "right", "bottom",
                 "rotation", "attached", "adapter", "_output")

    def __init__(self, index, output, desc, adapter):
        box = desc.DesktopCoordinates
        self.index = index
        self.device_name = desc.DeviceName
        self.left, self.top = box.left, box.top
        self.right, self.bottom = box.right, box.bottom
        self.rotation = ROTATION.get(_value(desc.Rotation), "unspecified")
        self.attached = bool(desc.AttachedToDesktop)
        self.adapter = adapter
        self._output = output

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def bounds(self):
        """(left, top, right, bottom) in desktop coordinates."""
        return (self.left, self.top, self.right, self.bottom)

    def __repr__(self):
        return "<Output %d %s %dx%d at (%d,%d) on %r>" % (
            self.index, self.device_name, self.width, self.height,
            self.left, self.top, self.adapter.description)


def enumerate_outputs(attached_only=True):
    """Every capturable monitor, in DXGI's own order.

    ``index`` counts outputs across the whole system, not within an adapter, so
    it can be used directly as ``CaptureOptions(output=N)``. That ordering is
    stable for a given display arrangement and changes when monitors are plugged
    in or rearranged - which is DXGI's behaviour, not something this layer can
    paper over.

    Software adapters have no outputs, so they drop out naturally.
    """
    factory = CreateDXGIFactory1()
    outputs, flat_index, adapter_index = [], 0, 0

    while True:
        adapter_ptr = ctypes.POINTER(IDXGIAdapter1)()
        try:
            factory.EnumAdapters1(adapter_index, ctypes.byref(adapter_ptr))
        except comtypes.COMError:
            break                    # DXGI_ERROR_NOT_FOUND ends the walk
        if not adapter_ptr:
            break

        desc = DXGI_ADAPTER_DESC1()
        adapter_ptr.GetDesc1(ctypes.byref(desc))
        adapter = Adapter(adapter_index, adapter_ptr, desc)

        out_index = 0
        while True:
            output_ptr = ctypes.POINTER(IDXGIOutput)()
            try:
                adapter_ptr.EnumOutputs(out_index, ctypes.byref(output_ptr))
            except comtypes.COMError:
                break
            if not output_ptr:
                break
            odesc = DXGI_OUTPUT_DESC()
            output_ptr.GetDesc(ctypes.byref(odesc))
            record = Output(flat_index, output_ptr, odesc, adapter)
            if record.attached or not attached_only:
                outputs.append(record)
                flat_index += 1
            out_index += 1

        adapter_index += 1

    return outputs


def resolve_output(spec, outputs=None):
    """Turn an index, a device name or an Output into an Output.

    Raises ValueError naming what is available, because "output 3 not found" is
    useless when the caller cannot see the list from where they are standing.
    """
    if isinstance(spec, Output):
        return spec

    # Type before availability. Passing a float is a programming error whether
    # or not a display happens to be attached, and reporting it as "no
    # capturable outputs" sends the reader looking at their hardware.
    if not isinstance(spec, (int, str)) or isinstance(spec, bool):
        raise TypeError("output must be an int, a device name or an Output, "
                        "not %s" % type(spec).__name__)

    available = enumerate_outputs() if outputs is None else outputs
    if not available:
        raise ValueError(
            "no capturable outputs. Every adapter reported zero attached "
            "displays - this happens over a disconnected RDP session and in "
            "services, where there is no interactive desktop to duplicate.")

    if isinstance(spec, int):
        for output in available:
            if output.index == spec:
                return output
        raise ValueError("no output with index %d. Available: %s"
                         % (spec, ", ".join("%d (%s)" % (o.index, o.device_name)
                                            for o in available)))

    if isinstance(spec, str):
        for output in available:
            if output.device_name == spec:
                return output
        raise ValueError("no output named %r. Available: %s"
                         % (spec, ", ".join(repr(o.device_name)
                                            for o in available)))
