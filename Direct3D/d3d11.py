## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  D3D11 IDL
## 
##  Contains interface definitions for the D3D11 API.
## 
##  Copyright (C) Microsoft Corporation
##  
##  SDK version : 10.0.19041.0
##
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import ctypes
import ctypes.wintypes as wintypes

import comtypes

from PyIdl.dxgicommon import *
from PyIdl.dxgiformat import *
from PyIdl.d3dcommon import *


D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT = 8



D3D11_INPUT_CLASSIFICATION = ctypes.c_uint
D3D11_INPUT_PER_VERTEX_DATA   = D3D11_INPUT_CLASSIFICATION(0)
D3D11_INPUT_PER_INSTANCE_DATA = D3D11_INPUT_CLASSIFICATION(1)

D3D11_APPEND_ALIGNED_ELEMENT = 0xFFFFFFFF

class D3D11_INPUT_ELEMENT_DESC(ctypes.Structure):
    _fields_ = [('SemanticName', wintypes.LPCSTR),
                ('SemanticIndex', ctypes.c_uint),
                ('Format', DXGI_FORMAT),
                ('InputSlot', ctypes.c_uint),
                ('AlignedByteOffset', ctypes.c_uint),
                ('InputSlotClass', D3D11_INPUT_CLASSIFICATION),
                ('InstanceDataSetRate', ctypes.c_uint),
    ]

## Keep FILL_MODE values in sync with earlier DX versions (HW consumes values directly).
D3D11_FILL_MODE = ctypes.c_uint
## 1 was POINT in D3D, unused in D3D11
D3D11_FILL_WIREFRAME = D3D11_FILL_MODE(2)
D3D11_FILL_SOLID = D3D11_FILL_MODE(3)

D3D11_PRIMITIVE_TOPOLOGY = D3D_PRIMITIVE_TOPOLOGY
D3D11_PRIMITIVE = D3D_PRIMITIVE

# Keep CULL_MODE values in sync with earlier DX versions (HW consumes values directly).
D3D11_CULL_MODE = ctypes.c_uint
D3D11_CULL_NONE = D3D11_CULL_MODE(1)
D3D11_CULL_FRONT = D3D11_CULL_MODE(2)
D3D11_CULL_BACK = D3D11_CULL_MODE(3)

class D3D11_SO_DECLARATION_ENTRY(ctypes.Structure):
    _fields_ = [('Stream', ctypes.c_uint),
                ('SemanticName', wintypes.LPCSTR),
                ('SemanticIndex', ctypes.c_uint),
                ('StartComponent', wintypes.BYTE),
                ('ComponentCount', wintypes.BYTE),
                ('OutputSlot', wintypes.BYTE),
    ]

class D3D11_VIEWPORT(ctypes.Structure):
    _fields_ = [('TopLeftX', ctypes.c_float),
                ('TopLeftY', ctypes.c_float),
                ('Width', ctypes.c_float),
                ('Height', ctypes.c_float),
                ('MinDepth', ctypes.c_float),
                ('MaxDepth', ctypes.c_float),
    ]

class D3D11_DRAW_INSTANCED_INDIRECT_ARGS(ctypes.Structure):
    _fields_ = [('VertexCountPerInstance', ctypes.c_uint),
                ('InstanceCount', ctypes.c_uint),
                ('StartVertexLocation', ctypes.c_uint),
                ('StartInstanceLocation', ctypes.c_uint),
    ]

class D3D11_DRAW_INDEXED_INSTANCED_INDIRECT_ARGS(ctypes.Structure):
    _fields_ = [('IndexCountPerInstance', ctypes.c_uint),
                ('InstanceCount', ctypes.c_uint),
                ('StartIndexLocation', ctypes.c_uint),
                ('BaseVertexLocation', ctypes.c_int),
                ('StartInstanceLocation', ctypes.c_uint),
    ]

D3D11_RESOURCE_DIMENSION = ctypes.c_uint
D3D11_RESOURCE_DIMENSION_UNKNOWN = D3D11_RESOURCE_DIMENSION(0)
D3D11_RESOURCE_DIMENSION_BUFFER = D3D11_RESOURCE_DIMENSION(1)
D3D11_RESOURCE_DIMENSION_TEXTURE1D = D3D11_RESOURCE_DIMENSION(2)
D3D11_RESOURCE_DIMENSION_TEXTURE2D = D3D11_RESOURCE_DIMENSION(3)
D3D11_RESOURCE_DIMENSION_TEXTURE3D = D3D11_RESOURCE_DIMENSION(4)

D3D11_SRV_DIMENSION = D3D_SRV_DIMENSION

D3D11_DSV_DIMENSION = ctypes.c_uint
D3D11_DSV_DIMENSION_UNKNOWN = D3D11_DSV_DIMENSION(0)
D3D11_DSV_DIMENSION_TEXTURE1D = D3D11_DSV_DIMENSION(1)
D3D11_DSV_DIMENSION_TEXTURE1DARRAY = D3D11_DSV_DIMENSION(2)
D3D11_DSV_DIMENSION_TEXTURE2D = D3D11_DSV_DIMENSION(3)
D3D11_DSV_DIMENSION_TEXTURE2DARRAY = D3D11_DSV_DIMENSION(4)
D3D11_DSV_DIMENSION_TEXTURE2DMS = D3D11_DSV_DIMENSION(5)
D3D11_DSV_DIMENSION_TEXTURE2DMSARRAY = D3D11_DSV_DIMENSION(6)

D3D11_RTV_DIMENSION = ctypes.c_uint
D3D11_RTV_DIMENSION_UNKNOWN = D3D11_RTV_DIMENSION(0)
D3D11_RTV_DIMENSION_BUFFER = D3D11_DSV_DIMENSION(1)
D3D11_RTV_DIMENSION_TEXTURE1D = D3D11_DSV_DIMENSION(2)
D3D11_RTV_DIMENSION_TEXTURE1DARRAY = D3D11_DSV_DIMENSION(3)
D3D11_RTV_DIMENSION_TEXTURE2D = D3D11_DSV_DIMENSION(4)
D3D11_RTV_DIMENSION_TEXTURE2DARRAY = D3D11_DSV_DIMENSION(5)
D3D11_RTV_DIMENSION_TEXTURE2DMS = D3D11_DSV_DIMENSION(6)
D3D11_RTV_DIMENSION_TEXTURE2DMSARRAY = D3D11_DSV_DIMENSION(7)
D3D11_RTV_DIMENSION_TEXTURE3D = D3D11_DSV_DIMENSION(8)

D3D11_UAV_DIMENSION = ctypes.c_uint
D3D11_UAV_DIMENSION_UNKNOWN = D3D11_UAV_DIMENSION(0)
D3D11_UAV_DIMENSION_BUFFER = D3D11_UAV_DIMENSION(1)
D3D11_UAV_DIMENSION_TEXTURE1D = D3D11_UAV_DIMENSION(2)
D3D11_UAV_DIMENSION_TEXTURE1DARRAY = D3D11_UAV_DIMENSION(3)
D3D11_UAV_DIMENSION_TEXTURE2D = D3D11_UAV_DIMENSION(4)
D3D11_UAV_DIMENSION_TEXTURE2DARRAY = D3D11_UAV_DIMENSION(5)
D3D11_UAV_DIMENSION_TEXTURE3D = D3D11_UAV_DIMENSION(8)

D3D11_USAGE = ctypes.c_uint
D3D11_USAGE_DEFAULT = D3D11_USAGE(0)
D3D11_USAGE_IMMUTABLE = D3D11_USAGE(1)
D3D11_USAGE_DYNAMIC = D3D11_USAGE(2)
D3D11_USAGE_STAGING = D3D11_USAGE(3)

D3D11_BING_FLAG = ctypes.c_uint
D3D11_BIND_VERTEX_BUFFER = D3D11_BING_FLAG(0x00000001)
D3D11_BIND_INDEX_BUFFER = D3D11_BING_FLAG(0x00000002)
D3D11_BIND_CONSTANT_BUFFER = D3D11_BING_FLAG(0x00000004)
D3D11_BIND_SHADER_RESOURCE = D3D11_BING_FLAG(0x00000008)
D3D11_BIND_STREAM_OUTPUT = D3D11_BING_FLAG(0x00000010)
D3D11_BIND_RENDER_TARGET = D3D11_BING_FLAG(0x00000020)
D3D11_BIND_DEPTH_STENCIL = D3D11_BING_FLAG(0x00000040)
D3D11_BIND_UNORDERED_ACCESS = D3D11_BING_FLAG(0x00000080)
D3D11_BIND_DECODER = D3D11_BING_FLAG(0x00000200)
D3D11_BIND_VIDEO_ENCODER = D3D11_BING_FLAG(0x00000400)


D3D11_CPU_ACCESS_FLAG = ctypes.c_uint
D3D11_CPU_ACCESS_WRITE = D3D11_CPU_ACCESS_FLAG(0x00010000)
D3D11_CPU_ACCESS_READ = D3D11_CPU_ACCESS_FLAG(0x00020000)

D3D11_RESOURCE_MISC_FLAG = ctypes.c_uint
D3D11_RESOURCE_MISC_GENERATE_MIPS                   = D3D11_RESOURCE_MISC_FLAG(0x00000001)
D3D11_RESOURCE_MISC_SHARED                          = D3D11_RESOURCE_MISC_FLAG(0x00000002)
D3D11_RESOURCE_MISC_TEXTURECUBE                     = D3D11_RESOURCE_MISC_FLAG(0x00000004)
D3D11_RESOURCE_MISC_DRAWINDIRECT_ARGS               = D3D11_RESOURCE_MISC_FLAG(0x00000010)
D3D11_RESOURCE_MISC_BUFFER_ALLOW_RAW_VIEWS          = D3D11_RESOURCE_MISC_FLAG(0x00000020)
D3D11_RESOURCE_MISC_BUFFER_STRUCTURED               = D3D11_RESOURCE_MISC_FLAG(0x00000040)
D3D11_RESOURCE_MISC_RESOURCE_CLAMP                  = D3D11_RESOURCE_MISC_FLAG(0x00000080)
D3D11_RESOURCE_MISC_SHARED_KEYEDMUTEX               = D3D11_RESOURCE_MISC_FLAG(0x00000100)
D3D11_RESOURCE_MISC_GDI_COMPATIBLE                  = D3D11_RESOURCE_MISC_FLAG(0x00000200)
D3D11_RESOURCE_MISC_SHARED_NTHANDLE                 = D3D11_RESOURCE_MISC_FLAG(0x00000800)
D3D11_RESOURCE_MISC_RESTRICTED_CONTENT              = D3D11_RESOURCE_MISC_FLAG(0x00001000)
D3D11_RESOURCE_MISC_RESTRICT_SHARED_RESOURCE        = D3D11_RESOURCE_MISC_FLAG(0x00002000)
D3D11_RESOURCE_MISC_RESTRICT_SHARED_RESOURCE_DRIVER = D3D11_RESOURCE_MISC_FLAG(0x00004000)
D3D11_RESOURCE_MISC_GUARDED                         = D3D11_RESOURCE_MISC_FLAG(0x00008000)
D3D11_RESOURCE_MISC_TILE_POOL                       = D3D11_RESOURCE_MISC_FLAG(0x00020000)
D3D11_RESOURCE_MISC_TILED                           = D3D11_RESOURCE_MISC_FLAG(0x00040000)
D3D11_RESOURCE_MISC_HW_PROTECTED                    = D3D11_RESOURCE_MISC_FLAG(0x00080000)

## for calling ID3D11Resource::Map()
D3D11_MAP = ctypes.c_uint
D3D11_MAP_READ               = D3D11_MAP(1)
D3D11_MAP_WRITE              = D3D11_MAP(2)
D3D11_MAP_READ_WRITE         = D3D11_MAP(3)
D3D11_MAP_WRITE_DISCARD      = D3D11_MAP(4)
D3D11_MAP_WRITE_NO_OVERWRITE = D3D11_MAP(5)

D3D11_MAP_FLAG = ctypes.c_uint
D3D11_MAP_FLAG_DO_NOT_WAIT = D3D11_MAP_FLAG(0x00100000)

D3D11_RAISE_FLAG = ctypes.c_uint
D3D11_RAISE_FLAG_DRIVER_INTERNAL_ERROR = D3D11_RAISE_FLAG(0x1)

## Flags for ClearDepthStencil
D3D11_CLEAR_FLAG = ctypes.c_uint
D3D11_CLEAR_DEPTH = D3D11_CLEAR_FLAG(0x01)
D3D11_CLEAR_STENCIL = D3D11_CLEAR_FLAG(0x02)

D3D11_RECT = wintypes.RECT

class D3D11_BOX(ctypes.Structure):
    _flags_ = [('left', ctypes.c_uint),
               ('top', ctypes.c_uint),
               ('front', ctypes.c_uint),
               ('right', ctypes.c_uint),
               ('bottom', ctypes.c_uint),
               ('back', ctypes.c_uint),
    ]

#class interface  ID3D11Device(comtypes.IUnknown):
#class interface  ID3D11ClassLinkage(comtypes.IUnknown):

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  DeviceChild
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11DeviceChild(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{1841e5c8-16b0-489b-bcc8-44cfb0d5deae}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDevice", [
            ctypes.POINTER(ctypes.c_void_p), # ctypes.POINTER(ctypes.POINTER(ID3D11Device)), ## 
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetPrivateData"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateData"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateDataInterface"),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
##
## Depth-Stencil State
##
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## Keep COMPARISON_FUNC values in sync with earlier DX versions (HW consumes values directly).
D3D11_COMPARISON_FUNC = ctypes.c_uint
D3D11_COMPARISON_NEVER = D3D11_COMPARISON_FUNC(1)
D3D11_COMPARISON_LESS = D3D11_COMPARISON_FUNC(2)
D3D11_COMPARISON_EQUAL = D3D11_COMPARISON_FUNC(3)
D3D11_COMPARISON_LESS_EQUAL = D3D11_COMPARISON_FUNC(4)
D3D11_COMPARISON_GREATER = D3D11_COMPARISON_FUNC(5)
D3D11_COMPARISON_NOT_EQUAL = D3D11_COMPARISON_FUNC(6)
D3D11_COMPARISON_GREATER_EQUAL = D3D11_COMPARISON_FUNC(7)
D3D11_COMPARISON_ALWAYS = D3D11_COMPARISON_FUNC(8)

D3D11_DEPTH_WRITE_MASK = ctypes.c_uint
D3D11_DEPTH_WRITE_MASK_ZERO = D3D11_DEPTH_WRITE_MASK(0)
D3D11_DEPTH_WRITE_MASK_ALL = D3D11_DEPTH_WRITE_MASK(1)

## Keep STENCILOP values in sync with earlier DX versions (HW consumes values directly).
D3D11_STENCIL_OP = ctypes.c_uint
D3D11_STENCIL_OP_KEEP = D3D11_STENCIL_OP(1)
D3D11_STENCIL_OP_ZERO = D3D11_STENCIL_OP(2)
D3D11_STENCIL_OP_REPLACE = D3D11_STENCIL_OP(3)
D3D11_STENCIL_OP_INCR_SAT = D3D11_STENCIL_OP(4)
D3D11_STENCIL_OP_DECR_SAT = D3D11_STENCIL_OP(5)
D3D11_STENCIL_OP_INVERT = D3D11_STENCIL_OP(6)
D3D11_STENCIL_OP_INCR = D3D11_STENCIL_OP(7)
D3D11_STENCIL_OP_DECR = D3D11_STENCIL_OP(8)

class D3D11_DEPTH_STENCILOP_DESC(ctypes.Structure):
    _fields_ = [('StencilFailOp', D3D11_STENCIL_OP),
                ('StenilDepthFailOp', D3D11_STENCIL_OP),
                ('StencilPassOp', D3D11_STENCIL_OP),
                ('StencilFunc', D3D11_COMPARISON_FUNC),
    ]

class D3D11_DEPTH_STENCIL_DESC(ctypes.Structure):
    _fields_ = [('DepthEnable', ctypes.c_bool),
                ('DepthWriteMask',D3D11_DEPTH_WRITE_MASK),
                ('DepthFunc',D3D11_COMPARISON_FUNC),
                ('StencilEnable',ctypes.c_bool),
                ('StencilReadMask',ctypes.c_ubyte),
                ('StencilWriteMask',ctypes.c_ubyte),
                ('FrontFace', D3D11_DEPTH_STENCILOP_DESC),
                ('BackFace', D3D11_DEPTH_STENCILOP_DESC),
    ]

class ID3D11DepthStencilState(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{03823efb-8d8f-4e1c-9aa2-f64bb2cbfdf1}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_DEPTH_STENCILOP_DESC),
            ])
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Blend State
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## Keep BLEND values in sync with earlier DX versions (HW consumes values directly).
D3D11_BLEND = ctypes.c_uint
D3D11_BLEND_ZERO = D3D11_BLEND(1)
D3D11_BLEND_ONE = D3D11_BLEND(2)
D3D11_BLEND_SRC_COLOR = D3D11_BLEND(3)       # PS output oN.rgb (N is current RT being blended)
D3D11_BLEND_INV_SRC_COLOR = D3D11_BLEND(4)   # 1.0f - PS output oN.rgb
D3D11_BLEND_SRC_ALPHA = D3D11_BLEND(5)       # PS output oN.a
D3D11_BLEND_INV_SRC_ALPHA = D3D11_BLEND(6)   # 1.0f - PS output oN.a
D3D11_BLEND_DEST_ALPHA = D3D11_BLEND(7)      # RT(N).a (N is current RT being blended)
D3D11_BLEND_INV_DEST_ALPHA = D3D11_BLEND(8)  # 1.0f - RT(N).a
D3D11_BLEND_DEST_COLOR = D3D11_BLEND(9)      # RT(N).rgb
D3D11_BLEND_INV_DEST_COLOR = D3D11_BLEND(10) # 1.0f - RT(N).rgb
D3D11_BLEND_SRC_ALPHA_SAT = D3D11_BLEND(11)  # (f,f,f,1), f = min(1 - RT(N).a, oN.a)
## 12 reserved (was BOTHSRCALPHA)
## 13 reserved (was BOTHSRCALPHA)
D3D11_BLEND_BLEND_FACTOR = D3D11_BLEND(14)
D3D11_BLEND_INV_BLEND_FACTOR = D3D11_BLEND(15)
D3D11_BLEND_SRC1_COLOR = D3D11_BLEND(16)     # PS output o1.rgb
D3D11_BLEND_INV_SRC1_COLOR = D3D11_BLEND(17) # 1.0f - PS output o1.rgb
D3D11_BLEND_SRC1_ALPHA = D3D11_BLEND(18)     # PS output o1.a
D3D11_BLEND_INV_SRC1_ALPHA = D3D11_BLEND(19) # 1.0f - PS output o1.a

