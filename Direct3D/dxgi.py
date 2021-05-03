import ctypes
import ctypes.wintypes as wintypes

import comtypes


import PyIdl.dxgicommon
import PyIdl.dxgiformat
import PyIdl.dxgitype

## --------------------------------------------------------------------------------------------------------
##  DXGI API-only types
## --------------------------------------------------------------------------------------------------------


# DXGI_USAGE
# Flags for surface and resource creation options.
# Each flag is defined as an unsigned integer (typedef UINT DXGI_USAGE)
DXGI_USAGE = ctypes.c_uint
DXGI_CPU_ACCESS_NONE       = 0
DXGI_CPU_ACCESS_DYNAMIC    = 1
DXGI_CPU_ACCESS_READ_WRITE = 2
DXGI_CPU_ACCESS_SCRATCH    = 3
DXGI_CPU_ACCESS_FIELD      = 15
DXGI_USAGE_SHADER_INPUT         = ( 1 << (0 + 4) )
DXGI_USAGE_RENDER_TARGET_OUTPUT = ( 1 << (1 + 4) )
DXGI_USAGE_BACK_BUFFER          = ( 1 << (2 + 4) )
DXGI_USAGE_SHARED               = ( 1 << (3 + 4) )
DXGI_USAGE_READ_ONLY            = ( 1 << (4 + 4) )
DXGI_USAGE_DISCARD_ON_PRESENT   = ( 1 << (5 + 4) )
DXGI_USAGE_UNORDERED_ACCESS     = ( 1 << (6 + 4) )

DXGI_USAGE_REMOTE_SWAPCHAIN_BUFER = ( 1 << (15 + 4) )
DXGI_USAGE_GDI_COMPATIBLE         = ( 1 << (16 + 4) )
# 1L = long int (C11, $6.4.4.1)
# 0L = 0 in long format
# ### Represents a rational number.  #


class DXGI_FRAME_STATISTICS(ctypes.Structure):
    _fields_ = [('PresentCount', ctypes.c_uint),
                ('PresentRefreshCount', ctypes.c_uint),
                ('SyncRefreshCount', ctypes.c_uint),
                ('SyncQPCTime',wintypes.LARGE_INTEGER),
                ('SyncGPUTime',wintypes.LARGE_INTEGER),
    ]


class DXGI_MAPPED_RECT(ctypes.Structure):
    _fields_ = [('Pitch', ctypes.c_int),
                ('pBits',ctypes.POINTER(wintypes.BYTE)),
    ]


class LUID(ctypes.Structure):
    _fields_ = [("LowPart", wintypes.DWORD), 
                ("HighPart", wintypes.LONG),
    ]


class DXGI_ADAPTER_DESC(ctypes.Structure):
    _fields_ = [('Description', wintypes.WCHAR * 128),
                ('VendorId', ctypes.c_uint),
                ('DeviceId', ctypes.c_uint),
                ('SubSysId', ctypes.c_uint),
                ('Revision', ctypes.c_uint),
                ('DedicatedVideoMemory', wintypes.ULARGE_INTEGER),
                ('DedicatedSystemMemory', wintypes.ULARGE_INTEGER),
                ('SharedSystemMemory', wintypes.ULARGE_INTEGER),
                ('AdapterLuid', LUID),
    ]

class DXGI_OUTPUT_DESC(ctypes.Structure):
    _fields_ = [('DeviceName', wintypes.WCHAR * 32),
                ('DesktopCoordinates', wintypes.RECT),
                ('AttachedToDesktop', wintypes.BOOL),
                ('Rotation', PyIdl.dxgitype.DXGI_MODE_ROTATION),
                ('Monitor', wintypes.HMONITOR)
    ]


class DXGI_SHARED_RESOURCE(ctypes.Structure):
    _fields_ = [('Handle', wintypes.HANDLE),
    ]


DXGI_RESOURCE_PRIORITY_MINIMUM = 0x28000000
DXGI_RESOURCE_PRIORITY_LOW     = 0x50000000
DXGI_RESOURCE_PRIORITY_NORMAL  = 0x78000000
DXGI_RESOURCE_PRIORITY_HIGH    = 0xa0000000
DXGI_RESOURCE_PRIORITY_MAXIMUM = 0xc8000000


