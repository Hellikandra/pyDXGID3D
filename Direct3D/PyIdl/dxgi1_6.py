##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from dxgi1_6.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py dxgi1_6.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES


from Direct3D.PyIdl.dxgi1_5 import *


## -------------------------------------------- enumerations ----

DXGI_ADAPTER_FLAG3 = ctypes.c_uint
DXGI_ADAPTER_FLAG3_NONE                         = DXGI_ADAPTER_FLAG3(0)
DXGI_ADAPTER_FLAG3_REMOTE                       = DXGI_ADAPTER_FLAG3(1)
DXGI_ADAPTER_FLAG3_SOFTWARE                     = DXGI_ADAPTER_FLAG3(2)
DXGI_ADAPTER_FLAG3_ACG_COMPATIBLE               = DXGI_ADAPTER_FLAG3(4)
DXGI_ADAPTER_FLAG3_SUPPORT_MONITORED_FENCES     = DXGI_ADAPTER_FLAG3(8)
DXGI_ADAPTER_FLAG3_SUPPORT_NON_MONITORED_FENCES = DXGI_ADAPTER_FLAG3(0x10)
DXGI_ADAPTER_FLAG3_KEYED_MUTEX_CONFORMANCE      = DXGI_ADAPTER_FLAG3(0x20)
DXGI_ADAPTER_FLAG3_FORCE_DWORD                  = DXGI_ADAPTER_FLAG3(0xFFFFFFFF)

DXGI_GPU_PREFERENCE = ctypes.c_uint
DXGI_GPU_PREFERENCE_UNSPECIFIED      = DXGI_GPU_PREFERENCE(0)
DXGI_GPU_PREFERENCE_MINIMUM_POWER    = DXGI_GPU_PREFERENCE()
DXGI_GPU_PREFERENCE_HIGH_PERFORMANCE = DXGI_GPU_PREFERENCE()

DXGI_HARDWARE_COMPOSITION_SUPPORT_FLAGS = ctypes.c_uint
DXGI_HARDWARE_COMPOSITION_SUPPORT_FLAG_FULLSCREEN       = DXGI_HARDWARE_COMPOSITION_SUPPORT_FLAGS(1)
DXGI_HARDWARE_COMPOSITION_SUPPORT_FLAG_WINDOWED         = DXGI_HARDWARE_COMPOSITION_SUPPORT_FLAGS(2)
DXGI_HARDWARE_COMPOSITION_SUPPORT_FLAG_CURSOR_STRETCHED = DXGI_HARDWARE_COMPOSITION_SUPPORT_FLAGS(4)


## ---------------------------------------------- structures ----


class DXGI_ADAPTER_DESC3(ctypes.Structure):
    _fields_ = [('Description',                   ctypes.c_wchar * 128),
                ('VendorId',                      ctypes.c_uint32),
                ('DeviceId',                      ctypes.c_uint32),
                ('SubSysId',                      ctypes.c_uint32),
                ('Revision',                      ctypes.c_uint32),
                ('DedicatedVideoMemory',          ctypes.c_size_t),
                ('DedicatedSystemMemory',         ctypes.c_size_t),
                ('SharedSystemMemory',            ctypes.c_size_t),
                ('AdapterLuid',                   LUID),
                ('Flags',                         DXGI_ADAPTER_FLAG3),
                ('GraphicsPreemptionGranularity', DXGI_GRAPHICS_PREEMPTION_GRANULARITY),
                ('ComputePreemptionGranularity',  DXGI_COMPUTE_PREEMPTION_GRANULARITY),
    ]


class DXGI_OUTPUT_DESC1(ctypes.Structure):
    _fields_ = [('DeviceName',            ctypes.c_wchar * 32),
                ('DesktopCoordinates',    wintypes.RECT),
                ('AttachedToDesktop',     wintypes.BOOL),
                ('Rotation',              DXGI_MODE_ROTATION),
                ('Monitor',               ctypes.c_void_p),
                ('BitsPerColor',          ctypes.c_uint32),
                ('ColorSpace',            DXGI_COLOR_SPACE_TYPE),
                ('RedPrimary',            ctypes.c_float * 2),
                ('GreenPrimary',          ctypes.c_float * 2),
                ('BluePrimary',           ctypes.c_float * 2),
                ('WhitePoint',            ctypes.c_float * 2),
                ('MinLuminance',          ctypes.c_float),
                ('MaxLuminance',          ctypes.c_float),
                ('MaxFullFrameLuminance', ctypes.c_float),
    ]


## ---------------------------------------------- interfaces ----


class IDXGIAdapter4(IDXGIAdapter3):
    _iid_ = comtypes.GUID("{3c8d99d1-4fbf-4181-a82c-af66bf7bd24e}")


class IDXGIFactory6(IDXGIFactory5):
    _iid_ = comtypes.GUID("{c1b6694f-ff09-44a9-b03c-77900a0a1d17}")


class IDXGIFactory7(IDXGIFactory6):
    _iid_ = comtypes.GUID("{a4966eed-76db-44da-84c1-ee9a7afb20a8}")


class IDXGIOutput6(IDXGIOutput5):
    _iid_ = comtypes.GUID("{068346e8-aaec-4b84-add7-137f513f77a1}")


## ------------------------- vtables, assigned once every class exists ----

IDXGIAdapter4._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc3", [
        ctypes.POINTER(DXGI_ADAPTER_DESC3),          # DXGI_ADAPTER_DESC3* pDesc
        ]),
]

IDXGIFactory6._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "EnumAdapterByGpuPreference", [
        ctypes.c_uint32,                             # UINT Adapter
        DXGI_GPU_PREFERENCE,                         # DXGI_GPU_PREFERENCE GpuPreference
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppvAdapter
        ]),
]

IDXGIFactory7._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "RegisterAdaptersChangedEvent", [
        ctypes.c_void_p,                             # HANDLE hEvent
        ctypes.POINTER(ctypes.c_uint32),             # DWORD* pdwCookie
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "UnregisterAdaptersChangedEvent", [
        ctypes.c_uint32,                             # DWORD dwCookie
        ]),
]

IDXGIOutput6._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc1", [
        ctypes.POINTER(DXGI_OUTPUT_DESC1),           # DXGI_OUTPUT_DESC1* pDesc
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckHardwareCompositionSupport", [
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFlags
        ]),
]


## -- End Of File --