## Keep BLENDOP values in sync with earlier DX versions (HW consumes values directly).
D3D11_BLEND_OP = ctypes.c_uint
D3D11_BLEND_OP_ADD = D3D11_BLEND_OP(1)
D3D11_BLEND_OP_SUBTRACT = D3D11_BLEND_OP(2)
D3D11_BLEND_OP_REV_SUBTRACT = D3D11_BLEND_OP(3)
D3D11_BLEND_OP_MIN = D3D11_BLEND_OP(4) # min semantics are like min shader instruction
D3D11_BLEND_OP_MAX = D3D11_BLEND_OP(5) # max semantics are like max shader instruction

D3D11_COLOR_WRITE_ENABLE = ctypes.c_uint
D3D11_COLOR_WRITE_ENABLE_RED = D3D11_COLOR_WRITE_ENABLE(1)
D3D11_COLOR_WRITE_ENABLE_GREEN = D3D11_COLOR_WRITE_ENABLE(2)
D3D11_COLOR_WRITE_ENABLE_BLUE = D3D11_COLOR_WRITE_ENABLE(4)
D3D11_COLOR_WRITE_ENABLE_ALPHA = D3D11_COLOR_WRITE_ENABLE(8)
D3D11_COLOR_WRITE_ENABLE_ALL = D3D11_COLOR_WRITE_ENABLE(1|2| 4|8) # cover all type

class D3D11_RENDER_TARGET_BLEND_DESC(ctypes.Structure):
    _fields_ = [('BlendEnable', ctypes.c_bool),
                ('SrcBlend', D3D11_BLEND),
                ('DestBlend', D3D11_BLEND),
                ('BlendOp', D3D11_BLEND_OP),
                ('SrcBlendAlpha', D3D11_BLEND),
                ('DestBlendAlpha', D3D11_BLEND),
                ('BlendOpAlpha', D3D11_BLEND_OP),
                ('RenderTargetWriteMask', ctypes.c_ubyte), # D3D11_COLOR_WRITE_ENABLE
    ]

class D3D11_BLEND_DESC(ctypes.Structure):
    _fields_ = [('AlphaToCoverageEnable', ctypes.c_bool), # relevant to multisample antialiasing only
                ('IndependentBlendEnable', ctypes.c_bool), # if FALSE, then replicate the first entry in RenderTarget array to other entries
                ('RenderTarget', D3D11_RENDER_TARGET_BLEND_DESC * D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT)
    ]

class ID3D11BlendState(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{75b68faa-347d-4159-8f45-a0640f01cd9a}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_BLEND_DESC)
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Rasterizer State
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_RASTERIZER_DESC(ctypes.Structure):
    _fields_ = [('FillMode', D3D11_FILL_MODE),
                ('CullMode', D3D11_CULL_MODE),
                ('FrontCounterClockwise', ctypes.c_bool),
                ('DepthBias', ctypes.c_int),
                ('DepthBiasClamp', ctypes.c_float),
                ('SlopeScaledDepthBias', ctypes.c_float),
                ('DepthClipEnable', ctypes.c_bool),
                ('ScissorEnable', ctypes.c_bool),
                ('MultisampleEnable', ctypes.c_bool),
                ('AntialiasedLineEnable', ctypes.c_bool),
    ]

class ID3D11RasterizerState(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{9bb4ab81-ab1a-4d8f-b506-fc04200b6ee7}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_RASTERIZER_DESC)
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Resource
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_SUBRESOURCE_DATA(ctypes.Structure):
    _fields_ = [('pSysMem', ctypes.c_void_p),
                ('SysMemPitch',ctypes.c_uint),
                ('SysMemSlicePitch',ctypes.c_uint),
    ]

class D3D11_MAPPED_SUBRESOURCE(ctypes.Structure):
    _fields_ = [('pData', ctypes.c_void_p),
                ('RowPitch', ctypes.c_uint),
                ('DepthPitch',ctypes.c_uint),
    ]

