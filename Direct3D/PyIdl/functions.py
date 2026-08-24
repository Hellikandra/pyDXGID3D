# -*- coding: utf-8 -*-
"""DLL entry points for DXGI and Direct3D 11.

Before this module the package declared 72 COM interfaces and zero functions, so
there was no way to obtain the first object. Callers had to reach into
`ctypes.windll` themselves - which is where the truncated-handle problem came
from, because `ctypes.windll.foo.Bar` has no argtypes and defaults its return
type to a 32-bit int.

Every export here declares explicit `argtypes` and `restype`, and every wrapper
routes failures through `status.check()`, so callers get a typed exception rather
than a bare HRESULT.

    from Direct3D.PyIdl.functions import CreateDXGIFactory1, D3D11CreateDevice
    from Direct3D.PyIdl.d3dcommon import D3D_DRIVER_TYPE_WARP

    factory = CreateDXGIFactory1()
    device, level, context = D3D11CreateDevice(driver_type=D3D_DRIVER_TYPE_WARP)

Note on restype
---------------
These prototypes use `ctypes.c_long` for the HRESULT rather than
`comtypes.HRESULT`. With `comtypes.HRESULT`, comtypes raises `COMError` itself on
failure, which would bypass the exception hierarchy in `status.py` and lose the
distinction between "retry", "rebuild" and "give up" - the distinction that makes
the capture loop recoverable at all.
"""
import ctypes
import ctypes.wintypes as wintypes

import comtypes

from Direct3D.PyIdl.status import check
from Direct3D.PyIdl.d3dcommon import (
    D3D_DRIVER_TYPE, D3D_FEATURE_LEVEL,
    D3D_DRIVER_TYPE_HARDWARE,
    D3D_FEATURE_LEVEL_11_1, D3D_FEATURE_LEVEL_11_0,
    D3D_FEATURE_LEVEL_10_1, D3D_FEATURE_LEVEL_10_0,
    D3D_FEATURE_LEVEL_9_3, D3D_FEATURE_LEVEL_9_1,
)
from Direct3D.PyIdl.d3d11 import (
    ID3D11Device, ID3D11DeviceContext, D3D11_SDK_VERSION,
)
from Direct3D.PyIdl.dxgi import (
    IDXGIAdapter, IDXGIFactory, IDXGIFactory1, IDXGISwapChain,
)

__all__ = [
    "CreateDXGIFactory", "CreateDXGIFactory1", "CreateDXGIFactory2",
    "DXGIGetDebugInterface", "DXGIGetDebugInterface1",
    "DXGIDeclareAdapterRemovalSupport",
    "D3D11CreateDevice", "D3D11CreateDeviceAndSwapChain",
    "DEFAULT_FEATURE_LEVELS", "DXGI_CREATE_FACTORY_DEBUG",
    "MissingEntryPoint",
]

E_INVALIDARG = 0x80070057

#: Flag for CreateDXGIFactory2. Needs the Graphics Tools optional feature.
DXGI_CREATE_FACTORY_DEBUG = 0x01

#: Tried in order by D3D11CreateDevice when the caller does not specify.
DEFAULT_FEATURE_LEVELS = (
    D3D_FEATURE_LEVEL_11_1, D3D_FEATURE_LEVEL_11_0,
    D3D_FEATURE_LEVEL_10_1, D3D_FEATURE_LEVEL_10_0,
    D3D_FEATURE_LEVEL_9_3,  D3D_FEATURE_LEVEL_9_1,
)


class MissingEntryPoint(NotImplementedError):
    """The export is absent on this Windows version, or its DLL is not installed.

    CreateDXGIFactory2 and DXGIGetDebugInterface1 arrived in Windows 8.1, and
    dxgidebug.dll ships only with the Graphics Tools optional feature. A distinct
    type lets a caller degrade gracefully instead of parsing an error message.
    """


# ------------------------------------------------------------- libraries ----
_dxgi = ctypes.WinDLL("dxgi")
_d3d11 = ctypes.WinDLL("d3d11")
_dxgidebug = None                       # lazy: frequently not installed


def _dxgidebug_lib():
    global _dxgidebug
    if _dxgidebug is None:
        try:
            _dxgidebug = ctypes.WinDLL("dxgidebug")
        except OSError:
            raise MissingEntryPoint(
                "dxgidebug.dll is not available. It ships with the Graphics "
                "Tools optional feature: Settings > Apps > Optional features.")
    return _dxgidebug