DXGI_RESIDENCY = ctypes.c_uint
DXGI_RESIDENCY_FULLY_RESIDENT            = DXGI_RESIDENCY(1)
DXGI_RESIDENCY_RESIDENT_IN_SHARED_MEMORY = DXGI_RESIDENCY(2)
DXGI_RESIDENCY_EVICTED_TO_DISK           = DXGI_RESIDENCY(3)


DXGI_SWAP_EFFECT = ctypes.c_uint
DXGI_SWAP_EFFECT_DISCARD         = DXGI_SWAP_EFFECT(0)
DXGI_SWAP_EFFECT_SEQUENTIAL      = DXGI_SWAP_EFFECT(1)
DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL = DXGI_SWAP_EFFECT(3)
DXGI_SWAP_EFFECT_FLIP_DISCARD    = DXGI_SWAP_EFFECT(4)


DXGI_SWAP_CHAIN_FLAG = ctypes.c_uint
DXGI_SWAP_CHAIN_FLAG_NONPREROTATED                          = DXGI_SWAP_CHAIN_FLAG(1)
DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH                      = DXGI_SWAP_CHAIN_FLAG(2)
DXGI_SWAP_CHAIN_FLAG_GDI_COMPATIBLE                         = DXGI_SWAP_CHAIN_FLAG(4)
DXGI_SWAP_CHAIN_FLAG_RESTRICTED_CONTENT                     = DXGI_SWAP_CHAIN_FLAG(8)
DXGI_SWAP_CHAIN_FLAG_RESTRICT_SHARED_RESOURCE_DRIVER        = DXGI_SWAP_CHAIN_FLAG(16)
DXGI_SWAP_CHAIN_FLAG_DISPLAY_ONLY                           = DXGI_SWAP_CHAIN_FLAG(32)
DXGI_SWAP_CHAIN_FLAG_FRAME_LATENCY_WAITABLE_OBJECT          = DXGI_SWAP_CHAIN_FLAG(64)
DXGI_SWAP_CHAIN_FLAG_FOREGROUND_LAYER                       = DXGI_SWAP_CHAIN_FLAG(128)
DXGI_SWAP_CHAIN_FLAG_FULLSCREEN_VIDEO                       = DXGI_SWAP_CHAIN_FLAG(256)
DXGI_SWAP_CHAIN_FLAG_YUV_VIDEO                              = DXGI_SWAP_CHAIN_FLAG(512)
DXGI_SWAP_CHAIN_FLAG_HW_PROTECTED                           = DXGI_SWAP_CHAIN_FLAG(1024)
DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING                          = DXGI_SWAP_CHAIN_FLAG(2048)
DXGI_SWAP_CHAIN_FLAG_RESTRICTED_TO_ALL_HOLOGRAPHIC_DISPLAYS = DXGI_SWAP_CHAIN_FLAG(4096)


class DXGI_SWAP_CHAIN_DESC(ctypes.Structure):
    _fields_ = [('BufferDesc', PyIdl.dxgitype.DXGI_MODE_DESC),
                ('SampleDesc', PyIdl.dxgicommon.DXGI_SAMPLE_DESC),
                ('BufferUsage', DXGI_USAGE),
                ('BufferCount', ctypes.c_uint),
                ('OutputWindow', wintypes.HWND),
                ('Windowed', wintypes.BOOL),
                ('SwapEffect', DXGI_SWAP_EFFECT),
                ('Flags', ctypes.c_uint), # DXGI_SWAP_CHAIN_FLAG
    ]


