##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from dxgi1_4.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py dxgi1_4.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES



from Direct3D.PyIdl.dxgi1_3 import *


## -------------------------------------------- enumerations ----

DXGI_MEMORY_SEGMENT_GROUP = ctypes.c_uint
DXGI_MEMORY_SEGMENT_GROUP_LOCAL     = DXGI_MEMORY_SEGMENT_GROUP(0).value
DXGI_MEMORY_SEGMENT_GROUP_NON_LOCAL = DXGI_MEMORY_SEGMENT_GROUP(1).value

DXGI_OVERLAY_COLOR_SPACE_SUPPORT_FLAG = ctypes.c_uint
DXGI_OVERLAY_COLOR_SPACE_SUPPORT_FLAG_PRESENT = DXGI_OVERLAY_COLOR_SPACE_SUPPORT_FLAG(0x00000001).value

DXGI_SWAP_CHAIN_COLOR_SPACE_SUPPORT_FLAG = ctypes.c_uint
DXGI_SWAP_CHAIN_COLOR_SPACE_SUPPORT_FLAG_PRESENT         = DXGI_SWAP_CHAIN_COLOR_SPACE_SUPPORT_FLAG(0x00000001).value
DXGI_SWAP_CHAIN_COLOR_SPACE_SUPPORT_FLAG_OVERLAY_PRESENT = DXGI_SWAP_CHAIN_COLOR_SPACE_SUPPORT_FLAG(0x00000002).value


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class IDXGIAdapter3(IDXGIAdapter2):
    _iid_ = comtypes.GUID("{645967A4-1392-4310-A798-8053CE3E93FD}")


class IDXGIFactory4(IDXGIFactory3):
    _iid_ = comtypes.GUID("{1bc6ea02-ef36-464f-bf0c-21ca39e5168a}")


class IDXGIOutput4(IDXGIOutput3):
    _iid_ = comtypes.GUID("{dc7dca35-2196-414d-9F53-617884032a60}")


class IDXGISwapChain3(IDXGISwapChain2):
    _iid_ = comtypes.GUID("{94d99bdb-f1f8-4ab0-b236-7da0170edab1}")


## ---------------------------------------------- structures ----


class DXGI_QUERY_VIDEO_MEMORY_INFO(ctypes.Structure):
    _fields_ = [('Budget',                  ctypes.c_uint64),
                ('CurrentUsage',            ctypes.c_uint64),
                ('AvailableForReservation', ctypes.c_uint64),
                ('CurrentReservation',      ctypes.c_uint64),
    ]


## ------------------------- vtables, assigned once every class exists ----

IDXGIAdapter3._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "RegisterHardwareContentProtectionTeardownStatusEvent", [
        ctypes.c_void_p,                             # HANDLE hEvent
        ctypes.POINTER(ctypes.c_uint32),             # DWORD* pdwCookie
        ]),
    comtypes.STDMETHOD(None, "UnregisterHardwareContentProtectionTeardownStatus", [
        ctypes.c_uint32,                             # DWORD dwCookie
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "QueryVideoMemoryInfo", [
        ctypes.c_uint32,                             # UINT NodeIndex
        DXGI_MEMORY_SEGMENT_GROUP,                   # DXGI_MEMORY_SEGMENT_GROUP MemorySegmentGroup
        ctypes.POINTER(DXGI_QUERY_VIDEO_MEMORY_INFO), # DXGI_QUERY_VIDEO_MEMORY_INFO* pVideoMemoryInfo
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetVideoMemoryReservation", [
        ctypes.c_uint32,                             # UINT NodeIndex
        DXGI_MEMORY_SEGMENT_GROUP,                   # DXGI_MEMORY_SEGMENT_GROUP MemorySegmentGroup
        ctypes.c_uint64,                             # UINT64 Reservation
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "RegisterVideoMemoryBudgetChangeNotificationEvent", [
        ctypes.c_void_p,                             # HANDLE hEvent
        ctypes.POINTER(ctypes.c_uint32),             # DWORD* pdwCookie
        ]),
    comtypes.STDMETHOD(None, "UnregisterVideoMemoryBudgetChangeNotification", [
        ctypes.c_uint32,                             # DWORD dwCookie
        ]),
]

IDXGIFactory4._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "EnumAdapterByLuid", [
        LUID,                                        # LUID AdapterLuid
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppvAdapter
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "EnumWarpAdapter", [
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppvAdapter
        ]),
]

IDXGIOutput4._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckOverlayColorSpaceSupport", [
        DXGI_FORMAT,                                 # DXGI_FORMAT Format
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE ColorSpace
        ctypes.POINTER(comtypes.IUnknown),           # IUnknown* pConcernedDevice
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFlags
        ]),
]

IDXGISwapChain3._methods_ = [
    comtypes.STDMETHOD(ctypes.c_uint32, "GetCurrentBackBufferIndex", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckColorSpaceSupport", [
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE ColorSpace
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pColorSpaceSupport
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetColorSpace1", [
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE ColorSpace
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "ResizeBuffers1", [
        ctypes.c_uint32,                             # UINT BufferCount
        ctypes.c_uint32,                             # UINT Width
        ctypes.c_uint32,                             # UINT Height
        DXGI_FORMAT,                                 # DXGI_FORMAT Format
        ctypes.c_uint32,                             # UINT SwapChainFlags
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pCreationNodeMask
        ctypes.POINTER(ctypes.POINTER(comtypes.IUnknown)), # IUnknown** ppPresentQueue
        ]),
]


## -- End Of File --
