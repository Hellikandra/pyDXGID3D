##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from d3d11_4.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py d3d11_4.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES



from Direct3D.PyIdl.dxgi1_5 import *
from Direct3D.PyIdl.d3dcommon import *
from Direct3D.PyIdl.d3d11_3 import *


## -------------------------------------------- enumerations ----

D3D11_CRYPTO_SESSION_KEY_EXCHANGE_FLAGS = ctypes.c_uint
D3D11_CRYPTO_SESSION_KEY_EXCHANGE_FLAG_NONE = D3D11_CRYPTO_SESSION_KEY_EXCHANGE_FLAGS(0x0).value

D3D11_FEATURE_VIDEO = ctypes.c_uint
D3D11_FEATURE_VIDEO_DECODER_HISTOGRAM = D3D11_FEATURE_VIDEO(0).value

D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT = ctypes.c_uint
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_Y = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT(0).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_U = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT(1).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_V = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT(2).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_R = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT(0).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_G = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT(1).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_B = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT(2).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_A = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT(3).value

D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS = ctypes.c_uint
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_NONE = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS(0x0).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_Y    = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS((1 << D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_Y)).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_U    = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS((1 << D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_U)).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_V    = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS((1 << D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_V)).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_R    = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS((1 << D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_R)).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_G    = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS((1 << D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_G)).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_B    = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS((1 << D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_B)).value
D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAG_A    = D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS((1 << D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_A)).value


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class ID3D11Device4(ID3D11Device3):
    _iid_ = comtypes.GUID("{8992ab71-02e6-4b8d-ba48-b056dcda42c4}")


class ID3D11Device5(ID3D11Device4):
    _iid_ = comtypes.GUID("{8ffde202-a0e7-45df-9e01-e837801b5ea0}")


class ID3D11Multithread(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{9B7E4E00-342C-4106-A19F-4F2704F689F0}")


class ID3D11VideoContext2(ID3D11VideoContext1):
    _iid_ = comtypes.GUID("{C4E7374C-6243-4D1B-AE87-52B4F740E261}")


class ID3D11VideoContext3(ID3D11VideoContext2):
    _iid_ = comtypes.GUID("{A9E2FAA0-CB39-418F-A0B7-D8AAD4DE672E}")


class ID3D11VideoDevice2(ID3D11VideoDevice1):
    _iid_ = comtypes.GUID("{59C0CB01-35F0-4A70-8F67-87905C906A53}")


## ---------------------------------------------- structures ----


class D3D11_FEATURE_DATA_D3D11_OPTIONS4(ctypes.Structure):
    _fields_ = [('ExtendedNV12SharedTextureSupported', wintypes.BOOL),
    ]


class D3D11_FEATURE_DATA_VIDEO_DECODER_HISTOGRAM(ctypes.Structure):
    _fields_ = [('DecoderDesc',     D3D11_VIDEO_DECODER_DESC),
                ('Components',      D3D11_VIDEO_DECODER_HISTOGRAM_COMPONENT_FLAGS),
                ('BinCount',        ctypes.c_uint32),
                ('CounterBitDepth', ctypes.c_uint32),
    ]


class D3D11_VIDEO_DECODER_BUFFER_DESC2(ctypes.Structure):
    _fields_ = [('BufferType',             D3D11_VIDEO_DECODER_BUFFER_TYPE),
                ('DataOffset',             ctypes.c_uint32),
                ('DataSize',               ctypes.c_uint32),
                ('pIV',                    ctypes.c_void_p),
                ('IVSize',                 ctypes.c_uint32),
                ('pSubSampleMappingBlock', ctypes.POINTER(D3D11_VIDEO_DECODER_SUB_SAMPLE_MAPPING_BLOCK)),
                ('SubSampleMappingCount',  ctypes.c_uint32),
                ('cBlocksStripeEncrypted', ctypes.c_uint32),
                ('cBlocksStripeClear',     ctypes.c_uint32),
    ]


## ------------------------- vtables, assigned once every class exists ----

ID3D11Device4._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "RegisterDeviceRemovedEvent", [
        ctypes.c_void_p,                             # HANDLE hEvent
        ctypes.POINTER(ctypes.c_uint32),             # DWORD* pdwCookie
        ]),
    comtypes.STDMETHOD(None, "UnregisterDeviceRemoved", [
        ctypes.c_uint32,                             # DWORD dwCookie
        ]),
]