class ID3D11Resource(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{dc8e63f3-d12b-4952-b47b-5e45026a862d}")
    _methods_ = [
        comtypes.STDMETHOD(None ,"GetType", [
            ctypes.POINTER(D3D11_RESOURCE_DIMENSION),
            ]),
        comtypes.STDMETHOD(None ,"SetEvictionPriority", [
            ctypes.c_uint
            ]),
        comtypes.STDMETHOD(ctypes.c_uint,"GetEvictionPriority"),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Buffer
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_BUFFER_DESC(ctypes.Structure):
    _fields_ = [('ByteWidth', ctypes.c_uint),
                ('Usage', D3D11_USAGE),
                ('BindFlags', ctypes.c_uint),
                ('CPUAccessFlags', ctypes.c_uint),
                ('MiscFlags', ctypes.c_uint),
                ('StructureByteStride', ctypes.c_uint), # Stride of Structured Buffer; ignored if STRUCTURED MiscFlag not set
    ]
class ID3D11Buffer(ID3D11Resource):
    _iid_ = comtypes.GUID("{48570b85-d1ee-4fcd-a250-eb350722b037}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc",[
            ctypes.POINTER(D3D11_BUFFER_DESC),
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Texture1D
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_TEXTURE1D_DESC(ctypes.Structure):
    _fields_ = [('Width', ctypes.c_uint),
                ('MipLevels',ctypes.c_uint),
                ('ArraySize',ctypes.c_uint),
                ('Format', DXGI_FORMAT),
                ('Usage',D3D11_USAGE),
                ('BindFlags',ctypes.c_uint),
                ('CPUAccessFlags',ctypes.c_uint),
                ('MiscFlags',ctypes.c_uint),
    ]

class ID3D11Texture1D(ID3D11Resource):
    _iid_ = comtypes.GUID("{f8fb5c27-c6b3-4f75-a4c8-439af2ef564c}")
    _methods_ = [
        comtypes.STDMETHOD(None,"GetDesc", [
            ctypes.POINTER(D3D11_TEXTURE1D_DESC),
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Texture2D
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_TEXTURE2D_DESC(ctypes.Structure):
    _fields_ = [('Width', ctypes.c_uint),
                ('Height', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
                ('Format', DXGI_FORMAT),
                ('SampleDesc', DXGI_SAMPLE_DESC),
                ('Usage', D3D11_USAGE),
                ('BindFlags', ctypes.c_uint),
                ('CPUAccessFlags', ctypes.c_uint),
                ('MiscFlags', ctypes.c_uint),
    ]

class ID3D11Texture2D(ID3D11Resource):
    _iid_ = comtypes.GUID("{6f15aaf2-d208-4e89-9ab4-489535d34f9c}")
    _methods_ = [
        comtypes.STDMETHOD(None,"GetDesc", [
            ctypes.POINTER(D3D11_TEXTURE2D_DESC),
            ]),
    ]
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Texture3D
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_TEXTURE3D_DESC(ctypes.Structure):
    _fields_ = [('Width', ctypes.c_uint),
                ('Height', ctypes.c_uint),
                ('Depth', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
                ('Format', DXGI_FORMAT),
                ('Usage', D3D11_USAGE),
                ('BindFlags', ctypes.c_uint),
                ('CPUAccessFlags', ctypes.c_uint),
                ('MiscFlags', ctypes.c_uint),
    ]

class ID3D11Texture3D(ID3D11Resource):
    _iid_ = comtypes.GUID("{037e866e-f56d-4357-a8af-9dabbe6e250e}")
    _methods_ = [
        comtypes.STDMETHOD(None,"GetDesc", [
            ctypes.POINTER(D3D11_TEXTURE3D_DESC),
            ]),
    ]

D3D11_TEXTURECUBE_FACE = ctypes.c_uint
D3D11_TEXTURECUBE_FACE_POSITIVE_X = D3D11_TEXTURECUBE_FACE(0)
D3D11_TEXTURECUBE_FACE_NEGATIVE_X = D3D11_TEXTURECUBE_FACE(1)
D3D11_TEXTURECUBE_FACE_POSITIVE_Y = D3D11_TEXTURECUBE_FACE(2)
D3D11_TEXTURECUBE_FACE_NEGATIVE_Y = D3D11_TEXTURECUBE_FACE(3)
D3D11_TEXTURECUBE_FACE_POSITIVE_Z = D3D11_TEXTURECUBE_FACE(4)
D3D11_TEXTURECUBE_FACE_NEGATIVE_Z = D3D11_TEXTURECUBE_FACE(5)


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  View
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11View(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{839d1216-bb2e-412b-b7f4-a9dbebe08ed1}")
    _methods_ = [
        comtypes.STDMETHOD(None,"GetResource", [
            ctypes.POINTER(ctypes.POINTER(ID3D11Resource)),
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  ShaderResourceView
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_BUFFER_SRV(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('FirstElement', ctypes.c_uint),
                    ('ElementOffset', ctypes.c_uint),
                    ]
    class _I2(ctypes.Union):
        _fields_ = [('NumElements', ctypes.c_uint),
                    ('ElementWidth', ctypes.c_uint),
                    ]
    _anonymous_ = ('i1', 'i2',)
    _fields_ = [('i1', _I1),
                ('i2', _I2),
                ]

D3D11_BUFFEREX_SRV_FLAG = ctypes.c_uint
D3D11_BUFFEREX_SRV_FLAG_RAW = D3D11_BUFFEREX_SRV_FLAG(0x00000001) # allow device multi-component reads with DWORD addressing

class D3D11_BUFFEREX_SRV(ctypes.Structure):
    _fields_ = [('FirstElement',ctypes.c_uint),
                ('NumElements',ctypes.c_uint),
                ('Flags', ctypes.c_uint),
    ]

class D3D11_TEX1D_SRV(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
    ]

class D3D11_TEX1D_ARRAY_SRV(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX2D_SRV(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
    ]

class D3D11_TEX2D_ARRAY_SRV(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX3D_SRV(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
    ]

class D3D11_TEXCUBE_SRV(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
    ]

class D3D11_TEXCUBE_ARRAY_SRV(ctypes.Structure):
    _fields_ = [('MostDetailedMip', ctypes.c_uint),
                ('MipLevels', ctypes.c_uint),
                ('First2DArrayFace', ctypes.c_uint),
                ('NumCubes', ctypes.c_uint),
    ]

class D3D11_TEX2DMS_SRV(ctypes.Structure):
    _fields_ = [('UnusedField_NothingToDefine', ctypes.c_uint),
    ]

class D3D11_TEX2DMS_ARRAY_SRV(ctypes.Structure):
    _fields_ = [('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_SHADER_RESOURCE_VIEW_DESC(ctypes.Structure):
    class _I1(ctypes.Union):
            _fields_ = [('Buffer', D3D11_BUFFER_SRV),
                        ('Texture1D', D3D11_TEX1D_SRV),
                        ('Texture1DArray', D3D11_TEX1D_ARRAY_SRV),
                        ('Texture2D', D3D11_TEX2D_SRV),
                        ('Texture2DArray', D3D11_TEX2D_ARRAY_SRV),
                        ('Texture2DMS', D3D11_TEX2DMS_SRV),
                        ('Texture2DMSArray', D3D11_TEX2DMS_ARRAY_SRV),
                        ('Texture3D', D3D11_TEX3D_SRV),
                        ('TextureCube', D3D11_TEXCUBE_SRV),
                        ('TextureCubeArray', D3D11_TEXCUBE_ARRAY_SRV),
                        ('BufferEx', D3D11_BUFFEREX_SRV),
            ]
    _anonymous_ = ('i1',)
    _fields_ = [('Format', DXGI_FORMAT),
                ('ViewDimension', D3D11_SRV_DIMENSION),
                ('i1', _I1),
    ]

class ID3D11ShaderResourceView(ID3D11View):
    _iid_ = comtypes.GUID("{b0e06fe0-8192-4e1a-b1ca-36d7414710b2}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_SHADER_RESOURCE_VIEW_DESC),
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  RenderTargetView
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_BUFFER_RTV(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('FirstElement', ctypes.c_uint),
                    ('ElementOffset', ctypes.c_uint),
        ]
    class _I2(ctypes.Union):
        _fields_ = [('NumElements', ctypes.c_uint),
                    ('ElementWidth', ctypes.c_uint),
        ]
    _anonymous_ = ('i1', 'i2',)
    _fields_ = [('i1', _I1),
                ('i2', _I2),
    ]

class D3D11_TEX1D_RTV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
    ]

class D3D11_TEX1D_ARRAY_RTV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX2D_RTV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
    ]

class D3D11_TEX2DMS_RTV(ctypes.Structure):
    _fields_ = [('UnusedField_NothingToDefine', ctypes.c_uint),
    ]

class D3D11_TEX2D_ARRAY_RTV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX2DMS_ARRAY_RTV(ctypes.Structure):
    _fields_ = [('FirstArraySlice', ctypes.c_uint),
                ('ArraySize',ctypes.c_uint),
    ]

class D3D11_TEX3D_RTV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstWSlice', ctypes.c_uint),
                ('WSize', ctypes.c_uint),
    ]

class D3D11_RENDER_TARGET_VIEW_DESC(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('Buffer', D3D11_BUFFER_RTV),
                    ('Texture1D', D3D11_TEX1D_RTV),
                    ('Texture1DArray', D3D11_TEX1D_ARRAY_RTV),
                    ('Texture2D', D3D11_TEX2D_RTV),
                    ('Texture2DArray', D3D11_TEX2D_ARRAY_RTV),
                    ('Texture2DMS', D3D11_TEX2DMS_RTV),
                    ('Texture2DMSArray', D3D11_TEX2DMS_ARRAY_RTV),
                    ('Texture3D', D3D11_TEX3D_RTV),
        ]
    _anonymous_ = ('i1',)
    _fields_ = [('Format', DXGI_FORMAT),
                ('ViewDimension', D3D11_RTV_DIMENSION),
                ('i1',_I1),
    ]

class ID3D11RenderTargetView(ID3D11View):
    _iid_ = comtypes.GUID("{dfdba067-0b8d-4865-875b-d7b4516cc164}")
    _methods_ = [
        comtypes.STDMETHOD(None,"GetDesc", [
            ctypes.POINTER(D3D11_RENDER_TARGET_VIEW_DESC),
            ]),
    ]

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  DepthStencilView
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_TEX1D_DSV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
    ]

class D3D11_TEX1D_ARRAY_DSV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX2D_DSV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
    ]

class D3D11_TEX2D_ARRAY_DSV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX2DMS_DSV(ctypes.Structure):
    _fields_ = [('UnusedField_NothingToDefine', ctypes.c_uint),
    ]

class D3D11_TEX2DMS_ARRAY_DSV(ctypes.Structure):
    _fields_ = [('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

D3D11_DSV_FLAG = ctypes.c_uint
D3D11_DSV_READ_ONLY_DEPTH  = D3D11_DSV_FLAG(0x1)
D3D11_DSV_READ_ONLY_STENCIL = D3D11_DSV_FLAG(0x2)

class D3D11_DEPTH_STENCIL_VIEW_DESC(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('Texture1D', D3D11_TEX1D_DSV),
                    ('Texture1DArray', D3D11_TEX1D_ARRAY_DSV),
                    ('Texture2D', D3D11_TEX2D_DSV),
                    ('Texture2DArray', D3D11_TEX2D_ARRAY_DSV),
                    ('Texture2DMS', D3D11_TEX2DMS_DSV),
                    ('Texture2DMSArray', D3D11_TEX2DMS_ARRAY_DSV),
        ]
    _anonymous_ =('i1',)
    _fields_ = [('Format', DXGI_FORMAT),
                ('ViewDimension', D3D11_DSV_DIMENSION),
                ('Flags', ctypes.c_uint), # D3D11_DSV_FLAG
                ('i1', _I1),
    ]

class ID3D11DepthStencilView(ID3D11View):
    _iid_ = comtypes.GUID("{9fdac92a-1876-48c3-afad-25b94f84a9b6}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_DEPTH_STENCIL_VIEW_DESC),
            ]),
    ]

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  UnorderedAccessView
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
D3D11_BUFFER_UAV_FLAG = ctypes.c_uint
D3D11_BUFFER_UAV_FLAG_RAW     = D3D11_BUFFER_UAV_FLAG(0x00000001)
D3D11_BUFFER_UAV_FLAG_APPEND  = D3D11_BUFFER_UAV_FLAG(0x00000002)
D3D11_BUFFER_UAV_FLAG_COUNTER = D3D11_BUFFER_UAV_FLAG(0x00000004)

class D3D11_BUFFER_UAV(ctypes.Structure):
    _fields_ = [('FirstElement', ctypes.c_uint),
                ('NumElements', ctypes.c_uint),
                ('Flags', ctypes.c_uint), # D3D11_BUFFER_UAV_FLAG_* below
    ]

class D3D11_TEX1D_UAV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
    ]

class D3D11_TEX1D_ARRAY_UAV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX2D_UAV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
    ]

class D3D11_TEX2D_ARRAY_UAV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_TEX3D_UAV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstWSlice', ctypes.c_uint),
                ('WSize', ctypes.c_uint),
    ]

class D3D11_UNORDERED_ACCESS_VIEW_DESC(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('Buffer', D3D11_BUFFER_UAV),
                    ('Texture1D',D3D11_TEX1D_UAV),
                    ('Texture1DArray',D3D11_TEX1D_ARRAY_UAV),
                    ('Texture2D',D3D11_TEX2D_UAV),
                    ('Texture2DArray',D3D11_TEX2D_ARRAY_UAV),
                    ('Texture3D',D3D11_TEX3D_UAV),
        ]

class ID3D11UnorderedAccessView(ID3D11View):
    _iid_ = comtypes.GUID("{28acf509-7f5c-48f6-8611-f316010a6380}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_UNORDERED_ACCESS_VIEW_DESC)
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Vertex Shader
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11VertexShader(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{3b301d64-d678-4289-8897-22f8928b72f3}")


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Hull Shader
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11HullShader(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{8e5c6061-628a-4c8e-8264-bbe45cb3d5dd}")


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Domain Shader
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11DomainShader(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{f582c508-0f36-490c-9977-31eece268cfa}")


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Geometry Shader
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11GeometryShader(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{38325b96-effb-4022-ba02-2e795b70275c}")


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Pixel Shader
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11PixelShader(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{ea82e40d-51dc-4f33-93d4-db7c9125ae8c}")

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Compute Shader
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11ComputeShader(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{4f5b196e-c2bd-495e-bd01-1fded38e4969}")

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  InputLayout
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11InputLayout(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{e4819ddc-4cf0-4025-bd26-5de82a3e07b7}")

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Sampler
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
D3D11_FILTER = ctypes.c_uint
## Bits used in defining enumeration of valid filters:
## bits [1:0] - mip: 0 == point, 1 == linear, 2,3 unused
## bits [3:2] - mag: 0 == point, 1 == linear, 2,3 unused
## bits [5:4] - min: 0 == point, 1 == linear, 2,3 unused
## bit  [6]   - aniso
## bits [8:7] - reduction type: 
##                0 == standard filtering
##                1 == comparison
##                2 == min
##                3 == max
## bit  [31]  - mono 1-bit (narrow-purpose filter) [no longer supported in D3D11]
D3D11_FILTER_MIN_MAG_MIP_POINT                              = D3D11_FILTER(0x00000000)
D3D11_FILTER_MIN_MAG_POINT_MIP_LINEAR                       = D3D11_FILTER(0x00000001)
D3D11_FILTER_MIN_POINT_MAG_LINEAR_MIP_POINT                 = D3D11_FILTER(0x00000004)
D3D11_FILTER_MIN_POINT_MAG_MIP_LINEAR                       = D3D11_FILTER(0x00000005)
D3D11_FILTER_MIN_LINEAR_MAG_MIP_POINT                       = D3D11_FILTER(0x00000010)
D3D11_FILTER_MIN_LINEAR_MAG_POINT_MIP_LINEAR                = D3D11_FILTER(0x00000011)
D3D11_FILTER_MIN_MAG_LINEAR_MIP_POINT                       = D3D11_FILTER(0x00000014)
D3D11_FILTER_MIN_MAG_MIP_LINEAR                             = D3D11_FILTER(0x00000015)
D3D11_FILTER_ANISOTROPIC                                    = D3D11_FILTER(0x00000055)
D3D11_FILTER_COMPARISON_MIN_MAG_MIP_POINT                   = D3D11_FILTER(0x00000080)
D3D11_FILTER_COMPARISON_MIN_MAG_POINT_MIP_LINEAR            = D3D11_FILTER(0x00000081)
D3D11_FILTER_COMPARISON_MIN_POINT_MAG_LINEAR_MIP_POINT      = D3D11_FILTER(0x00000084)
D3D11_FILTER_COMPARISON_MIN_POINT_MAG_MIP_LINEAR            = D3D11_FILTER(0x00000085)
D3D11_FILTER_COMPARISON_MIN_LINEAR_MAG_MIP_POINT            = D3D11_FILTER(0x00000090)
D3D11_FILTER_COMPARISON_MIN_LINEAR_MAG_POINT_MIP_LINEAR     = D3D11_FILTER(0x00000091)
D3D11_FILTER_COMPARISON_MIN_MAG_LINEAR_MIP_POINT            = D3D11_FILTER(0x00000094)
D3D11_FILTER_COMPARISON_MIN_MAG_MIP_LINEAR                  = D3D11_FILTER(0x00000095)
D3D11_FILTER_COMPARISON_ANISOTROPIC                         = D3D11_FILTER(0x000000d5)
D3D11_FILTER_MINIMUM_MIN_MAG_MIP_POINT                      = D3D11_FILTER(0x00000100)
D3D11_FILTER_MINIMUM_MIN_MAG_POINT_MIP_LINEAR               = D3D11_FILTER(0x00000101)
D3D11_FILTER_MINIMUM_MIN_POINT_MAG_LINEAR_MIP_POINT         = D3D11_FILTER(0x00000104)
D3D11_FILTER_MINIMUM_MIN_POINT_MAG_MIP_LINEAR               = D3D11_FILTER(0x00000105)
D3D11_FILTER_MINIMUM_MIN_LINEAR_MAG_MIP_POINT               = D3D11_FILTER(0x00000110)
D3D11_FILTER_MINIMUM_MIN_LINEAR_MAG_POINT_MIP_LINEAR        = D3D11_FILTER(0x00000111)
D3D11_FILTER_MINIMUM_MIN_MAG_LINEAR_MIP_POINT               = D3D11_FILTER(0x00000114)
D3D11_FILTER_MINIMUM_MIN_MAG_MIP_LINEAR                     = D3D11_FILTER(0x00000115)
D3D11_FILTER_MINIMUM_ANISOTROPIC                            = D3D11_FILTER(0x00000155)
D3D11_FILTER_MAXIMUM_MIN_MAG_MIP_POINT                      = D3D11_FILTER(0x00000180)
D3D11_FILTER_MAXIMUM_MIN_MAG_POINT_MIP_LINEAR               = D3D11_FILTER(0x00000181)
D3D11_FILTER_MAXIMUM_MIN_POINT_MAG_LINEAR_MIP_POINT         = D3D11_FILTER(0x00000184)
D3D11_FILTER_MAXIMUM_MIN_POINT_MAG_MIP_LINEAR               = D3D11_FILTER(0x00000185)
D3D11_FILTER_MAXIMUM_MIN_LINEAR_MAG_MIP_POINT               = D3D11_FILTER(0x00000190)
D3D11_FILTER_MAXIMUM_MIN_LINEAR_MAG_POINT_MIP_LINEAR        = D3D11_FILTER(0x00000191)
D3D11_FILTER_MAXIMUM_MIN_MAG_LINEAR_MIP_POINT               = D3D11_FILTER(0x00000194)
D3D11_FILTER_MAXIMUM_MIN_MAG_MIP_LINEAR                     = D3D11_FILTER(0x00000195)
D3D11_FILTER_MAXIMUM_ANISOTROPIC                            = D3D11_FILTER(0x000001d5)

D3D11_FILTER_TYPE = ctypes.c_uint
D3D11_FILTER_TYPE_POINT = D3D11_FILTER_TYPE(0)
D3D11_FILTER_TYPE_LINEAR = D3D11_FILTER_TYPE(1)

D3D11_FILTER_REDUCTION_TYPE = ctypes.c_uint
D3D11_FILTER_REDUCTION_TYPE_STANDARD   = D3D11_FILTER_REDUCTION_TYPE(0)
D3D11_FILTER_REDUCTION_TYPE_COMPARISON = D3D11_FILTER_REDUCTION_TYPE(1)
D3D11_FILTER_REDUCTION_TYPE_MINIMUM    = D3D11_FILTER_REDUCTION_TYPE(2)
D3D11_FILTER_REDUCTION_TYPE_MAXIMUM    = D3D11_FILTER_REDUCTION_TYPE(3)

D3D11_FILTER_REDUCTION_TYPE_MASK =  0x00000003  # const UINT
D3D11_FILTER_REDUCTION_TYPE_SHIFT = 7           # const UINT
D3D11_FILTER_TYPE_MASK = 0x00000003             # const UINT
D3D11_MIN_FILTER_SHIFT = 4                      # const UINT
D3D11_MAG_FILTER_SHIFT = 2                      # const UINT
D3D11_MIP_FILTER_SHIFT = 0                      # const UINT
D3D11_COMPARISON_FILTERING_BIT = 0x00000008     # const UINT
D3D11_ANISOTROPIC_FILTERING_BIT = 0x00000040    # const UINT

D3D11_TEXTURE_ADDRESS_MODE = ctypes.c_uint
D3D11_TEXTURE_ADDRESS_WRAP        = D3D11_TEXTURE_ADDRESS_MODE(1)
D3D11_TEXTURE_ADDRESS_MIRROR      = D3D11_TEXTURE_ADDRESS_MODE(2)
D3D11_TEXTURE_ADDRESS_CLAMP       = D3D11_TEXTURE_ADDRESS_MODE(3)
D3D11_TEXTURE_ADDRESS_BORDER      = D3D11_TEXTURE_ADDRESS_MODE(4)
D3D11_TEXTURE_ADDRESS_MIRROR_ONCE = D3D11_TEXTURE_ADDRESS_MODE(5)

class D3D11_SAMPLER_DESC(ctypes.Structure):
    _fields_ = [('Filter', D3D11_FILTER),
                ('AddressU', D3D11_TEXTURE_ADDRESS_MODE),
                ('AddressV', D3D11_TEXTURE_ADDRESS_MODE),
                ('AddressW', D3D11_TEXTURE_ADDRESS_MODE),
                ('MipLODBias', ctypes.c_float),
                ('MaxAnisotropy', ctypes.c_uint),
                ('ComparisonFunc', D3D11_COMPARISON_FUNC),
                ('BorderColor',ctypes.c_float * 4),
                ('MinLOD', ctypes.c_float),
                ('MaxLOD', ctypes.c_float),
    ]

class ID3D11SamplerState(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{da6fea51-564c-4487-9810-f0d0f9b4e3a5}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_SAMPLER_DESC),
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Format Support Flags for CheckFormatSupport API
##  Extended enum (and the original one) are also used in CheckFeatureSupport API (which is a superset of CheckFormatSupport).
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
D3D11_FORMAT_SUPPORT = ctypes.c_uint
D3D11_FORMAT_SUPPORT_BUFFER                      = D3D11_FORMAT_SUPPORT(0x00000001)
D3D11_FORMAT_SUPPORT_IA_VERTEX_BUFFER            = D3D11_FORMAT_SUPPORT(0x00000002)
D3D11_FORMAT_SUPPORT_IA_INDEX_BUFFER             = D3D11_FORMAT_SUPPORT(0x00000004)
D3D11_FORMAT_SUPPORT_SO_BUFFER                   = D3D11_FORMAT_SUPPORT(0x00000008)
D3D11_FORMAT_SUPPORT_TEXTURE1D                   = D3D11_FORMAT_SUPPORT(0x00000010)
D3D11_FORMAT_SUPPORT_TEXTURE2D                   = D3D11_FORMAT_SUPPORT(0x00000020)
D3D11_FORMAT_SUPPORT_TEXTURE3D                   = D3D11_FORMAT_SUPPORT(0x00000040)
D3D11_FORMAT_SUPPORT_TEXTURECUBE                 = D3D11_FORMAT_SUPPORT(0x00000080)
D3D11_FORMAT_SUPPORT_SHADER_LOAD                 = D3D11_FORMAT_SUPPORT(0x00000100)
D3D11_FORMAT_SUPPORT_SHADER_SAMPLE               = D3D11_FORMAT_SUPPORT(0x00000200)
D3D11_FORMAT_SUPPORT_SHADER_SAMPLE_COMPARISON    = D3D11_FORMAT_SUPPORT(0x00000400)
D3D11_FORMAT_SUPPORT_SHADER_SAMPLE_MONO_TEXT     = D3D11_FORMAT_SUPPORT(0x00000800)
D3D11_FORMAT_SUPPORT_MIP                         = D3D11_FORMAT_SUPPORT(0x00001000)
D3D11_FORMAT_SUPPORT_MIP_AUTOGEN                 = D3D11_FORMAT_SUPPORT(0x00002000)
D3D11_FORMAT_SUPPORT_RENDER_TARGET               = D3D11_FORMAT_SUPPORT(0x00004000)
D3D11_FORMAT_SUPPORT_BLENDABLE                   = D3D11_FORMAT_SUPPORT(0x00008000)
D3D11_FORMAT_SUPPORT_DEPTH_STENCIL               = D3D11_FORMAT_SUPPORT(0x00010000)
D3D11_FORMAT_SUPPORT_CPU_LOCKABLE                = D3D11_FORMAT_SUPPORT(0x00020000)
D3D11_FORMAT_SUPPORT_MULTISAMPLE_RESOLVE         = D3D11_FORMAT_SUPPORT(0x00040000)
D3D11_FORMAT_SUPPORT_DISPLAY                     = D3D11_FORMAT_SUPPORT(0x00080000)
D3D11_FORMAT_SUPPORT_CAST_WITHIN_BIT_LAYOUT      = D3D11_FORMAT_SUPPORT(0x00100000)
D3D11_FORMAT_SUPPORT_MULTISAMPLE_RENDERTARGET    = D3D11_FORMAT_SUPPORT(0x00200000)
D3D11_FORMAT_SUPPORT_MULTISAMPLE_LOAD            = D3D11_FORMAT_SUPPORT(0x00400000)
D3D11_FORMAT_SUPPORT_SHADER_GATHER               = D3D11_FORMAT_SUPPORT(0x00800000)
D3D11_FORMAT_SUPPORT_BACK_BUFFER_CAST            = D3D11_FORMAT_SUPPORT(0x01000000)
D3D11_FORMAT_SUPPORT_TYPED_UNORDERED_ACCESS_VIEW = D3D11_FORMAT_SUPPORT(0x02000000)
D3D11_FORMAT_SUPPORT_SHADER_GATHER_COMPARISON    = D3D11_FORMAT_SUPPORT(0x04000000)
D3D11_FORMAT_SUPPORT_DECODER_OUTPUT              = D3D11_FORMAT_SUPPORT(0x08000000)
D3D11_FORMAT_SUPPORT_VIDEO_PROCESSOR_OUTPUT      = D3D11_FORMAT_SUPPORT(0x10000000)
D3D11_FORMAT_SUPPORT_VIDEO_PROCESSOR_INPUT       = D3D11_FORMAT_SUPPORT(0x20000000)
D3D11_FORMAT_SUPPORT_VIDEO_ENCODER               = D3D11_FORMAT_SUPPORT(0x40000000)

D3D11_FORMAT_SUPPORT2 = ctypes.c_uint
D3D11_FORMAT_SUPPORT2_UAV_ATOMIC_ADD                               = D3D11_FORMAT_SUPPORT2(0x00000001)
D3D11_FORMAT_SUPPORT2_UAV_ATOMIC_BITWISE_OPS                       = D3D11_FORMAT_SUPPORT2(0x00000002)
D3D11_FORMAT_SUPPORT2_UAV_ATOMIC_COMPARE_STORE_OR_COMPARE_EXCHANGE = D3D11_FORMAT_SUPPORT2(0x00000004)
D3D11_FORMAT_SUPPORT2_UAV_ATOMIC_EXCHANGE                          = D3D11_FORMAT_SUPPORT2(0x00000008)
D3D11_FORMAT_SUPPORT2_UAV_ATOMIC_SIGNED_MIN_OR_MAX                 = D3D11_FORMAT_SUPPORT2(0x00000010)
D3D11_FORMAT_SUPPORT2_UAV_ATOMIC_UNSIGNED_MIN_OR_MAX               = D3D11_FORMAT_SUPPORT2(0x00000020)
D3D11_FORMAT_SUPPORT2_UAV_TYPED_LOAD                               = D3D11_FORMAT_SUPPORT2(0x00000040)
D3D11_FORMAT_SUPPORT2_UAV_TYPED_STORE                              = D3D11_FORMAT_SUPPORT2(0x00000080)
D3D11_FORMAT_SUPPORT2_OUTPUT_MERGER_LOGIC_OP                       = D3D11_FORMAT_SUPPORT2(0x00000100)
D3D11_FORMAT_SUPPORT2_TILED                                        = D3D11_FORMAT_SUPPORT2(0x00000200)
D3D11_FORMAT_SUPPORT2_SHAREABLE                                    = D3D11_FORMAT_SUPPORT2(0x00000400)
D3D11_FORMAT_SUPPORT2_MULTIPLANE_OVERLAY                           = D3D11_FORMAT_SUPPORT2(0x00004000)


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Query
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11Asynchronous(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{4b35d0cd-1e15-4258-9c98-1b1333f6dd3b}")
    _methods_ = [
        comtypes.STDMETHOD(ctypes.c_uint, "GetDataSize"),
    ]

D3D11_ASYNC_GETDATA_FLAG = ctypes.c_uint
D3D11_ASYNC_GETDATA_DONOTFLUSH = D3D11_ASYNC_GETDATA_FLAG(0x1)

D3D11_QUERY = ctypes.c_uint
D3D11_QUERY_EVENT                         = D3D11_QUERY(0)
D3D11_QUERY_OCCLUSION                     = D3D11_QUERY(1)
D3D11_QUERY_TIMESTAMP                     = D3D11_QUERY(2)
D3D11_QUERY_TIMESTAMP_DISJOINT            = D3D11_QUERY(3)
D3D11_QUERY_PIPELINE_STATISTICS           = D3D11_QUERY(4)
D3D11_QUERY_OCCLUSION_PREDICATE           = D3D11_QUERY(5)
D3D11_QUERY_SO_STATISTICS                 = D3D11_QUERY(6)
D3D11_QUERY_SO_OVERFLOW_PREDICATE         = D3D11_QUERY(7)
D3D11_QUERY_SO_STATISTICS_STREAM0         = D3D11_QUERY(8)
D3D11_QUERY_SO_OVERFLOW_PREDICATE_STREAM0 = D3D11_QUERY(9)
D3D11_QUERY_SO_STATISTICS_STREAM1         = D3D11_QUERY(10)
D3D11_QUERY_SO_OVERFLOW_PREDICATE_STREAM1 = D3D11_QUERY(11)
D3D11_QUERY_SO_STATISTICS_STREAM2         = D3D11_QUERY(12)
D3D11_QUERY_SO_OVERFLOW_PREDICATE_STREAM2 = D3D11_QUERY(13)
D3D11_QUERY_SO_STATISTICS_STREAM3         = D3D11_QUERY(14)
D3D11_QUERY_SO_OVERFLOW_PREDICATE_STREAM3 = D3D11_QUERY(15)

D3D11_QUERY_MISC_FLAG = ctypes.c_uint
D3D11_QUERY_MISC_PREDICATEHINT = D3D11_QUERY_MISC_FLAG(0x1)

class D3D11_QUERY_DESC(ctypes.Structure):
    _fields_ = [('Query', D3D11_QUERY),
                ('MiscFlags', ctypes.c_uint),
    ]

class ID3D11Query(ID3D11Asynchronous):
    _iid_ = comtypes.GUID("{d6c00747-87b7-425e-b84d-44d108560afd}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_QUERY_DESC),
            ]),
    ]

class ID3D11Predicate(ID3D11Query):
    _iid_ = comtypes.GUID("{9eb576dd-9f77-4d86-81aa-8bab5fe490e2}")

class D3D11_QUERY_DATA_TIMESTAMP_DISJOINT(ctypes.Structure):
    _fields_ = [('Frequency', ctypes.c_ulonglong),
                ('Disjoint', ctypes.c_bool),
    ]

class D3D11_QUERY_DATA_PIPELINE_STATISTICS(ctypes.Structure):
    _fields_ = [('IAVertices', ctypes.c_ulonglong),
                ('IAPrimitives', ctypes.c_ulonglong),
                ('VSInvocations', ctypes.c_ulonglong),
                ('GSInvocations', ctypes.c_ulonglong),
                ('GSPrimitives', ctypes.c_ulonglong),
                ('CInvocations', ctypes.c_ulonglong),
                ('CPrimitives', ctypes.c_ulonglong),
                ('PSInvocations', ctypes.c_ulonglong),
                ('HSInvocations', ctypes.c_ulonglong),
                ('DSInvocations', ctypes.c_ulonglong),
                ('CSInvocations', ctypes.c_ulonglong),
    ]

class D3D11_QUERY_DATA_SO_STATISTICS(ctypes.Structure):
    _fields_ = [('NumPrimitivesWritten',ctypes.c_ulonglong),
                ('PrimitivesStorageNeeded', ctypes.c_ulonglong),
    ]

D3D11_COUNTER = ctypes.c_uint
D3D11_COUNTER_DEVICE_DEPENDENT_0 = D3D11_COUNTER(0x40000000) # DO NOT define any more D3D11_COUNTER values after this.

D3D11_COUNTER_TYPE = ctypes.c_uint
D3D11_COUNTER_TYPE_FLOAT32 = D3D11_COUNTER_TYPE(0)
D3D11_COUNTER_TYPE_UINT16  = D3D11_COUNTER_TYPE(1)
D3D11_COUNTER_TYPE_UINT32  = D3D11_COUNTER_TYPE(2)
D3D11_COUNTER_TYPE_UINT64  = D3D11_COUNTER_TYPE(3)

class D3D11_COUNTER_DESC(ctypes.Structure):
    _fields_ = [('Counter', D3D11_COUNTER),
                ('MiscFlags', ctypes.c_uint),
    ]

class D3D11_COUNTER_INFO(ctypes.Structure):
    _fields_ = [('LastDeviceDependentCounter', D3D11_COUNTER),
                ('NumSimultaneousCounters', ctypes.c_uint),
                ('NumDetectableParallelUnits', ctypes.c_ubyte),
    ]

class ID3D11Counter(ID3D11Asynchronous):
    _iid_ = comtypes.GUID("{6e8c49fb-a371-4770-b440-29086022b741}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_COUNTER_DESC)
            ]),
    ]

D3D11_STANDARD_MULTISAMPLE_QUALITY_LEVELS = ctypes.c_uint
D3D11_STANDARD_MULTISAMPLE_PATTERN = D3D11_STANDARD_MULTISAMPLE_QUALITY_LEVELS(0xffffffff)
D3D11_CENTER_MULTISAMPLE_PATTERN   = D3D11_STANDARD_MULTISAMPLE_QUALITY_LEVELS(0xfffffffe)

D3D11_DEVICE_CONTEXT_TYPE = ctypes.c_uint
D3D11_DEVICE_CONTEXT_IMMEDIATE = D3D11_DEVICE_CONTEXT_TYPE(0)
D3D11_DEVICE_CONTEXT_DEFERRED  = D3D11_DEVICE_CONTEXT_TYPE(1)

class D3D11_CLASS_INSTANCE_DESC(ctypes.Structure):
    _fields_ = [ # the first two entries are valid if the instance was created using GetClassInstance
                ('InstanceId', ctypes.c_uint),
                ('InstanceIndex', ctypes.c_uint), # entry in an array of instances
                # the rest of the entries are valid for instances created with CreateClassInstance
                ('TypeId', ctypes.c_uint),
                ('ConstantBuffer', ctypes.c_uint),
                ('BaseConstantBufferOffset', ctypes.c_uint),
                ('BaseTexture', ctypes.c_uint),
                ('BaseSampler', ctypes.c_uint),
                # this lets you know which of the two an instance is
                ('Created', ctypes.c_bool),
    ]

class ID3D11ClassInstance(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{a6cd7faa-b0b7-4a2f-9436-8662a65797cb}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetClassLinkage", [
            # ctypes.POINTER(ctypes.POINTER(ID3D11ClassLinkage)), => No solution to resolve that
            ]),
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_CLASS_INSTANCE_DESC),
            ]),
        comtypes.STDMETHOD(None, "GetInstanceName", [
            wintypes.LPSTR,
            ctypes.POINTER(ctypes.c_size_t),
            ]),
        comtypes.STDMETHOD(None, "GetTypeName", [
            wintypes.LPSTR,
            ctypes.POINTER(ctypes.c_size_t),
            ]),
    ]

class ID3D11ClassLinkage(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{ddf57cba-9543-46e4-a12b-f207a0fe7fed}")
    _methods_ = [
        ## Get a reference to an instance of a class
        ## that exists in a shader.  The common scenario is to refer to
        ## variables declared in shaders, which means that a reference is
        ## acquired with this function and then passed in on SetShader.
        comtypes.STDMETHOD(comtypes.HRESULT, "GetClassInstance", [
            wintypes.LPCSTR,
            ctypes.c_uint,
            ctypes.POINTER(ctypes.POINTER(ID3D11ClassInstance)),
            ]),
        ## Create a class instance reference that is the combination of a class
        ## type and the location of the data to use for the class instance
        ## - not the common scenario, but useful in case the data location
        ## for a class is dynamic or not known until runtime.
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateClassInstance", [
            wintypes.LPCSTR,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.POINTER(ctypes.POINTER(ID3D11ClassInstance)),
            ]),
    ]

class ID3D11CommandList(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{a24bc4d1-769e-43f7-8013-98ff566c18e2}")
    _methods_ = [
        comtypes.STDMETHOD(ctypes.c_uint, "GetContextFlags", [])
    ]

D3D11_FEATURE = ctypes.c_uint
D3D11_FEATURE_THREADING                      = D3D11_FEATURE(0) # D3D11_FEATURE_DATA_THREADING
D3D11_FEATURE_DOUBLES                        = D3D11_FEATURE(1) # D3D11_FEATURE_DATA_DOUBLES
D3D11_FEATURE_FORMAT_SUPPORT                 = D3D11_FEATURE(2) # D3D11_FEATURE_DATA_FORMAT_SUPPORT
D3D11_FEATURE_FORMAT_SUPPORT2                = D3D11_FEATURE(3) # D3D11_FEATURE_DATA_FORMAT_SUPPORT2
D3D11_FEATURE_D3D10_X_HARDWARE_OPTIONS       = D3D11_FEATURE(4) # D3D11_FEATURE_DATA_D3D10_X_HARDWARE_OPTIONS
D3D11_FEATURE_D3D11_OPTIONS                  = D3D11_FEATURE(5) # D3D11_FEATURE_DATA_D3D11_OPTIONS
D3D11_FEATURE_ARCHITECTURE_INFO              = D3D11_FEATURE(6) # D3D11_FEATURE_DATA_ARCHITECTURE_INFO
D3D11_FEATURE_D3D9_OPTIONS                   = D3D11_FEATURE(7) # D3D11_FEATURE_DATA_D3D9_OPTIONS
D3D11_FEATURE_SHADER_MIN_PRECISION_SUPPORT   = D3D11_FEATURE(8) # D3D11_FEATURE_DATA_SHADER_MIN_PRECISION_SUPPORT
D3D11_FEATURE_D3D9_SHADOW_SUPPORT            = D3D11_FEATURE(9) # D3D11_FEATURE_DATA_D3D9_SHADOW_SUPPORT
D3D11_FEATURE_D3D11_OPTIONS1                 = D3D11_FEATURE(10) # D3D11_FEATURE_D3D11_OPTIONS1
D3D11_FEATURE_D3D9_SIMPLE_INSTANCING_SUPPORT = D3D11_FEATURE(11) # D3D11_FEATURE_DATA_D3D9_SIMPLE_INSTANCING_SUPPORT
D3D11_FEATURE_MARKER_SUPPORT                 = D3D11_FEATURE(12) # D3D11_FEATURE_DATA_MARKER_SUPPORT
D3D11_FEATURE_D3D9_OPTIONS1                  = D3D11_FEATURE(13) # D3D11_FEATURE_DATA_D3D9_OPTIONS1
D3D11_FEATURE_D3D11_OPTIONS2                 = D3D11_FEATURE(14) # D3D11_FEATURE_DATA_D3D11_OPTIONS2
D3D11_FEATURE_D3D11_OPTIONS3                 = D3D11_FEATURE(15) # D3D11_FEATURE_DATA_D3D11_OPTIONS3
D3D11_FEATURE_GPU_VIRTUAL_ADDRESS_SUPPORT    = D3D11_FEATURE(16) # D3D11_FEATURE_DATA_GPU_VIRTUAL_ADDRESS_SUPPORT
D3D11_FEATURE_D3D11_OPTIONS4                 = D3D11_FEATURE(17) # D3D11_FEATURE_DATA_D3D11_OPTIONS4
D3D11_FEATURE_SHADER_CACHE                   = D3D11_FEATURE(18) # D3D11_FEATURE_DATA_SHADER_CACHE
D3D11_FEATURE_D3D11_OPTIONS5                 = D3D11_FEATURE(19) # D3D11_FEATURE_DATA_D3D11_OPTIONS5

class D3D11_FEATURE_DATA_THREADING(ctypes.Structure):
    _fields_ = [('DriverConcurrentCreates', ctypes.c_bool),
                ('DriverCommandLists', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_DOUBLES(ctypes.Structure):
    _fields_ = [('DoublePrecisionFloatShaderOps', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_FORMAT_SUPPORT(ctypes.Structure):
    _fields_ = [('InFormat', DXGI_FORMAT),
                ('OutFormatSupport', ctypes.c_uint),
    ]

class D3D11_FEATURE_DATA_FORMAT_SUPPORT2(ctypes.Structure):
    _fields_ = [('InFormat', DXGI_FORMAT),
                ('OutFormatSupport2', ctypes.c_uint),
    ]

class D3D11_FEATURE_DATA_D3D10_X_HARDWARE_OPTIONS(ctypes.Structure):
    _fields_ = [('ComputeShaders_Plus_RawAndStructuredBuffers_Via_Shader_4_x', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_D3D11_OPTIONS(ctypes.Structure):
    _fields_ = [('OutputMergerLogicOp', ctypes.c_bool),
                ('UAVOnlyRenderingForcedSampleCount', ctypes.c_bool),
                ('DiscardAPIsSeenByDriver', ctypes.c_bool),
                ('FlagsForUpdateAndCopySeenByDriver', ctypes.c_bool),
                ('ClearView', ctypes.c_bool),
                ('CopyWithOverlap', ctypes.c_bool),
                ('ConstantBufferPartialUpdate', ctypes.c_bool),
                ('ConstantBufferOffsetting', ctypes.c_bool),
                ('MapNoOverwriteOnDynamicConstantBuffer', ctypes.c_bool),
                ('MapNoOverwriteOnDynamicBufferSRV', ctypes.c_bool),
                ('MultisampleRTVWithForcedSampleCountOne', ctypes.c_bool),
                ('SAD4ShaderInstructions', ctypes.c_bool),
                ('ExtendedDoublesShaderInstructions', ctypes.c_bool),
                ('ExtendedResourceSharing', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_ARCHITECTURE_INFO(ctypes.Structure):
    _fields_ = [('TileBasedDeferredRenderer', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_D3D9_OPTIONS(ctypes.Structure):
    _fields_ = [('FullNonPow2TextureSupport', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_D3D9_SHADOW_SUPPORT(ctypes.Structure):
    _fields_ = [('SupportsDepthAsTextureWithLessEqualComparisonFilter', ctypes.c_bool),
    ]

D3D11_SHADER_MIN_PRECISION_SUPPORT = ctypes.c_uint
D3D11_SHADER_MIN_PRECISION_10_BIT = D3D11_SHADER_MIN_PRECISION_SUPPORT(0x1)
D3D11_SHADER_MIN_PRECISION_16_BIT = D3D11_SHADER_MIN_PRECISION_SUPPORT(0x2)

class D3D11_FEATURE_DATA_SHADER_MIN_PRECISION_SUPPORT(ctypes.Structure):
    _fields_ = [('PixelShaderMinPrecision', ctypes.c_uint), # D3D11_SHADER_MIN_PRECISION_SUPPORT flags for PS
                ('AllOtherShaderStagesMinPrecision', ctypes.c_uint), # D3D11_SHADER_MIN_PRECISION_SUPPORT flags for other stages
    ]


D3D11_TILED_RESOURCES_TIER = ctypes.c_uint
D3D11_TILED_RESOURCES_NOT_SUPPORTED = D3D11_TILED_RESOURCES_TIER(0)
D3D11_TILED_RESOURCES_TIER_1 = D3D11_TILED_RESOURCES_TIER(1)
D3D11_TILED_RESOURCES_TIER_2 = D3D11_TILED_RESOURCES_TIER(2)
D3D11_TILED_RESOURCES_TIER_3 = D3D11_TILED_RESOURCES_TIER(3)

class D3D11_FEATURE_DATA_D3D11_OPTIONS1(ctypes.Structure):
    _fields_ = [('TiledResourcesTier', D3D11_TILED_RESOURCES_TIER),
                ('MinMaxFiltering', ctypes.c_bool),
                ('ClearViewAlsoSupportsDepthOnlyFormats', ctypes.c_bool),
                ('MapOnDefaultBuffers', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_D3D9_SIMPLE_INSTANCING_SUPPORT(ctypes.Structure):
    _fields_ = [('SimpleInstancingSupported', ctypes.c_bool),
    ] 

class D3D11_FEATURE_DATA_MARKER_SUPPORT(ctypes.Structure):
    _fields_ = [('Profile', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_D3D9_OPTIONS1(ctypes.Structure):
    _fields_ = [('FullNonPow2TextureSupported', ctypes.c_bool),
                ('DepthAsTextureWithLessEqualComparisonFilterSupported', ctypes.c_bool),
                ('SimpleInstancingSupported', ctypes.c_bool),
                ('TextureCubeFaceRenderTargetWithNonCubeDepthStencilSupported', ctypes.c_bool),
    ]

D3D11_CONSERVATIVE_RASTERIZATION_TIER = ctypes.c_uint 
D3D11_CONSERVATIVE_RASTERIZATION_NOT_SUPPORTED  = D3D11_CONSERVATIVE_RASTERIZATION_TIER(0)
D3D11_CONSERVATIVE_RASTERIZATION_TIER_1         = D3D11_CONSERVATIVE_RASTERIZATION_TIER(1)
D3D11_CONSERVATIVE_RASTERIZATION_TIER_2         = D3D11_CONSERVATIVE_RASTERIZATION_TIER(2)
D3D11_CONSERVATIVE_RASTERIZATION_TIER_3         = D3D11_CONSERVATIVE_RASTERIZATION_TIER(3)

class D3D11_FEATURE_DATA_D3D11_OPTIONS2(ctypes.Structure):
    _fields_ = [('PSSpecifiedStencilRefSupported', ctypes.c_bool),
                ('TypedUAVLoadAdditionalFormats', ctypes.c_bool),
                ('ROVsSupported', ctypes.c_bool),
                ('ConservativeRasterizationTier', D3D11_CONSERVATIVE_RASTERIZATION_TIER),
                ('TiledResourcesTier', D3D11_TILED_RESOURCES_TIER),
                ('MapOnDefaultTextures', ctypes.c_bool),
                ('StandardSwizzle', ctypes.c_bool),
                ('UnifiedMemoryArchitecture', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_D3D11_OPTIONS3(ctypes.Structure):
    _fields_ = [('VPAndRTArrayIndexFromAnyShaderFeedingRasterizer', ctypes.c_bool),
    ]

class D3D11_FEATURE_DATA_GPU_VIRTUAL_ADDRESS_SUPPORT(ctypes.Structure):
    _fields_ = [('MaxGPUVirtualAddressBitsPerResource', ctypes.c_uint),
                ('MaxGPUVirtualAddressBitsPerProcess', ctypes.c_uint),
    ]

D3D11_SHADER_CACHE_SUPPORT_FLAGS = ctypes.c_uint
D3D11_SHADER_CACHE_SUPPORT_NONE                     = D3D11_SHADER_CACHE_SUPPORT_FLAGS(0x0)
D3D11_SHADER_CACHE_SUPPORT_AUTOMATIC_INPROC_CACHE   = D3D11_SHADER_CACHE_SUPPORT_FLAGS(0x1)
D3D11_SHADER_CACHE_SUPPORT_AUTOMATIC_DISK_CACHE     = D3D11_SHADER_CACHE_SUPPORT_FLAGS(0x2)

class D3D11_FEATURE_DATA_SHADER_CACHE(ctypes.Structure):
    _fields_ = [('SupportFlags', ctypes.c_uint),
    ]

D3D11_SHARED_RESOURCE_TIER = ctypes.c_uint
D3D11_SHARED_RESOURCE_TIER_0 = D3D11_SHARED_RESOURCE_TIER(0)
D3D11_SHARED_RESOURCE_TIER_1 = D3D11_SHARED_RESOURCE_TIER(1)
D3D11_SHARED_RESOURCE_TIER_2 = D3D11_SHARED_RESOURCE_TIER(2)
D3D11_SHARED_RESOURCE_TIER_3 = D3D11_SHARED_RESOURCE_TIER(3)

class D3D11_FEATURE_DATA_D3D11_OPTIONS5(ctypes.Structure):
    _fields_ = [('SharedResourceTier', D3D11_SHARED_RESOURCE_TIER),
    ]

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  DeviceContext
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11DeviceContext(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{c0bfa96c-e089-44fb-8eaf-26f8796190da}")
    _methods_ = [
        ## !!! Order of functions is in decreasing order of priority ( as far as performance is concerned ) !!!
        ## !!! BEGIN HIGH-FREQUENCY !!!
        comtypes.STDMETHOD(None, "VSSetConstantBuffers", []),
        comtypes.STDMETHOD(None, "PSSetShaderResources", []),
        comtypes.STDMETHOD(None, "PSSetShader", []),
        comtypes.STDMETHOD(None, "PSSetSamplers", []),
        comtypes.STDMETHOD(None, "VSSetShader", []),
        comtypes.STDMETHOD(None, "DrawIndexed", []),
        comtypes.STDMETHOD(None, "Draw", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "Map", []),
        comtypes.STDMETHOD(None, "Unmap", []),
        comtypes.STDMETHOD(None, "PSSetConstantBuffers", []),
        comtypes.STDMETHOD(None, "IASetInputLayout", []),
        comtypes.STDMETHOD(None, "IASetVertexBuffers", []),
        comtypes.STDMETHOD(None, "IASetIndexBuffer", []),
        ## !!! END HIGH-FREQUENCY !!!

        ## !!! Order of functions is in decreasing order of priority ( as far as performance is concerned ) !!!
        ## !!! BEGIN MIDDLE-FREQUENCY !!!
        comtypes.STDMETHOD(None, "DrawIndexedInstanced", []),
        comtypes.STDMETHOD(None, "DrawInstanced", []),
        comtypes.STDMETHOD(None, "GSSetConstantBuffers", []),
        comtypes.STDMETHOD(None, "GSSetShader", []),
        comtypes.STDMETHOD(None, "IASetPrimitiveTopology", []),
        comtypes.STDMETHOD(None, "VSSetShaderResources", []),
        comtypes.STDMETHOD(None, "VSSetSamplers", []),
        comtypes.STDMETHOD(None, "Begin", []),
        comtypes.STDMETHOD(None, "End", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetData", []),
        comtypes.STDMETHOD(None, "SetPredication", []),
        comtypes.STDMETHOD(None, "GSSetShaderResources", []),
        comtypes.STDMETHOD(None, "GSSetSamplers", []),
        comtypes.STDMETHOD(None, "OMSetRenderTargets", [
            ctypes.c_uint,                # UINT NumViews
            ctypes.POINTER(ctypes.POINTER(ID3D11RenderTargetView)),     # ID3D11RenderTargetView * const * ppRenderTargetsViews
            ctypes.POINTER(ID3D11DepthStencilView),     # ID3D11DepthStencilView *pDepthStencilView
            ]),
        comtypes.STDMETHOD(None, "OMSetRenderTargetsAndUnorderedAccessViews", []),
        comtypes.STDMETHOD(None, "OMSetBlendState", []),
        comtypes.STDMETHOD(None, "SOSetTargets", []),
        comtypes.STDMETHOD(None, "DrawAuto", []),
        comtypes.STDMETHOD(None, "DrawIndexedInstancedIndirect", []),
        comtypes.STDMETHOD(None, "DrawInstancedIndirect", []),
        comtypes.STDMETHOD(None, "Dispatch", []),
        comtypes.STDMETHOD(None, "DispatchIndirect", []),
        comtypes.STDMETHOD(None, "RSSetState", []),
        comtypes.STDMETHOD(None, "RSSetViewports", []),
        comtypes.STDMETHOD(None, "RSSetScissorRects", []),
        comtypes.STDMETHOD(None, "CopySubresourceRegion", []),
        comtypes.STDMETHOD(None, "CopyResource", []),
        comtypes.STDMETHOD(None, "UpdateSubresource", []),
        comtypes.STDMETHOD(None, "CopyStructureCount", []),
        comtypes.STDMETHOD(None, "ClearRenderTargetView", [
            ctypes.POINTER(ID3D11RenderTargetView),    # ID3D11RenderTargetView *pRenderTargetView
            ctypes.c_float * 4,                        # const FLOAT [4]        ColorRGBA
            ]),
        comtypes.STDMETHOD(None, "ClearUnorderedAccessViewUint", []),
        comtypes.STDMETHOD(None, "ClearUnorderedAccessViewFloat", []),
        comtypes.STDMETHOD(None, "ClearDepthStencilView", []),
        comtypes.STDMETHOD(None, "GenerateMips", []),
        comtypes.STDMETHOD(None, "SetResourceMinLOD", []),
        comtypes.STDMETHOD(ctypes.c_float, "GetResourceMinLOD", []),
        comtypes.STDMETHOD(None, "ResolveSubresource", []),
        comtypes.STDMETHOD(None, "ExecuteCommandList", []),
        comtypes.STDMETHOD(None, "HSSetShaderResources", []),
        comtypes.STDMETHOD(None, "HSSetShader", []),
        comtypes.STDMETHOD(None, "HSSetSamplers", []),
        comtypes.STDMETHOD(None, "HSSetConstantBuffers", []),
        comtypes.STDMETHOD(None, "DSSetShaderResources", []),
        comtypes.STDMETHOD(None, "DSSetShader", []),
        comtypes.STDMETHOD(None, "DSSetSamplers", []),
        comtypes.STDMETHOD(None, "DSSetConstantBuffers", []),
        comtypes.STDMETHOD(None, "CSSetShaderResources", []),
        comtypes.STDMETHOD(None, "CSSetUnorderedAccessViews", []),
        comtypes.STDMETHOD(None, "CSSetShader", []),
        comtypes.STDMETHOD(None, "CSSetSamplers", []),
        comtypes.STDMETHOD(None, "CSSetConstantBuffers", []),

        ## GET functions
        comtypes.STDMETHOD(None, "VSGetConstantBuffers", []),
        comtypes.STDMETHOD(None, "PSGetShaderResources", []),
        comtypes.STDMETHOD(None, "PSGetShader", []),
        comtypes.STDMETHOD(None, "PSGetSamplers", []),
        comtypes.STDMETHOD(None, "VSGetShader", []),
        comtypes.STDMETHOD(None, "PSGetConstantBuffers", []),
        comtypes.STDMETHOD(None, "IAGetInputLayout", []),
        comtypes.STDMETHOD(None, "IAGetVertexBuffers", []),
        comtypes.STDMETHOD(None, "IAGetIndexBuffer", []),
        comtypes.STDMETHOD(None, "GSGetConstantBuffers", []),
        comtypes.STDMETHOD(None, "GSGetShader", []),
        comtypes.STDMETHOD(None, "IAGetPrimitiveTopology", []),
        comtypes.STDMETHOD(None, "VSGetShaderResources", []),
        comtypes.STDMETHOD(None, "VSGetSamplers", []),
        comtypes.STDMETHOD(None, "GetPredication", []),
        comtypes.STDMETHOD(None, "GSGetShaderResources", []),
        comtypes.STDMETHOD(None, "GSGetSamplers", []),
        comtypes.STDMETHOD(None, "OMGetRenderTargets", []),
        comtypes.STDMETHOD(None, "OMGetRenderTargetsAndUnorderedAccessViews", []),
        comtypes.STDMETHOD(None, "OMGetBlendState", []),
        comtypes.STDMETHOD(None, "OMGetDepthStencilState", []),
        comtypes.STDMETHOD(None, "SOGetTargets", []),
        comtypes.STDMETHOD(None, "RSGetState", []),
        comtypes.STDMETHOD(None, "RSGetViewports", []),
        comtypes.STDMETHOD(None, "RSGetScissorRects", []),
        comtypes.STDMETHOD(None, "HSGetShaderResources", []),
        comtypes.STDMETHOD(None, "HSGetShader", []),
        comtypes.STDMETHOD(None, "HSGetSamplers", []),
        comtypes.STDMETHOD(None, "HSGetConstantBuffers", []),
        comtypes.STDMETHOD(None, "DSGetShaderResources", []),
        comtypes.STDMETHOD(None, "DSGetShader", []),
        comtypes.STDMETHOD(None, "DSGetSamplers", []),
        comtypes.STDMETHOD(None, "DSGetConstantBuffers", []),
        comtypes.STDMETHOD(None, "CSGetShaderResources", []),
        comtypes.STDMETHOD(None, "CSGetUnorderedAccessViews", []),
        comtypes.STDMETHOD(None, "CSGetShader", []),
        comtypes.STDMETHOD(None, "CSGetSamplers", []),
        comtypes.STDMETHOD(None, "CSGetConstantBuffers", []),
        ## END GET Functions

        comtypes.STDMETHOD(None, "ClearState", []),
        comtypes.STDMETHOD(None, "Flush", []),
        ## !!! END MIDDLE-FREQUENCY !!!

        ## !!! Order of functions is in decreasing order of priority ( as far as performance is concerned ) !!!
        ## !!! BEGIN LOW-FREQUENCY !!!
        comtypes.STDMETHOD(D3D11_DEVICE_CONTEXT_TYPE, "GetType", []),
        comtypes.STDMETHOD(ctypes.c_uint, "GetContextFlags", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "FinishCommandList", [
            ctypes.c_bool,
            ctypes.POINTER(ctypes.POINTER(ID3D11CommandList)),
            ]),
        ## !!! END LOW-FREQUENCY !!!
    ]

## class interface ID3D11VideoDecoderOutputView
## class interface ID3D11VideoProcessorInputView
APP_DEPRECATED_HRESULT = comtypes.HRESULT
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  VideoDecoder
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_VIDEO_DECODER_DESC(ctypes.Structure):
    _fields_ = [('Guid', comtypes.GUID),
                ('SampleWidth', ctypes.c_uint),
                ('SampleHeight', ctypes.c_uint),
                ('OutputFormat', DXGI_FORMAT),
    ]

class D3D11_VIDEO_DECODER_CONFIG(ctypes.Structure):
    _fields_ = [('guidConfigBitstreamEncryption', comtypes.GUID),
                ('guidConfigMBcontrolEncryption', comtypes.GUID),
                ('guidConfigResidDiffEncryption', comtypes.GUID),
                ('ConfigBitstreamRaw',ctypes.c_uint),
                ('ConfigMBcontrolRasterOrder',ctypes.c_uint),
                ('ConfigResidDiffHost',ctypes.c_uint),
                ('ConfigSpatialResid8',ctypes.c_uint),
                ('ConfigResid8Subtraction',ctypes.c_uint),
                ('ConfigSpatialHost8or9Clipping',ctypes.c_uint),
                ('ConfigSpatialResidInterleaved',ctypes.c_uint),
                ('ConfigIntraResidUnsigned',ctypes.c_uint),
                ('ConfigResidDiffAccelerator',ctypes.c_uint),
                ('ConfigHostInverseScan',ctypes.c_uint),
                ('ConfigSpecificIDCT',ctypes.c_uint),
                ('Config4GroupedCoefs',ctypes.c_uint),
                ('ConfigMinRenderTargetBuffCount', ctypes.c_ushort),
                ('ConfigDecoderSpecific',ctypes.c_ushort),
    ]

D3D11_VIDEO_DECODER_BUFFER_TYPE = ctypes.c_uint
D3D11_VIDEO_DECODER_BUFFER_PICTURE_PARAMETERS               = D3D11_VIDEO_DECODER_BUFFER_TYPE(0)
D3D11_VIDEO_DECODER_BUFFER_MACROBLOCK_CONTROL               = D3D11_VIDEO_DECODER_BUFFER_TYPE(1)
D3D11_VIDEO_DECODER_BUFFER_RESIDUAL_DIFFERENCE              = D3D11_VIDEO_DECODER_BUFFER_TYPE(2)
D3D11_VIDEO_DECODER_BUFFER_DEBLOCKING_CONTROL               = D3D11_VIDEO_DECODER_BUFFER_TYPE(3)
D3D11_VIDEO_DECODER_BUFFER_INVERSE_QUANTIZATION_MATRIX      = D3D11_VIDEO_DECODER_BUFFER_TYPE(4)
D3D11_VIDEO_DECODER_BUFFER_SLICE_CONTROL                    = D3D11_VIDEO_DECODER_BUFFER_TYPE(5)
D3D11_VIDEO_DECODER_BUFFER_BITSTREAM                        = D3D11_VIDEO_DECODER_BUFFER_TYPE(6)
D3D11_VIDEO_DECODER_BUFFER_MOTION_VECTOR                    = D3D11_VIDEO_DECODER_BUFFER_TYPE(7)
D3D11_VIDEO_DECODER_BUFFER_FILM_GRAIN                       = D3D11_VIDEO_DECODER_BUFFER_TYPE(8)

class _D3D11_AES_CTR_IV(ctypes.Structure):
    _fields_ = [('IV', ctypes.c_ulonglong), # Big-Endian IV
                ('Count', ctypes.c_ulonglong), # Big-Endian Block Count
    ]

class D3D11_ENCRYPTED_BLOCK_INFO(ctypes.Structure):
    _fields_ = [('NumEncryptedBytesAtBeginning', ctypes.c_uint),
                ('NumBytesInSkipPattern', ctypes.c_uint),
                ('NumBytesInEncryptPattern', ctypes.c_uint),
    ]

class D3D11_VIDEO_DECODER_BUFFER_DESC(ctypes.Structure):
    _fields_ = [('BufferType', D3D11_VIDEO_DECODER_BUFFER_TYPE),
                ('BufferIndex', ctypes.c_uint),
                ('DataOffset', ctypes.c_uint),
                ('DataSize', ctypes.c_uint),
                ('FirstMBaddress', ctypes.c_uint),
                ('NumMBsInBuffer', ctypes.c_uint),
                ('Width', ctypes.c_uint),
                ('Height', ctypes.c_uint),
                ('Stride', ctypes.c_uint),
                ('ReservedBits', ctypes.c_uint),
                ('pIV', ctypes.c_void_p), # [annotation("_Field_size_opt_(IVSize)")] void* pIV;
                ('IVSize', ctypes.c_uint),
                ('PartialEncryption', ctypes.c_bool),
                ('EncryptedBlockInfo', D3D11_ENCRYPTED_BLOCK_INFO),
    ]

class D3D11_VIDEO_DECODER_EXTENSION(ctypes.Structure):
    _fields_ = [('Function', ctypes.c_uint),
                ('pPrivateInputData', ctypes.c_void_p),
                ('PrivateInputDataSize', ctypes.c_uint),
                ('pPrivateOutputData', ctypes.c_void_p),
                ('PrivateOutputDataSize', ctypes.c_uint),
                ('ResourceCount', ctypes.c_uint),
                ('ppResourceList', ctypes.POINTER(ctypes.POINTER(ID3D11Resource))),
    ]

class ID3D11VideoDecoder(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{3C9C5B51-995D-48d1-9B8D-FA5CAEDED65C}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetCreationParameters", [
            ctypes.POINTER(D3D11_VIDEO_DECODER_DESC),
            ctypes.POINTER(D3D11_VIDEO_DECODER_CONFIG),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDriverHandle", [
            ctypes.POINTER(wintypes.HANDLE),
            ]),
    ]

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  VideoProcessorEnum
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

D3D11_VIDEO_PROCESSOR_FORMAT_SUPPORT = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_FORMAT_SUPPORT_INPUT  = D3D11_VIDEO_PROCESSOR_FORMAT_SUPPORT(0x00000001)
D3D11_VIDEO_PROCESSOR_FORMAT_SUPPORT_OUTPUT = D3D11_VIDEO_PROCESSOR_FORMAT_SUPPORT(0x00000002)

D3D11_VIDEO_PROCESSOR_DEVICE_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_DEVICE_CAPS_LINEAR_SPACE            = D3D11_VIDEO_PROCESSOR_DEVICE_CAPS(0x1)
D3D11_VIDEO_PROCESSOR_DEVICE_CAPS_xvYCC                   = D3D11_VIDEO_PROCESSOR_DEVICE_CAPS(0x2)
D3D11_VIDEO_PROCESSOR_DEVICE_CAPS_RGB_RANGE_CONVERSION    = D3D11_VIDEO_PROCESSOR_DEVICE_CAPS(0x4)
D3D11_VIDEO_PROCESSOR_DEVICE_CAPS_YCbCr_MATRIX_CONVERSION = D3D11_VIDEO_PROCESSOR_DEVICE_CAPS(0x8)
D3D11_VIDEO_PROCESSOR_DEVICE_CAPS_NOMINAL_RANGE           = D3D11_VIDEO_PROCESSOR_DEVICE_CAPS(0x10)    

D3D11_VIDEO_PROCESSOR_FEATURE_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_ALPHA_FILL             = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x1)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_CONSTRICTION           = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x2)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_LUMA_KEY               = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x4)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_ALPHA_PALETTE          = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x8)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_LEGACY                 = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x10)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_STEREO                 = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x20)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_ROTATION               = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x40)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_ALPHA_STREAM           = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x80)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_PIXEL_ASPECT_RATIO     = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x100)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_MIRROR                 = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x200)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_SHADER_USAGE           = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x400)
D3D11_VIDEO_PROCESSOR_FEATURE_CAPS_METADATA_HDR10         = D3D11_VIDEO_PROCESSOR_FEATURE_CAPS(0x800)

D3D11_VIDEO_PROCESSOR_FILTER_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_BRIGHTNESS         = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x1)
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_CONTRAST           = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x2)
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_HUE                = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x4)
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_SATURATION         = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x8)
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_NOISE_REDUCTION    = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x10)
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_EDGE_ENHANCEMENT   = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x20)
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_ANAMORPHIC_SCALING = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x40)
D3D11_VIDEO_PROCESSOR_FILTER_CAPS_STEREO_ADJUSTMENT  = D3D11_VIDEO_PROCESSOR_FILTER_CAPS(0x80)

D3D11_VIDEO_PROCESSOR_FORMAT_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_FORMAT_CAPS_RGB_INTERLACED     = D3D11_VIDEO_PROCESSOR_FORMAT_CAPS(0x1)
D3D11_VIDEO_PROCESSOR_FORMAT_CAPS_RGB_PROCAMP        = D3D11_VIDEO_PROCESSOR_FORMAT_CAPS(0x2)
D3D11_VIDEO_PROCESSOR_FORMAT_CAPS_RGB_LUMA_KEY       = D3D11_VIDEO_PROCESSOR_FORMAT_CAPS(0x4)
D3D11_VIDEO_PROCESSOR_FORMAT_CAPS_PALETTE_INTERLACED = D3D11_VIDEO_PROCESSOR_FORMAT_CAPS(0x8)

D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_DENOISE              = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x01)
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_DERINGING            = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x02)
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_EDGE_ENHANCEMENT     = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x04)
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_COLOR_CORRECTION     = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x08)
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_FLESH_TONE_MAPPING   = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x10)
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_IMAGE_STABILIZATION  = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x20)
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_SUPER_RESOLUTION     = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x40)
D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS_ANAMORPHIC_SCALING   = D3D11_VIDEO_PROCESSOR_AUTO_STREAM_CAPS(0x80)

D3D11_VIDEO_PROCESSOR_STEREO_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_STEREO_CAPS_MONO_OFFSET         = D3D11_VIDEO_PROCESSOR_STEREO_CAPS(0x01)
D3D11_VIDEO_PROCESSOR_STEREO_CAPS_ROW_INTERLEAVED     = D3D11_VIDEO_PROCESSOR_STEREO_CAPS(0x02)
D3D11_VIDEO_PROCESSOR_STEREO_CAPS_COLUMN_INTERLEAVED  = D3D11_VIDEO_PROCESSOR_STEREO_CAPS(0x04)
D3D11_VIDEO_PROCESSOR_STEREO_CAPS_CHECKERBOARD        = D3D11_VIDEO_PROCESSOR_STEREO_CAPS(0x08)
D3D11_VIDEO_PROCESSOR_STEREO_CAPS_FLIP_MODE           = D3D11_VIDEO_PROCESSOR_STEREO_CAPS(0x10)

class D3D11_VIDEO_PROCESSOR_CAPS(ctypes.Structure):
    _fields_ = [('DeviceCaps', ctypes.c_uint),
                ('FeatureCaps', ctypes.c_uint),
                ('FilterCaps', ctypes.c_uint),
                ('InputFormatCaps', ctypes.c_uint),
                ('AutoStreamCaps', ctypes.c_uint),
                ('StereoCaps', ctypes.c_uint),
                ('RateConversionCapsCount', ctypes.c_uint),
                ('MaxInputStreams', ctypes.c_uint),
                ('MaxStreamStates', ctypes.c_uint),
    ]

D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS_DEINTERLACE_BLEND                 = D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS(0x1)
D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS_DEINTERLACE_BOB                   = D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS(0x2)
D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS_DEINTERLACE_ADAPTIVE              = D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS(0x4)
D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS_DEINTERLACE_MOTION_COMPENSATION   = D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS(0x8)
D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS_INVERSE_TELECINE                  = D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS(0x10)
D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS_FRAME_RATE_CONVERSION             = D3D11_VIDEO_PROCESSOR_PROCESSOR_CAPS(0x20)

D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_32             = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x1)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_22             = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x2)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_2224           = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x4)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_2332           = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x8)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_32322          = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x10)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_55             = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x20)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_64             = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x40)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_87             = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x80)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_222222222223   = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x100)
D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS_OTHER          = D3D11_VIDEO_PROCESSOR_ITELECINE_CAPS(0x80000000)

