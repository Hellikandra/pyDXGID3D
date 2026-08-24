##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from d3d11_1.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py d3d11_1.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES


from Direct3D.PyIdl.dxgi1_2 import *
from Direct3D.PyIdl.d3dcommon import *
from Direct3D.PyIdl.d3d11 import *


## -------------------------------------------- enumerations ----

D3D11_1_CREATE_DEVICE_CONTEXT_STATE_FLAG = ctypes.c_uint
D3D11_1_CREATE_DEVICE_CONTEXT_STATE_SINGLETHREADED = D3D11_1_CREATE_DEVICE_CONTEXT_STATE_FLAG(0x1).value

D3D11_COPY_FLAGS = ctypes.c_uint
D3D11_COPY_NO_OVERWRITE = D3D11_COPY_FLAGS(0x00000001).value
D3D11_COPY_DISCARD      = D3D11_COPY_FLAGS(0x00000002).value

D3D11_CRYPTO_SESSION_STATUS = ctypes.c_uint
D3D11_CRYPTO_SESSION_STATUS_OK                   = D3D11_CRYPTO_SESSION_STATUS(0).value
D3D11_CRYPTO_SESSION_STATUS_KEY_LOST             = D3D11_CRYPTO_SESSION_STATUS(1).value
D3D11_CRYPTO_SESSION_STATUS_KEY_AND_CONTENT_LOST = D3D11_CRYPTO_SESSION_STATUS(2).value

D3D11_LOGIC_OP = ctypes.c_uint
D3D11_LOGIC_OP_CLEAR         = D3D11_LOGIC_OP(0).value
D3D11_LOGIC_OP_SET           = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_COPY          = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_COPY_INVERTED = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_NOOP          = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_INVERT        = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_AND           = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_NAND          = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_OR            = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_NOR           = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_XOR           = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_EQUIV         = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_AND_REVERSE   = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_AND_INVERTED  = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_OR_REVERSE    = D3D11_LOGIC_OP().value
D3D11_LOGIC_OP_OR_INVERTED   = D3D11_LOGIC_OP().value

D3D11_VIDEO_DECODER_CAPS = ctypes.c_uint
D3D11_VIDEO_DECODER_CAPS_DOWNSAMPLE          = D3D11_VIDEO_DECODER_CAPS(0x1).value
D3D11_VIDEO_DECODER_CAPS_NON_REAL_TIME       = D3D11_VIDEO_DECODER_CAPS(0x02).value
D3D11_VIDEO_DECODER_CAPS_DOWNSAMPLE_DYNAMIC  = D3D11_VIDEO_DECODER_CAPS(0x04).value
D3D11_VIDEO_DECODER_CAPS_DOWNSAMPLE_REQUIRED = D3D11_VIDEO_DECODER_CAPS(0x08).value
D3D11_VIDEO_DECODER_CAPS_UNSUPPORTED         = D3D11_VIDEO_DECODER_CAPS(0x10).value

D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINTS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINT_MULTIPLANE_OVERLAY_ROTATION               = D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINTS(0x01).value
D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINT_MULTIPLANE_OVERLAY_RESIZE                 = D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINTS(0x02).value
D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINT_MULTIPLANE_OVERLAY_COLOR_SPACE_CONVERSION = D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINTS(0x04).value
D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINT_TRIPLE_BUFFER_OUTPUT                      = D3D11_VIDEO_PROCESSOR_BEHAVIOR_HINTS(0x08).value


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class ID3D11BlendState1(ID3D11BlendState):
    _iid_ = comtypes.GUID("{cc86fabe-da55-401d-85e7-e3c9de2877e9}")


class ID3D11Device1(ID3D11Device):
    _iid_ = comtypes.GUID("{a04bfb29-08ef-43d6-a49c-a9bdbdcbe686}")


class ID3D11DeviceContext1(ID3D11DeviceContext):
    _iid_ = comtypes.GUID("{bb2c6faa-b5fb-4082-8e6b-388b8cfa90e1}")


class ID3D11RasterizerState1(ID3D11RasterizerState):
    _iid_ = comtypes.GUID("{1217d7a6-5039-418c-b042-9cbe256afd6e}")


class ID3D11VideoContext1(ID3D11VideoContext):
    _iid_ = comtypes.GUID("{A7F026DA-A5F8-4487-A564-15E34357651E}")


class ID3D11VideoDevice1(ID3D11VideoDevice):
    _iid_ = comtypes.GUID("{29DA1D51-1321-4454-804B-F5FC9F861F0F}")


