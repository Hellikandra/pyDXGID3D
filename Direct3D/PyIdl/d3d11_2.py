##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from d3d11_2.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py d3d11_2.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES



from Direct3D.PyIdl.dxgi1_3 import *
from Direct3D.PyIdl.d3dcommon import *
from Direct3D.PyIdl.d3d11_1 import *


## ---------------------------------------------- constants ----
D3D11_PACKED_TILE                              = 0xffffffff


## -------------------------------------------- enumerations ----

D3D11_CHECK_MULTISAMPLE_QUALITY_LEVELS_FLAG = ctypes.c_uint
D3D11_CHECK_MULTISAMPLE_QUALITY_LEVELS_TILED_RESOURCE = D3D11_CHECK_MULTISAMPLE_QUALITY_LEVELS_FLAG(0x00000001).value

D3D11_TILE_COPY_FLAG = ctypes.c_uint
D3D11_TILE_COPY_NO_OVERWRITE                             = D3D11_TILE_COPY_FLAG(0x00000001).value
D3D11_TILE_COPY_LINEAR_BUFFER_TO_SWIZZLED_TILED_RESOURCE = D3D11_TILE_COPY_FLAG(0x00000002).value
D3D11_TILE_COPY_SWIZZLED_TILED_RESOURCE_TO_LINEAR_BUFFER = D3D11_TILE_COPY_FLAG(0x00000004).value

D3D11_TILE_MAPPING_FLAG = ctypes.c_uint
D3D11_TILE_MAPPING_NO_OVERWRITE = D3D11_TILE_MAPPING_FLAG(0x00000001).value

D3D11_TILE_RANGE_FLAG = ctypes.c_uint
D3D11_TILE_RANGE_NULL              = D3D11_TILE_RANGE_FLAG(0x00000001).value
D3D11_TILE_RANGE_SKIP              = D3D11_TILE_RANGE_FLAG(0x00000002).value
D3D11_TILE_RANGE_REUSE_SINGLE_TILE = D3D11_TILE_RANGE_FLAG(0x00000004).value


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class ID3D11Device2(ID3D11Device1):
    _iid_ = comtypes.GUID("{9d06dffa-d1e5-4d07-83a8-1bb123f2f841}")


class ID3D11DeviceContext2(ID3D11DeviceContext1):
    _iid_ = comtypes.GUID("{420d5b32-b90c-4da4-bef0-359f6a24a83a}")


## ---------------------------------------------- structures ----


class D3D11_PACKED_MIP_DESC(ctypes.Structure):
    _fields_ = [('NumStandardMips',                 ctypes.c_uint8),
                ('NumPackedMips',                   ctypes.c_uint8),
                ('NumTilesForPackedMips',           ctypes.c_uint32),
                ('StartTileIndexInOverallResource', ctypes.c_uint32),
    ]


class D3D11_SUBRESOURCE_TILING(ctypes.Structure):
    _fields_ = [('WidthInTiles',                    ctypes.c_uint32),
                ('HeightInTiles',                   ctypes.c_uint16),
                ('DepthInTiles',                    ctypes.c_uint16),
                ('StartTileIndexInOverallResource', ctypes.c_uint32),
    ]


class D3D11_TILED_RESOURCE_COORDINATE(ctypes.Structure):
    _fields_ = [('X',           ctypes.c_uint32),
                ('Y',           ctypes.c_uint32),
                ('Z',           ctypes.c_uint32),
                ('Subresource', ctypes.c_uint32),
    ]


class D3D11_TILE_REGION_SIZE(ctypes.Structure):
    _fields_ = [('NumTiles', ctypes.c_uint32),
                ('bUseBox',  wintypes.BOOL),
                ('Width',    ctypes.c_uint32),
                ('Height',   ctypes.c_uint16),
                ('Depth',    ctypes.c_uint16),
    ]


class D3D11_TILE_SHAPE(ctypes.Structure):
    _fields_ = [('WidthInTexels',  ctypes.c_uint32),
                ('HeightInTexels', ctypes.c_uint32),
                ('DepthInTexels',  ctypes.c_uint32),
    ]


## ------------------------- vtables, assigned once every class exists ----