class D3D11_VIDEO_PROCESSOR_RATE_CONVERSION_CAPS(ctypes.Structure):
    _fields_ = [('PastFrames', ctypes.c_uint),
                ('FutureFrames', ctypes.c_uint),
                ('ProcessorCaps', ctypes.c_uint),
                ('ITelecineCaps', ctypes.c_uint),
                ('CustomRateCount', ctypes.c_uint),
    ]

D3D11_CONTENT_PROTECTION_CAPS = ctypes.c_uint
D3D11_CONTENT_PROTECTION_CAPS_SOFTWARE                                  = D3D11_CONTENT_PROTECTION_CAPS(0x00000001)
D3D11_CONTENT_PROTECTION_CAPS_HARDWARE                                  = D3D11_CONTENT_PROTECTION_CAPS(0x00000002)
D3D11_CONTENT_PROTECTION_CAPS_PROTECTION_ALWAYS_ON                      = D3D11_CONTENT_PROTECTION_CAPS(0x00000004)
D3D11_CONTENT_PROTECTION_CAPS_PARTIAL_DECRYPTION                        = D3D11_CONTENT_PROTECTION_CAPS(0x00000008)
D3D11_CONTENT_PROTECTION_CAPS_CONTENT_KEY                               = D3D11_CONTENT_PROTECTION_CAPS(0x00000010)
D3D11_CONTENT_PROTECTION_CAPS_FRESHEN_SESSION_KEY                       = D3D11_CONTENT_PROTECTION_CAPS(0x00000020)
D3D11_CONTENT_PROTECTION_CAPS_ENCRYPTED_READ_BACK                       = D3D11_CONTENT_PROTECTION_CAPS(0x00000040)
D3D11_CONTENT_PROTECTION_CAPS_ENCRYPTED_READ_BACK_KEY                   = D3D11_CONTENT_PROTECTION_CAPS(0x00000080)
D3D11_CONTENT_PROTECTION_CAPS_SEQUENTIAL_CTR_IV                         = D3D11_CONTENT_PROTECTION_CAPS(0x00000100)
D3D11_CONTENT_PROTECTION_CAPS_ENCRYPT_SLICEDATA_ONLY                    = D3D11_CONTENT_PROTECTION_CAPS(0x00000200)
D3D11_CONTENT_PROTECTION_CAPS_DECRYPTION_BLT                            = D3D11_CONTENT_PROTECTION_CAPS(0x00000400)
D3D11_CONTENT_PROTECTION_CAPS_HARDWARE_PROTECT_UNCOMPRESSED             = D3D11_CONTENT_PROTECTION_CAPS(0x00000800)
D3D11_CONTENT_PROTECTION_CAPS_HARDWARE_PROTECTED_MEMORY_PAGEABLE        = D3D11_CONTENT_PROTECTION_CAPS(0x00001000)
D3D11_CONTENT_PROTECTION_CAPS_HARDWARE_TEARDOWN                         = D3D11_CONTENT_PROTECTION_CAPS(0x00002000)
D3D11_CONTENT_PROTECTION_CAPS_HARDWARE_DRM_COMMUNICATION                = D3D11_CONTENT_PROTECTION_CAPS(0x00004000)
D3D11_CONTENT_PROTECTION_CAPS_HARDWARE_DRM_COMMUNICATION_MULTI_THREADED = D3D11_CONTENT_PROTECTION_CAPS(0x00008000)

