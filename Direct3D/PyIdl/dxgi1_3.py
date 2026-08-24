##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from dxgi1_3.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py dxgi1_3.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES


from Direct3D.PyIdl.dxgi1_2 import *


## ---------------------------------------------- constants ----
DXGI_CREATE_FACTORY_DEBUG                      = 0x1


## -------------------------------------------- enumerations ----

DXGI_FRAME_PRESENTATION_MODE = ctypes.c_uint
DXGI_FRAME_PRESENTATION_MODE_COMPOSED            = DXGI_FRAME_PRESENTATION_MODE(0)
DXGI_FRAME_PRESENTATION_MODE_OVERLAY             = DXGI_FRAME_PRESENTATION_MODE(1)
DXGI_FRAME_PRESENTATION_MODE_NONE                = DXGI_FRAME_PRESENTATION_MODE(2)
DXGI_FRAME_PRESENTATION_MODE_COMPOSITION_FAILURE = DXGI_FRAME_PRESENTATION_MODE(3)

DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAGS = ctypes.c_uint
DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAG_NOMINAL_RANGE = DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAGS(0x1)
DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAG_BT709         = DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAGS(0x2)
DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAG_xvYCC         = DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAGS(0x4)

DXGI_OVERLAY_SUPPORT_FLAG = ctypes.c_uint
DXGI_OVERLAY_SUPPORT_FLAG_DIRECT  = DXGI_OVERLAY_SUPPORT_FLAG(0x1)
DXGI_OVERLAY_SUPPORT_FLAG_SCALING = DXGI_OVERLAY_SUPPORT_FLAG(0x2)


## ---------------------------------------------- structures ----


class DXGI_DECODE_SWAP_CHAIN_DESC(ctypes.Structure):
    _fields_ = [('Flags', ctypes.c_uint32),
    ]


class DXGI_FRAME_STATISTICS_MEDIA(ctypes.Structure):
    _fields_ = [('PresentCount',            ctypes.c_uint32),
                ('PresentRefreshCount',     ctypes.c_uint32),
                ('SyncRefreshCount',        ctypes.c_uint32),
                ('SyncQPCTime',             ctypes.c_int64),
                ('SyncGPUTime',             ctypes.c_int64),
                ('CompositionMode',         DXGI_FRAME_PRESENTATION_MODE),
                ('ApprovedPresentDuration', ctypes.c_uint32),
    ]


class DXGI_MATRIX_3X2_F(ctypes.Structure):
    _fields_ = [('_11', ctypes.c_float),
                ('_12', ctypes.c_float),
                ('_21', ctypes.c_float),
                ('_22', ctypes.c_float),
                ('_31', ctypes.c_float),
                ('_32', ctypes.c_float),
    ]


## ---------------------------------------------- interfaces ----


