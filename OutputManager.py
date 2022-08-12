# OutputManager
import ctypes

from Direct3D.PyIdl.d3dcommon      import *
from Direct3D.PyIdl.d3d11          import *
from Direct3D.PyIdl.dxgi           import *
from Direct3D.PyIdl.dxgi1_2        import *
from Direct3D.PyIdl.d3d11sdklayers import *
from Direct3D.PyIdl.dxgidebug      import *

from VertexShader import g_VS, g_VS_array
from PixelShader import g_PS, g_PS_array

WM_USER    = 0x0400
OCCLUSION_STATUS_MSG = WM_USER
INT_MIN = (-2147483647 - 1) ## minimum (signed) int value
INT_MAX = 2147483647

class RECT(ctypes.Structure): # https://docs.microsoft.com/en-us/windows/desktop/api/windef/ns-windef-rect
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)
                ]

class OutputManager:
    ## ## public ## ##
    ##
    ## Constructor NULLs out all pointers & set appropriatee var vals
    ##
    def __init__(self): # OUTPUTMANAGER()
        self.__m_SwapChain     = ctypes.POINTER(IDXGISwapChain1)() # IDXGISwapChain1*
        self.__m_Device        = ctypes.POINTER(ID3D11Device)() # ID3D11Device*
        self.__m_Factory       = ctypes.POINTER(IDXGIFactory2)() # IDXGIFactory2*
        self.__m_DeviceContext = ctypes.POINTER(ID3D11DeviceContext)() # ID3D11DeviceContext*
        self.__m_RTV           = ctypes.POINTER(ID3D11RenderTargetView)() # ID3D11RenderTargetView*
        self.__m_SamplerLinear = ctypes.POINTER(ID3D11SamplerState)() # ID3D11SamplerState*
        self.__m_BlendState    = ctypes.POINTER(ID3D11BlendState)() # ID3D11BlendState*
        self.__m_VertexShader  = ctypes.POINTER(ID3D11VertexShader)() # ID3D11VertexShader*
        self.__m_PixelShader   = ctypes.POINTER(ID3D11PixelShader)() # ID3D11PixelShader*
        self.__m_InputLayout   = ctypes.POINTER(ID3D11InputLayout)() # ID3D11InputLayout*
        self.__m_SharedSurf    = ctypes.POINTER(ID3D11Texture2D)() # ID3D11Texture2D*
        self.__m_KeyMutex      = ctypes.POINTER(IDXGIKeyedMutex)() # IDXGIKeyedMutex*
        
        self.__m_WindowHandle    = None # HWND
        self.__m_NeedsResize     = False # bool
        self.__m_OcclusionCookie = wintypes.DWORD(0) # DWORD
        self.__m_CreateDeviceFlags = D3D11_CREATE_DEVICE_DEBUG
        self.__m_DeviceDebug = ctypes.POINTER(ID3D11Debug)()


    ##
    ## Destructor which calls CleanRefs to release all reference and memory.
    ##
    def __del__(self): # ~OUTPUTMANAGER();
        #print("I am being automatically destroyed. Goodbye!")
        self.CleanRefs()


    ##
    ## Indicates that window has been resized.
    ##
    def WindowResize(self):
        __m_NeedsResize = True


    ## 
    ## Initialize all state
    ## 
    def InitOutput(self, Window, SingleOutput, OutCount, DeskBounds):
        # # Store Window handle
        self.__m_WindowHandle = Window
        # # Drive types supported
        DriverType = [D3D_DRIVER_TYPE_HARDWARE, D3D_DRIVER_TYPE_WARP, D3D_DRIVER_TYPE_REFERENCE]
        NumDriverTypes = len(DriverType)

        # # Feature levels supported
        FeatureLevels = [D3D_FEATURE_LEVEL_11_0.value, D3D_FEATURE_LEVEL_10_1.value, D3D_FEATURE_LEVEL_10_0.value, D3D_FEATURE_LEVEL_9_1.value]
        NumFeatureLevels = len(FeatureLevels)
        FeatureLevel = ctypes.POINTER(D3D_FEATURE_LEVEL)()

        # # Create Device
        for DriverTypeIndex in range(NumDriverTypes):
            hr = ctypes.windll.d3d11.D3D11CreateDevice(None, 
                        DriverType[DriverTypeIndex], 
                        None, 
                        0, 
                        ctypes.byref((ctypes.c_uint * D3D11_SDK_VERSION)(*FeatureLevels)), 
                        NumFeatureLevels, 
                        D3D11_SDK_VERSION, 
                        ctypes.byref(self.__m_Device), 
                        ctypes.byref(FeatureLevel), 
                        ctypes.byref(self.__m_DeviceContext))
            if hr == 0:
                # Device creation succeeded, no need to loop anymore
                break
        if hr != 0:
            return print("Device creation in OUTPUTMANAGER failed") # ProcessFailure with DUPL_...

        # Get DXGI Factory
        DxgiDevice = ctypes.POINTER(IDXGIDevice)() # == nullptr
        DxgiDevice = self.__m_Device.QueryInterface(IDXGIDevice, IDXGIDevice._iid_)
        print("test dxgidevice query : ", DxgiDevice)
        # how to test if DxgiDevice is clearly set ?
        if hr != 0:
            return print("Failed to QI for DXGI Device") # ProcesFailure with DUPL_...

        DxgiAdapter = ctypes.POINTER(IDXGIAdapter)()
        hr = DxgiDevice.GetParent(IDXGIAdapter._iid_, ctypes.byref(DxgiAdapter))
        DxgiDevice.Release()
        DxgiDevice = ctypes.POINTER(IDXGIDevice)() # == nullptr
        if hr != 0:
            return print("Failed to get parent DXGI Adapter") # ProcessFailure with DUPL_...

        hr = DxgiAdapter.GetParent(IDXGIFactory2._iid_, ctypes.byref(self.__m_Factory))
        ## Both line provoke a problem on call RegisterOcclusionStatusWindow
        DxgiAdapter.Release()
        #DxgiAdapter = ctypes.POINTER(IDXGIAdapter)() # == nullptr
        if hr != 0:
            return print("Failed to get parent DXGI Factory") # ProcessFailure with DUPL_...

        # Register for occlusion status windows message
        self.__m_OcclusionCookie = 1 # in the C/C++ code, OcclusionCoockie change from 0 to 1.
        hr = self.__m_Factory.RegisterOcclusionStatusWindow(Window, OCCLUSION_STATUS_MSG, ctypes.byref(wintypes.DWORD(self.__m_OcclusionCookie)))
        print("test after  : ", self.__m_OcclusionCookie)
        if hr != 0:
            return print("Failed to register for occlusion message") # ProcessFailure DUPL_RETURN...

        # Get window size
        WindowRect = RECT()
        ctypes.windll.user32.GetClientRect(self.__m_WindowHandle, ctypes.byref(WindowRect))
        Width = WindowRect.right - WindowRect.left
        Height = WindowRect.bottom - WindowRect.top
        #print("Width x Height = %d x %d" %(Width, Height) )

        # Create Swapchain for window
        SwapChainDesc = DXGI_SWAP_CHAIN_DESC1()
        ctypes.memset(ctypes.addressof(SwapChainDesc), 0, ctypes.sizeof(SwapChainDesc))
        SwapChainDesc.SwapEffect         = DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL
        SwapChainDesc.BufferCount        = 2
        SwapChainDesc.Width              = Width
        SwapChainDesc.Height             = Height
        SwapChainDesc.Format             = DXGI_FORMAT_B8G8R8A8_UNORM
        SwapChainDesc.BufferUsage        = DXGI_USAGE_RENDER_TARGET_OUTPUT
        SwapChainDesc.SampleDesc.Count   = 1
        SwapChainDesc.SampleDesc.Quality = 0
        #SwapChainDesc.Flags                 = DXGI_SWAP_CHAIN_FLAG_DISPLAY_ONLY

        hr = self.__m_Factory.CreateSwapChainForHwnd(self.__m_Device, Window, SwapChainDesc, None, None, ctypes.byref(self.__m_SwapChain))
        if hr != 0:
            return print("Failed to create window swapchain") # ProcessFailure DUPL_RETURN...

        ## Disable the ALT-ENTER shortcut for entering full-screen mode
        hr = self.__m_Factory.MakeWindowAssociation(Window, DXGI_MWA_NO_ALT_ENTER)
        if hr != 0:
            return print("Failed to make window association")

        # Create Shared Texture 
        Return = self.__CreateSharedSurf(SingleOutput, OutCount, DeskBounds)
        if Return != 0: # DUPL_RETURN_SUCCESS
            return Return

        # Make new render target view
        Return = self.__MakeRTV()
        if Return != 0: # DUPL_RETURN_SUCCESS
            return Return

        # Set view port
        self.__SetViewPort(Width, Height)
        

        # Create the sample state
        sampleDesc = D3D11_SAMPLER_DESC()
        ctypes.memset(ctypes.byref(sampleDesc), 0, ctypes.sizeof(D3D11_SAMPLER_DESC))
        sampleDesc.Filter = D3D11_FILTER_MIN_MAG_MIP_LINEAR
        sampleDesc.AddressU = D3D11_TEXTURE_ADDRESS_CLAMP
        sampleDesc.AddressV = D3D11_TEXTURE_ADDRESS_CLAMP
        sampleDesc.AddressW = D3D11_TEXTURE_ADDRESS_CLAMP
        sampleDesc.ComparisonFunc = D3D11_COMPARISON_NEVER
        sampleDesc.MinLOD = 0
        sampleDesc.MaxLOD = D3D11_FLOAT32_MAX
        # print("D3D11_FLOAT32_MAX = ", D3D11_FLOAT32_MAX)
        hr = self.__m_Device.CreateSamplerState(sampleDesc, ctypes.byref(self.__m_SamplerLinear))
        if hr != 0:
            return print("Failed to create sampler state in OUTPUTMANAGER")

        # Create the blend state
        BlendStateDesc = D3D11_BLEND_DESC()
        BlendStateDesc.AlphaToCoverageEnable                 = False
        BlendStateDesc.IndependentBlendEnable                = False
        BlendStateDesc.RenderTarget[0].BlendEnable           = True
        BlendStateDesc.RenderTarget[0].SrcBlend              = D3D11_BLEND_SRC_ALPHA
        BlendStateDesc.RenderTarget[0].DestBlend             = D3D11_BLEND_INV_SRC_ALPHA
        BlendStateDesc.RenderTarget[0].BlendOp               = D3D11_BLEND_OP_ADD
        BlendStateDesc.RenderTarget[0].SrcBlendAlpha         = D3D11_BLEND_ONE
        BlendStateDesc.RenderTarget[0].DestBlendAlpha        = D3D11_BLEND_ZERO
        BlendStateDesc.RenderTarget[0].BlendOpAlpha          = D3D11_BLEND_OP_ADD
        BlendStateDesc.RenderTarget[0].RenderTargetWriteMask = D3D11_COLOR_WRITE_ENABLE_ALL
        hr = self.__m_Device.CreateBlendState(BlendStateDesc, ctypes.byref(self.__m_BlendState))
        if hr != 0:
            return print("Failed to create blend state in OUTPUTMANAGER")

        # Initialize shaders
        Return = self.__InitShaders()
        if Return != 0:
            return print("Failed to init Shaders in OUTPUTMANAGER")

        ctypes.windll.user32.GetWindowRect(self.__m_WindowHandle, ctypes.byref(WindowRect))
        # print(WindowRect.left, "\t", WindowRect.top)
        # print((DeskBounds.right - DeskBounds.left)/2,"\t" , (DeskBounds.bottom - DeskBounds.top)/2)
        ctypes.windll.user32.MoveWindow(self.__m_WindowHandle, WindowRect.left, WindowRect.top, int((DeskBounds.right - DeskBounds.left) / 2), int((DeskBounds.bottom - DeskBounds.top) / 2), True)
        return 0 # return DUPL_RETURN...


    def UpdateApplicationWindow(self, PointerInfo, Occluded):
        return 0 # return DUPL_RETURN

    ##
    ## Release all reference
    ##
    def CleanRefs(self):
        if (self.__m_VertexShader):
            self.__m_VertexShader.Release()
            self.__m_VertexShader = None
        if (self.__m_PixelShader):
            self.__m_PixelShader.Release()
            self.__m_PixelShader = None
        if (self.__m_InputLayout):
            self.__m_InputLayout.Release()
            self.__m_InputLayout = None
        if (self.__m_RTV):
            self.__m_RTV.Release()
            self.__m_RTV = None
        if (self.__m_BlendState):
            self.__m_BlendState.Release()
            self.__m_BlendState = None
        if (self.__m_DeviceContext):
            self.__m_DeviceContext.Release()
            self.__m_DeviceContext = None
        if (self.__m_Device):
            self.__m_Device.Release()
            self.__m_Device = None
        if (self.__m_SwapChain):
            self.__m_SwapChain.Release()
            self.__m_SwapChain = None
        if (self.__m_SharedSurf):
            self.__m_SharedSurf.Release()
            self.__m_SharedSurf = None
        if (self.__m_KeyMutex):
            self.__m_KeyMutex.Release()
            self.__m_KeyMutex = None
        if (self.__m_Factory):
            if (self.__m_OcclusionCookie):
                self.__m_Factory.UnregisterOcclusionStatus(self.__m_OcclusionCookie)
                self.__m_OcclusionCookie = 0
            self.__m_Factory.Release()
            self.__m_Factory = None


    def GetSharedHandle(self):
        return 0 # return HANDLE


    ## ## private ## ##
    def __ProcessMonoMask(self):
        return 0 # return DUPL_RETURN

    def __MakeRTV(self):
        ## Get Buffer
        BackBuffer = ctypes.POINTER(ID3D11Texture2D)()
        hr = self.__m_SwapChain.GetBuffer(0, ID3D11Texture2D._iid_, ctypes.byref(BackBuffer))
        if hr != 0:
            return print("Failed to get backbuffer for making render target view in OUTPUTMANAGER")
        
        ## Create a rendre target view
        hr = self.__m_Device.CreateRenderTargetView(BackBuffer, None, ctypes.byref(self.__m_RTV))
        BackBuffer.Release()
        if hr != 0:
            return print("Failed to create render target view in OUTPUTMANAGER")

        # Set a new render target
        self.__m_DeviceContext.OMSetRenderTargets(1, ctypes.byref(self.__m_RTV), None)
        return 0 # return DUPL_RETURN

    def __SetViewPort(self, Width, Height):
        VP = D3D11_VIEWPORT()
        ctypes.memset(ctypes.addressof(VP),0, ctypes.sizeof(D3D11_VIEWPORT))
        print(Width, "x",Height)
        print(self.__m_SwapChain)
        print(self.__m_Device)
        print(self.__m_Factory)
        print(self.__m_RTV)
        print(self.__m_SharedSurf)
        print(self.__m_KeyMutex)
        print(self.__m_WindowHandle)
        print(self.__m_NeedsResize)
        print(self.__m_OcclusionCookie)
        VP.Width    = float(Width)
        VP.Height   = float(Height)
        VP.MinDepth = 0.0
        VP.MaxDepth = 1.0
        VP.TopLeftX = 0.0
        VP.TopLeftY = 0.0
        print(VP)
        #self.__m_DeviceDebug = self.__m_Device.QueryInterface(ID3D11Debug, ID3D11Debug._iid_)
        print(self.__m_DeviceDebug)
        self.__m_DeviceContext.RSSetViewports(1, VP)


    def __InitShaders(self):
        # VertexShaders.... need to be different 
        g_VS_t = ctypes.c_char_p(g_VS)
        hr = self.__m_Device.CreateVertexShader(g_VS_t, len(g_VS), None, ctypes.byref(self.__m_VertexShader))
        if hr != 0:
            return print("Failed to create vertex shader in OUTPUTMANAGER")

        tmp_type = D3D11_INPUT_ELEMENT_DESC * 2
        tmp = tmp_type()
        tmp[0].SemanticName        = ctypes.c_char_p("POSITION".encode('utf-8'))
        tmp[0].SemanticIndex       = 0
        tmp[0].Format              = DXGI_FORMAT_R32G32B32_FLOAT
        tmp[0].InputSlot           = 0
        tmp[0].AlignedByteOffset   = 0
        tmp[0].InputSlotClass      = D3D11_INPUT_PER_VERTEX_DATA
        tmp[0].InstanceDataSetRate = 0
        tmp[1].SemanticName        = ctypes.c_char_p("TEXCOORD".encode('utf-8'))
        tmp[1].SemanticIndex       = 0
        tmp[1].Format              = DXGI_FORMAT_R32G32_FLOAT
        tmp[1].InputSlot           = 0
        tmp[1].AlignedByteOffset   = 12
        tmp[1].InputSlotClass      = D3D11_INPUT_PER_VERTEX_DATA
        tmp[1].InstanceDataSetRate = 0
        Layout = tmp
        print(len(Layout))
        hr = self.__m_Device.CreateInputLayout(Layout, len(Layout), g_VS_t, len(g_VS), self.__m_InputLayout)
        if hr != 0:
            return print("Failed to create input layout in OUTPUTMANAGER")
        self.__m_DeviceContext.IASetInputLayout(self.__m_InputLayout)

        g_PS_t = ctypes.c_char_p(g_PS)
        hr = self.__m_Device.CreatePixelShader(g_PS_t, len(g_PS), None, self.__m_PixelShader)
        if hr != 0:
            return print("Failed to create pixel shader in OUTPUTMANAGER")
        return 0 # return DUPL_RETURN


    def __CreateSharedSurf(self, SingleOutput, OutCount, DeskBounds):
        hr = 0
        # Get DXGI Resource
        DxgiDevice = ctypes.POINTER(IDXGIDevice)()
        DxgiDevice = self.__m_Device.QueryInterface(IDXGIDevice, IDXGIDevice._iid_)
        if hr != 0:
            return print("Failed to QI for DXGI Device") # ProcesFailure with DUPL_...

        DxgiAdapter = ctypes.POINTER(IDXGIAdapter)()
        hr = DxgiDevice.GetParent(IDXGIAdapter._iid_, ctypes.byref(DxgiAdapter))
        DxgiDevice.Release()
        DxgiDevice = ctypes.POINTER(IDXGIDevice)() # == nullptr
        if hr != 0:
            return print("Failed to get parent DXGI Adapter") # ProcessFailure with DUPL_...

        DeskBounds.left = INT_MAX
        DeskBounds.right = INT_MIN
        DeskBounds.top = INT_MAX
        DeskBounds.bottom = INT_MIN

        DxgiOutput = ctypes.POINTER(IDXGIOutput)()
        # Figure out right dimensions for full size desktop texture and # of outputs to duplicate
        OutputCount = 0
        if SingleOutput < 0:
            hr = 0 # S_OK
            while hr == 0:
                if DxgiOutput:
                    pass
                try:
                    hr = DxgiAdapter.EnumOutputs(OutputCount, ctypes.byref(DxgiOutput)) # DXGI_ERROR_NOT_FOUND
                except:
                    #print(hr)
                    break
                if DxgiOutput and (hr == 0):
                    DesktopDesc = DXGI_OUTPUT_DESC()
                    DxgiOutput.GetDesc(ctypes.byref(DesktopDesc))
                    #print("Get Desc")
                    DeskBounds.left   = min(DesktopDesc.DesktopCoordinates.left,   DeskBounds.left)
                    DeskBounds.top    = min(DesktopDesc.DesktopCoordinates.top,    DeskBounds.top)
                    DeskBounds.right  = max(DesktopDesc.DesktopCoordinates.right,  DeskBounds.right)
                    DeskBounds.bottom = max(DesktopDesc.DesktopCoordinates.bottom, DeskBounds.bottom)
                OutputCount += 1
            OutputCount -= 1
        else:
            hr = DxgiAdapter.EnumOutputs(SingleOutput, ctypes.byref(DxgiOutput));
            if hr != 0:
                DxgiAdapter.Release()
                DxgiAdapter = None
                return print("Output specified to be duplicated does not exist")
            DesktopDesc = DXGI_OUTPUT_DESC()
            DxgiOutput.GetDesc(ctypes.byref(DesktopDesc))
            DeskBounds.left    = DesktopDesc.DesktopCoordinates.left
            DeskBounds.top     = DesktopDesc.DesktopCoordinates.top
            DeskBounds.right   = DesktopDesc.DesktopCoordinates.right
            DeskBounds.bottom  = DesktopDesc.DesktopCoordinates.bottom
            DxgiOutput.Release()
            DxgiOutput = ctypes.POINTER(IDXGIOutput)() # == nullptr
            OutputCount = 1

        DxgiAdapter.Release()
        DxgiAdapter = ctypes.POINTER(IDXGIAdapter)() # == nullptr

        # # Set passed in output count variable
        OutCount = OutputCount
        if OutputCount == 0:
            # we could not find any outputs, the system must be in a transition so return error
            # so we will attempt to recreate
            return print("DUPL_RETURN_ERROR_EXPECTED")

        ## Create shared texture for all duplication threads to draw into
        DeskTexD = D3D11_TEXTURE2D_DESC()
        ctypes.memset(ctypes.addressof(DeskTexD),0, ctypes.sizeof(DeskTexD))
        DeskTexD.Width = DeskBounds.right - DeskBounds.left
        DeskTexD.Height = DeskBounds.bottom - DeskBounds.top
        DeskTexD.MipLevels = 1
        DeskTexD.ArraySize = 1
        DeskTexD.Format = DXGI_FORMAT_B8G8R8A8_UNORM
        DeskTexD.SampleDesc.Count = 1
        DeskTexD.Usage = D3D11_USAGE_DEFAULT.value
        DeskTexD.BindFlags = D3D11_BIND_RENDER_TARGET.value | D3D11_BIND_SHADER_RESOURCE.value
        DeskTexD.CPUAccessFlags = 0
        DeskTexD.MiscFlags = D3D11_RESOURCE_MISC_SHARED_KEYEDMUTEX.value

        hr = self.__m_Device.CreateTexture2D(ctypes.byref(DeskTexD), None, ctypes.byref(self.__m_SharedSurf));
        if hr != 0:
            if OutputCount != 1:
                return print("Failed to create DirectX shared texture - we are attempting to create a texture the size of the complete desktop and this may be larger than the maximum texture size of your GPU.  Please try again using the -output command line parameter to duplicate only 1 monitor or configure your computer to a single monitor configuration")
            else:
                return print("Failed to create shared texture")
        ## Get Keyed Mutex
        self.__m_KeyMutex = self.__m_SharedSurf.QueryInterface(IDXGIKeyedMutex, IDXGIKeyedMutex._iid_)

        if hr != 0:
            return print("Failed to query for keyed mutex in OUTPUTMANAGER")
        return 0 # return DUPL_RETURN

    def __UpdateApplicationWIndow(self):
        hr = 0
        return 0 # return DUPL_RETURN
    def __DrawFrame(self):
        return 0 # return DUPL_RETURN


    def __DrawMouse(self):
        return 0 # return DUPL_RETURN


    def __ResizeSwapChain(self):
        return 0 # return DUPL_RETURN


