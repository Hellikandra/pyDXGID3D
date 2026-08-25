# -*- coding: utf-8 -*-
"""Tier 1 - the bindings actually work.

Needs Windows and comtypes. It does NOT need a GPU: every device here is created
with the WARP software rasteriser, so this whole file runs on a hosted CI runner.

The gate for integration phase P1 is `test_warp_device_and_qi_chain`. Until that
passes, the package cannot obtain its first COM object.
"""
import ctypes
import ctypes.wintypes as wintypes
import importlib
import io
import os

import pytest

from conftest import needs_comtypes, needs_windows

pytestmark = [pytest.mark.tier1, needs_windows, needs_comtypes]

MODULES = [
    "Direct3D.PyIdl.dxgicommon",
    "Direct3D.PyIdl.dxgiformat",
    "Direct3D.PyIdl.dxgitype",
    "Direct3D.PyIdl.dxgi",
    "Direct3D.PyIdl.dxgi1_2",
    "Direct3D.PyIdl.dxgidebug",
    "Direct3D.PyIdl.d3dcommon",
    "Direct3D.PyIdl.d3d11",
    "Direct3D.PyIdl.d3d11sdklayers",
    "Direct3D.PyIdl.typemap",
    "Direct3D.PyIdl.status",
    "Direct3D.PyIdl.functions",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    """Importing is not a formality: comtypes builds each vtable at class
    creation, so a malformed _methods_ raises here rather than at first call."""
    assert importlib.import_module(name) is not None


# --------------------------------------------------------------- typemap ----
def test_typemap_self_check():
    """The canonical table agrees with itself and with this interpreter."""
    from Direct3D.PyIdl import typemap
    problems = typemap.self_check()
    assert not problems, "typemap problems:\n  " + "\n  ".join(problems)


def test_bool_is_four_bytes():
    """F-47, stated as bluntly as it deserves."""
    from Direct3D.PyIdl import typemap
    assert ctypes.sizeof(typemap.TYPES["BOOL"]) == 4
    assert typemap.TYPES["BOOL"] is not ctypes.c_bool


def test_typemap_resolve():
    from Direct3D.PyIdl import typemap
    assert typemap.resolve("UINT") is ctypes.c_uint32
    assert typemap.resolve("void") is None
    assert ctypes.sizeof(typemap.resolve("FLOAT", array_length=4)) == 16
    assert typemap.resolve("UINT", pointer_depth=1)._type_ is ctypes.c_uint32
    with pytest.raises(KeyError):
        typemap.resolve("NO_SUCH_IDL_TYPE")


# ---------------------------------------------------------------- status ----
def test_status_codes_and_signedness():
    """ctypes hands back HRESULTs as signed; the tables are unsigned."""
    from Direct3D.PyIdl import status
    assert status.DXGI_ERROR_ACCESS_LOST == 0x887A0026
    assert status.DXGI_ERROR_WAIT_TIMEOUT == 0x887A0027
    assert status.DXGI_STATUS_OCCLUDED == 0x087A0001
    # -2005270489 is how 0x887A0027 arrives from a c_long restype.
    assert status.name_of(-2005270489) == "DXGI_ERROR_WAIT_TIMEOUT"


def test_status_success_is_not_just_zero():
    """DXGI_STATUS_* codes are successes. Testing `hr == 0` misses them."""
    from Direct3D.PyIdl import status
    assert status.succeeded(status.S_OK)
    assert status.succeeded(status.S_FALSE)
    assert status.succeeded(status.DXGI_STATUS_OCCLUDED)
    assert status.failed(status.DXGI_ERROR_ACCESS_LOST)


def test_status_check_raises_mapped_exception():
    from Direct3D.PyIdl import status
    assert status.check(status.S_OK) == 0
    with pytest.raises(status.AccessLost):
        status.check(status.DXGI_ERROR_ACCESS_LOST)
    with pytest.raises(status.WaitTimeout):
        status.check(status.DXGI_ERROR_WAIT_TIMEOUT)
    with pytest.raises(status.DeviceRemoved):
        status.check(status.DXGI_ERROR_DEVICE_REMOVED)
    # An unmapped failure still raises, as the base class.
    with pytest.raises(status.DXGIError):
        status.check(0x8000FFFF)


def test_status_exception_carries_hresult():
    from Direct3D.PyIdl import status
    try:
        status.check(status.DXGI_ERROR_ACCESS_LOST, "AcquireNextFrame")
    except status.AccessLost as exc:
        assert exc.hresult == 0x887A0026
        assert "AcquireNextFrame" in str(exc)
        assert "DXGI_ERROR_ACCESS_LOST" in str(exc)
    else:
        pytest.fail("check() did not raise")


# ------------------------------------------------------------- functions ----
def test_factory_creation():
    """CreateDXGIFactory1 through the package's own entry point (F-43)."""
    from Direct3D.PyIdl.functions import CreateDXGIFactory1
    factory = CreateDXGIFactory1()
    assert factory


def test_warp_device_and_qi_chain(warp_device):
    """T1.5 - the P1 gate.

    Create a device with the package's own D3D11CreateDevice, then walk
    Device -> IDXGIDevice -> IDXGIAdapter -> IDXGIFactory2. That chain is the
    one OutputManager needs and the one where the stale-HRESULT checks of F-15
    live.
    """
    from Direct3D.PyIdl.dxgi import IDXGIDevice, IDXGIAdapter
    from Direct3D.PyIdl.dxgi1_2 import IDXGIFactory2

    device, level, context = warp_device
    assert device, "no device"
    assert context, "no immediate context"
    assert level.value >= 0x9100, "implausible feature level 0x%X" % level.value

    dxgi_device = device.QueryInterface(IDXGIDevice)
    assert dxgi_device

    adapter = ctypes.POINTER(IDXGIAdapter)()
    dxgi_device.GetParent(IDXGIAdapter._iid_, ctypes.byref(adapter))
    assert adapter, "GetParent returned a null adapter"

    factory = ctypes.POINTER(IDXGIFactory2)()
    adapter.GetParent(IDXGIFactory2._iid_, ctypes.byref(factory))
    assert factory, "GetParent returned a null factory"



def test_adapter_description_is_readable(warp_device):
    """Proves a struct out-parameter round-trips, not merely that a call
    returns S_OK. WARP reports itself as 'Microsoft Basic Render Driver'."""
    from Direct3D.PyIdl.dxgi import IDXGIDevice, IDXGIAdapter, DXGI_ADAPTER_DESC

    device, _level, _context = warp_device
    dxgi_device = device.QueryInterface(IDXGIDevice)
    adapter = ctypes.POINTER(IDXGIAdapter)()
    dxgi_device.GetParent(IDXGIAdapter._iid_, ctypes.byref(adapter))

    desc = DXGI_ADAPTER_DESC()
    adapter.GetDesc(ctypes.byref(desc))
    description = desc.Description
    assert isinstance(description, str) and description.strip()



def test_staging_texture_roundtrip(warp_device):
    """T1.6 - the readback path, with no display involved.

    Create a default texture, copy it to a STAGING texture, Map it, and verify
    the mapping honours RowPitch. Getting pitch wrong is the single most common
    readback bug, and this is the shape of the capture path that phase N2 will
    build on.
    """
    from Direct3D.PyIdl.d3d11 import (
        D3D11_TEXTURE2D_DESC, ID3D11Texture2D, ID3D11Resource,
        D3D11_MAPPED_SUBRESOURCE, D3D11_USAGE_DEFAULT, D3D11_USAGE_STAGING,
        D3D11_CPU_ACCESS_READ, D3D11_MAP_READ,
    )
    from Direct3D.PyIdl.dxgiformat import DXGI_FORMAT_B8G8R8A8_UNORM

    device, _level, context = warp_device
    width, height = 64, 32

    def make(usage, cpu_access, bind_flags):
        desc = D3D11_TEXTURE2D_DESC()
        ctypes.memset(ctypes.byref(desc), 0, ctypes.sizeof(desc))
        desc.Width = width
        desc.Height = height
        desc.MipLevels = 1
        desc.ArraySize = 1
        desc.Format = DXGI_FORMAT_B8G8R8A8_UNORM
        desc.SampleDesc.Count = 1
        desc.SampleDesc.Quality = 0
        desc.Usage = usage
        desc.BindFlags = bind_flags
        desc.CPUAccessFlags = cpu_access
        desc.MiscFlags = 0
        texture = ctypes.POINTER(ID3D11Texture2D)()
        device.CreateTexture2D(ctypes.byref(desc), None, ctypes.byref(texture))
        assert texture, "CreateTexture2D returned null"
        return texture

    source = make(_value(D3D11_USAGE_DEFAULT), 0, 0)
    staging = make(_value(D3D11_USAGE_STAGING), _value(D3D11_CPU_ACCESS_READ), 0)

    context.CopyResource(
        staging.QueryInterface(ID3D11Resource),
        source.QueryInterface(ID3D11Resource))

    mapped = D3D11_MAPPED_SUBRESOURCE()
    context.Map(staging.QueryInterface(ID3D11Resource), 0,
                _value(D3D11_MAP_READ), 0, ctypes.byref(mapped))
    try:
        assert mapped.pData, "Map returned a null pointer"
        assert mapped.RowPitch >= width * 4, (
            "RowPitch %d is smaller than one row of %d BGRA pixels"
            % (mapped.RowPitch, width))
        # Reading the last byte of the last row proves the whole mapping is
        # addressable at the reported pitch.
        buf = ctypes.cast(mapped.pData, ctypes.POINTER(ctypes.c_ubyte))
        last = mapped.RowPitch * (height - 1) + width * 4 - 1
        _ = buf[last]
    finally:
        context.Unmap(staging.QueryInterface(ID3D11Resource), 0)



def _value(constant):
    """The enum constants are ctypes instances; the APIs want plain ints."""
    return constant.value if hasattr(constant, "value") else constant


def test_explicit_release_is_a_double_free(warp_device):
    """F-52: calling Release() on a comtypes pointer double-releases it.

    In C++ every interface pointer must be Released by hand. Under comtypes it
    must not: `_compointer_base.__del__` releases the reference comtypes owns, so
    an explicit Release() plus the implicit one is two releases for one
    reference. The object is destroyed by the first, and the second writes into
    freed memory - an access violation, raised from a destructor where it cannot
    be caught.

    This is the single most dangerous habit carried over from the C++ sample.
    `OutputManager.CleanRefs()` does it to eleven pointers, and `__del__` calls
    CleanRefs, so it runs at interpreter shutdown when it is hardest to diagnose.

    The test asserts the safe direction: a pointer that is only ever released by
    comtypes survives repeated create/collect cycles. It deliberately does NOT
    perform the double release - doing so corrupts the process and would take
    the rest of the suite with it.
    """
    import gc

    from Direct3D.PyIdl.functions import CreateDXGIFactory1

    for _ in range(5):
        factory = CreateDXGIFactory1()
        assert factory
        del factory
        gc.collect()


def test_bindings_do_not_call_release_on_com_pointers():
    """F-52, statically: no new code should adopt the explicit-Release habit.

    Every Python file in the package is in scope now. The exclusion that used
    to live here covered OutputManager.py and DesktopDuplication.py, the
    unported C++ sample; those were deleted in P6, so the rule applies
    everywhere without exception.
    """
    import ast
    import glob

    from conftest import REPO_ROOT

    offenders = []
    scoped = (glob.glob(os.path.join(REPO_ROOT, "Direct3D", "PyIdl", "*.py"))
              + glob.glob(os.path.join(REPO_ROOT, "Direct3D", "Core", "*.py"))
              + glob.glob(os.path.join(REPO_ROOT, "Direct3D", "Capture", "*.py")))
    for path in scoped:
        tree = ast.parse(io.open(path, encoding="utf-8").read())
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "Release"
                    and not node.args):
                offenders.append("%s:%d" % (os.path.basename(path), node.lineno))

    assert not offenders, (
        "explicit Release() on a COM pointer - comtypes releases it too, and the "
        "second release faults (F-52):\n  " + "\n  ".join(offenders))