class ID3D11VideoProcessorEnumerator1(ID3D11VideoProcessorEnumerator):
    _iid_ = comtypes.GUID("{465217F2-5568-43CF-B5B9-F61D54531CA1}")


class ID3DDeviceContextState(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{5c1e0d8a-7c23-48f9-8c59-a92958ceff11}")


class ID3DUserDefinedAnnotation(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{b2daad8b-03d4-4dbf-95eb-32ab4b63d0ab}")


## ---------------------------------------------- structures ----


class D3D11_KEY_EXCHANGE_HW_PROTECTION_INPUT_DATA(ctypes.Structure):
    _fields_ = [('PrivateDataSize',      ctypes.c_uint32),
                ('HWProtectionDataSize', ctypes.c_uint32),
                ('pbInput',              ctypes.c_ubyte * 4),
    ]


class D3D11_KEY_EXCHANGE_HW_PROTECTION_OUTPUT_DATA(ctypes.Structure):
    _fields_ = [('PrivateDataSize',         ctypes.c_uint32),
                ('MaxHWProtectionDataSize', ctypes.c_uint32),
                ('HWProtectionDataSize',    ctypes.c_uint32),
                ('TransportTime',           ctypes.c_uint64),
                ('ExecutionTime',           ctypes.c_uint64),
                ('pbOutput',                ctypes.c_ubyte * 4),
    ]


class D3D11_RASTERIZER_DESC1(ctypes.Structure):
    _fields_ = [('FillMode',              D3D11_FILL_MODE),
                ('CullMode',              D3D11_CULL_MODE),
                ('FrontCounterClockwise', wintypes.BOOL),
                ('DepthBias',             ctypes.c_int32),
                ('DepthBiasClamp',        ctypes.c_float),
                ('SlopeScaledDepthBias',  ctypes.c_float),
                ('DepthClipEnable',       wintypes.BOOL),
                ('ScissorEnable',         wintypes.BOOL),
                ('MultisampleEnable',     wintypes.BOOL),
                ('AntialiasedLineEnable', wintypes.BOOL),
                ('ForcedSampleCount',     ctypes.c_uint32),
    ]


class D3D11_RENDER_TARGET_BLEND_DESC1(ctypes.Structure):
    _fields_ = [('BlendEnable',           wintypes.BOOL),
                ('LogicOpEnable',         wintypes.BOOL),
                ('SrcBlend',              D3D11_BLEND),
                ('DestBlend',             D3D11_BLEND),
                ('BlendOp',               D3D11_BLEND_OP),
                ('SrcBlendAlpha',         D3D11_BLEND),
                ('DestBlendAlpha',        D3D11_BLEND),
                ('BlendOpAlpha',          D3D11_BLEND_OP),
                ('LogicOp',               D3D11_LOGIC_OP),
                ('RenderTargetWriteMask', ctypes.c_uint8),
    ]


class D3D11_VIDEO_DECODER_BEGIN_FRAME_CRYPTO_SESSION(ctypes.Structure):
    _fields_ = [('pCryptoSession',  ctypes.POINTER(ID3D11CryptoSession)),
                ('BlobSize',        ctypes.c_uint32),
                ('pBlob',           ctypes.c_void_p),
                ('pKeyInfoId',      ctypes.POINTER(comtypes.GUID)),
                ('PrivateDataSize', ctypes.c_uint32),
                ('pPrivateData',    ctypes.c_void_p),
    ]


class D3D11_VIDEO_DECODER_SUB_SAMPLE_MAPPING_BLOCK(ctypes.Structure):
    _fields_ = [('ClearSize',     ctypes.c_uint32),
                ('EncryptedSize', ctypes.c_uint32),
    ]


class D3D11_VIDEO_PROCESSOR_STREAM_BEHAVIOR_HINT(ctypes.Structure):
    _fields_ = [('Enable', wintypes.BOOL),
                ('Width',  ctypes.c_uint32),
                ('Height', ctypes.c_uint32),
                ('Format', DXGI_FORMAT),
    ]


class D3D11_VIDEO_SAMPLE_DESC(ctypes.Structure):
    _fields_ = [('Width',      ctypes.c_uint32),
                ('Height',     ctypes.c_uint32),
                ('Format',     DXGI_FORMAT),
                ('ColorSpace', DXGI_COLOR_SPACE_TYPE),
    ]


class D3D11_BLEND_DESC1(ctypes.Structure):
    _fields_ = [('AlphaToCoverageEnable',  wintypes.BOOL),
                ('IndependentBlendEnable', wintypes.BOOL),
                ('RenderTarget',           D3D11_RENDER_TARGET_BLEND_DESC1 * D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT),
    ]


class D3D11_KEY_EXCHANGE_HW_PROTECTION_DATA(ctypes.Structure):
    _fields_ = [('HWProtectionFunctionID', ctypes.c_uint32),
                ('pInputData',             ctypes.POINTER(D3D11_KEY_EXCHANGE_HW_PROTECTION_INPUT_DATA)),
                ('pOutputData',            ctypes.POINTER(D3D11_KEY_EXCHANGE_HW_PROTECTION_OUTPUT_DATA)),
                ('Status',                 comtypes.HRESULT),
    ]


class D3D11_VIDEO_DECODER_BUFFER_DESC1(ctypes.Structure):
    _fields_ = [('BufferType',             D3D11_VIDEO_DECODER_BUFFER_TYPE),
                ('DataOffset',             ctypes.c_uint32),
                ('DataSize',               ctypes.c_uint32),
                ('pIV',                    ctypes.c_void_p),
                ('IVSize',                 ctypes.c_uint32),
                ('pSubSampleMappingBlock', ctypes.POINTER(D3D11_VIDEO_DECODER_SUB_SAMPLE_MAPPING_BLOCK)),
                ('SubSampleMappingCount',  ctypes.c_uint32),
    ]


## ------------------------- vtables, assigned once every class exists ----

ID3D11BlendState1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_BLEND_DESC1),           # D3D11_BLEND_DESC1* pDesc
        ]),
]