class D3D11_VIDEO_CONTENT_PROTECTION_CAPS(ctypes.Structure):
    _fields_ = [('Caps', ctypes.c_uint),
                ('KeyExchangeTypeCount', ctypes.c_uint),
                ('BlockAlignmentSize', ctypes.c_uint),
                ('ProtectedMemorySize', ctypes.c_ulonglong),
    ]

class D3D11_VIDEO_PROCESSOR_CUSTOM_RATE(ctypes.Structure):
    _fields_ = [('CustomRate', DXGI_RATIONAL),
                ('OutputFrames', ctypes.c_uint),
                ('InputInterlaced', ctypes.c_bool),
                ('InputFramesOrFields', ctypes.c_uint),
    ]

D3D11_VIDEO_PROCESSOR_FILTER = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_FILTER_BRIGHTNESS           = D3D11_VIDEO_PROCESSOR_FILTER(0)
D3D11_VIDEO_PROCESSOR_FILTER_CONTRAST             = D3D11_VIDEO_PROCESSOR_FILTER(1)
D3D11_VIDEO_PROCESSOR_FILTER_HUE                  = D3D11_VIDEO_PROCESSOR_FILTER(2)
D3D11_VIDEO_PROCESSOR_FILTER_SATURATION           = D3D11_VIDEO_PROCESSOR_FILTER(3)
D3D11_VIDEO_PROCESSOR_FILTER_NOISE_REDUCTION      = D3D11_VIDEO_PROCESSOR_FILTER(4)
D3D11_VIDEO_PROCESSOR_FILTER_EDGE_ENHANCEMENT     = D3D11_VIDEO_PROCESSOR_FILTER(5)
D3D11_VIDEO_PROCESSOR_FILTER_ANAMORPHIC_SCALING   = D3D11_VIDEO_PROCESSOR_FILTER(6) 
D3D11_VIDEO_PROCESSOR_FILTER_STEREO_ADJUSTMENT    = D3D11_VIDEO_PROCESSOR_FILTER(7)

