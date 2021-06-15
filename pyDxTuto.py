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

    hr = ctypes.windll.d3d11.D3D11CreateDeviceAndSwapChain(
        None,                       # IDXGIAdapter                  *pAdapter
        D3D_DRIVER_TYPE_HARDWARE,   # D3D_DRIVER_TYPE               DriverType
        None,                       # HMODULE                       Software
        None,                       # UINT                          Flags
        None,                       # const D3D_FEATURE_LEVEL       *pFeatureLevels
        None,                       # UNIT                          FeatureLevels
        D3D11_SDK_VERSION,          # UINT                          SDKVersion
        scd,                        # const DXGI_SWAP_CHAIN_DESC    *pSwapChainDesc
        ctypes.byref(swapchain),    # IDXGISwapChain                **ppSwapChain
        ctypes.byref(dev),          # ID3D11Device                  **ppDevice
        None,                       # D3D_FEATURE_LEVEL             *pFeatureLevel
        ctypes.byref(devcon)        # ID3D11DeviceContext           **ppImmediateContext
        )
    hr = hex((hr + (1 << 64)) % (1 << 64))
    print(hr)


    # # get the address of the back buffer
    pBackBuffer = ctypes.POINTER(ID3D11Texture2D)()
    hr = swapchain.GetBuffer(0, ID3D11Texture2D._iid_, ctypes.byref(pBackBuffer))
    hr = hex((hr + (1 << 64)) % (1 << 64))
    print(hr)
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
    devcon.RSSetViewports(1, ctypes.byref(viewport))

    # # Close and release all existing COM objects
    #swapchain.Release()
    #dev.Release()
    #devcon.Release()

if __name__ == '__main__':
    main()


## EOF