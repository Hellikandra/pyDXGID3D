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

    

if __name__ == '__main__':
    main()