class D3D11_VIDEO_PROCESSOR_FILTER_RANGE(ctypes.Structure):
    _fields_ = [('Minimum', ctypes.c_int),
                ('Maximum', ctypes.c_int),
                ('Default', ctypes.c_int),
                ('Multiplier', ctypes.c_float),
    ]

D3D11_VIDEO_FRAME_FORMAT = ctypes.c_uint
D3D11_VIDEO_FRAME_FORMAT_PROGRESSIVE                    = D3D11_VIDEO_FRAME_FORMAT(0)
D3D11_VIDEO_FRAME_FORMAT_INTERLACED_TOP_FIELD_FIRST     = D3D11_VIDEO_FRAME_FORMAT(1)
D3D11_VIDEO_FRAME_FORMAT_INTERLACED_BOTTOM_FIELD_FIRST  = D3D11_VIDEO_FRAME_FORMAT(2)

D3D11_VIDEO_USAGE = ctypes.c_uint
D3D11_VIDEO_USAGE_PLAYBACK_NORMAL = D3D11_VIDEO_USAGE(0)
D3D11_VIDEO_USAGE_OPTIMAL_SPEED   = D3D11_VIDEO_USAGE(1)
D3D11_VIDEO_USAGE_OPTIMAL_QUALITY = D3D11_VIDEO_USAGE(2)