class IDXGIDecodeSwapChain(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{2633066b-4514-4c7a-8fd8-12ea98059d18}")


class IDXGIDevice3(IDXGIDevice2):
    _iid_ = comtypes.GUID("{6007896c-3244-4afd-bf18-a6d3beda5023}")


class IDXGIFactory3(IDXGIFactory2):
    _iid_ = comtypes.GUID("{25483823-cd46-4c7d-86ca-47aa95b837bd}")


class IDXGIFactoryMedia(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{41e7d1f2-a591-4f7b-a2e5-fa9c843e1c12}")


class IDXGIOutput2(IDXGIOutput1):
    _iid_ = comtypes.GUID("{595e39d1-2724-4663-99b1-da969de28364}")


class IDXGIOutput3(IDXGIOutput2):
    _iid_ = comtypes.GUID("{8a6bb301-7e7e-41F4-a8e0-5b32f7f99b18}")


class IDXGISwapChain2(IDXGISwapChain1):
    _iid_ = comtypes.GUID("{a8be2ac4-199f-4946-b331-79599fb98de7}")


class IDXGISwapChainMedia(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{dd95b90b-f05f-4f6a-bd65-25bfb264bd84}")


## ------------------------- vtables, assigned once every class exists ----

IDXGIDecodeSwapChain._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "PresentBuffer", [
        ctypes.c_uint32,                             # UINT BufferToPresent
        ctypes.c_uint32,                             # UINT SyncInterval
        ctypes.c_uint32,                             # UINT Flags
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetSourceRect", [
        ctypes.POINTER(wintypes.RECT),               # RECT* pRect
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetTargetRect", [
        ctypes.POINTER(wintypes.RECT),               # RECT* pRect
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetDestSize", [
        ctypes.c_uint32,                             # UINT Width
        ctypes.c_uint32,                             # UINT Height
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetSourceRect", [
        ctypes.POINTER(wintypes.RECT),               # RECT* pRect
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetTargetRect", [
        ctypes.POINTER(wintypes.RECT),               # RECT* pRect
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDestSize", [
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pWidth
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pHeight
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetColorSpace", [
        DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAGS,         # DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAGS ColorSpace
        ]),
    comtypes.STDMETHOD(DXGI_MULTIPLANE_OVERLAY_YCbCr_FLAGS, "GetColorSpace", []),
]

IDXGIDevice3._methods_ = [
    comtypes.STDMETHOD(None, "Trim", []),
]

IDXGIFactory3._methods_ = [
    comtypes.STDMETHOD(ctypes.c_uint32, "GetCreationFlags", []),
]

IDXGIFactoryMedia._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateSwapChainForCompositionSurfaceHandle", [
        ctypes.POINTER(comtypes.IUnknown),           # IUnknown* pDevice
        ctypes.c_void_p,                             # HANDLE hSurface
        ctypes.POINTER(DXGI_SWAP_CHAIN_DESC1),       # DXGI_SWAP_CHAIN_DESC1* pDesc
        ctypes.POINTER(IDXGIOutput),                 # IDXGIOutput* pRestrictToOutput
        ctypes.POINTER(ctypes.POINTER(IDXGISwapChain1)), # IDXGISwapChain1** ppSwapChain
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateDecodeSwapChainForCompositionSurfaceHandle", [
        ctypes.POINTER(comtypes.IUnknown),           # IUnknown* pDevice
        ctypes.c_void_p,                             # HANDLE hSurface
        ctypes.POINTER(DXGI_DECODE_SWAP_CHAIN_DESC), # DXGI_DECODE_SWAP_CHAIN_DESC* pDesc
        ctypes.POINTER(IDXGIResource),               # IDXGIResource* pYuvDecodeBuffers
        ctypes.POINTER(IDXGIOutput),                 # IDXGIOutput* pRestrictToOutput
        ctypes.POINTER(ctypes.POINTER(IDXGIDecodeSwapChain)), # IDXGIDecodeSwapChain** ppSwapChain
        ]),
]

IDXGIOutput2._methods_ = [
    comtypes.STDMETHOD(wintypes.BOOL, "SupportsOverlays", []),
]

IDXGIOutput3._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckOverlaySupport", [
        DXGI_FORMAT,                                 # DXGI_FORMAT EnumFormat
        ctypes.POINTER(comtypes.IUnknown),           # IUnknown* pConcernedDevice
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFlags
        ]),
]

IDXGISwapChain2._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SetSourceSize", [
        ctypes.c_uint32,                             # UINT Width
        ctypes.c_uint32,                             # UINT Height
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetSourceSize", [
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pWidth
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pHeight
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetMaximumFrameLatency", [
        ctypes.c_uint32,                             # UINT MaxLatency
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetMaximumFrameLatency", [
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pMaxLatency
        ]),
    comtypes.STDMETHOD(ctypes.c_void_p, "GetFrameLatencyWaitableObject", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetMatrixTransform", [
        ctypes.POINTER(DXGI_MATRIX_3X2_F),           # DXGI_MATRIX_3X2_F* pMatrix
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetMatrixTransform", [
        ctypes.POINTER(DXGI_MATRIX_3X2_F),           # DXGI_MATRIX_3X2_F* pMatrix
        ]),
]

IDXGISwapChainMedia._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "GetFrameStatisticsMedia", [
        ctypes.POINTER(DXGI_FRAME_STATISTICS_MEDIA), # DXGI_FRAME_STATISTICS_MEDIA* pStats
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetPresentDuration", [
        ctypes.c_uint32,                             # UINT Duration
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckPresentDurationSupport", [
        ctypes.c_uint32,                             # UINT DesiredPresentDuration
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pClosestSmallerPresentDuration
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pClosestLargerPresentDuration
        ]),
]


## -- End Of File --
