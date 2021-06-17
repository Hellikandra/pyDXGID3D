#Lib Tester
import ctypes 
import comtypes

## D3D11 Layer
from Direct3D.PyIdl.d3dcommon      import *
from Direct3D.PyIdl.d3d11          import *
## DXGI Layer
from Direct3D.PyIdl.dxgi           import *
from Direct3D.PyIdl.dxgi1_2        import *

## DXGI and D3D11 Debug Layer
from Direct3D.PyIdl.d3d11sdklayers import *
from Direct3D.PyIdl.dxgidebug      import *



## ########################################################
def main():
    swapchain  = ctypes.POINTER(IDXGISwapChain)()
    dev        = ctypes.POINTER(ID3D11Device)()
    devcon     = ctypes.POINTER(ID3D11DeviceContext)()
    
    backbuffer = ctypes.POINTER(ID3D11RenderTargetView)()

    scd = DXGI_SWAP_CHAIN_DESC()
    ctypes.memset(ctypes.byref(scd), 0, ctypes.sizeof(DXGI_SWAP_CHAIN_DESC))
    # # file the swap chain descriptor struct
    scd.BufferCount = 1
    scd.BufferDesc.Format = 87 # DXGI_FORMAT_B8G8R8A8_UNORM
    scd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT
    scd.OutputWindow = ctypes.windll.kernel32.GetConsoleWindow() # must be changed https://docs.microsoft.com/en-us/windows/console/getconsolewindow?redirectedfrom=MSDN
    scd.SampleDesc.Count = 4
    scd.Windowed = True

    FeatureLevels = [D3D_FEATURE_LEVEL_11_0.value, D3D_FEATURE_LEVEL_10_1.value, D3D_FEATURE_LEVEL_10_0.value, D3D_FEATURE_LEVEL_9_1.value]
    NumFeatureLevels = len(FeatureLevels)

    hr = ctypes.windll.d3d11.D3D11CreateDeviceAndSwapChain(
        None,                       # IDXGIAdapter                  *pAdapter
        D3D_DRIVER_TYPE_HARDWARE,   # D3D_DRIVER_TYPE               DriverType
        None,                       # HMODULE                       Software
        D3D11_CREATE_DEVICE_DEBUG,  # UINT                          Flags
        ctypes.byref((ctypes.c_uint * D3D11_SDK_VERSION)(*FeatureLevels)),                       # const D3D_FEATURE_LEVEL       *pFeatureLevels
        NumFeatureLevels,                       # UNIT                          FeatureLevels
        D3D11_SDK_VERSION,          # UINT                          SDKVersion
        scd,                        # const DXGI_SWAP_CHAIN_DESC    *pSwapChainDesc
        ctypes.byref(swapchain),    # IDXGISwapChain                **ppSwapChain
        ctypes.byref(dev),          # ID3D11Device                  **ppDevice
        None,                       # D3D_FEATURE_LEVEL             *pFeatureLevel
        ctypes.byref(devcon)        # ID3D11DeviceContext           **ppImmediateContext
        )
    hr = hex((hr + (1 << 64)) % (1 << 64))
    print(hr)

    d3dDebug = ctypes.POINTER(ID3D11Debug)()
    d3dDebug = dev.QueryInterface(ID3D11Debug, ID3D11Debug._iid_)
    print(d3dDebug)
    print(ctypes.byref(d3dDebug))
    d3dInfoQueue = ctypes.POINTER(ID3D11InfoQueue)
    d3dInfoQueue = d3dDebug.QueryInterface(ID3D11InfoQueue, ID3D11InfoQueue._iid_)
    print(d3dInfoQueue)
    
    print(D3D11_MESSAGE_SEVERITY_ERROR)
    d3dInfoQueue.SetBreakOnSeverity(D3D11_MESSAGE_SEVERITY_ERROR, True)
    hide = (ctypes.c_ulong*1)()
    print(hide)
    hide_cast = ctypes.cast(hide, ctypes.POINTER(ctypes.c_ulong))

    filter = D3D11_INFO_QUEUE_FILTER()
    filter.DenyList.NumIDs = len(hide)
    filter.DenyList.pIDList = hide_cast
    d3dInfoQueue.AddStorageFilterEntries(filter)


    # # get the address of the back buffer
    pBackBuffer = ctypes.POINTER(ID3D11Texture2D)()
    hr = swapchain.GetBuffer(0, ID3D11Texture2D._iid_, ctypes.byref(pBackBuffer))
    hr = hex((hr + (1 << 64)) % (1 << 64))
    print("swapchain.GetBuffer : ", hr)
    # # use the back buffer address to create the render target
    hr = dev.CreateRenderTargetView(pBackBuffer, None, ctypes.byref(backbuffer))
    #pBackBuffer.Release()
    hr = hex((hr + (1 << 64)) % (1 << 64))
    print(hr)
    # # set the render target as the back buffer
    devcon.OMSetRenderTargets(1, ctypes.byref(backbuffer), None)

    # # set the viewport
    viewport = D3D11_VIEWPORT()
    ctypes.memset(ctypes.byref(viewport), 0, ctypes.sizeof(D3D11_VIEWPORT))
    viewport.TopLeftX = 0 
    viewport.TopLeftY = 0
    viewport.Width = 800
    viewport.Height = 600
    try:
        devcon.RSSetViewports(1, ctypes.byref(viewport))
    except:
        print("error")
        d3dInfoQueue.ClearStoredMessages()
        d3dDebug.ReportLiveDeviceObjects(D3D11_RLDO_SUMMARY | D3D11_RLDO_DETAIL)
    # # Close and release all existing COM objects
    #swapchain.Release()
    #dev.Release()
    #devcon.Release()

if __name__ == '__main__':
    main()


## EOF