ID3D11Device1._methods_ = [
    comtypes.STDMETHOD(None, "GetImmediateContext1", [
        ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext1)), # ID3D11DeviceContext1** ppImmediateContext
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateDeferredContext1", [
        ctypes.c_uint32,                             # UINT ContextFlags
        ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext1)), # ID3D11DeviceContext1** ppDeferredContext
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateBlendState1", [
        ctypes.POINTER(D3D11_BLEND_DESC1),           # D3D11_BLEND_DESC1* pBlendStateDesc
        ctypes.POINTER(ctypes.POINTER(ID3D11BlendState1)), # ID3D11BlendState1** ppBlendState
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateRasterizerState1", [
        ctypes.POINTER(D3D11_RASTERIZER_DESC1),      # D3D11_RASTERIZER_DESC1* pRasterizerDesc
        ctypes.POINTER(ctypes.POINTER(ID3D11RasterizerState1)), # ID3D11RasterizerState1** ppRasterizerState
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateDeviceContextState", [
        ctypes.c_uint32,                             # UINT Flags
        ctypes.POINTER(D3D_FEATURE_LEVEL),           # D3D_FEATURE_LEVEL* pFeatureLevels
        ctypes.c_uint32,                             # UINT FeatureLevels
        ctypes.c_uint32,                             # UINT SDKVersion
        comtypes.GUID,                               # REFIID EmulatedInterface
        ctypes.POINTER(D3D_FEATURE_LEVEL),           # D3D_FEATURE_LEVEL* pChosenFeatureLevel
        ctypes.POINTER(ctypes.POINTER(ID3DDeviceContextState)), # ID3DDeviceContextState** ppContextState
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "OpenSharedResource1", [
        ctypes.c_void_p,                             # HANDLE hResource
        comtypes.GUID,                               # REFIID returnedInterface
        ctypes.POINTER(ctypes.c_void_p),             # void** ppResource
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "OpenSharedResourceByName", [
        ctypes.c_wchar_p,                            # LPCWSTR lpName
        ctypes.c_uint32,                             # DWORD dwDesiredAccess
        comtypes.GUID,                               # REFIID returnedInterface
        ctypes.POINTER(ctypes.c_void_p),             # void** ppResource
        ]),
]

