##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from d3d11_3.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py d3d11_3.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES


from Direct3D.PyIdl.dxgi1_3 import *
from Direct3D.PyIdl.d3dcommon import *
from Direct3D.PyIdl.d3d11_2 import *


## -------------------------------------------- enumerations ----

D3D11_CONSERVATIVE_RASTERIZATION_MODE = ctypes.c_uint
D3D11_CONSERVATIVE_RASTERIZATION_MODE_OFF = D3D11_CONSERVATIVE_RASTERIZATION_MODE(0).value
D3D11_CONSERVATIVE_RASTERIZATION_MODE_ON  = D3D11_CONSERVATIVE_RASTERIZATION_MODE(1).value

D3D11_CONTEXT_TYPE = ctypes.c_uint
D3D11_CONTEXT_TYPE_ALL     = D3D11_CONTEXT_TYPE(0).value
D3D11_CONTEXT_TYPE_3D      = D3D11_CONTEXT_TYPE(1).value
D3D11_CONTEXT_TYPE_COMPUTE = D3D11_CONTEXT_TYPE(2).value
D3D11_CONTEXT_TYPE_COPY    = D3D11_CONTEXT_TYPE(3).value
D3D11_CONTEXT_TYPE_VIDEO   = D3D11_CONTEXT_TYPE(4).value

D3D11_FENCE_FLAG = ctypes.c_uint
D3D11_FENCE_FLAG_NONE                 = D3D11_FENCE_FLAG(0x0).value
D3D11_FENCE_FLAG_SHARED               = D3D11_FENCE_FLAG(0x2).value
D3D11_FENCE_FLAG_SHARED_CROSS_ADAPTER = D3D11_FENCE_FLAG(0x4).value
D3D11_FENCE_FLAG_NON_MONITORED        = D3D11_FENCE_FLAG(0x8).value

D3D11_TEXTURE_LAYOUT = ctypes.c_uint
D3D11_TEXTURE_LAYOUT_UNDEFINED            = D3D11_TEXTURE_LAYOUT(0).value
D3D11_TEXTURE_LAYOUT_ROW_MAJOR            = D3D11_TEXTURE_LAYOUT(1).value
D3D11_TEXTURE_LAYOUT_64K_STANDARD_SWIZZLE = D3D11_TEXTURE_LAYOUT(2).value


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class ID3D11Device3(ID3D11Device2):
    _iid_ = comtypes.GUID("{A05C8C37-D2C6-4732-B3A0-9CE0B0DC9AE6}")


class ID3D11DeviceContext3(ID3D11DeviceContext2):
    _iid_ = comtypes.GUID("{b4e3c01d-e79e-4637-91b2-510e9f4c9b8f}")


class ID3D11DeviceContext4(ID3D11DeviceContext3):
    _iid_ = comtypes.GUID("{917600da-f58c-4c33-98d8-3e15b390fa24}")


class ID3D11Fence(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{affde9d1-1df7-4bb7-8a34-0f46251dab80}")


class ID3D11Query1(ID3D11Query):
    _iid_ = comtypes.GUID("{631b4766-36dc-461d-8db6-c47e13e60916}")


class ID3D11RasterizerState2(ID3D11RasterizerState1):
    _iid_ = comtypes.GUID("{6fbd02fb-209f-46c4-b059-2ed15586a6ac}")


class ID3D11RenderTargetView1(ID3D11RenderTargetView):
    _iid_ = comtypes.GUID("{ffbe2e23-f011-418a-ac56-5ceed7c5b94b}")


class ID3D11ShaderResourceView1(ID3D11ShaderResourceView):
    _iid_ = comtypes.GUID("{91308b87-9040-411d-8c67-c39253ce3802}")


class ID3D11Texture2D1(ID3D11Texture2D):
    _iid_ = comtypes.GUID("{51218251-1E33-4617-9CCB-4D3A4367E7BB}")


class ID3D11Texture3D1(ID3D11Texture3D):
    _iid_ = comtypes.GUID("{0C711683-2853-4846-9BB0-F3E60639E46A}")


class ID3D11UnorderedAccessView1(ID3D11UnorderedAccessView):
    _iid_ = comtypes.GUID("{7b3b6153-a886-4544-ab37-6537c8500403}")


## ---------------------------------------------- structures ----


class D3D11_QUERY_DESC1(ctypes.Structure):
    _fields_ = [('Query',       D3D11_QUERY),
                ('MiscFlags',   ctypes.c_uint32),
                ('ContextType', D3D11_CONTEXT_TYPE),
    ]


class D3D11_RASTERIZER_DESC2(ctypes.Structure):
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
                ('ConservativeRaster',    D3D11_CONSERVATIVE_RASTERIZATION_MODE),
    ]


