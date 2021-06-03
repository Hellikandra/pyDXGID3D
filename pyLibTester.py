#Lib Tester
import ctypes 

from Direct3D.PyIdl.d3dcommon      import *
from Direct3D.PyIdl.d3d11          import *

from Direct3D.PyIdl.dxgi           import *
from Direct3D.PyIdl.dxgi1_2        import *

from Direct3D.PyIdl.d3d11sdklayers import *
from Direct3D.PyIdl.dxgidebug      import *

def main():
    print("hello wolrd !")
    ## Init Var
    vDriverType       = D3D_DRIVER_TYPE_UNKNOWN.value
    vFeatureLevel     = D3D_FEATURE_LEVEL_11_0
    vDxgiFactory      = ctypes.POINTER(IDXGIFactory)()
    vDxgiAdapter      = ctypes.POINTER(IDXGIAdapter)()
    vD3dDevice        = ctypes.POINTER(ID3D11Device)()
    vD3dContext       = ctypes.POINTER(ID3D11DeviceContext)()
    vSwapChain        = ctypes.POINTER(IDXGISwapChain)()
    vBackBUffer       = ctypes.POINTER(ID3D11Texture2D)()
    vRenderTargetView = ctypes.POINTER(ID3D11RenderTargetView)()
    
    vDebugger         = ctypes.POINTER(ID3D11Debug)()
    vInfoQueue        = ctypes.POINTER(ID3D11InfoQueue)()

    ##
    hr = ctypes.windll.dxgi.CreateDXGIFactory(IDXGIFactory._iid_, ctypes.byref(vDxgiFactory))
    if hr != 0:
        print(hr)
    hr = vDxgiFactory.EnumAdapters(0, ctypes.byref(vDxgiAdapter))
    if hr != 0:
        print(hr)
    vRequestedFeatureLevels = [D3D_FEATURE_LEVEL_11_0.value]
    vNumFeatureLevel = len(vRequestedFeatureLevels)
    vDeviceFlags = 0
    # can be killed
    vDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG.value

    hr = ctypes.windll.d3d11.D3D11CreateDevice(vDxgiAdapter, vDriverType, 
                                                None, vDeviceFlags, ctypes.byref((ctypes.c_uint * D3D11_SDK_VERSION)(*vRequestedFeatureLevels)),
                                                vNumFeatureLevel, D3D11_SDK_VERSION, 
                                                ctypes.byref(vD3dDevice), ctypes.byref(vFeatureLevel), 
                                                ctypes.byref(vD3dContext))
    if hr != 0:
        print(hr)

    vMsaaQuality = 0
    if vD3dDevice.CheckMultisampleQualityLevels(DXGI_FORMAT_R8G8B8A8_UNORM, 4, ctypes.byref(ctypes.c_uint(vMsaaQuality))) or (vMsaaQuality < 1) :
        print("Success")
        print("vMsaaQuality of max %d supported for count 4" % vMsaaQuality)
    else:
        print("Failed")

    vSwapChainDesc = DXGI_SWAP_CHAIN_DESC()
    ctypes.memset(ctypes.byref(vSwapChainDesc), 0, ctypes.sizeof(vSwapChainDesc))

    vSwapChainDesc.BufferCount = 2
    vSwapChainDesc.BufferDesc.Width = 800 #vWidth
    vSwapChainDesc.BufferDesc.Height = 600 #vHeight
    vSwapChainDesc.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM
    vSwapChainDesc.BufferDesc.RefreshRate.Numerator   = 60
    vSwapChainDesc.BufferDesc.RefreshRate.Denominator = 1
    vSwapChainDesc.BufferDesc.ScanlineOredering = DXGI_MODE_SCANLINE_ORDER_UNSPECIFIED
    vSwapChainDesc.BufferDesc.Scaling = DXGI_MODE_SCALING_CENTERED
    vSwapChainDesc.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT
    vSwapChainDesc.SampleDesc.Count = 4 # set 1 to work
    vSwapChainDesc.SampleDesc.Quality = vMsaaQuality - 1
    vSwapChainDesc.OutputWindow = 0# vHwnd
    vSwapChainDesc.Windowed = True
    vSwapChainDesc.SwapEffect = DXGI_SWAP_EFFECT_DISCARD
    vSwapChainDesc.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH

    hr = vDxgiFactory.CreateSwapChain(vD3dDevice, ctypes.byref(vSwapChainDesc), ctypes.byref(vSwapChain))
    print(hr)
if __name__ == '__main__':
    main()