## --------------------------------------------------------------------------------------------------------
##  DXGI object hierarchy base interfaces
## --------------------------------------------------------------------------------------------------------
class IDXGIObject(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{aec22fb8-76f3-4639-9be0-28eb43a67a2e}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateData", 
            [comtypes.GUID,
            ctypes.c_uint,
            ctypes.c_void_p
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateDataInterface",
            [comtypes.GUID, # REFGUID        Name
            ctypes.c_void_p # const IUnknown *pUnknown
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetPrivateData",
            [comtypes.GUID, 
            ctypes.c_uint, 
            ctypes.c_void_p
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetParent",
            [comtypes.GUID,
            ctypes.POINTER(ctypes.c_void_p)
            ]),
    ]


class IDXGIDeviceSubObject(IDXGIObject):
    _iid_ = comtypes.GUID("{3d3e0379-f9de-4d58-bb6c-18d62992f1a6}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDevice",
            [comtypes.GUID,
            ctypes.POINTER(ctypes.c_void_p)
            ]),
    ]


class IDXGIResource(IDXGIDeviceSubObject):
    _iid_ = comtypes.GUID("{035f3ab4-482e-4e50-b41f-8a7f8bd8960b}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetSharedHandle"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetUsage"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetEvictionPriority"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetEvictionPriority"),
    ]


class IDXGIKeyedMutex(IDXGIDeviceSubObject):
    _iid_ = comtypes.GUID("{9d8e1289-d7b3-465f-8126-250e349af85d}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "AcquireSync"),
        comtypes.STDMETHOD(comtypes.HRESULT, "ReleaseSync"),
    ]

DXGI_MAP_READ    = 1 # 1UL
DXGI_MAP_WRITE   = 2 # 2UL
DXGI_MAP_DISCARD = 4 # 3UL

class IDXGISurface(IDXGIDeviceSubObject):
    _iid_ = comtypes.GUID("{cafcb56c-6ac3-4889-bf47-9e23bbd260ec}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc"),
        comtypes.STDMETHOD(comtypes.HRESULT, "Map"),
        comtypes.STDMETHOD(comtypes.HRESULT, "Unmap"),
    ]


class IDXGISurface1(IDXGISurface):
    _iid_ = comtypes.GUID("{4AE63092-6327-4c1b-80AE-BFE12EA32B86}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDC"),
        comtypes.STDMETHOD(comtypes.HRESULT, "ReleaseDC"),
    ]

class IDXGIAdapter(IDXGIObject):
    _iid_ = comtypes.GUID("{2411e7e1-12ac-4ccf-bd14-9798e8534dc0}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "EnumOutputs"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc",
            [ctypes.POINTER(DXGI_ADAPTER_DESC)]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckInterfaceSupport"),
    ]

DXGI_ENUM_MODES_INTERLACED = 1 # 1UL
DXGI_ENUM_MODES_SCALING    = 2 # 2UL

class IDXGIOutput(IDXGIObject):
    _iid_ = comtypes.GUID()
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDisplayModeList", [
            PyIdl.dxgiformat.DXGI_FORMAT,
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_uint),
            ctypes.POINTER(PyIdl.dxgitype.DXGI_MODE_DESC),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "FindClosesMatchingMode"),
        comtypes.STDMETHOD(comtypes.HRESULT, "WaitForVBlank"),
        comtypes.STDMETHOD(comtypes.HRESULT, "TakeOwnerShip"),
        comtypes.STDMETHOD(None, "ReleaseOwnership"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetGammaControlCapabilities"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetGammaControl"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetGammaControl"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetDisplaySurface"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDisplaySurfaceData"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetFrameStatistics"),
    ]

DXGI_MAX_SWAP_CHAIN_BUFFERS = 16
DXGI_PRESENT_TEST                  = 1   # 0x00000001UL" )
DXGI_PRESENT_DO_NOT_SEQUENCE       = 2   # 0x00000002UL" )
DXGI_PRESENT_RESTART               = 4   # 0x00000004UL" )
DXGI_PRESENT_DO_NOT_WAIT           = 8   # 0x00000008UL" )
DXGI_PRESENT_STEREO_PREFER_RIGHT   = 10  # 0x00000010UL" )
DXGI_PRESENT_STEREO_TEMPORARY_MONO = 20  # 0x00000020UL" )
DXGI_PRESENT_RESTRICT_TO_OUTPUT    = 40  # 0x00000040UL" )
DXGI_PRESENT_DDA_PROTECTED_CONTENT = 80  # 0x00000080UL" ) reserved
DXGI_PRESENT_USE_DURATION          = 100 # 0x00000100UL" )
DXGI_PRESENT_ALLOW_TEARING         = 200 # 0x00000200UL" )

