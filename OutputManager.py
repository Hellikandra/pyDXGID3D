# OutputManager
import ctypes 

from Direct3D.PyIdl.d3dcommon import *
from Direct3D.PyIdl.d3d11     import *
from Direct3D.PyIdl.dxgi      import *
from Direct3D.PyIdl.dxgi1_2	  import *

from Direct3D.PyIdl.dxgidebug import *

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
	def __init__(self): # OUTPUTMANAGER()
		print("Hi, I am being instanciated!")
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
		self.__m_OcclusionCookie = 0 # DWORD


	def __del__(self): # ~OUTPUTMANAGER();
		#print("I am being automatically destroyed. Goodbye!")
		self.CleanRefs()


	def InitOutput(self, Window, SingleOutput, OutCount, DeskBounds):
		#hr # HRESULT
		self.__m_WindowHandle = Window

		DriverType = [D3D_DRIVER_TYPE_HARDWARE.value, D3D_DRIVER_TYPE_WARP.value, D3D_DRIVER_TYPE_REFERENCE.value]
		NumDriverTypes = len(DriverType)
		FeatureLevels = [D3D_FEATURE_LEVEL_11_1.value, D3D_FEATURE_LEVEL_11_0.value, D3D_FEATURE_LEVEL_10_1.value, D3D_FEATURE_LEVEL_10_0.value, D3D_FEATURE_LEVEL_9_3.value, D3D_FEATURE_LEVEL_9_2.value, D3D_FEATURE_LEVEL_9_1.value]
		NumFeatureLevels = len(FeatureLevels)
		FeatureLevel = ctypes.POINTER(D3D_FEATURE_LEVEL)()

		for DriverTypeIndex in range(NumDriverTypes):
			hr = ctypes.windll.d3d11.D3D11CreateDevice(None, DriverType[DriverTypeIndex], None, 0, ctypes.byref((ctypes.c_uint * D3D11_SDK_VERSION)(*FeatureLevels)), NumFeatureLevels, D3D11_SDK_VERSION, ctypes.byref(self.__m_Device), ctypes.byref(FeatureLevel), ctypes.byref(self.__m_DeviceContext))
			if hr == 0:
				# Device creation succeeded, no need to loop anymore
				break
			if hr != 0:
				return print("Device creation in OUTPUTMANAGER failed") #ProcessFailure with DUPL_...

		# Get DXGI Factory
		DxgiDevice = ctypes.POINTER(IDXGIDevice)()
		DxgiDevice = self.__m_Device.QueryInterface(IDXGIDevice, IDXGIDevice._iid_)
		if hr != 0:
			return print("Failed to QI for DXGI Device") # ProcesFailure with DUPL_...

		DxgiAdapter = ctypes.POINTER(IDXGIAdapter)()
		hr = DxgiDevice.GetParent(IDXGIAdapter._iid_, ctypes.byref(DxgiAdapter))
		if hr != 0:
			return print("Failed to get parent DXGI Adapter") # ProcessFailure with DUPL_...

		hr = DxgiAdapter.GetParent(IDXGIFactory2._iid_, ctypes.byref(self.__m_Factory))
		if hr != 0:
			return print("Failed to get parent DXGI Factory") # ProcessFailure with DUPL_...

		# Register for occlusion status windows message
		hr = self.__m_Factory.RegisterOcclusionStatusWindow(Window, OCCLUSION_STATUS_MSG, ctypes.byref(ctypes.c_uint(self.__m_OcclusionCookie)))
		if hr != 0:
			return print("Failed to register for occlusion message") # ProcessFailure DUPL_RETURN...

		# Get window size
		WindowRect = RECT()
		ctypes.windll.user32.GetClientRect(Window, ctypes.byref(WindowRect))	
		Width = WindowRect.right - WindowRect.left
		Height = WindowRect.bottom - WindowRect.top
		#print("Width x Height = %d x %d" %(Width, Height) )

		# Create Swapchain for window
		SwapChainDesc = DXGI_SWAP_CHAIN_DESC1()
		ctypes.memset(ctypes.addressof(SwapChainDesc),0, ctypes.sizeof(SwapChainDesc))
		SwapChainDesc.SwapEffect         = DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL
		SwapChainDesc.BufferCount        = 2
		SwapChainDesc.Width              = Width	
		SwapChainDesc.Height             = Height	
		SwapChainDesc.Format             = DXGI_FORMAT_B8G8R8A8_UNORM
		SwapChainDesc.BufferUsage        = DXGI_USAGE_RENDER_TARGET_OUTPUT
		SwapChainDesc.SampleDesc.Count   = 1
		SwapChainDesc.SampleDesc.Quality = 0
		SwapChainDesc.Flags				 = DXGI_SWAP_CHAIN_FLAG_DISPLAY_ONLY
		
		hr = self.__m_Factory.CreateSwapChainForHwnd(self.__m_Device, Window, SwapChainDesc, None, None, self.__m_SwapChain)
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
		# Crea
		return print("InitOutput currently in success") # return DUPL_RETURN...


	def UpdateApplicationWindow(self, PointerInfo, Occluded):
		return 0 # return DUPL_RETURN


	def CleanRefs(self):
		#print("OutputManager CleanRefs()")
		return 0 # return void


	def GetSharedHandle(self):
		return 0 # return HANDLE


	def WindowResize(self):
		__m_NeedsResize = True


	## ## private ## ##
	def __ProcessMonoMask(self):
		return 0 # return DUPL_RETURN

	def __MakeRTV(self):
		BackBuffer = ctypes.POINTER(ID3D11Texture2D)()
		hr = self.__m_SwapChain.GetBuffer(0, ID3D11Texture2D._iid_, ctypes.byref(BackBuffer))
		if hr != 0:
			return print("Failed to get backbuffer for making render target view in OUTPUTMANAGER")

		hr = self.__m_Device.CreateRenderTargetView(BackBuffer, None, ctypes.byref(self.__m_RTV))
		if hr != 0:
			return print("Failed to create render target view in OUTPUTMANAGER")

		# Set a new render target
		self.__m_DeviceContext.OMSetRenderTargets(1, ctypes.byref(self.__m_RTV), None)		

		return 0 # return DUPL_RETURN

	def __SetViewPort(self, Width, Height):
		VP = D3D11_VIEWPORT()
		ctypes.memset(ctypes.addressof(VP),0, ctypes.sizeof(VP))
		#print(Width, "x",Height)
		VP.Width    = float(Width)
		VP.Height   = float(Height)
		VP.MinDepth = 0.0
		VP.MaxDepth = 1.0
		VP.TopLeftX = 0
		VP.TopLeftY = 0
		
		self.__m_DeviceContext.RSSetViewports(1, ctypes.byref(VP))


	def __InitShaders(self):
		return 0 # return DUPL_RETURN


	def __CreateSharedSurf(self, SingleOutput, OutCount, DeskBounds):
		hr = 0
		# Get DXGI Resource
		DxgiDevice = ctypes.POINTER(IDXGIDevice)()
		# print("Print before : DxgiDevice : ", DxgiDevice)
		DxgiDevice = self.__m_Device.QueryInterface(IDXGIDevice, IDXGIDevice._iid_)
		# print("Print after  : DxgiDevice : ", DxgiDevice)
		# print("test of self.__m_Device   : ", self.__m_Device)
		if hr != 0:
			return print("Failed to QI for DXGI Device") # ProcesFailure with DUPL_...

		DxgiAdapter = ctypes.POINTER(IDXGIAdapter)()
		# print("Print before : DxgiAdapter : ", DxgiAdapter)
		hr = DxgiDevice.GetParent(IDXGIAdapter._iid_, ctypes.byref(DxgiAdapter))
		# print("Print after  : DxgiAdapter : ", DxgiAdapter)

		if hr != 0:
			return print("Failed to get parent DXGI Adapter") # ProcessFailure with DUPL_...

		DeskBounds.left = INT_MAX
		DeskBounds.right = INT_MIN
		DeskBounds.top = INT_MAX
		DeskBounds.bottom = INT_MIN

		DxgiOutput = ctypes.POINTER(IDXGIOutput)()
		# DxgiOutputDesc = DXGI_OUTPUT_DESC()
		# ctypes.memset(ctypes.addressof(DxgiOutputDesc), 0, ctypes.sizeof(DXGI_OUTPUT_DESC()))
		# print(DxgiOutputDesc)
		# print(DxgiOutput.GetDesc(DxgiOutputDesc))
		# Figure out right dimensions for full size desktop texture and # of outputs to duplicate
		OutputCount = 0
		if SingleOutput < 0:
			hr = 0
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

			OutputCount = 1

		if OutputCount == 0:
			# we could not find any outputs, the system must be in a transition so return error
			# so we will attempt to recreate
			return print("DUPL_RETURN_ERROR_EXPECTED")

		DeskTexD = D3D11_TEXTURE2D_DESC()
		ctypes.memset(ctypes.addressof(DeskTexD),0, ctypes.sizeof(DeskTexD))
		DeskTexD.Width = DeskBounds.right - DeskBounds.left
		DeskTexD.Height = DeskBounds.bottom - DeskBounds.top
		DeskTexD.MipLevels = 1
		DeskTexD.ArraySize = 1
		DeskTexD.Format = DXGI_FORMAT_B8G8R8A8_UNORM.value
		DeskTexD.SampleDesc.Count = 1
		DeskTexD.Usage = D3D11_USAGE_DEFAULT
		DeskTexD.BindFlags = D3D11_BIND_RENDER_TARGET.value | D3D11_BIND_SHADER_RESOURCE.value
		DeskTexD.CPUAccessFlags = 0
		DeskTexD.MiscFlags = D3D11_RESOURCE_MISC_SHARED_KEYEDMUTEX.value

		hr = self.__m_Device.CreateTexture2D(ctypes.byref(DeskTexD), None, ctypes.byref(self.__m_SharedSurf));
		if hr != 0:
			print('hr failed')
			if OutputCount != 1:
				return print("Failed to create DirectX shared texture - we are attempting to create a texture the size of the complete desktop and this may be larger than the maximum texture size of your GPU.  Please try again using the -output command line parameter to duplicate only 1 monitor or configure your computer to a single monitor configuration")
			else:
				return print("Failed to create shared texture")

		self.__m_KeyMutex = self.__m_SharedSurf.QueryInterface(IDXGIKeyedMutex, IDXGIKeyedMutex._iid_)
		print(self.__m_KeyMutex)	
		if hr != 0:
			return print("Failed to query for keyed mutex in OUTPUTMANAGER")
		return 0 # return DUPL_RETURN


	def __DrawFrame(self):
		return 0 # return DUPL_RETURN


	def __DrawMouse(self):
		return 0 # return DUPL_RETURN


	def __ResizeSwapChain(self):
		return 0 # return DUPL_RETURN