def _bind(lib, name, restype, argtypes):
    """Look up an export and declare it. Returns None if the export is absent."""
    try:
        fn = getattr(lib, name)
    except AttributeError:
        return None
    fn.restype = restype
    fn.argtypes = argtypes
    return fn


def _require(fn, name):
    if fn is None:
        raise MissingEntryPoint(
            "%s is not exported by this version of Windows." % name)
    return fn


_PVOID_PP = ctypes.POINTER(ctypes.c_void_p)

_CreateDXGIFactory = _bind(
    _dxgi, "CreateDXGIFactory", ctypes.c_long,
    [ctypes.POINTER(comtypes.GUID), _PVOID_PP])
_CreateDXGIFactory1 = _bind(
    _dxgi, "CreateDXGIFactory1", ctypes.c_long,
    [ctypes.POINTER(comtypes.GUID), _PVOID_PP])
_CreateDXGIFactory2 = _bind(
    _dxgi, "CreateDXGIFactory2", ctypes.c_long,
    [wintypes.UINT, ctypes.POINTER(comtypes.GUID), _PVOID_PP])
_DXGIGetDebugInterface1 = _bind(
    _dxgi, "DXGIGetDebugInterface1", ctypes.c_long,
    [wintypes.UINT, ctypes.POINTER(comtypes.GUID), _PVOID_PP])
_DXGIDeclareAdapterRemovalSupport = _bind(
    _dxgi, "DXGIDeclareAdapterRemovalSupport", ctypes.c_long, [])

_D3D11CreateDevice = _bind(
    _d3d11, "D3D11CreateDevice", ctypes.c_long,
    [ctypes.POINTER(IDXGIAdapter),          # pAdapter
     D3D_DRIVER_TYPE,                       # DriverType
     ctypes.c_void_p,                       # Software (HMODULE)
     wintypes.UINT,                         # Flags
     ctypes.POINTER(D3D_FEATURE_LEVEL),     # pFeatureLevels
     wintypes.UINT,                         # FeatureLevels
     wintypes.UINT,                         # SDKVersion
     ctypes.POINTER(ctypes.POINTER(ID3D11Device)),
     ctypes.POINTER(D3D_FEATURE_LEVEL),
     ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext))])


def _levels_array(levels):
    levels = tuple(levels)
    arr = (D3D_FEATURE_LEVEL * len(levels))()
    for i, level in enumerate(levels):
        arr[i] = level.value if hasattr(level, "value") else level
    return arr


def _factory(fn, name, interface, flags=None):
    _require(fn, name)
    out = ctypes.POINTER(interface)()
    args = [ctypes.byref(interface._iid_),
            ctypes.cast(ctypes.byref(out), _PVOID_PP)]
    if flags is not None:
        args.insert(0, flags)
    check(fn(*args), name)
    return out


# --------------------------------------------------------------- exports ----
def CreateDXGIFactory(interface=IDXGIFactory):
    """Create a DXGI 1.0 factory. Prefer CreateDXGIFactory1."""
    return _factory(_CreateDXGIFactory, "CreateDXGIFactory", interface)


def CreateDXGIFactory1(interface=IDXGIFactory1):
    """Create a DXGI 1.1 factory.

    The default choice. Unlike CreateDXGIFactory it tracks adapter changes, so
    `IsCurrent()` means something.
    """
    return _factory(_CreateDXGIFactory1, "CreateDXGIFactory1", interface)


def CreateDXGIFactory2(flags=0, interface=IDXGIFactory1):
    """Create a factory with flags. Windows 8.1 and later.

    Pass DXGI_CREATE_FACTORY_DEBUG to route DXGI messages to the debug layer;
    that needs the Graphics Tools optional feature installed.
    """
    return _factory(_CreateDXGIFactory2, "CreateDXGIFactory2", interface, flags)


def DXGIGetDebugInterface(interface):
    """Obtain IDXGIDebug or IDXGIInfoQueue. Needs Graphics Tools installed."""
    fn = _bind(_dxgidebug_lib(), "DXGIGetDebugInterface", ctypes.c_long,
               [ctypes.POINTER(comtypes.GUID), _PVOID_PP])
    return _factory(fn, "DXGIGetDebugInterface", interface)


def DXGIGetDebugInterface1(flags=0, interface=None):
    """As above, from dxgi.dll rather than dxgidebug.dll. Windows 8.1 and later."""
    if interface is None:
        raise TypeError("DXGIGetDebugInterface1 requires an interface")
    return _factory(_DXGIGetDebugInterface1, "DXGIGetDebugInterface1",
                    interface, flags)


