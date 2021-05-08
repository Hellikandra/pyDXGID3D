# OutputManager
import ctypes 

from Direct3D.PyIdl.d3dcommon import *
from Direct3D.PyIdl.d3d11     import *
from Direct3D.PyIdl.dxgi      import *
from Direct3D.PyIdl.dxgi1_2	  import *

from Direct3D.PyIdl.dxgidebug import *

WM_USER    = 0x0400
OCCLUSION_STATUS_MSG = WM_USER

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
		if hr is None:
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
		Return = __CreateSharedSurf(SingleOutput,)
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
		return 0 # return DUPL_RETURN

	def __SetViewPort(self):
		return 0 # return void
	def __InitShaders(self):
		return 0 # return DUPL_RETURN
	def __CreateSharedSurf(self):
		return 0 # return DUPL_RETURN
	def __DrawFrame(self):
		return 0 # return DUPL_RETURN
	def __DrawMouse(self):
		return 0 # return DUPL_RETURN
	def __ResizeSwapChain(self):
		return 0 # return DUPL_RETURN


