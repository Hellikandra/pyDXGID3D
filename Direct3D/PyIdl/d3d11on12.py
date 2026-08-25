##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from d3d11on12.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py d3d11on12.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES



from Direct3D.PyIdl.d3d11 import *
from Direct3D.PyIdl.d3d12 import *


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class ID3D11On12Device(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{85611e73-70a9-490e-9614-a9e302777904}")


class ID3D11On12Device1(ID3D11On12Device):
    _iid_ = comtypes.GUID("{bdb64df4-ea2f-4c70-b861-aaab1258bb5d}")


class ID3D11On12Device2(ID3D11On12Device1):
    _iid_ = comtypes.GUID("{dc90f331-4740-43fa-866e-67f12cb58223}")


## ---------------------------------------------- structures ----


class D3D11_RESOURCE_FLAGS(ctypes.Structure):
    _fields_ = [('BindFlags',           ctypes.c_uint32),
                ('MiscFlags',           ctypes.c_uint32),
                ('CPUAccessFlags',      ctypes.c_uint32),
                ('StructureByteStride', ctypes.c_uint32),
    ]


## ------------------------- vtables, assigned once every class exists ----

ID3D11On12Device._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateWrappedResource", [
        ctypes.POINTER(comtypes.IUnknown),           # IUnknown* pResource12
        ctypes.POINTER(D3D11_RESOURCE_FLAGS),        # D3D11_RESOURCE_FLAGS* pFlags11
        D3D12_RESOURCE_STATES,                       # D3D12_RESOURCE_STATES InState
        D3D12_RESOURCE_STATES,                       # D3D12_RESOURCE_STATES OutState
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppResource11
        ]),
    comtypes.STDMETHOD(None, "ReleaseWrappedResources", [
        ctypes.POINTER(ctypes.POINTER(ID3D11Resource)), # ID3D11Resource** ppResources
        ctypes.c_uint32,                             # UINT NumResources
        ]),
    comtypes.STDMETHOD(None, "AcquireWrappedResources", [
        ctypes.POINTER(ctypes.POINTER(ID3D11Resource)), # ID3D11Resource** ppResources
        ctypes.c_uint32,                             # UINT NumResources
        ]),
]

ID3D11On12Device1._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "GetD3D12Device", [
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppvDevice
        ]),
]

ID3D11On12Device2._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "UnwrapUnderlyingResource", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pResource11
        ctypes.POINTER(ID3D12CommandQueue),          # ID3D12CommandQueue* pCommandQueue
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppvResource12
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "ReturnUnderlyingResource", [
        ctypes.POINTER(ID3D11Resource),              # ID3D11Resource* pResource11
        ctypes.c_uint32,                             # UINT NumSync
        ctypes.POINTER(ctypes.c_uint64),             # UINT64* pSignalValues
        ctypes.POINTER(ctypes.POINTER(ID3D12Fence)), # ID3D12Fence** ppFences
        ]),
]


## -- End Of File --
