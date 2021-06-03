# test from : https://www.gamedev.net/forums/topic/664849-how-to-properly-switch-to-fullscreen-with-dxgi/
# https://www.codementor.io/@malortie/build-win32-api-application-window-c-cpp-visual-studio-du107nrh6
# http://www.christophekeller.com/hello-world-in-python-using-win32/
# http://www.kbdedit.com/manual/low_level_vk_list.html

import sys
import ctypes
import ctypes.wintypes as wintypes
import enum
import numpy
import comtypes
import os

import Direct3D.PyIdl.dxgi
import Direct3D.PyIdl.dxgi1_2
import Direct3D.PyIdl.dxgiformat
import Direct3D.PyIdl.dxgitype
import Direct3D.PyIdl.d3d11
import Direct3D.PyIdl.d3dcommon

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM)

WM_PAINT   = 15
WM_DESTROY = 2
WM_QUIT    = 0x0012
# Class
class WNDCLASSEXW(ctypes.Structure): # https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-wndclassexw
    _fields_ = [('cbSize'       , ctypes.c_uint),
                ('style'        , ctypes.c_uint),
                ('lpfnWndProc'  , WNDPROC),
                ('cbClsExtra'   , ctypes.c_int),
                ('cbWndExtra'   , ctypes.c_int),
                ('hInstance'    , wintypes.HANDLE), #typedef void *PVOID HANDLE HINSTANCE; ctypes.c_void_p
                ('hIcon'        , wintypes.HICON),
                ('hCursor'      , wintypes.HICON), #typedef void *PVOID HANDLE HICON HCURSOR;
                ('hbrBackground', wintypes.HBRUSH), #typedef void *PVOID HANDLE HBRUSH;  
                ('lpszMenuName' , wintypes.LPCWSTR),   
                ('lpszClassName', wintypes.LPCWSTR),
                ('hIconSm'      , wintypes.HICON),
                ]
class RECT(ctypes.Structure): # https://docs.microsoft.com/en-us/windows/desktop/api/windef/ns-windef-rect
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]
class PAINTSTRUCT(ctypes.Structure): # https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-paintstruct
    _fields_ = [('hdc', wintypes.HDC),
                ('fErase', ctypes.c_bool),
                ('rcPaint', RECT),
                ('fRestore',ctypes.c_bool),
                ('fIncUpdate',ctypes.c_bool),
                ('rgbReserved',ctypes.c_char * 32)
                ]
class POINT(ctypes.Structure): #https://docs.microsoft.com/en-us/previous-versions/dd162805(v=vs.85)
    _fields_ = [('x', ctypes.c_long),
                ('y', ctypes.c_long),
                ]

class MSG(ctypes.Structure): #https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-msg
    _fields_ = [('hwnd',wintypes.HWND),
                ('message',ctypes.c_uint),
                ('wParam',wintypes.WPARAM),
                ('lParam',wintypes.LPARAM),
                ('time',wintypes.DWORD),
                ('pt', POINT),
                ('lPrivate',wintypes.DWORD),
                ]
class D3DXCOLOR(ctypes.Structure):
    _fields_ = [('r', ctypes.c_float),
                ('g', ctypes.c_float),
                ('b', ctypes.c_float),
                ('a', ctypes.c_float),
                ]
# Global Var
CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001

IDI_APPLICATION = 32512
IDI_SMALL       = 108
IDC_ARROW       = 32512

WS_OVERLAPPED       = 0x00000000#L
WS_CAPTION          = 0x00C00000#L
WS_SYSMENU          = 0x00080000#L
WS_THICKFRAME       = 0x00040000#L
WS_MINIMIZEBOX      = 0x00020000#L
WS_MAXIMIZEBOX      = 0x00010000#L   
WS_OVERLAPPEDWINDOW = (WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX)

SW_SHOW = 5

DT_SINGLELINE = 0x20
DT_CENTER = 0x1
DT_VCENTER = 0x4

