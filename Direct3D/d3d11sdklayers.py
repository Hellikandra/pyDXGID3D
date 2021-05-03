## ////////////////////////////////////////////////////////////////////////////////////////////
##                                                                                           
##  D3D11SDKLayers.idl
##                                                                                           
##  Contains interface definitions for the D3D11 SDK Layers .                                
##                                                                                           
##  Copyright (c) Microsoft Corporation.                                                     
##                                                                                           
## ////////////////////////////////////////////////////////////////////////////////////////////
import ctypes
import ctypes.wintypes as wintypes

import comtypes

D3D11_SDK_LAYER_VERSION = 1

## ==================================================================================================================================
## 
##  Debugging Layer
## 
## ==================================================================================================================================
D3D11_DEBUG_FEATURE_FLUSH_PER_RENDER_OP = 0x1
D3D11_DEBUG_FEATURE_FINISH_PER_RENDER_OP = 0x2
D3D11_DEBUG_FEATURE_PRESENT_PER_RENDER_OP = 0x4
D3D11_DEBUG_FEATURE_ALWAYS_DISCARD_OFFERED_RESOURCE = 0x8
D3D11_DEBUG_FEATURE_NEVER_DISCARD_OFFERED_RESOURCE = 0x10
D3D11_DEBUG_FEATURE_AVOID_BEHAVIOR_CHANGING_DEBUG_AIDS = 0x40
D3D11_DEBUG_FEATURE_DISABLE_TILED_RESOURCE_MAPPING_TRACKING_AND_VALIDATION = 0x80

D3D11_RLDO_FLAGS = ctypes.c_uint
D3D11_RLDO_SUMMARY = D3D11_RLDO_FLAGS(0x1)
D3D11_RLDO_DETAIL = D3D11_RLDO_FLAGS(0x2)
D3D11_RLDO_IGNORE_INTERNAL = D3D11_RLDO_FLAGS(0x4)

class ID3D11Debug(comtypes.IUnknown):
	_iid_ = comtypes.GUID("{79CF2233-7536-4948-9D36-1E4692DC5760}")
	_mehtods_ = [
		comtypes.STDMETHOD(comtypes.HRESULT,"SetFeatureMask", []),
		comtypes.STDMETHOD(ctypes.c_uint,"GetFeatureMask",[])
		comtypes.STDMETHOD(comtypes.HRESULT,"SetPresentPerRenderOpDelay",[])
		comtypes.STDMETHOD(ctypes.c_uint,"GetPresentPerRenderOpDelay",[])
		comtypes.STDMETHOD(comtypes.HRESULT,"SetSwapChain",[])
		comtypes.STDMETHOD(comtypes.HRESULT,"GetSwapChain",[])
		comtypes.STDMETHOD(comtypes.HRESULT,"ValidateContext",[])
		comtypes.STDMETHOD(comtypes.HRESULT,"ReportLiveDeviceObjects",[])
		comtypes.STDMETHOD(comtypes.HRESULT,"ValidateContextForDispatch",[])
	]

class ID3D11SwitchToRef(comtypes.IUnknown):
	_iid_ = comtypes.GUID("{1EF337E3-58E7-4F83-A692-DB221F5ED47E}")
	_mehtods_ = [
		comtypes.STDMETHOD(ctypes.wintypes.BOOL,"SetUseRef", [])
		comtypes.STDMETHOD(ctypes.wintypes.BOOL,"GetUseRef", [])
	]

D3D11_SHADER_TRACKING_RESOURCE_TYPE = ctypes.c_uint
D3D11_SHADER_TRACKING_RESOURCE_TYPE_NONE = 0                  # call has no effect
D3D11_SHADER_TRACKING_RESOURCE_TYPE_UAV_DEVICEMEMORY = 1      # call affects device memory created with UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_NON_UAV_DEVICEMEMORY = 2  # call affects device memory created without UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_ALL_DEVICEMEMORY = 3      # call affects all device memory
D3D11_SHADER_TRACKING_RESOURCE_TYPE_GROUPSHARED_MEMORY = 4    # call affects all shaders that use group shared memory created
D3D11_SHADER_TRACKING_RESOURCE_TYPE_ALL_SHARED_MEMORY = 5     # call affects everything except device memory created without UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_GROUPSHARED_NON_UAV = 6   # call affects everything except device memory created with UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_ALL = 7                   # call affects all memory on the device