ID3D11DeviceContext1._methods_ = [
    comtypes.STDMETHOD(None, "CopySubresourceRegion1", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pDstResource
        ctypes.c_uint32,                             # UINT DstSubresource
        ctypes.c_uint32,                             # UINT DstX
        ctypes.c_uint32,                             # UINT DstY
        ctypes.c_uint32,                             # UINT DstZ
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pSrcResource
        ctypes.c_uint32,                             # UINT SrcSubresource
        ctypes.POINTER(D3D11_BOX),                   # D3D11_BOX* pSrcBox
        ctypes.c_uint32,                             # UINT CopyFlags
        ]),
    comtypes.STDMETHOD(None, "UpdateSubresource1", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pDstResource
        ctypes.c_uint32,                             # UINT DstSubresource
        ctypes.POINTER(D3D11_BOX),                   # D3D11_BOX* pDstBox
        ctypes.c_void_p,                             # void* pSrcData
        ctypes.c_uint32,                             # UINT SrcRowPitch
        ctypes.c_uint32,                             # UINT SrcDepthPitch
        ctypes.c_uint32,                             # UINT CopyFlags
        ]),
    comtypes.STDMETHOD(None, "DiscardResource", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pResource
        ]),
    comtypes.STDMETHOD(None, "DiscardView", [
        ctypes.POINTER(ID3D11View),                  # ID3D11View* pResourceView
        ]),
    comtypes.STDMETHOD(None, "VSSetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "HSSetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "DSSetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "GSSetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "PSSetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "CSSetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "VSGetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "HSGetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "DSGetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "GSGetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "PSGetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "CSGetConstantBuffers1", [
        ctypes.c_uint32,                             # UINT StartSlot
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)), # ID3D11Buffer** ppConstantBuffers
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pFirstConstant
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumConstants
        ]),
    comtypes.STDMETHOD(None, "SwapDeviceContextState", [
        ctypes.POINTER(ID3DDeviceContextState),      # ID3DDeviceContextState* pState
        ctypes.POINTER(ctypes.POINTER(ID3DDeviceContextState)), # ID3DDeviceContextState** ppPreviousState
        ]),
    comtypes.STDMETHOD(None, "ClearView", [
        ctypes.POINTER(ID3D11View),                  # ID3D11View* pView
        ctypes.c_float,                              # FLOAT Color
        ctypes.POINTER(D3D11_RECT),                  # D3D11_RECT* pRect
        ctypes.c_uint32,                             # UINT NumRects
        ]),
    comtypes.STDMETHOD(None, "DiscardView1", [
        ctypes.POINTER(ID3D11View),                  # ID3D11View* pResourceView
        ctypes.POINTER(D3D11_RECT),                  # D3D11_RECT* pRects
        ctypes.c_uint32,                             # UINT NumRects
        ]),
]

ID3D11RasterizerState1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_RASTERIZER_DESC1),      # D3D11_RASTERIZER_DESC1* pDesc
        ]),
]

ID3D11VideoContext1._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SubmitDecoderBuffers1", [
        ctypes.POINTER(ID3D11VideoDecoder),          # ID3D11VideoDecoder* pDecoder
        ctypes.c_uint32,                             # UINT NumBuffers
        ctypes.POINTER(D3D11_VIDEO_DECODER_BUFFER_DESC1), # D3D11_VIDEO_DECODER_BUFFER_DESC1* pBufferDesc
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDataForNewHardwareKey", [
        ctypes.POINTER(ID3D11CryptoSession),         # ID3D11CryptoSession* pCryptoSession
        ctypes.c_uint32,                             # UINT PrivateInputSize
        ctypes.c_void_p,                             # void* pPrivatInputData
        ctypes.POINTER(ctypes.c_uint64),             # UINT64* pPrivateOutputData
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckCryptoSessionStatus", [
        ctypes.POINTER(ID3D11CryptoSession),         # ID3D11CryptoSession* pCryptoSession
        ctypes.POINTER(D3D11_CRYPTO_SESSION_STATUS), # D3D11_CRYPTO_SESSION_STATUS* pStatus
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "DecoderEnableDownsampling", [
        ctypes.POINTER(ID3D11VideoDecoder),          # ID3D11VideoDecoder* pDecoder
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE InputColorSpace
        ctypes.POINTER(D3D11_VIDEO_SAMPLE_DESC),     # D3D11_VIDEO_SAMPLE_DESC* pOutputDesc
        ctypes.c_uint32,                             # UINT ReferenceFrameCount
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "DecoderUpdateDownsampling", [
        ctypes.POINTER(ID3D11VideoDecoder),          # ID3D11VideoDecoder* pDecoder
        ctypes.POINTER(D3D11_VIDEO_SAMPLE_DESC),     # D3D11_VIDEO_SAMPLE_DESC* pOutputDesc
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorSetOutputColorSpace1", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE ColorSpace
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorSetOutputShaderUsage", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        wintypes.BOOL,                               # BOOL ShaderUsage
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorGetOutputColorSpace1", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.POINTER(DXGI_COLOR_SPACE_TYPE),       # DXGI_COLOR_SPACE_TYPE* pColorSpace
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorGetOutputShaderUsage", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pShaderUsage
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorSetStreamColorSpace1", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.c_uint32,                             # UINT StreamIndex
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE ColorSpace
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorSetStreamMirror", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.c_uint32,                             # UINT StreamIndex
        wintypes.BOOL,                               # BOOL Enable
        wintypes.BOOL,                               # BOOL FlipHorizontal
        wintypes.BOOL,                               # BOOL FlipVertical
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorGetStreamColorSpace1", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.c_uint32,                             # UINT StreamIndex
        ctypes.POINTER(DXGI_COLOR_SPACE_TYPE),       # DXGI_COLOR_SPACE_TYPE* pColorSpace
        ]),
    comtypes.STDMETHOD(None, "VideoProcessorGetStreamMirror", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.c_uint32,                             # UINT StreamIndex
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pEnable
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pFlipHorizontal
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pFlipVertical
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "VideoProcessorGetBehaviorHints", [
        ctypes.POINTER(ID3D11VideoProcessor),        # ID3D11VideoProcessor* pVideoProcessor
        ctypes.c_uint32,                             # UINT OutputWidth
        ctypes.c_uint32,                             # UINT OutputHeight
        DXGI_FORMAT,                                 # DXGI_FORMAT OutputFormat
        ctypes.c_uint32,                             # UINT StreamCount
        ctypes.POINTER(D3D11_VIDEO_PROCESSOR_STREAM_BEHAVIOR_HINT), # D3D11_VIDEO_PROCESSOR_STREAM_BEHAVIOR_HINT* pStreams
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pBehaviorHints
        ]),
]