class D3D11_TEX2D_ARRAY_RTV1(ctypes.Structure):
    _fields_ = [('MipSlice',        ctypes.c_uint32),
                ('FirstArraySlice', ctypes.c_uint32),
                ('ArraySize',       ctypes.c_uint32),
                ('PlaneSlice',      ctypes.c_uint32),
    ]


class D3D11_TEX2D_ARRAY_SRV1(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint32),
                ('MipLevels',       ctypes.c_uint32),
                ('FirstArraySlice', ctypes.c_uint32),
                ('ArraySize',       ctypes.c_uint32),
                ('PlaneSlice',      ctypes.c_uint32),
    ]


class D3D11_TEX2D_ARRAY_UAV1(ctypes.Structure):
    _fields_ = [('MipSlice',        ctypes.c_uint32),
                ('FirstArraySlice', ctypes.c_uint32),
                ('ArraySize',       ctypes.c_uint32),
                ('PlaneSlice',      ctypes.c_uint32),
    ]


class D3D11_TEX2D_RTV1(ctypes.Structure):
    _fields_ = [('MipSlice',   ctypes.c_uint32),
                ('PlaneSlice', ctypes.c_uint32),
    ]


class D3D11_TEX2D_SRV1(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint32),
                ('MipLevels',       ctypes.c_uint32),
                ('PlaneSlice',      ctypes.c_uint32),
    ]


class D3D11_TEX2D_UAV1(ctypes.Structure):
    _fields_ = [('MipSlice',   ctypes.c_uint32),
                ('PlaneSlice', ctypes.c_uint32),
    ]


class D3D11_TEXTURE2D_DESC1(ctypes.Structure):
    _fields_ = [('Width',          ctypes.c_uint32),
                ('Height',         ctypes.c_uint32),
                ('MipLevels',      ctypes.c_uint32),
                ('ArraySize',      ctypes.c_uint32),
                ('Format',         DXGI_FORMAT),
                ('SampleDesc',     DXGI_SAMPLE_DESC),
                ('Usage',          D3D11_USAGE),
                ('BindFlags',      ctypes.c_uint32),
                ('CPUAccessFlags', ctypes.c_uint32),
                ('MiscFlags',      ctypes.c_uint32),
                ('TextureLayout',  D3D11_TEXTURE_LAYOUT),
    ]


class D3D11_TEXTURE3D_DESC1(ctypes.Structure):
    _fields_ = [('Width',          ctypes.c_uint32),
                ('Height',         ctypes.c_uint32),
                ('Depth',          ctypes.c_uint32),
                ('MipLevels',      ctypes.c_uint32),
                ('Format',         DXGI_FORMAT),
                ('Usage',          D3D11_USAGE),
                ('BindFlags',      ctypes.c_uint32),
                ('CPUAccessFlags', ctypes.c_uint32),
                ('MiscFlags',      ctypes.c_uint32),
                ('TextureLayout',  D3D11_TEXTURE_LAYOUT),
    ]


