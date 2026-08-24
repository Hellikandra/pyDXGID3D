##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from dxgi1_5.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py dxgi1_5.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES


from Direct3D.PyIdl.dxgi1_4 import *


## -------------------------------------------- enumerations ----

DXGI_FEATURE = ctypes.c_uint
DXGI_FEATURE_PRESENT_ALLOW_TEARING = DXGI_FEATURE(0).value

DXGI_HDR_METADATA_TYPE = ctypes.c_uint
DXGI_HDR_METADATA_TYPE_NONE      = DXGI_HDR_METADATA_TYPE(0).value
DXGI_HDR_METADATA_TYPE_HDR10     = DXGI_HDR_METADATA_TYPE(1).value
DXGI_HDR_METADATA_TYPE_HDR10PLUS = DXGI_HDR_METADATA_TYPE(2).value

DXGI_OFFER_RESOURCE_FLAGS = ctypes.c_uint
DXGI_OFFER_RESOURCE_FLAG_ALLOW_DECOMMIT = DXGI_OFFER_RESOURCE_FLAGS(0x1).value

DXGI_OUTDUPL_FLAG = ctypes.c_uint
DXGI_OUTDUPL_COMPOSITED_UI_CAPTURE_ONLY = DXGI_OUTDUPL_FLAG(1).value

DXGI_RECLAIM_RESOURCE_RESULTS = ctypes.c_uint
DXGI_RECLAIM_RESOURCE_RESULT_OK            = DXGI_RECLAIM_RESOURCE_RESULTS(0).value
DXGI_RECLAIM_RESOURCE_RESULT_DISCARDED     = DXGI_RECLAIM_RESOURCE_RESULTS(1).value
DXGI_RECLAIM_RESOURCE_RESULT_NOT_COMMITTED = DXGI_RECLAIM_RESOURCE_RESULTS(2).value


## ---------------------------------------------- structures ----


class DXGI_HDR_METADATA_HDR10(ctypes.Structure):
    _fields_ = [('RedPrimary',                ctypes.c_uint16 * 2),
                ('GreenPrimary',              ctypes.c_uint16 * 2),
                ('BluePrimary',               ctypes.c_uint16 * 2),
                ('WhitePoint',                ctypes.c_uint16 * 2),
                ('MaxMasteringLuminance',     ctypes.c_uint32),
                ('MinMasteringLuminance',     ctypes.c_uint32),
                ('MaxContentLightLevel',      ctypes.c_uint16),
                ('MaxFrameAverageLightLevel', ctypes.c_uint16),
    ]


class DXGI_HDR_METADATA_HDR10PLUS(ctypes.Structure):
    _fields_ = [('Data', ctypes.c_ubyte * 72),
    ]


## ---------------------------------------------- interfaces ----


class IDXGIDevice4(IDXGIDevice3):
    _iid_ = comtypes.GUID("{95B4F95F-D8DA-4CA4-9EE6-3B76D5968A10}")


class IDXGIFactory5(IDXGIFactory4):
    _iid_ = comtypes.GUID("{7632e1f5-ee65-4dca-87fd-84cd75f8838d}")


class IDXGIOutput5(IDXGIOutput4):
    _iid_ = comtypes.GUID("{80A07424-AB52-42EB-833C-0C42FD282D98}")


class IDXGISwapChain4(IDXGISwapChain3):
    _iid_ = comtypes.GUID("{3D585D5A-BD4A-489E-B1F4-3DBCB6452FFB}")


## ------------------------- vtables, assigned once every class exists ----

IDXGIDevice4._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "OfferResources1", [
        ctypes.c_uint32,                             # UINT NumResources
        ctypes.POINTER(ctypes.POINTER(IDXGIResource)), # IDXGIResource** ppResources
        DXGI_OFFER_RESOURCE_PRIORITY,                # DXGI_OFFER_RESOURCE_PRIORITY Priority
        ctypes.c_uint32,                             # UINT Flags
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "ReclaimResources1", [
        ctypes.c_uint32,                             # UINT NumResources
        ctypes.POINTER(ctypes.POINTER(IDXGIResource)), # IDXGIResource** ppResources
        ctypes.POINTER(DXGI_RECLAIM_RESOURCE_RESULTS), # DXGI_RECLAIM_RESOURCE_RESULTS* pResults
        ]),
]

IDXGIFactory5._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckFeatureSupport", [
        DXGI_FEATURE,                                # DXGI_FEATURE Feature
        ctypes.c_void_p,                             # void* pFeatureSupportData
        ctypes.c_uint32,                             # UINT FeatureSupportDataSize
        ]),
]

IDXGIOutput5._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "DuplicateOutput1", [
        ctypes.POINTER(comtypes.IUnknown),           # IUnknown* pDevice
        ctypes.c_uint32,                             # UINT Flags
        ctypes.c_uint32,                             # UINT SupportedFormatsCount
        ctypes.POINTER(DXGI_FORMAT),                 # DXGI_FORMAT* pSupportedFormats
        ctypes.POINTER(ctypes.POINTER(IDXGIOutputDuplication)), # IDXGIOutputDuplication** ppOutputDuplication
        ]),
]

IDXGISwapChain4._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SetHDRMetaData", [
        DXGI_HDR_METADATA_TYPE,                      # DXGI_HDR_METADATA_TYPE Type
        ctypes.c_uint32,                             # UINT Size
        ctypes.c_void_p,                             # void* pMetaData
        ]),
]


## -- End Of File --