# PeekMessageA
PM_NOREMOVE = 0x0000
PM_REMOVE   = 0x0001
PM_NOYIELD  = 0x0002

# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VK_ADD = 0x6B      # Add key
VK_SUBTRACT = 0x6D # Subtract key

def ErrorIfZero(handle):
    if handle == 0:
        raise ctypes.WinError()
    else:
        return handle


def WindowProc(hwnd, uMsg, wParam, lParam):
    print("hwnd : ", hwnd, "\tuMsg : ", uMsg, "\twParam : ", wParam,  "\tlParam : ", lParam)
    if uMsg == WM_DESTROY:
        print("WM_DESTROY")
        ctypes.windll.user32.PostQuitMessage(0)
    # elif uMsg == WM_PAINT:
    #     print("WM_PAINT")
    #     ps = PAINTSTRUCT()
    #     rect = RECT()
    #     hdc = ctypes.windll.user32.BeginPaint(hwnd, ctypes.byref(ps))
    #     ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))
    #     ctypes.windll.user32.DrawTextW(hdc, u"Hello, windows 10 64-bit", -1, ctypes.byref(rect),
    #         DT_SINGLELINE | DT_CENTER | DT_VCENTER)

    #     ctypes.windll.user32.EndPaint(ctypes.c_int(hwnd), ctypes.byref(ps))
    #     return 0
    else:
        return ctypes.windll.user32.DefWindowProcW(hwnd, uMsg, ctypes.c_ulonglong(wParam), ctypes.c_longlong(lParam))
    return 0