ID3D11Device2._methods_ = [
    comtypes.STDMETHOD(None, "GetImmediateContext2", [
        ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext2)), # ID3D11DeviceContext2** ppImmediateContext
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateDeferredContext2", [
        ctypes.c_uint32,                             # UINT ContextFlags
        ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext2)), # ID3D11DeviceContext2** ppDeferredContext
        ]),
    comtypes.STDMETHOD(None, "GetResourceTiling", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pTiledResource
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumTilesForEntireResource
        ctypes.POINTER(D3D11_PACKED_MIP_DESC),       # D3D11_PACKED_MIP_DESC* pPackedMipDesc
        ctypes.POINTER(D3D11_TILE_SHAPE),            # D3D11_TILE_SHAPE* pStandardTileShapeForNonPackedMips
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumSubresourceTilings
        ctypes.c_uint32,                             # UINT FirstSubresourceTilingToGet
        ctypes.POINTER(D3D11_SUBRESOURCE_TILING),    # D3D11_SUBRESOURCE_TILING* pSubresourceTilingsForNonPackedMips
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CheckMultisampleQualityLevels1", [
        DXGI_FORMAT,                                 # DXGI_FORMAT Format
        ctypes.c_uint32,                             # UINT SampleCount
        ctypes.c_uint32,                             # UINT Flags
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pNumQualityLevels
        ]),
]

ID3D11DeviceContext2._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "UpdateTileMappings", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pTiledResource
        ctypes.c_uint32,                             # UINT NumTiledResourceRegions
        ctypes.POINTER(D3D11_TILED_RESOURCE_COORDINATE), # D3D11_TILED_RESOURCE_COORDINATE* pTiledResourceRegionStartCoordinates
        ctypes.POINTER(D3D11_TILE_REGION_SIZE),      # D3D11_TILE_REGION_SIZE* pTiledResourceRegionSizes
        ctypes.POINTER(ID3D11Buffer),                # ID3D11Buffer* pTilePool
        ctypes.c_uint32,                             # UINT NumRanges
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pRangeFlags
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pTilePoolStartOffsets
        ctypes.POINTER(ctypes.c_uint32),             # UINT* pRangeTileCounts
        ctypes.c_uint32,                             # UINT Flags
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CopyTileMappings", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pDestTiledResource
        ctypes.POINTER(D3D11_TILED_RESOURCE_COORDINATE), # D3D11_TILED_RESOURCE_COORDINATE* pDestRegionStartCoordinate
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pSourceTiledResource
        ctypes.POINTER(D3D11_TILED_RESOURCE_COORDINATE), # D3D11_TILED_RESOURCE_COORDINATE* pSourceRegionStartCoordinate
        ctypes.POINTER(D3D11_TILE_REGION_SIZE),      # D3D11_TILE_REGION_SIZE* pTileRegionSize
        ctypes.c_uint32,                             # UINT Flags
        ]),
    comtypes.STDMETHOD(None, "CopyTiles", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pTiledResource
        ctypes.POINTER(D3D11_TILED_RESOURCE_COORDINATE), # D3D11_TILED_RESOURCE_COORDINATE* pTileRegionStartCoordinate
        ctypes.POINTER(D3D11_TILE_REGION_SIZE),      # D3D11_TILE_REGION_SIZE* pTileRegionSize
        ctypes.POINTER(ID3D11Buffer),                # ID3D11Buffer* pBuffer
        ctypes.c_uint64,                             # UINT64 BufferStartOffsetInBytes
        ctypes.c_uint32,                             # UINT Flags
        ]),
    comtypes.STDMETHOD(None, "UpdateTiles", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pDestTiledResource
        ctypes.POINTER(D3D11_TILED_RESOURCE_COORDINATE), # D3D11_TILED_RESOURCE_COORDINATE* pDestTileRegionStartCoordinate
        ctypes.POINTER(D3D11_TILE_REGION_SIZE),      # D3D11_TILE_REGION_SIZE* pDestTileRegionSize
        ctypes.c_void_p,                             # void* pSourceTileData
        ctypes.c_uint32,                             # UINT Flags
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "ResizeTilePool", [
        ctypes.POINTER(ID3D11Buffer),                # ID3D11Buffer* pTilePool
        ctypes.c_uint64,                             # UINT64 NewSizeInBytes
        ]),
    comtypes.STDMETHOD(None, "TiledResourceBarrier", [
        ctypes.POINTER(ID3D11DeviceChild),           # ID3D11DeviceChild* pTiledResourceOrViewAccessBeforeBarrier
        ctypes.POINTER(ID3D11DeviceChild),           # ID3D11DeviceChild* pTiledResourceOrViewAccessAfterBarrier
        ]),
    comtypes.STDMETHOD(wintypes.BOOL, "IsAnnotationEnabled", []),
    comtypes.STDMETHOD(None, "SetMarkerInt", [
        ctypes.c_wchar_p,                            # LPCWSTR pLabel
        ctypes.c_int32,                              # INT Data
        ]),
    comtypes.STDMETHOD(None, "BeginEventInt", [
        ctypes.c_wchar_p,                            # LPCWSTR pLabel
        ctypes.c_int32,                              # INT Data
        ]),
    comtypes.STDMETHOD(None, "EndEvent", []),
]


## -- End Of File --