class D3D11_UNORDERED_ACCESS_VIEW_DESC1(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [('Buffer',         D3D11_BUFFER_UAV),
                    ('Texture1D',      D3D11_TEX1D_UAV),
                    ('Texture1DArray', D3D11_TEX1D_ARRAY_UAV),
                    ('Texture2D',      D3D11_TEX2D_UAV1),
                    ('Texture2DArray', D3D11_TEX2D_ARRAY_UAV1),
                    ('Texture3D',      D3D11_TEX3D_UAV),
        ]
    _anonymous_ = ('u',)
    _fields_ = [('Format',        DXGI_FORMAT),
                ('ViewDimension', D3D11_UAV_DIMENSION),
                ('u',             _U),
    ]


class D3D11_RENDER_TARGET_VIEW_DESC1(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [('Buffer',           D3D11_BUFFER_RTV),
                    ('Texture1D',        D3D11_TEX1D_RTV),
                    ('Texture1DArray',   D3D11_TEX1D_ARRAY_RTV),
                    ('Texture2D',        D3D11_TEX2D_RTV1),
                    ('Texture2DArray',   D3D11_TEX2D_ARRAY_RTV1),
                    ('Texture2DMS',      D3D11_TEX2DMS_RTV),
                    ('Texture2DMSArray', D3D11_TEX2DMS_ARRAY_RTV),
                    ('Texture3D',        D3D11_TEX3D_RTV),
        ]
    _anonymous_ = ('u',)
    _fields_ = [('Format',        DXGI_FORMAT),
                ('ViewDimension', D3D11_RTV_DIMENSION),
                ('u',             _U),
    ]


class D3D11_SHADER_RESOURCE_VIEW_DESC1(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [('Buffer',           D3D11_BUFFER_SRV),
                    ('Texture1D',        D3D11_TEX1D_SRV),
                    ('Texture1DArray',   D3D11_TEX1D_ARRAY_SRV),
                    ('Texture2D',        D3D11_TEX2D_SRV1),
                    ('Texture2DArray',   D3D11_TEX2D_ARRAY_SRV1),
                    ('Texture2DMS',      D3D11_TEX2DMS_SRV),
                    ('Texture2DMSArray', D3D11_TEX2DMS_ARRAY_SRV),
                    ('Texture3D',        D3D11_TEX3D_SRV),
                    ('TextureCube',      D3D11_TEXCUBE_SRV),
                    ('TextureCubeArray', D3D11_TEXCUBE_ARRAY_SRV),
                    ('BufferEx',         D3D11_BUFFEREX_SRV),
        ]
    _anonymous_ = ('u',)
    _fields_ = [('Format',        DXGI_FORMAT),
                ('ViewDimension', D3D11_SRV_DIMENSION),
                ('u',             _U),
    ]


## ------------------------- vtables, assigned once every class exists ----

ID3D11Device3._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateTexture2D1", [
        ctypes.POINTER(D3D11_TEXTURE2D_DESC1),       # D3D11_TEXTURE2D_DESC1* pDesc1
        ctypes.POINTER(D3D11_SUBRESOURCE_DATA),      # D3D11_SUBRESOURCE_DATA* pInitialData
        ctypes.POINTER(ctypes.POINTER(ID3D11Texture2D1)), # ID3D11Texture2D1** ppTexture2D
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateTexture3D1", [
        ctypes.POINTER(D3D11_TEXTURE3D_DESC1),       # D3D11_TEXTURE3D_DESC1* pDesc1
        ctypes.POINTER(D3D11_SUBRESOURCE_DATA),      # D3D11_SUBRESOURCE_DATA* pInitialData
        ctypes.POINTER(ctypes.POINTER(ID3D11Texture3D1)), # ID3D11Texture3D1** ppTexture3D
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateRasterizerState2", [
        ctypes.POINTER(D3D11_RASTERIZER_DESC2),      # D3D11_RASTERIZER_DESC2* pRasterizerDesc
        ctypes.POINTER(ctypes.POINTER(ID3D11RasterizerState2)), # ID3D11RasterizerState2** ppRasterizerState
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateShaderResourceView1", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pResource
        ctypes.POINTER(D3D11_SHADER_RESOURCE_VIEW_DESC1), # D3D11_SHADER_RESOURCE_VIEW_DESC1* pDesc1
        ctypes.POINTER(ctypes.POINTER(ID3D11ShaderResourceView1)), # ID3D11ShaderResourceView1** ppSRView1
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateUnorderedAccessView1", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pResource
        ctypes.POINTER(D3D11_UNORDERED_ACCESS_VIEW_DESC1), # D3D11_UNORDERED_ACCESS_VIEW_DESC1* pDesc1
        ctypes.POINTER(ctypes.POINTER(ID3D11UnorderedAccessView1)), # ID3D11UnorderedAccessView1** ppUAView1
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateRenderTargetView1", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pResource
        ctypes.POINTER(D3D11_RENDER_TARGET_VIEW_DESC1), # D3D11_RENDER_TARGET_VIEW_DESC1* pDesc1
        ctypes.POINTER(ctypes.POINTER(ID3D11RenderTargetView1)), # ID3D11RenderTargetView1** ppRTView1
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateQuery1", [
        ctypes.POINTER(D3D11_QUERY_DESC1),           # D3D11_QUERY_DESC1* pQueryDesc1
        ctypes.POINTER(ctypes.POINTER(ID3D11Query1)), # ID3D11Query1** ppQuery1
        ]),
    comtypes.STDMETHOD(None, "GetImmediateContext3", [
        ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext3)), # ID3D11DeviceContext3** ppImmediateContext
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateDeferredContext3", [
        ctypes.c_uint32,                             # UINT ContextFlags
        ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext3)), # ID3D11DeviceContext3** ppDeferredContext
        ]),
    comtypes.STDMETHOD(None, "WriteToSubresource", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pDstResource
        ctypes.c_uint32,                             # UINT DstSubresource
        ctypes.POINTER(D3D11_BOX),                   # D3D11_BOX* pDstBox
        ctypes.c_void_p,                             # void* pSrcData
        ctypes.c_uint32,                             # UINT SrcRowPitch
        ctypes.c_uint32,                             # UINT SrcDepthPitch
        ]),
    comtypes.STDMETHOD(None, "ReadFromSubresource", [
        ctypes.c_void_p,                             # void* pDstData
        ctypes.c_uint32,                             # UINT DstRowPitch
        ctypes.c_uint32,                             # UINT DstDepthPitch
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pSrcResource
        ctypes.c_uint32,                             # UINT SrcSubresource
        ctypes.POINTER(D3D11_BOX),                   # D3D11_BOX* pSrcBox
        ]),
]