def MainWindowFrame():
    # create_factory_func = ctypes.windll.user32.CreateWindowExW
    # create_factory_func.argtypes = (ctypes.c_ulong, ctypes.c_wchar_p)
    #### DXGO Factory

    wcexw               = WNDCLASSEXW()
    wcexw.cbSize        = ctypes.sizeof(WNDCLASSEXW)
    wcexw.style         = CS_HREDRAW | CS_VREDRAW
    wcexw.lpfnWndProc   = WNDPROC(WindowProc)
    wcexw.cbClsExtra    = 0
    wcexw.cbWndExtra    = 0
    wcexw.hInstance     = ctypes.windll.kernel32.GetModuleHandleW(None)
    print("hInstance : ", wcexw.hInstance)
    wcexw.hIcon         = ctypes.windll.user32.LoadIconW(ctypes.c_int(wcexw.hInstance), ctypes.c_wchar_p(IDI_APPLICATION)) # typedef CONST WCHAR *LPCWSTR; typedf wchar_t WCHAR;
    wcexw.hCursor       = ctypes.windll.user32.LoadCursorW(None, ctypes.c_wchar_p(IDC_ARROW))
    wcexw.hbrBackground = ctypes.windll.gdi32.GetStockObject(ctypes.c_void_p(0))
    wcexw.lpszMenuName  = None
    wcexw.lpszClassName = u"Main Wind"
    wcexw.hIconSm       = ctypes.windll.user32.LoadIconW(ctypes.c_int(wcexw.hInstance), ctypes.c_wchar_p(IDI_SMALL))
    # #wnd_class_a.hInstance   = ctypes.windll.kernel32.GetModuleHandleExA(None,ctypes.c_int(int("0x00000004",16)).value, None)
    # wcexw.hInstance   = ctypes.windll.kernel32.GetModuleHandleA(None)
    # if not ctypes.windll.kernel32.GetModuleHandleA(None):
    #     raise ctypes.WinError()
    # if not ctypes.windll.kernel32.GetModuleHandleW(0):
    #     raise ctypes.WinError()
    # print(ctypes.windll.kernel32.GetModuleHandleA(None)) 
    # print(ctypes.windll.kernel32.GetModuleHandleW(0)) 
    # wcexw.lpszClassName = b"Sample Window Class"
    
    if not ctypes.windll.user32.RegisterClassExW(ctypes.byref(wcexw)):
        raise ctypes.WinError()

    #print(win32api.GetModuleHandle(None))
    #print("dword value : ", ctypes.c_int(int("0x40000000",16)).value)
    #print("GetModuleHandleA : ", ctypes.windll.kernel32.GetModuleHandleA(None))
    hwnd = ctypes.windll.user32.CreateWindowExW(0, wcexw.lpszClassName, u"Main Pyth", ctypes.c_int(WS_OVERLAPPEDWINDOW),10,10,400,500, None, None, ctypes.c_ulonglong(wcexw.hInstance), None)
    if not hwnd :
        raise ctypes.WinError()
    # 18446744072772059136
    # Max 64 bits values : [-9223372036854775808; 9223372036854775807]
    print("hwnd of CreateWindowExW : ", hwnd)


    dxgi_mode_desc = Direct3D.PyIdl.dxgitype.DXGI_MODE_DESC()
    dxgi_scd = Direct3D.PyIdl.dxgi.DXGI_SWAP_CHAIN_DESC()
    dxgi_swap_chain = ctypes.POINTER(Direct3D.PyIdl.dxgi.IDXGISwapChain)()
    print("dxgi_swap_chain before :", dxgi_swap_chain)
    d3d_device = ctypes.POINTER(Direct3D.PyIdl.d3d11.ID3D11Device)()
    d3d_device_context = ctypes.POINTER(Direct3D.PyIdl.d3d11.ID3D11DeviceContext)()

    ctypes.memset(ctypes.addressof(dxgi_mode_desc),0, ctypes.sizeof(dxgi_mode_desc))
    dxgi_mode_desc.Width = 300
    dxgi_mode_desc.Height = 300
    dxgi_mode_desc.RefreshRate.Numerator = 60
    dxgi_mode_desc.RefreshRate.Denominator = 1
    dxgi_mode_desc.Fromat = Direct3D.PyIdl.dxgiformat.DXGI_FORMAT_R8G8B8A8_UNORM
    dxgi_mode_desc.ScanlineOrdering = Direct3D.PyIdl.dxgitype.DXGI_MODE_SCANLINE_ORDER_UNSPECIFIED
    dxgi_mode_desc.Scaling = Direct3D.PyIdl.dxgitype.DXGI_MODE_SCALING_UNSPECIFIED
    print(dxgi_mode_desc.Scaling)
    ctypes.memset(ctypes.addressof(dxgi_scd),0, ctypes.sizeof(dxgi_scd))
    dxgi_scd.BufferCount       = 1
    #dxgi_scd.BufferDesc        = dxgi_mode_desc
    dxgi_scd.BufferDesc.Format = Direct3D.PyIdl.dxgiformat.DXGI_FORMAT_R8G8B8A8_UNORM
    dxgi_scd.BufferUsage       = Direct3D.PyIdl.dxgi.DXGI_USAGE_RENDER_TARGET_OUTPUT
    dxgi_scd.OutputWindow      = hwnd
    dxgi_scd.SampleDesc.Count  = 1
    dxgi_scd.Windowed          = True
    dxgi_scd.Flags             = 2
    print(dxgi_scd.BufferDesc.Format) # 28
    print(dxgi_scd.SampleDesc.Count)  # 1
    print(dxgi_scd.BufferUsage)       # 32
    print(dxgi_scd.BufferCount)       # 1
    print(dxgi_scd.OutputWindow)      # same than hwnd
    print(dxgi_scd.SwapEffect)        # 0
    print(dxgi_scd.Windowed)          # True = 1
    print(dxgi_scd.Flags)             # 2

    # hResult = ctypes.windll.d3d11.D3D11CreateDevice(
    #     None, 1,
    #     None, 1,
    #     None, 0, 7,
    #     # swapchain no
    #     # swapchain no
    #     ctypes.byref(d3d_device),
    #     None,
    #     ctypes.byref(d3d_device_context)
    #     )
    # print("post call : ", d3d_device)
    # if hResult < 0:
    #     print("error hResult D3D11CreateDevice : ", hex(hResult), hResult)
    # else:
    #     print("Sucess hResult D3D11CreateDevice :", hex(hResult), hResult)
    
    hResult = ctypes.windll.d3d11.D3D11CreateDeviceAndSwapChain(
        None, 1,    # D3D_DRIVE_TYPE_HARDWARE
        None, 2,    # D3D11_CREATE_DEVICE_DEBUG (0x2) # D3D11_CREATE_DEVICE_SINGLETHREADED (0x1) default use
        None, None , 7, # D3D11_SDK_VERSION
        ctypes.byref(dxgi_scd),
        ctypes.byref(dxgi_swap_chain),
        ctypes.byref(d3d_device),
        None,
        ctypes.byref(d3d_device_context)
        )
    if hResult < 0:
        print("error hResult D3D11CreateDeviceAndSwapChain : ", hex(hResult), hResult)
    else:
        print("Sucess hResult D3D11CreateDeviceAndSwapChain :", hex(hResult), hResult)
        print("dxgi_swap_chain after :", dxgi_swap_chain)

    ## TEST #########################################################################
    print("Flags : ",d3d_device.GetCreationFlags())
    dxgidevice   = ctypes.POINTER(Direct3D.PyIdl.dxgi.IDXGIDevice)()
    dxgiadapter   = ctypes.POINTER(Direct3D.PyIdl.dxgi.IDXGIAdapter)()
    dxgiFactory2  = ctypes.POINTER(Direct3D.PyIdl.dxgi1_2.IDXGIFactory2)()
    dxgiswpchain1 = ctypes.POINTER(Direct3D.PyIdl.dxgi1_2.IDXGISwapChain1)()

    dxgidevice = d3d_device.QueryInterface(Direct3D.PyIdl.dxgi.IDXGIDevice, Direct3D.PyIdl.dxgi.IDXGIDevice._iid_)
    hr = dxgidevice.GetParent(Direct3D.PyIdl.dxgi.IDXGIAdapter._iid_, ctypes.byref(dxgiadapter))
    print("dxgidevice : hr = ", hr)
    hr = dxgiadapter.GetParent(Direct3D.PyIdl.dxgi1_2.IDXGIFactory2._iid_, ctypes.byref(dxgiFactory2))
    print("dxgiadapter : hr = ", hr)
    dxgiswp1 = Direct3D.PyIdl.dxgi1_2.DXGI_SWAP_CHAIN_DESC1()
    ctypes.memset(ctypes.addressof(dxgiswp1), 0, ctypes.sizeof(Direct3D.PyIdl.dxgi1_2.DXGI_SWAP_CHAIN_DESC1()))
    dxgiswp1.SwapEffect         = Direct3D.PyIdl.dxgi.DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL
    dxgiswp1.BufferCount        = 2
    dxgiswp1.Width              = 800    
    dxgiswp1.Height             = 600   
    dxgiswp1.Format             = Direct3D.PyIdl.dxgiformat.DXGI_FORMAT_B8G8R8A8_UNORM
    dxgiswp1.BufferUsage        = Direct3D.PyIdl.dxgi.DXGI_USAGE_RENDER_TARGET_OUTPUT
    dxgiswp1.SampleDesc.Count   = 1
    dxgiswp1.SampleDesc.Quality = 0
    dxgiswp1.Flags              = Direct3D.PyIdl.dxgi.DXGI_SWAP_CHAIN_FLAG_DISPLAY_ONLY    
    hr = dxgiFactory2.CreateSwapChainForHwnd(d3d_device, hwnd, dxgiswp1, None, None, dxgiswpchain1)
    print("dxgiswpchain1 : hr = ", hr)
    ## END TEST #########################################################################

    pBackBuffer = ctypes.POINTER(Direct3D.PyIdl.d3d11.ID3D11Texture2D)()
    pRTV        = ctypes.POINTER(Direct3D.PyIdl.d3d11.ID3D11RenderTargetView)()
    backBufferDesc = Direct3D.PyIdl.d3d11.D3D11_TEXTURE2D_DESC()

    hResult = dxgi_swap_chain.GetBuffer(0, pBackBuffer._iid_, ctypes.byref(pBackBuffer))
    print("GetBuffer : ", hResult)
    hResult = d3d_device.CreateRenderTargetView(pBackBuffer, None, ctypes.byref(pRTV))    
    print("CreateRenderTargetView : ", hResult)
    pBackBuffer.GetDesc(ctypes.byref(backBufferDesc))
    print("Width", backBufferDesc.Width)
    print("Height", backBufferDesc.Height)
    pBackBuffer.Release()
    
    d3d_device_context.OMSetRenderTargets(1, ctypes.byref(pRTV), None)
    VP = Direct3D.PyIdl.d3d11.D3D11_VIEWPORT()
    ctypes.memset(ctypes.addressof(VP),0, ctypes.sizeof(VP))
    VP.Width = 800.0
    VP.Height = 600.0
    VP.MinDepth = 0.0
    VP.MaxDepth = 1.0
    VP.TopLeftX = 0.0
    VP.TopLeftY = 0.0
    d3d_device_context.RSSetViewports(1, ctypes.byref(VP))

    # Mode Switching
    currentMode = 0
    modeChanged = False
    currentFullScreen = ctypes.wintypes.BOOL(False)
    dxgi_swap_chain.GetFullscreenState(ctypes.byref(currentFullScreen), None)

    ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)

    # # # OLD CODE and replaced # # #
    # ctypes.windll.user32.UpdateWindow(hwnd)

    # msg = MSG()
    # pMsg = ctypes.pointer(msg)

    # while ctypes.windll.user32.GetMessageW(pMsg, None, 0, 0) != 0:
    #     ctypes.windll.user32.TranslateMessage(pMsg)
    #     ctypes.windll.user32.DispatchMessageW(pMsg)
    
    peekMsgA = ctypes.windll.user32.PeekMessageA
    print(peekMsgA)
    bLoop = True
    while bLoop:
        msg = MSG()
        #pMsg = ctypes.POINTER(msg)
        hResult = ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, PM_REMOVE)
        #print("PeekMessageW return : " + str(hResult))
        if hResult != 0:
            if msg.message == WM_QUIT:
                bLoop = False
                print("bLoop = False")
            else:
                print("bLoop = True")
                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
        else:
            #print("PeekMessageW return : " + str(hResult))
            changeMode = False
            if ctypes.windll.user32.GetAsyncKeyState(VK_ADD) and 0x8000 :
                if not modeChanged:
                    currentMode += 1
                    changeMode = True
                    print("changeMode to True")
            elif ctypes.windll.user32.GetAsyncKeyState(VK_SUBTRACT) and 0x8000:
                if not modeChanged:
                    currentMode -= 1
                    changeMode = True
                    print("changeMode to True")
            else:
                modeChanged = False

            # Change mode
            changeThisFrame = False
            if changeMode:
                print("Change Mode 1")
                pOutput = ctypes.POINTER(Direct3D.PyIdl.dxgi.IDXGIOutput)()
                dxgi_swap_chain.GetContainingOutput(ctypes.byref(pOutput))
                print("Change Mode 2")
                numModes = 1024
                modes = (Direct3D.PyIdl.dxgitype.DXGI_MODE_DESC * 1024)()
                print("Change Mode 3")
                print(modes, numModes)
                print("Change Mode 4")
                print(sys.getsizeof(modes))
                print(ctypes.byref(modes))
                #print(sizeof(modes))
                pOutput.GetDisplayModeList(dxgi_scd.BufferDesc.Format, 0, ctypes.byref(ctypes.c_uint(numModes)), modes)
                
                if currentMode < numModes:
                    print("Change Mode 5 ")
                    print(numModes)
                    print(currentMode)
                    mode = (Direct3D.PyIdl.dxgitype.DXGI_MODE_DESC * currentMode)
                    print("Change Mode 6")
                    mode = modes[currentMode]
                    print("Switching to mode %u / %u, %ux%u@%uHz (%u, %u, %u)" % (currentMode+1, numModes, mode.Width, mode.Height, mode.RefreshRate.Numerator , mode.Scaling, mode.ScanlineOrdering, mode.Format))# mode.RefreshRate.Numerator/ mode.RefreshRate.Denominator
                    dxgi_swap_chain.ResizeTarget(ctypes.byref(modes[currentMode]))
                    changeThisFrame = True
                modeChanged = True
            # end of if changeMode
            
            # Check fullscreen state
            newFullscreen = ctypes.wintypes.BOOL()
            dxgi_swap_chain.GetFullscreenState(ctypes.byref(newFullscreen), None)

            # Resize if needed
            rect = RECT()
            ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))
            width  = rect.right
            height = rect.bottom

            if (width != backBufferDesc.Width) or (height != backBufferDesc.Height) or changeThisFrame or (newFullscreen != currentFullScreen):
                #d3d_device_context.ClearState() # Error here OSError:[WinError 2173] Windows Error 0x87d
                pRTV.Release()
                dxgi_swap_chain.ResizeBuffers(0, 0, 0, Direct3D.PyIdl.dxgiformat.DXGI_FORMAT_UNKNOWN, Direct3D.PyIdl.dxgi.DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH)

                # Recreate render target
                dxgi_swap_chain.GetBuffer(0, pBackBuffer._iid_, ctypes.byref(pBackBuffer))
                d3d_device.CreateRenderTargetView(pBackBuffer, None, ctypes.byref(pRTV))
                pBackBuffer.GetDesc(ctypes.byref(backBufferDesc))
                pBackBuffer.Release()

            # Remember fullscreen state
            currentFullScreen = newFullscreen

            # Clear backbuffer
            color = (ctypes.c_float * 4)()
            color[0] = 1.0
            color[1] = 1.0
            color[2] = 1.0
            color[3] = 0.0
            # d3d_device_context.ClearRenderTargetView(pRTV, color) # Error here OSError:[WinError 2173] Windows Error 0x87d
            # Present
            dxgi_swap_chain.Present(1, 0)
            # end of else PeekMessageW
    # Release
    dxgi_swap_chain.SetFullscreenState(False, None)
    # d3d_device_context.ClearState()
    pRTV.Release()
    print("pRTV released")
    #ID3D11Debug

    d3d_device.Release()
    print("d3d_device released")
    dxgi_swap_chain.Release()
    print("dxgi_swap_chain released")
    # debug interface
    #ctypes.windll.user32.UnregisterClassW(wcexw.lpszClassName, ctypes.c_ulonglong(wcexw.hInstance))
    print("exit")
    print(msg.wParam)
    return msg.wParam


