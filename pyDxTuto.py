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
    scd.BufferUsage = 32
    scd.OutputWindow = ctypes.windll.kernel32.GetConsoleWindow() # must be changed https://docs.microsoft.com/en-us/windows/console/getconsolewindow?redirectedfrom=MSDN
    scd.SampleDesc.Count = 4
    scd.Windowed = True

    FeatureLevels = [D3D_FEATURE_LEVEL_11_0.value, D3D_FEATURE_LEVEL_10_1.value, D3D_FEATURE_LEVEL_10_0.value]
    NumFeatureLevels = len(FeatureLevels)

    hr = ctypes.windll.d3d11.D3D11CreateDeviceAndSwapChain(
        None,                       # IDXGIAdapter                  *pAdapter
        D3D_DRIVER_TYPE_HARDWARE,   # D3D_DRIVER_TYPE               DriverType
        None,                       # HMODULE                       Software
        D3D11_CREATE_DEVICE_DEBUG, #D3D11_CREATE_DEVICE_DEBUG,  # UINT                          Flags
        ctypes.byref((ctypes.c_uint * D3D11_SDK_VERSION)(*FeatureLevels)),                       # const D3D_FEATURE_LEVEL       *pFeatureLevels
        NumFeatureLevels,                       # UNIT                          FeatureLevels
        D3D11_SDK_VERSION,          # UINT                          SDKVersion
        ctypes.byref(scd),                        # const DXGI_SWAP_CHAIN_DESC    *pSwapChainDesc
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

    # # get the address of the back buffer
    pBackBuffer = ctypes.POINTER(ID3D11Texture2D)()
    print(pBackBuffer)
    hr = swapchain.GetBuffer(0, ID3D11Texture2D._iid_, ctypes.byref(pBackBuffer))
    print(pBackBuffer)
    hr = hex((hr + (1 << 64)) % (1 << 64))
    print("swapchain.GetBuffer : ", hr)
    d3dText2d = D3D11_TEXTURE2D_DESC()
    pBackBuffer.GetDesc(ctypes.byref(d3dText2d))
    print("test d3dText2d :", d3dText2d.Width)
    print("test d3dText2d :", d3dText2d.Height)
    print("test d3dText2d :", d3dText2d.MipLevels)
    print("test d3dText2d :", d3dText2d.ArraySize)
    print("test d3dText2d :", d3dText2d.Format)
    print("test d3dText2d :", d3dText2d.SampleDesc.Count)
    print("test d3dText2d :", d3dText2d.SampleDesc.Quality)
    print("test d3dText2d :", d3dText2d.Usage)
    print("test d3dText2d :", d3dText2d.BindFlags)
    print("test d3dText2d :", d3dText2d.CPUAccessFlags)
    print("test d3dText2d :", d3dText2d.MiscFlags)

    # # use the back buffer address to create the render target
    print(backbuffer)
    hr = dev.CreateRenderTargetView(pBackBuffer, None, ctypes.byref(backbuffer))
    print(backbuffer)


    rtvd = D3D11_RENDER_TARGET_VIEW_DESC()
    backbuffer.GetDesc(ctypes.byref(rtvd))
    print("test rtvd : ", rtvd.Buffer.FirstElement)
    print("test rtvd : ", rtvd.Buffer.ElementOffset)
    print("test rtvd : ", rtvd.Buffer.NumElements)
    print("test rtvd : ", rtvd.Buffer.ElementWidth)
    print("test rtvd : ", rtvd.Texture1DArray.ArraySize)
    
    #pBackBuffer.Release()
    hr = hex((hr + (1 << 64)) % (1 << 64))
    print(hr)
    # # set the render target as the back buffer
    devcon.OMSetRenderTargets(1, ctypes.byref(backbuffer), None)
    

    devcon.Dispatch(100,100,100)



    # # set the viewport
    viewport = D3D11_VIEWPORT()
    ctypes.memset(ctypes.byref(viewport), 0, ctypes.sizeof(D3D11_VIEWPORT))
    viewport.TopLeftX = 0 
    viewport.TopLeftY = 0
    viewport.Width = 941
    viewport.Height = 1008
    #d3dDebug.ReportLiveDeviceObjects(D3D11_RLDO_SUMMARY | D3D11_RLDO_DETAIL)    
    # d3dSDK = ctypes.windll.d3d11sdklayers what those line can help ?
    devcon.RSSetViewports(1, ctypes.byref(viewport))
    # try:
       
    # except:
    #     print("error")

    #     #d3dDebug.SetPresentPerRenderOpDelay(200)
    #     #d3dDebug.GetFeatureMask()
    #     d3dDebug.ReportLiveDeviceObjects(D3D11_RLDO_SUMMARY | D3D11_RLDO_DETAIL)
    # # Close and release all existing COM objects
    #swapchain.Release()
    #dev.Release()
    #devcon.Release()

if __name__ == '__main__':
    main()


# https://github.com/operator-framework/operator-lifecycle-manager/blob/master/vendor/golang.org/x/sys/windows/zerrors_windows.go
## EOF