def DXGIDeclareAdapterRemovalSupport():
    """Declare that this process survives adapter removal. Windows 10 1803+."""
    fn = _require(_DXGIDeclareAdapterRemovalSupport,
                  "DXGIDeclareAdapterRemovalSupport")
    check(fn(), "DXGIDeclareAdapterRemovalSupport")


def D3D11CreateDevice(adapter=None,
                      driver_type=D3D_DRIVER_TYPE_HARDWARE,
                      software=None,
                      flags=0,
                      feature_levels=None,
                      sdk_version=D3D11_SDK_VERSION,
                      want_context=True):
    """Create a Direct3D 11 device.

    Returns ``(device, feature_level, context)``; `context` is None when
    `want_context` is False.

    Passing an `adapter` forces `driver_type` to UNKNOWN, which the API requires.
    That is also how you pin the device to the adapter that owns a particular
    output, which is what makes capture work on a hybrid-GPU laptop.

    If the driver predates the 11.1 runtime, D3D11CreateDevice rejects the whole
    call with E_INVALIDARG merely because 11_1 appears in the list. This retries
    once without it rather than surfacing a confusing failure.
    """
    fn = _require(_D3D11CreateDevice, "D3D11CreateDevice")
    levels = tuple(feature_levels) if feature_levels else DEFAULT_FEATURE_LEVELS

    if adapter is not None:
        driver_type = D3D_DRIVER_TYPE(0)    # UNKNOWN, mandated with an adapter

    def attempt(candidate_levels):
        arr = _levels_array(candidate_levels)
        device = ctypes.POINTER(ID3D11Device)()
        context = ctypes.POINTER(ID3D11DeviceContext)()
        obtained = D3D_FEATURE_LEVEL()
        hr = fn(adapter, driver_type, software, flags,
                arr, len(candidate_levels), sdk_version,
                ctypes.byref(device),
                ctypes.byref(obtained),
                ctypes.byref(context) if want_context else None)
        return hr, device, obtained, context

    hr, device, obtained, context = attempt(levels)

    if (hr & 0xFFFFFFFF) == E_INVALIDARG and levels[0] is D3D_FEATURE_LEVEL_11_1:
        hr, device, obtained, context = attempt(levels[1:])

    check(hr, "D3D11CreateDevice")
    return device, obtained, (context if want_context else None)


def D3D11CreateDeviceAndSwapChain(swap_chain_desc,
                                  adapter=None,
                                  driver_type=D3D_DRIVER_TYPE_HARDWARE,
                                  software=None,
                                  flags=0,
                                  feature_levels=None,
                                  sdk_version=D3D11_SDK_VERSION):
    """Create a device and a swap chain together.

    Returns ``(swapchain, device, feature_level, context)``.

    Kept for completeness. New code should create the device with
    D3D11CreateDevice and the swap chain with
    IDXGIFactory2::CreateSwapChainForHwnd, which supports the flip models this
    legacy entry point cannot express.
    """
    fn = _bind(_d3d11, "D3D11CreateDeviceAndSwapChain", ctypes.c_long,
               [ctypes.POINTER(IDXGIAdapter), D3D_DRIVER_TYPE, ctypes.c_void_p,
                wintypes.UINT, ctypes.POINTER(D3D_FEATURE_LEVEL), wintypes.UINT,
                wintypes.UINT, ctypes.c_void_p,
                ctypes.POINTER(ctypes.POINTER(IDXGISwapChain)),
                ctypes.POINTER(ctypes.POINTER(ID3D11Device)),
                ctypes.POINTER(D3D_FEATURE_LEVEL),
                ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext))])
    _require(fn, "D3D11CreateDeviceAndSwapChain")

    levels = tuple(feature_levels) if feature_levels else DEFAULT_FEATURE_LEVELS
    if adapter is not None:
        driver_type = D3D_DRIVER_TYPE(0)

    arr = _levels_array(levels)
    swapchain = ctypes.POINTER(IDXGISwapChain)()
    device = ctypes.POINTER(ID3D11Device)()
    context = ctypes.POINTER(ID3D11DeviceContext)()
    obtained = D3D_FEATURE_LEVEL()

    check(fn(adapter, driver_type, software, flags, arr, len(levels), sdk_version,
             ctypes.byref(swap_chain_desc) if swap_chain_desc else None,
             ctypes.byref(swapchain),
             ctypes.byref(device),
             ctypes.byref(obtained),
             ctypes.byref(context)),
          "D3D11CreateDeviceAndSwapChain")
    return swapchain, device, obtained, context