if __name__ == '__main__':
    #dxgi.hello_test("Hello from module dxgi")

    sys.exit(MainWindowFrame())



    # d3d_texture = ctypes.POINTER(PyIdl.d3d11.ID3D11Texture2D)()
    # print(dxgi_swap_chain.GetBuffer)
    # print(ctypes.windll.dxgi)
    # print(ctypes.windll)
    # #print(ctypes.windll.Lz32) test
    # # print(os.path.dirname(sys.argv[0]))
    # # print(os.environ['PATH'])
    # kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    # kernel32.GetModuleHandleW.restype = wintypes.HMODULE
    # kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    # print('kernel32 : ', kernel32)
    # print("getmodule :", ctypes.windll.kernel32.GetModuleHandleW(b'kernel32.dll'))
    # print("getmodule dxgi : ", ctypes.windll.kernel32.GetModuleHandleW(b'Dxgidebug.lib'))
    # print("getmodule dxgi : ", ctypes.windll.kernel32.GetModuleHandleW(b'Dxgi.lib'))
    # print("getprocaddr : ", ctypes.windll.kernel32.GetProcAddress(ctypes.windll.kernel32.GetModuleHandleW(b'Dxgidebug.lib'), "DXGIGetDebugInterface"))
    # print(ctypes.windll.dxgidebug)
    # print(ctypes.windll.dxgidebug.DXGIGetDebugInterface)
    # h = ctypes.c_void_p(0)
    # print("fixing test byref  : ", ctypes.byref(dxgi_swap_chain._iid_))
    # print("fixing test direct : ", PyIdl.dxgi.IDXGISwapChain._iid_)

    # testing = ctypes.windll.dxgidebug.DXGIGetDebugInterface(dxgi_swap_chain._iid_, ctypes.byref(h))
    # print("testing     : ", hex(testing)) # HRESULT renvoie un 0x80004002 => NO_INTERFACE
    # print("direct call : ", hex(ctypes.windll.dxgidebug.DXGIGetDebugInterface(dxgi_swap_chain._iid_, ctypes.byref(h))))

    # handle = ctypes.c_void_p(0)
    # print(PyIdl.d3d11.ID3D11Texture2D._iid_)
    # print(PyIdl.d3d11.ID3D11Resource._iid_)
    # print(PyIdl.d3d11.ID3D11DeviceChild._iid_)
    # d3d_resource = ctypes.POINTER(PyIdl.d3d11.ID3D11Resource)()
    # print("getBuffer Test")
    # print(ctypes.byref(d3d_texture._iid_))
    # iid_text = d3d_texture._iid_
    # print("iid_text : ", iid_text)
    # hResult = dxgi_swap_chain.GetBuffer(0, d3d_texture._iid_,ctypes.byref(d3d_texture))
    # if hResult == 0:
    #     print("yes")
    # else:
    #     print("no")
    #     print(dxgi_swap_chain.GetBuffer(0, d3d_texture._iid_,ctypes.byref(d3d_texture)))
    # # return DXGI_ERROR_INVALID_CALL
    
    # pRTV = ctypes.POINTER(PyIdl.d3d11.ID3D11RenderTargetView)()
    # pRTV  = d3d_device.QueryInterface(PyIdl.d3d11.ID3D11RenderTargetView)
    # hResult = d3d_device.CreateRenderTargetView(ctypes.byref(d3d_resource), None, ctypes.byref(pRTV))
    # print("hResult : pRTV", hResult)

    # Example from source code in GameCap\Test
    # d3d_device_context.OMSetRenderTargets(1, pRTV, None) 
    
    # # np_float_rgba = numpy.array((0,0,0,1), dtype=ctypes.c_float)
    # # print(np_float_rgba)
    # # x = np_float_rgba.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    # # print(np_float_rgba)
    # d3dxClr = D3DXCOLOR()
    # ctypes.memset(ctypes.addressof(d3dxClr),0, ctypes.sizeof(d3dxClr))
    # d3dxClr.r = 0.0
    # d3dxClr.g = 0.0
    # d3dxClr.b = 0.0
    # d3dxClr.a = 1.0
    # print(d3dxClr)
    # four_float = ctypes.c_float * 4
    # float_rgba = four_float(d3dxClr.r, d3dxClr.g, d3dxClr.b, d3dxClr.a)
    # print(ctypes.byref(float_rgba))
    # print(float_rgba)
    # #d3d_device_context.ClearRenderTargetView(pRTV, float_rgba)