class D3D11_VIDEO_PROCESSOR_CONTENT_DESC(ctypes.Structure):
    _fields_ = [('InputFrameFormat', D3D11_VIDEO_FRAME_FORMAT),
                ('InputFrameRate', DXGI_RATIONAL),
                ('InputWidth', ctypes.c_uint),
                ('InputHeight', ctypes.c_uint),
                ('OutputFrameRate', DXGI_RATIONAL),
                ('OutputWidth', ctypes.c_uint),
                ('OutputHeight', ctypes.c_uint),
                ('Usage', D3D11_VIDEO_USAGE),
    ]

class ID3D11VideoProcessorEnumerator(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{31627037-53AB-4200-9061-05FAA9AB45F9}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoProcessorContentDesc", [
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_CONTENT_DESC),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckVideoProcessorFormat", [
            DXGI_RATIONAL,
            ctypes.POINTER(ctypes.c_uint),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoProcessorCaps", [
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_CAPS),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoProcessorRateConversionCaps", [
            ctypes.c_uint,
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_RATE_CONVERSION_CAPS)
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoProcessorCustomRate", [
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_CUSTOM_RATE),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoProcessorFilterRange", [
            D3D11_VIDEO_PROCESSOR_FILTER,
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_FILTER_RANGE),
            ]),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  VideoProcessor
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class D3D11_VIDEO_COLOR_RGBA(ctypes.Structure):
    _fields_ = [('R', ctypes.c_float), 
                ('G', ctypes.c_float),
                ('B', ctypes.c_float),
                ('A', ctypes.c_float),
    ]

class D3D11_VIDEO_COLOR_YCbCrA(ctypes.Structure):
    _fields_ = [('Y', ctypes.c_float),
                ('Cb', ctypes.c_float),
                ('Cr', ctypes.c_float),
                ('A', ctypes.c_float),
    ]

class D3D11_VIDEO_COLOR(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('YCbCr', D3D11_VIDEO_COLOR_YCbCrA),
                    ('RGBA', D3D11_VIDEO_COLOR_RGBA),
        ]
    _anonymous_ = ('i1',)
    _fields_ = [('i1', _I1),
    ]

D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE_UNDEFINED         = D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE(0)
D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE_16_235            = D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE(1)
D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE_0_255             = D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE(2)

class D3D11_VIDEO_PROCESSOR_COLOR_SPACE(ctypes.Structure):
    _fields_ = [('Usage', ctypes.c_uint),       # 1 or 0
                ('RGB_Range', ctypes.c_uint),   # 1 or 0
                ('YCbCr_Matrix', ctypes.c_uint), # 1 or 0
                ('YCbCr_xvYCC', ctypes.c_uint), # 1 or 0
                ('Nominal_Range', ctypes.c_uint), # 2 # D3D11_VIDEO_PROCESSOR_NOMINAL_RANGE
                ('Reserved', ctypes.c_uint), # 26
    ]

D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE_OPAQUE          = D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE(0)
D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE_BACKGROUND      = D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE(1)
D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE_DESTINATION     = D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE(2)
D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE_SOURCE_STREAM   = D3D11_VIDEO_PROCESSOR_ALPHA_FILL_MODE(3)

D3D11_VIDEO_PROCESSOR_OUTPUT_RATE = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_OUTPUT_RATE_NORMAL   = D3D11_VIDEO_PROCESSOR_OUTPUT_RATE(0)
D3D11_VIDEO_PROCESSOR_OUTPUT_RATE_HALF     = D3D11_VIDEO_PROCESSOR_OUTPUT_RATE(1)
D3D11_VIDEO_PROCESSOR_OUTPUT_RATE_CUSTOM   = D3D11_VIDEO_PROCESSOR_OUTPUT_RATE(2)

D3D11_VIDEO_PROCESSOR_STEREO_FORMAT = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_MONO               = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(0)
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_HORIZONTAL         = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(1)
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_VERTICAL           = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(2)
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_SEPARATE           = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(3)
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_MONO_OFFSET        = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(4)
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_ROW_INTERLEAVED    = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(5)
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_COLUMN_INTERLEAVED = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(6)
D3D11_VIDEO_PROCESSOR_STEREO_FORMAT_CHECKERBOARD       = D3D11_VIDEO_PROCESSOR_STEREO_FORMAT(7)

D3D11_VIDEO_PROCESSOR_STEREO_FLIP_MODE = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_STEREO_FLIP_NONE   = D3D11_VIDEO_PROCESSOR_STEREO_FLIP_MODE(0)
D3D11_VIDEO_PROCESSOR_STEREO_FLIP_FRAME0 = D3D11_VIDEO_PROCESSOR_STEREO_FLIP_MODE(1)
D3D11_VIDEO_PROCESSOR_STEREO_FLIP_FRAME1 = D3D11_VIDEO_PROCESSOR_STEREO_FLIP_MODE(2)

D3D11_VIDEO_PROCESSOR_ROTATION = ctypes.c_uint
D3D11_VIDEO_PROCESSOR_ROTATION_IDENTITY      = D3D11_VIDEO_PROCESSOR_ROTATION(0)
D3D11_VIDEO_PROCESSOR_ROTATION_90            = D3D11_VIDEO_PROCESSOR_ROTATION(1)
D3D11_VIDEO_PROCESSOR_ROTATION_180           = D3D11_VIDEO_PROCESSOR_ROTATION(2)
D3D11_VIDEO_PROCESSOR_ROTATION_270           = D3D11_VIDEO_PROCESSOR_ROTATION(3)

class D3D11_VIDEO_PROCESSOR_STREAM(ctypes.Structure):
    _fields_ = [('Enable', ctypes.c_bool), 
                ('OutputIndex', ctypes.c_uint),
                ('InputFrameOrField', ctypes.c_uint),
                ('PastFrames', ctypes.c_uint),
                ('FutureFrames', ctypes.c_uint),
                # Interface dependance defined after 
                #('ppPastSurfaces', ctypes.POINTER(ctypes.POINTER(ID3D11VideoProcessorInputView))),
                #('pInputSurface', ctypes.POINTER(ID3D11VideoProcessorInputView)),
                #('ppFutureSurfaces', ctypes.POINTER(ctypes.POINTER(ID3D11VideoProcessorInputView))),
                #('ppPastSurfacesRight', ctypes.POINTER(ctypes.POINTER(ID3D11VideoProcessorInputView))),
                #('pInputSurfaceRight', ctypes.POINTER(ID3D11VideoProcessorInputView)),
                #('ppFutureSurfacesRight', ctypes.POINTER(ctypes.POINTER(ID3D11VideoProcessorInputView))),
    ]

class ID3D11VideoProcessor(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{1D7B0652-185F-41c6-85CE-0C5BE3D4AE6C}")
    _methods_ = [
        comtypes.STDMETHOD(None , "GetContentDesc", [
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_CONTENT_DESC),
            ]),
        comtypes.STDMETHOD(None , "GetRateConversionCaps", [
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_RATE_CONVERSION_CAPS),
            ]),
    ]

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  AuthenticatedChannel
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
D3D11_OMAC_SIZE = 16

class D3D11_OMAC(ctypes.Structure):
    _fields_ = [('Omac', wintypes.BYTE * D3D11_OMAC_SIZE),
    ]

D3D11_AUTHENTICATED_CHANNEL_TYPE = ctypes.c_uint
D3D11_AUTHENTICATED_CHANNEL_D3D11           = D3D11_AUTHENTICATED_CHANNEL_TYPE(1)
D3D11_AUTHENTICATED_CHANNEL_DRIVER_SOFTWARE = D3D11_AUTHENTICATED_CHANNEL_TYPE(2)
D3D11_AUTHENTICATED_CHANNEL_DRIVER_HARDWARE = D3D11_AUTHENTICATED_CHANNEL_TYPE(3)

class ID3D11AuthenticatedChannel(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{3015A308-DCBD-47aa-A747-192486D14D4A}")
    _methods_ = [
        comtypes.STDMETHOD(ctypes.HRESULT, "GetCertificateSize", [
            ctypes.POINTER(ctypes.c_uint),
            ]),
        comtypes.STDMETHOD(ctypes.HRESULT, "GetCertificate", [
            ctypes.c_uint,
            ctypes.POINTER(wintypes.BYTE),
            ]),
        comtypes.STDMETHOD(None, "GetChannelHandle", [
            ctypes.POINTER(wintypes.HANDLE),
            ]),
    ]

class D3D11_AUTHENTICATED_QUERY_INPUT(ctypes.Structure):
    _fields_ = [('QueryType', comtypes.GUID),
                ('hChannel', wintypes.HANDLE),
                ('SequenceNumber', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_QUERY_OUTPUT(ctypes.Structure):
    _fields_ = [('omac', D3D11_OMAC),
                ('QueryType', comtypes.GUID),
                ('hChannel', wintypes.HANDLE),
                ('SequenceNumber', ctypes.c_uint),
                ('ReturnCode', comtypes.HRESULT),
    ]

class D3D11_AUTHENTICATED_PROTECTION_FLAGS(ctypes.Union):
    class _Flags(ctypes.Structure):
        _fields_ = [('ProtectionEnabled', ctypes.c_uint), # 1
                    ('OverlayOrFullscreenRequired', ctypes.c_uint), # 1
                    ('Reserved', ctypes.c_uint), # 30
        ]
    _anonymous_ = ('Flags',)
    _fields_ = [('Flags',_Flags),
                ('Value', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_QUERY_PROTECTION_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('ProtectionFlags', D3D11_AUTHENTICATED_PROTECTION_FLAGS),
    ]

class D3D11_AUTHENTICATED_QUERY_CHANNEL_TYPE_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('DeviceHandle', wintypes.HANDLE),
    ]

class D3D11_AUTHENTICATED_QUERY_CRYPTO_SESSION_INPUT(ctypes.Structure):
    _fields_ = [('Input', D3D11_AUTHENTICATED_QUERY_INPUT),
                ('DecoderHandle', wintypes.HANDLE),
    ]

class D3D11_AUTHENTICATED_QUERY_CRYPTO_SESSION_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('DecoderHandle', wintypes.HANDLE),
                ('CryptoSessionHandle', wintypes.HANDLE),
                ('DeviceHandle', wintypes.HANDLE),
    ]

class D3D11_AUTHENTICATED_QUERY_RESTRICTED_SHARED_RESOURCE_PROCESS_COUNT_OUTPUT(ctypes.Structure):
    _fields_ = [('Input', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('ProcessIndex', ctypes.c_uint),
    ]

D3D11_AUTHENTICATED_PROCESS_IDENTIFIER_TYPE = ctypes.c_uint
D3D11_PROCESSIDTYPE_UNKNOWN  = D3D11_AUTHENTICATED_PROCESS_IDENTIFIER_TYPE(0)
D3D11_PROCESSIDTYPE_DWM      = D3D11_AUTHENTICATED_PROCESS_IDENTIFIER_TYPE(1)
D3D11_PROCESSIDTYPE_HANDLE   = D3D11_AUTHENTICATED_PROCESS_IDENTIFIER_TYPE(2)

class D3D11_AUTHENTICATED_QUERY_RESTRICTED_SHARED_RESOURCE_PROCESS_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('ProcessIndex', ctypes.c_uint),
                ('ProcessIdentifier', D3D11_AUTHENTICATED_PROCESS_IDENTIFIER_TYPE),
                ('ProcessHandle', wintypes.HANDLE),
    ]

class D3D11_AUTHENTICATED_QUERY_UNRESTRICTED_PROTECTED_SHARED_RESOURCE_COUNT_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('UnrestrictedProtectedSharedResourceCount', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_QUERY_OUTPUT_ID_COUNT_INPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_INPUT),
                ('DeviceHandle', wintypes.HANDLE),
                ('CryptoSessionHandle', wintypes.HANDLE),
    ]

class D3D11_AUTHENTICATED_QUERY_OUTPUT_ID_COUNT_OUTPUT(ctypes.Structure):
    _fields_ = [('Output',D3D11_AUTHENTICATED_QUERY_OUTPUT), 
                ('DeviceHandle', wintypes.HANDLE),
                ('CryptoSessionHandle', wintypes.HANDLE),
                ('OutputIDCount', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_QUERY_OUTPUT_ID_INPUT(ctypes.Structure):
    _fields_ = [('Input', D3D11_AUTHENTICATED_QUERY_INPUT),
                ('DeviceHandle', wintypes.HANDLE),
                ('CryptoSessionHandle', wintypes.HANDLE),
                ('OutputIDIndex', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_QUERY_OUTPUT_ID_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('DeviceHandle', wintypes.HANDLE),
                ('CryptoSessionHandle', wintypes.HANDLE),
                ('OutputIDIndex', ctypes.c_uint),
                ('OutputID', ctypes.c_ulonglong),

    ]

D3D11_BUS_TYPE = ctypes.c_uint
D3D11_BUS_TYPE_OTHER                                     = D3D11_BUS_TYPE(0x00000000)
D3D11_BUS_TYPE_PCI                                       = D3D11_BUS_TYPE(0x00000001)
D3D11_BUS_TYPE_PCIX                                      = D3D11_BUS_TYPE(0x00000002)
D3D11_BUS_TYPE_PCIEXPRESS                                = D3D11_BUS_TYPE(0x00000003)
D3D11_BUS_TYPE_AGP                                       = D3D11_BUS_TYPE(0x00000004)
D3D11_BUS_IMPL_MODIFIER_INSIDE_OF_CHIPSET                = D3D11_BUS_TYPE(0x00010000)
D3D11_BUS_IMPL_MODIFIER_TRACKS_ON_MOTHER_BOARD_TO_CHIP   = D3D11_BUS_TYPE(0x00020000)
D3D11_BUS_IMPL_MODIFIER_TRACKS_ON_MOTHER_BOARD_TO_SOCKET = D3D11_BUS_TYPE(0x00030000)
D3D11_BUS_IMPL_MODIFIER_DAUGHTER_BOARD_CONNECTOR         = D3D11_BUS_TYPE(0x00040000)
D3D11_BUS_IMPL_MODIFIER_DAUGHTER_BOARD_CONNECTOR_INSIDE_OF_NUAE = D3D11_BUS_TYPE(0x00050000)
D3D11_BUS_IMPL_MODIFIER_NON_STANDARD                     = D3D11_BUS_TYPE(0x80000000)

class D3D11_AUTHENTICATED_QUERY_ACESSIBILITY_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('BusType', D3D11_BUS_TYPE),
                ('AccessibleInContiguousBlocks', ctypes.c_bool),
                ('AccessibleInNonContiguousBlocks', ctypes.c_bool),
    ]

class D3D11_AUTHENTICATED_QUERY_ACCESSIBILITY_ENCRYPTION_GUID_COUNT_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('EncryptionGuidCount', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_QUERY_ACCESSIBILITY_ENCRYPTION_GUID_INPUT(ctypes.Structure):
    _fields_ = [('Input', D3D11_AUTHENTICATED_QUERY_INPUT),
                ('EncryptionGuidIndex', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_QUERY_ACCESSIBILITY_ENCRYPTION_GUID_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('EncryptionGuidIndex', ctypes.c_uint),
                ('EncryptionGuid', comtypes.GUID),
    ]

class D3D11_AUTHENTICATED_QUERY_CURRENT_ACCESSIBILITY_ENCRYPTION_OUTPUT(ctypes.Structure):
    _fields_ = [('Output', D3D11_AUTHENTICATED_QUERY_OUTPUT),
                ('EncryptionGuid', comtypes.GUID),
    ]

class D3D11_AUTHENTICATED_CONFIGURE_INPUT(ctypes.Structure):
    _fields_ = [('omac', D3D11_OMAC),
                ('ConfigureType', comtypes.GUID),
                ('hChannel', wintypes.HANDLE),
                ('SequenceNumber', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_CONFIGURE_OUTPUT(ctypes.Structure):
    _fields_ = [('omac', D3D11_OMAC),
                ('ConfigureType', comtypes.GUID),
                ('hChannel', wintypes.HANDLE),
                ('SequenceNumber', ctypes.c_uint),
                ('ReturnCode', comtypes.HRESULT),
    ]

class D3D11_AUTHENTICATED_CONFIGURE_INITIALIZE_INPUT(ctypes.Structure):
    _fields_ = [('Parameters', D3D11_AUTHENTICATED_CONFIGURE_INPUT),
                ('StartSequenceQuery', ctypes.c_uint),
                ('StartSequenceConfigure', ctypes.c_uint),
    ]

class D3D11_AUTHENTICATED_CONFIGURE_PROTECTION_INPUT(ctypes.Structure):
    _fields_ = [('Parameters', D3D11_AUTHENTICATED_CONFIGURE_INPUT),
                ('Protections', D3D11_AUTHENTICATED_PROTECTION_FLAGS)
    ]

class D3D11_AUTHENTICATED_CONFIGURE_CRYPTO_SESSION_INPUT(ctypes.Structure):
    _fields_ = [('Parameters', D3D11_AUTHENTICATED_CONFIGURE_INPUT),
                ('DecoderHandle', wintypes.HANDLE),
                ('CryptoSessionHandle', wintypes.HANDLE),
                ('DeviceHandle', wintypes.HANDLE),
    ]

class D3D11_AUTHENTICATED_CONFIGURE_SHARED_RESOURCE_INPUT(ctypes.Structure):
    _fields_ = [('Parameters', D3D11_AUTHENTICATED_CONFIGURE_INPUT),
                ('ProcessType', D3D11_AUTHENTICATED_PROCESS_IDENTIFIER_TYPE),
                ('ProcessHandle', wintypes.HANDLE),
                ('AllowAccess', ctypes.c_bool),
    ]

class D3D11_AUTHENTICATED_CONFIGURE_ACCESSIBLE_ENCRYPTION_INPUT(ctypes.Structure):
    _fields_ = [('Parameters', D3D11_AUTHENTICATED_CONFIGURE_INPUT),
                ('EncryptionGuid', comtypes.GUID),
    ]
 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  CryptoSession
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11CryptoSession(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{9B32F9AD-BDCC-40a6-A39D-D5C865845720}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetCryptoType", [
            ctypes.POINTER(comtypes.GUID),
            ]),
        comtypes.STDMETHOD(None, "GetDecoderProfile", [
            ctypes.POINTER(comtypes.GUID),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetCertificateSize", [
            ctypes.POINTER(ctypes.c_uint),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetCertificate", [
            ctypes.c_uint,
            ctypes.POINTER(wintypes.BYTE),
            ]),
        comtypes.STDMETHOD(None, "GetCryptoSessionHandle", [
            ctypes.POINTER(wintypes.HANDLE),
            ]),
    ]

D3D11_VDOV_DIMENSION = ctypes.c_uint
D3D11_VDOV_DIMENSION_UNKNOWN   = D3D11_VDOV_DIMENSION(0)
D3D11_VDOV_DIMENSION_TEXTURE2D = D3D11_VDOV_DIMENSION(1)

class D3D11_TEX2D_VDOV(ctypes.Structure):
    _fields_ = [('ArraySlice', ctypes.c_uint),
    ]

class D3D11_VIDEO_DECODER_OUTPUT_VIEW_DESC(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('Texture2D', D3D11_TEX2D_VDOV),
        ]
    _anonymous_ = ('i1',)
    _fields_ = [('DecodeProfile', comtypes.GUID),
                ('ViewDimension', D3D11_VDOV_DIMENSION),
                ('i1', _I1),
    ]

class ID3D11VideoDecoderOutputView(ID3D11View):
    _iid_ = comtypes.GUID("{C2931AEA-2A85-4f20-860F-FBA1FD256E18}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_VIDEO_DECODER_OUTPUT_VIEW_DESC),
            ])
    ]

D3D11_VPIV_DIMENSION = ctypes.c_uint
D3D11_VPIV_DIMENSION_UNKNOWN   = D3D11_VPIV_DIMENSION(0)
D3D11_VPIV_DIMENSION_TEXTURE2D = D3D11_VPIV_DIMENSION(1)

class D3D11_TEX2D_VPIV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('ArraySlice', ctypes.c_uint),
    ]

class D3D11_VIDEO_PROCESSOR_INPUT_VIEW_DESC(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('Texture2D', D3D11_TEX2D_VPIV),
        ]
    _anonymous_ = ('i1',)
    _fields_ = [('FourCC', ctypes.c_uint),
                ('ViewDimension', D3D11_VPIV_DIMENSION),
                ('i1', _I1),
    ]

class ID3D11VideoProcessorInputView(ID3D11View):
    _iid_ = comtypes.GUID("{11EC5A5F-51DC-4945-AB34-6E8C21300EA5}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_INPUT_VIEW_DESC),
            ]),
    ]