ID3D11DeviceContext3._methods_ = [
    comtypes.STDMETHOD(None, "Flush1", [
        D3D11_CONTEXT_TYPE,                          # D3D11_CONTEXT_TYPE ContextType
        ctypes.c_void_p,                             # HANDLE hEvent
        ]),
    comtypes.STDMETHOD(None, "SetHardwareProtectionState", [
        wintypes.BOOL,                               # BOOL HwProtectionEnable
        ]),
    comtypes.STDMETHOD(None, "GetHardwareProtectionState", [
        ctypes.POINTER(wintypes.BOOL),               # BOOL* pHwProtectionEnable
        ]),
]

ID3D11DeviceContext4._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "Signal", [
        ctypes.POINTER(ID3D11Fence),                 # ID3D11Fence* pFence
        ctypes.c_uint64,                             # UINT64 Value
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "Wait", [
        ctypes.POINTER(ID3D11Fence),                 # ID3D11Fence* pFence
        ctypes.c_uint64,                             # UINT64 Value
        ]),
]

ID3D11Fence._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateSharedHandle", [
        ctypes.POINTER(SECURITY_ATTRIBUTES),         # SECURITY_ATTRIBUTES* pAttributes
        ctypes.c_uint32,                             # DWORD dwAccess
        ctypes.c_wchar_p,                            # LPCWSTR lpName
        ctypes.POINTER(ctypes.c_void_p),             # HANDLE* pHandle
        ]),
    comtypes.STDMETHOD(ctypes.c_uint64, "GetCompletedValue", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetEventOnCompletion", [
        ctypes.c_uint64,                             # UINT64 Value
        ctypes.c_void_p,                             # HANDLE hEvent
        ]),
]

ID3D11Query1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_QUERY_DESC1),           # D3D11_QUERY_DESC1* pDesc1
        ]),
]

ID3D11RasterizerState2._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc2", [
        ctypes.POINTER(D3D11_RASTERIZER_DESC2),      # D3D11_RASTERIZER_DESC2* pDesc
        ]),
]

ID3D11RenderTargetView1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_RENDER_TARGET_VIEW_DESC1), # D3D11_RENDER_TARGET_VIEW_DESC1* pDesc1
        ]),
]

ID3D11ShaderResourceView1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_SHADER_RESOURCE_VIEW_DESC1), # D3D11_SHADER_RESOURCE_VIEW_DESC1* pDesc1
        ]),
]

ID3D11Texture2D1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_TEXTURE2D_DESC1),       # D3D11_TEXTURE2D_DESC1* pDesc
        ]),
]

ID3D11Texture3D1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_TEXTURE3D_DESC1),       # D3D11_TEXTURE3D_DESC1* pDesc
        ]),
]

ID3D11UnorderedAccessView1._methods_ = [
    comtypes.STDMETHOD(None, "GetDesc1", [
        ctypes.POINTER(D3D11_UNORDERED_ACCESS_VIEW_DESC1), # D3D11_UNORDERED_ACCESS_VIEW_DESC1* pDesc1
        ]),
]


## -- End Of File --
