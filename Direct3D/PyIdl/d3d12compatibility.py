##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from d3d12compatibility.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py d3d12compatibility.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES



from Direct3D.PyIdl.d3d11on12 import *


## -------------------------------------------- enumerations ----

D3D12_COMPATIBILITY_SHARED_FLAGS = ctypes.c_uint
D3D12_COMPATIBILITY_SHARED_FLAG_NONE          = D3D12_COMPATIBILITY_SHARED_FLAGS(0).value
D3D12_COMPATIBILITY_SHARED_FLAG_NON_NT_HANDLE = D3D12_COMPATIBILITY_SHARED_FLAGS(0x1).value
D3D12_COMPATIBILITY_SHARED_FLAG_KEYED_MUTEX   = D3D12_COMPATIBILITY_SHARED_FLAGS(0x2).value
D3D12_COMPATIBILITY_SHARED_FLAG_9_ON_12       = D3D12_COMPATIBILITY_SHARED_FLAGS(0x4).value

D3D12_REFLECT_SHARED_PROPERTY = ctypes.c_uint
D3D12_REFLECT_SHARED_PROPERTY_D3D11_RESOURCE_FLAGS       = D3D12_REFLECT_SHARED_PROPERTY().value
D3D12_REFELCT_SHARED_PROPERTY_COMPATIBILITY_SHARED_FLAGS = D3D12_REFLECT_SHARED_PROPERTY().value
D3D12_REFLECT_SHARED_PROPERTY_NON_NT_SHARED_HANDLE       = D3D12_REFLECT_SHARED_PROPERTY().value


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class ID3D12CompatibilityDevice(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{8f1c0e3c-fae3-4a82-b098-bfe1708207ff}")


## ------------------------- vtables, assigned once every class exists ----

ID3D12CompatibilityDevice._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateSharedResource", [
        ctypes.POINTER(D3D12_HEAP_PROPERTIES),       # D3D12_HEAP_PROPERTIES* pHeapProperties
        D3D12_HEAP_FLAGS,                            # D3D12_HEAP_FLAGS HeapFlags
        ctypes.POINTER(D3D12_RESOURCE_DESC),         # D3D12_RESOURCE_DESC* pDesc
        D3D12_RESOURCE_STATES,                       # D3D12_RESOURCE_STATES InitialResourceState
        ctypes.POINTER(D3D12_CLEAR_VALUE),           # D3D12_CLEAR_VALUE* pOptimizedClearValue
        ctypes.POINTER(D3D11_RESOURCE_FLAGS),        # D3D11_RESOURCE_FLAGS* pFlags11
        D3D12_COMPATIBILITY_SHARED_FLAGS,            # D3D12_COMPATIBILITY_SHARED_FLAGS CompatibilityFlags
        ctypes.POINTER(ID3D12LifetimeTracker),       # ID3D12LifetimeTracker* pLifetimeTracker
        ctypes.POINTER(ID3D12SwapChainAssistant),    # ID3D12SwapChainAssistant* pOwningSwapchain
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppResource
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "CreateSharedHeap", [
        ctypes.POINTER(D3D12_HEAP_DESC),             # D3D12_HEAP_DESC* pHeapDesc
        D3D12_COMPATIBILITY_SHARED_FLAGS,            # D3D12_COMPATIBILITY_SHARED_FLAGS CompatibilityFlags
        comtypes.GUID,                               # REFIID riid
        ctypes.POINTER(ctypes.c_void_p),             # void** ppHeap
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "ReflectSharedProperties", [
        ctypes.POINTER(ID3D12Object),                # ID3D12Object* pHeapOrResource
        D3D12_REFLECT_SHARED_PROPERTY,               # D3D12_REFLECT_SHARED_PROPERTY ReflectType
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
]


## -- End Of File --