ID3D11Device5._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "OpenSharedFence", [
        ctypes.c_void_p,                             # HANDLE hFence
        comtypes.GUID,                               # REFIID ReturnedInterface
        ctypes.POINTER(ctypes.c_void_p),             # void** ppFence
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateFence", [
        ctypes.c_uint64,                             # UINT64 InitialValue
        D3D11_FENCE_FLAG,                            # D3D11_FENCE_FLAG Flags
        comtypes.GUID,                               # REFIID ReturnedInterface
        ctypes.POINTER(ctypes.c_void_p),             # void** ppFence
        ]),
]

ID3D11Multithread._methods_ = [
    comtypes.STDMETHOD(None, "Enter", []),
    comtypes.STDMETHOD(None, "Leave", []),
    comtypes.STDMETHOD(wintypes.BOOL, "SetMultithreadProtected", [
        wintypes.BOOL,                               # BOOL bMTProtect
        ]),
    comtypes.STDMETHOD(wintypes.BOOL, "GetMultithreadProtected", []),
]

ID3D11VideoContext2._methods_ = [
    comtypes.STDMETHOD(None, "VideoProcessorSetOutputHDRMetaData", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        DXGI_HDR_METADATA_TYPE,                      # DXGI_HDR_METADATA_TYPE Type
        ctypes.c_uint32,                             # UINT Size
        ctypes.c_void_p,                             # void* pHDRMetaData
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorGetOutputHDRMetaData", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.POINTER(DXGI_HDR_METADATA_TYPE),      # DXGI_HDR_METADATA_TYPE* pType
        ctypes.c_uint32,                             # UINT Size
        ctypes.c_void_p,                             # void* pMetaData
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorSetStreamHDRMetaData", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.c_uint32,                             # UINT StreamIndex
        DXGI_HDR_METADATA_TYPE,                      # DXGI_HDR_METADATA_TYPE Type
        ctypes.c_uint32,                             # UINT Size
        ctypes.c_void_p,                             # void* pHDRMetaData
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorGetStreamHDRMetaData", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.c_uint32,                             # UINT StreamIndex
        ctypes.POINTER(DXGI_HDR_METADATA_TYPE),      # DXGI_HDR_METADATA_TYPE* pType
        ctypes.c_uint32,                             # UINT Size
        ctypes.c_void_p,                             # void* pMetaData
        ]),
]

ID3D11VideoContext3._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "DecoderBeginFrame1", [
        ctypes.POINTER(ID3D11VideoDecoder),          # ID3D11VideoDecoder* pDecoder
        ctypes.POINTER(ID3D11VideoDecoderOutputView), # ID3D11VideoDecoderOutputView* pView
        ctypes.c_uint32,                             # UINT ContentKeySize
        ctypes.c_void_p,                             # void* pContentKey
        ctypes.c_uint32,                             # UINT NumComponentHistograms
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pHistogramOffsets
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppHistogramBuffers
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SubmitDecoderBuffers2", [
        ctypes.POINTER(ID3D11VideoDecoder),          # ID3D11VideoDecoder* pDecoder
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(D3D11_VIDEO_DECODER_BUFFER_DESC2), # D3D11_VIDEO_DECODER_BUFFER_DESC2* pBufferDesc
        ]),
]

ID3D11VideoDevice2._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckFeatureSupport", [
        D3D11_FEATURE_VIDEO,                         # D3D11_FEATURE_VIDEO Feature
        ctypes.c_void_p,                             # void* pFeatureSupportData
        ctypes.c_uint32,                             # UINT FeatureSupportDataSize
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "NegotiateCryptoSessionKeyExchangeMT", [
        ctypes.POINTER(ID3D11CryptoSession),         # ID3D11CryptoSession* pCryptoSession
        D3D11_CRYPTO_SESSION_KEY_EXCHANGE_FLAGS,     # D3D11_CRYPTO_SESSION_KEY_EXCHANGE_FLAGS flags
        ctypes.c_uint32,                             # UINT DataSize
        ctypes.c_void_p,                             # void* pData
        ]),
]


## -- End Of File --