class IDXGISwapChain(IDXGIDeviceSubObject):
    _iid_ = comtypes.GUID("{310d36a0-d2e7-4c0a-aa04-6a9d23b8886a}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "Present", [
            ctypes.c_uint,
            ctypes.c_uint,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetBuffer", [
            ctypes.c_uint,
            ctypes.POINTER(comtypes.GUID),
            ctypes.POINTER(ctypes.c_void_p),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetFullscreenState",[
            ctypes.wintypes.BOOL,
            ctypes.POINTER(IDXGIOutput),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetFullscreenState", [
            ctypes.POINTER(ctypes.wintypes.BOOL),
            ctypes.POINTER(ctypes.POINTER(IDXGIOutput)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc"),
        comtypes.STDMETHOD(comtypes.HRESULT, "ResizeBuffers", [
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            PyIdl.dxgiformat.DXGI_FORMAT,
            ctypes.c_uint,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "ResizeTarget", [
            ctypes.POINTER(PyIdl.dxgitype.DXGI_MODE_DESC),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetContainingOutput", [
            ctypes.POINTER(ctypes.POINTER(IDXGIOutput)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetFrameStatistics"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetLastPresentCount"),
    ]

DXGI_MWA_NO_WINDOW_CHANGES = ( 1 << 0 )
DXGI_MWA_NO_ALT_ENTER      = ( 1 << 1 )
DXGI_MWA_NO_PRINT_SCREEN   = ( 1 << 2 )
DXGI_MWA_VALID             = 0x7

class IDXGIFactory(IDXGIObject):
    _iid_ = comtypes.GUID("{7b7166ec-21c7-44ae-b21a-c9ae321ae369}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "EnumAdapters",
            [ctypes.c_uint, ctypes.POINTER(ctypes.POINTER(IDXGIAdapter))]),
        comtypes.STDMETHOD(comtypes.HRESULT, "MakeWindowAssociation"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetWindowAssociation"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSwapChain"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSoftwareAdapter"),
    ]

class IDXGIDevice(IDXGIObject):
    _iid_ = comtypes.GUID("{54ec77fa-1377-44e6-8c32-88fd5f44c84c}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetAdapter"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSurface"),
        comtypes.STDMETHOD(comtypes.HRESULT, "QueryResourceResidency"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetGPUThreadPriority"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetGPUThreadPriority"),
    ]


## --------------------------------------------------------------------------------------------------------
##  DXGI 1.1
## --------------------------------------------------------------------------------------------------------

DXGI_ADAPTER_FLAG = ctypes.c_uint
DXGI_ADAPTER_FLAG_NONE        = DXGI_ADAPTER_FLAG(0)
DXGI_ADAPTER_FLAG_REMOTE      = DXGI_ADAPTER_FLAG(1)
DXGI_ADAPTER_FLAG_SOFTWARE    = DXGI_ADAPTER_FLAG(2)
DXGI_ADAPTER_FLAG_FORCE_DWORD = DXGI_ADAPTER_FLAG(0xFFFFFFFF)

class DXGI_ADAPTER_DESC1(ctypes.Structure):
    _fields_ = [('Description', wintypes.WCHAR * 128),
                ('VendorId', ctypes.c_uint),
                ('DeviceId', ctypes.c_uint),
                ('SubSysId', ctypes.c_uint),
                ('Revision', ctypes.c_uint),
                ('DedicatedVideoMemory', wintypes.ULARGE_INTEGER),
                ('DedicatedSystemMemory', wintypes.ULARGE_INTEGER),
                ('SharedSystemMemory', wintypes.ULARGE_INTEGER),
                ('AdapterLuid', LUID),
                ('Flags', ctypes.c_uint),
    ]

class DXGI_DISPLAY_COLOR_SPACE(ctypes.Structure):
    _fields_ = [('PrimaryCoordinates', (ctypes.c_float * 8) * 2),
                ('WhitePoints', (ctypes.c_float * 16) * 2),
    ]

class IDXGIFactory1(IDXGIFactory):
    _iid_ = comtypes.GUID("{770aae78-f26f-4dba-a829-253c83d1b387}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "EnumAdapters1"),
        comtypes.STDMETHOD(wintypes.BOOL, "IsCurrent"),
    ]

class IDXGIAdapter1(IDXGIAdapter):
    _iid_ = comtypes.GUID("{29038f61-3839-4626-91fd-086879011a05}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc1"),
    ]

class IDXGIDevice1(IDXGIDevice):
    _iid_ = comtypes.GUID("{77db970f-6276-48ba-ba28-070143b4392c}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "SetMaximumFrameltency"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetMaximumFrameltency"),
    ]


####### END OF FILE #######