# https://hakril.github.io/PythonForWindows/build/html/winerror_generated.html



        # print("1 IN OFFICIAL : ", ctypes.POINTER(comtypes.IUnknown))
        # print("1 IN REAL     : ", self.__m_Device)
        # print("1 IN REAL     : ", ctypes.byref(self.__m_Device))
        # print(" ============== ")
        # print("2 IN OFFICIAL : ", wintypes.HWND)
        # print("2 IN REAL     : ", Window)
        # print(" ============== ")
        # print("3 IN OFFICIAL : ", ctypes.POINTER(DXGI_SWAP_CHAIN_DESC1))
        # print("3 IN REAL     : ", SwapChainDesc)
        # #SwapChainDesc = ctypes.pointer(SwapChainDesc)
        # print("3 IN REAL     : ", SwapChainDesc)
        # print(" ============== ")
        # print("4 IN OFFICIAL : ", ctypes.POINTER(DXGI_SWAP_CHAIN_FULLSCREEN_DESC))
        # print("4 IN OFFICIAL : ", ctypes.POINTER(DXGI_SWAP_CHAIN_FULLSCREEN_DESC))
        # print("4 IN REAL     : ", None)
        # print(" ============== ")
        # print("5 IN OFFICIAL : ", ctypes.POINTER(IDXGIOutput))
        # print("5 IN REAL     : ", None)
        # print(" ============== ")
        # print("6 IN OFFICIAL : ", ctypes.POINTER(ctypes.POINTER(IDXGISwapChain1)))
        # print("6 IN REAL     : ", self.__m_SwapChain)
        # print("6 IN REAL     : ", ctypes.POINTER(ctypes.c_char_p))
        # print("6 IN REAL     : ", ctypes.pointer(self.__m_SwapChain))
        # #self.__m_SwapChain = ctypes.pointer(self.__m_SwapChain)
        # print("6 IN REAL     : ", ctypes.byref(self.__m_SwapChain))
        # print("6 IN REAL     : ", ctypes.byref(self.__m_SwapChain))
        # print("6 IN REAL     : ", ctypes.addressof(self.__m_SwapChain))
        # print(" ============== ")
        # #temp = ctypes.c_void_p(0)
        # #swapChain_Test = ctypes.POINTER(IDXGISwapChain)()
        # #ctypes.memset(swapChain_Test, 0, ctypes.sizeof(swapChain_Test))
        # #hr = self.__m_Factory.CreateSwapChainForComposition(self.__m_Device, SwapChainDesc, None, self.__m_SwapChain)
        # #print(hr)
        # #hr = self.__m_Factory.CreateSwapChainForCoreWindow(self.__m_Device, Window, SwapChainDesc, None, self.__m_SwapChain)
        # dxgiDebug = ctypes.POINTER(IDXGIDebug)()
        # print(dxgiDebug)
        # print(IDXGIDebug._iid_)
        # ctypes.windll.dxgidebug.DXGIGetDebugInterface(IDXGIDebug._iid_, ctypes.byref(dxgiDebug))
        # print("dxgiDebug test : ", dxgiDebug)
        # #print(tt)
        # dxgiDebugRLO = DXGI_DEBUG_RLO_FLAGS()
        # ctypes.memset(ctypes.addressof(dxgiDebugRLO), 0, ctypes.sizeof(DXGI_DEBUG_RLO_FLAGS))
        # print(IDXGISwapChain1._iid_)
        # print(ctypes.byref(IDXGISwapChain1._iid_))
        # print(IDXGIFactory2._iid_)
        # print(self.__m_Factory._iid_)
        # print(self.__m_Factory)
        
        # print(comtypes.GUID)
        # print("test reportlive : ", dxgiDebug.ReportLiveObjects(ctypes.byref(self.__m_SwapChain._iid_), 4))
        # print(ctypes.windll.dxgidebug.DXGIGetDebugInterface(IDXGISwapChain1._iid_, ctypes.byref(self.__m_SwapChain)))
        # print(ctypes.windll.dxgidebug.DXGIGetDebugInterface(IDXGIFactory2._iid_, ctypes.byref(self.__m_Factory)))
        # # Valeur de retour : 0x80004002 : E_NOINTERFACE : No Such Interface Supported
        # # print(dxgiDebug)
        # # print(ctypes.windll.dxgidebug.DXGIGetDebugInterface)
        # # print(ctypes.windll.dxgidebug.DXGIGetDebugInterface(IDXGISwapChain1._iid_, ctypes.byref(self.__m_SwapChain)))