ID3D11VideoDevice1._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "GetCryptoSessionPrivateDataSize", [
        ctypes.POINTER(comtypes.GUID),               # GUID* pCryptoType
        ctypes.POINTER(comtypes.GUID),               # GUID* pDecoderProfile
        ctypes.POINTER(comtypes.GUID),               # GUID* pKeyExchangeType
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pPrivateInputSize
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pPrivateOutputSize
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoDecoderCaps", [
        ctypes.POINTER(comtypes.GUID),               # GUID* pDecoderProfile
        ctypes.c_uint32,                             # UINT SampleWidth
        ctypes.c_uint32,                             # UINT SampleHeight
        ctypes.POINTER(DXGI_RATIONAL),               # DXGI_RATIONAL* pFrameRate
        ctypes.c_uint32,                             # UINT BitRate
        ctypes.POINTER(comtypes.GUID),               # GUID* pCryptoType
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pDecoderCaps
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckVideoDecoderDownsampling", [
        ctypes.POINTER(D3D11_VIDEO_DECODER_DESC),    # D3D11_VIDEO_DECODER_DESC* pInputDesc
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE InputColorSpace
        ctypes.POINTER(D3D11_VIDEO_DECODER_CONFIG),  # D3D11_VIDEO_DECODER_CONFIG* pInputConfig
        ctypes.POINTER(DXGI_RATIONAL),               # DXGI_RATIONAL* pFrameRate
        ctypes.POINTER(D3D11_VIDEO_SAMPLE_DESC),     # D3D11_VIDEO_SAMPLE_DESC* pOutputDesc
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pSupported
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pRealTimeHint
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "RecommendVideoDecoderDownsampleParameters", [
        ctypes.POINTER(D3D11_VIDEO_DECODER_DESC),    # D3D11_VIDEO_DECODER_DESC* pInputDesc
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE InputColorSpace
        ctypes.POINTER(D3D11_VIDEO_DECODER_CONFIG),  # D3D11_VIDEO_DECODER_CONFIG* pInputConfig
        ctypes.POINTER(DXGI_RATIONAL),               # DXGI_RATIONAL* pFrameRate
        ctypes.POINTER(D3D11_VIDEO_SAMPLE_DESC),     # D3D11_VIDEO_SAMPLE_DESC* pRecommendedOutputDesc
        ]),
]

ID3D11VideoProcessorEnumerator1._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckVideoProcessorFormatConversion", [
        DXGI_FORMAT,                                 # DXGI_FORMAT InputFormat
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE InputColorSpace
        DXGI_FORMAT,                                 # DXGI_FORMAT OutputFormat
        DXGI_COLOR_SPACE_TYPE,                       # DXGI_COLOR_SPACE_TYPE OutputColorSpace
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pSupported
        ]),
]

## ID3DDeviceContextState adds no methods to ID3D11DeviceChild.

ID3DUserDefinedAnnotation._methods_ = [
    comtypes.STDMETHOD(ctypes.c_int32, "BeginEvent", [
        ctypes.c_wchar_p,                            # LPCWSTR Name
        ]),
    comtypes.STDMETHOD(ctypes.c_int32, "EndEvent", []),
    comtypes.STDMETHOD(None, "SetMarker", [
        ctypes.c_wchar_p,                            # LPCWSTR Name
        ]),
    comtypes.STDMETHOD(wintypes.BOOL, "GetStatus", []),
]


## -- End Of File --