D3D11_VPOV_DIMENSION = ctypes.c_uint
D3D11_VPOV_DIMENSION_UNKNOWN = D3D11_VPOV_DIMENSION(0)
D3D11_VPOV_DIMENSION_TEXTURE2D = D3D11_VPOV_DIMENSION(1)
D3D11_VPOV_DIMENSION_TEXTURE2DARRAY = D3D11_VPOV_DIMENSION(2)

class D3D11_TEX2D_VPOV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
    ]

class D3D11_TEX2D_ARRAY_VPOV(ctypes.Structure):
    _fields_ = [('MipSlice', ctypes.c_uint),
                ('FirstArraySlice', ctypes.c_uint),
                ('ArraySize', ctypes.c_uint),
    ]

class D3D11_VIDEO_PROCESSOR_OUTPUT_VIEW_DESC(ctypes.Structure):
    class _I1(ctypes.Union):
        _fields_ = [('Texture2D', D3D11_TEX2D_VPOV),
                    ('Texture2DArray', D3D11_TEX2D_ARRAY_VPOV),
        ]
    _anonymous_ = ('i1',)
    _fields_ = [('ViewDimension', D3D11_VPOV_DIMENSION),
                ('i1', _I1),
    ]

class ID3D11VideoProcessorOutputView(ID3D11View):
    _iid_ = comtypes.GUID("{A048285E-25A9-4527-BD93-D68B68C44254}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [
            ctypes.POINTER(D3D11_VIDEO_PROCESSOR_OUTPUT_VIEW_DESC),
            ]),
    ]
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  VideoContext
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11VideoContext(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{61F21C45-3C0E-4a74-9CEA-67100D9AD5E4}")
    _methods_ = [
        # Decode
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDecoderBuffer", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "ReleaseDecoderBuffer", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "DecoderBeginFrame", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "DecoderEndFrame", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "SubmitDecoderBuffers", []),
        comtypes.STDMETHOD(APP_DEPRECATED_HRESULT, "DecoderExtension", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetOutputTargetRect", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetOutputBackgroundColor", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetOutputColorSpace", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetOutputAlphaFillMode", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetOutputConstriction", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetOutputStereoMode", []),
        comtypes.STDMETHOD(APP_DEPRECATED_HRESULT, "VideoProcessorSetOutputExtension", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetOutputTargetRect", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetOutputBackgroundColor", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetOutputColorSpace", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetOutputAlphaFillMode", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetOutputConstriction", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetOutputStereoMode", []),
        comtypes.STDMETHOD(APP_DEPRECATED_HRESULT, "VideoProcessorGetOutputExtension", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamFrameFormat", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamColorSpace", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamOutputRate", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamSourceRect", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamDestRect", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamAlpha", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamPalette", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamPixelAspectRatio", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamStereoFormat", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamAutoProcessingMode", []),
        comtypes.STDMETHOD(APP_DEPRECATED_HRESULT, "VideoProcessorSetStreamExtension", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamFrameFormat", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamColorSpace", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamOutputRate", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamSourceRect", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamDestRect", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamAlpha", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamPalette", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamPixelAspectRatio", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamLumaKey", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamStereoFormat", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamAutoProcessingMode", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamFilter", []),
        comtypes.STDMETHOD(APP_DEPRECATED_HRESULT, "VideoProcessorGetStreamExtension", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "VideoProcessorBlt", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "NegotiateCryptoSessionKeyExchange", []),
        comtypes.STDMETHOD(None, "EncryptionBlt", []),
        comtypes.STDMETHOD(None, "DecryptionBlt", []),
        comtypes.STDMETHOD(None, "StartSessionKeyRefresh", []),
        comtypes.STDMETHOD(None, "FinishSessionKeyRefresh", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetEncryptionBltKey", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "NegotiateAuthenticatedChannelKeyExchange", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "QueryAuthenticatedChannel", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "ConfigureAuthenticatedChannel", []),
        comtypes.STDMETHOD(None, "VideoProcessorSetStreamRotation", []),
        comtypes.STDMETHOD(None, "VideoProcessorGetStreamRotation", []),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Device
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11VideoDevice(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{10EC4D5B-975A-4689-B9E4-D0AAC30FE333}")
    _methods_ = [
    # Create*
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVideoDecoder", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVideoProcessor", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateAuthenticatedChannel", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateCryptoSession", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVideoDecoderOutputView", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVideoProcessorInputView", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVideoProcessorOutputView", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVideoProcessorEnumerator", []),
    # Check
        comtypes.STDMETHOD(ctypes.c_uint, "GetVideoDecoderProfileCount", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoDecoderProfile", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckVideoDecoderFormat", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoDecoderConfigCount", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetVideoDecoderConfig", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetContentProtectionCaps", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckCryptoKeyExchange", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateData", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateDataInterface", []),
    ]


## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  Device
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class ID3D11Device(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{db6f6ddb-ac77-4e88-8253-819df9bbf140}")
    _methods_ = [
    # Create
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateBuffer", [
            ctypes.POINTER(D3D11_BUFFER_DESC),
            ctypes.POINTER(D3D11_SUBRESOURCE_DATA),
            ctypes.POINTER(ctypes.POINTER(ID3D11Buffer)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateTexture1D", [
            ctypes.POINTER(D3D11_TEXTURE1D_DESC),
            ctypes.POINTER(D3D11_SUBRESOURCE_DATA),
            ctypes.POINTER(ctypes.POINTER(ID3D11Texture1D)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateTexture2D", [
            ctypes.POINTER(D3D11_TEXTURE2D_DESC),
            ctypes.POINTER(D3D11_SUBRESOURCE_DATA),
            ctypes.POINTER(ctypes.POINTER(ID3D11Texture2D)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateTexture3D", [
            ctypes.POINTER(D3D11_TEXTURE3D_DESC),
            ctypes.POINTER(D3D11_SUBRESOURCE_DATA),
            ctypes.POINTER(ctypes.POINTER(ID3D11Texture3D)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateShaderResourceView", [
            ctypes.POINTER(ID3D11Resource),
            ctypes.POINTER(D3D11_SHADER_RESOURCE_VIEW_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11ShaderResourceView)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateUnorderedAccessView", [
            ctypes.POINTER(ID3D11Resource),
            ctypes.POINTER(D3D11_UNORDERED_ACCESS_VIEW_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11RenderTargetView)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateRenderTargetView", [
            ctypes.POINTER(ID3D11Resource),
            ctypes.POINTER(D3D11_RENDER_TARGET_VIEW_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11RenderTargetView)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDepthStencilView", [
            ctypes.POINTER(ID3D11Resource),
            ctypes.POINTER(D3D11_DEPTH_STENCIL_VIEW_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11DepthStencilView)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateInputLayout", [
            ctypes.POINTER(D3D11_INPUT_ELEMENT_DESC),
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.POINTER(ID3D11InputLayout)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVertexShader", [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ID3D11ClassLinkage),
            ctypes.POINTER(ctypes.POINTER(ID3D11VertexShader)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateGeometryShader", [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ID3D11ClassLinkage),
            ctypes.POINTER(ctypes.POINTER(ID3D11GeometryShader)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateGeometryShaderWithStreamOutput", [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(D3D11_SO_DECLARATION_ENTRY),
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.POINTER(ID3D11ClassLinkage),
            ctypes.POINTER(ctypes.POINTER(ID3D11GeometryShader)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreatePixelShader", [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ID3D11ClassLinkage),
            ctypes.POINTER(ctypes.POINTER(ID3D11PixelShader)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateHullShader", [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ID3D11ClassLinkage),
            ctypes.POINTER(ctypes.POINTER(ID3D11HullShader)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDomainShader", [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ID3D11ClassLinkage),
            ctypes.POINTER(ctypes.POINTER(ID3D11DomainShader)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateComputeShader", [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ID3D11ClassLinkage),
            ctypes.POINTER(ctypes.POINTER(ID3D11ComputeShader)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateClassLinkage", [
            ctypes.POINTER(ctypes.POINTER(ID3D11ClassLinkage)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateBlendState", [
            ctypes.POINTER(D3D11_BLEND_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11BlendState)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDepthStencilState", [
            ctypes.POINTER(D3D11_DEPTH_STENCIL_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11DepthStencilState)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateRasterizerState", [
            ctypes.POINTER(D3D11_RASTERIZER_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11RasterizerState)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSamplerState", [
            ctypes.POINTER(D3D11_SAMPLER_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11SamplerState)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateQuery", [
            ctypes.POINTER(D3D11_QUERY_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11Query)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreatePredicate", [
            ctypes.POINTER(D3D11_QUERY_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11Predicate)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateCounter", [
            ctypes.POINTER(D3D11_COUNTER_DESC),
            ctypes.POINTER(ctypes.POINTER(ID3D11Counter)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDeferredContext", [
            ctypes.c_uint, # Reserved parameter; must be 0
            ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "OpenSharedResource", [
            wintypes.HANDLE,
            ctypes.POINTER(comtypes.GUID), # typedef GUID IID <=> typedef IID* REFIID; 
            ctypes.POINTER(ctypes.c_void_p),
            ]),
    # Check
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckFormatSupport", [
            DXGI_FORMAT,
            ctypes.POINTER(ctypes.c_uint),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckMultisampleQualityLevels", [
            DXGI_FORMAT,
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_uint),
            ]),
        comtypes.STDMETHOD(None, "CheckCounterInfo", [
            ctypes.POINTER(D3D11_COUNTER_INFO),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckCounter", [
            ctypes.POINTER(D3D11_COUNTER_DESC),
            ctypes.POINTER(D3D11_COUNTER_TYPE),
            ctypes.POINTER(ctypes.c_uint),
            wintypes.LPSTR,
            ctypes.POINTER(ctypes.c_uint),
            wintypes.LPSTR,
            ctypes.POINTER(ctypes.c_uint),
            wintypes.LPSTR,
            ctypes.POINTER(ctypes.c_uint),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckFeatureSupport", [
            D3D11_FEATURE,
            ctypes.c_void_p,
            ctypes.c_uint,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetPrivateData", [
            ctypes.POINTER(comtypes.GUID),
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_void_p,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateData", [
            ctypes.POINTER(comtypes.GUID),
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_void_p,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateDataInterface", [
            ctypes.POINTER(comtypes.GUID),
            ctypes.POINTER(comtypes.IUnknown),
            ]),

        comtypes.STDMETHOD(D3D_FEATURE_LEVEL, "GetFeatureLevel", []),
        comtypes.STDMETHOD(ctypes.c_uint, "GetCreationFlags", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDeviceRemovedReason", []),
        comtypes.STDMETHOD(None, "GetImmediateContext", [
            ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetExceptionMode", [
            ctypes.c_uint,
            ]),
        comtypes.STDMETHOD(ctypes.c_uint, "GetExceptionMode", []),
    ]

D3D11_CREATE_DEVICE_FLAG = ctypes.c_uint
D3D11_CREATE_DEVICE_SINGLETHREADED = D3D11_CREATE_DEVICE_FLAG(0x1)
D3D11_CREATE_DEVICE_DEBUG = D3D11_CREATE_DEVICE_FLAG(0x2)
D3D11_CREATE_DEVICE_SWITCH_TO_REF = D3D11_CREATE_DEVICE_FLAG(0x4)
D3D11_CREATE_DEVICE_PREVENT_INTERNAL_THREADING_OPTIMIZATIONS = D3D11_CREATE_DEVICE_FLAG(0x8)
D3D11_CREATE_DEVICE_BGRA_SUPPORT = D3D11_CREATE_DEVICE_FLAG(0x20)
D3D11_CREATE_DEVICE_DEBUGGABLE = D3D11_CREATE_DEVICE_FLAG(0x40)
D3D11_CREATE_DEVICE_PREVENT_ALTERING_LAYER_SETTINGS_FROM_REGISTRY = D3D11_CREATE_DEVICE_FLAG(0x0080)
D3D11_CREATE_DEVICE_DISABLE_GPU_TIMEOUT = D3D11_CREATE_DEVICE_FLAG(0x0100)
D3D11_CREATE_DEVICE_VIDEO_SUPPORT = D3D11_CREATE_DEVICE_FLAG(0x0800)

D3D11_SDK_VERSION = 7

## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## 
##  End of file
## 
## //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
