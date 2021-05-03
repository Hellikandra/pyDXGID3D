import sys
import ctypes
import ctypes.wintypes as wintypes
import enum
import numpy
import comtypes
import os


WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM)

CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001

IDC_ARROW = 32512

SW_SHOW = 5

WM_DESTROY = 2

WS_OVERLAPPED       = 0x00000000#L
WS_CAPTION          = 0x00C00000#L
WS_SYSMENU          = 0x00080000#L
WS_THICKFRAME       = 0x00040000#L
WS_MINIMIZEBOX      = 0x00020000#L
WS_MAXIMIZEBOX      = 0x00010000#L   
WS_OVERLAPPEDWINDOW = (WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX)


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
				('bottom', ctypes.c_long)
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

def WndProc(hwnd, uMsg, wParam, lParam):
	if uMsg == WM_DESTROY:
		ctypes.windll.user32.PostQuitMessage(0)
	else:
		return ctypes.windll.user32.DefWindowProcW(hwnd, uMsg, ctypes.c_ulonglong(wParam), ctypes.c_longlong(lParam))
	return 0

def WinMain():

	# Register Class
	Wc = WNDCLASSEXW()
	Wc.cbSize        = ctypes.sizeof(WNDCLASSEXW)
	Wc.style         = CS_HREDRAW | CS_VREDRAW
	Wc.lpfnWndProc   = WNDPROC(WndProc)
	Wc.cbClsExtra    = 0
	Wc.cbWndExtra    = 0
	Wc.hInstance     = ctypes.windll.kernel32.GetModuleHandleW(None)
	Wc.hIcon         = None
	Wc.hCursor       = ctypes.windll.user32.LoadCursorW(None, ctypes.c_wchar_p(IDC_ARROW))
	Wc.hbrBackground = None
	Wc.lpszMenuName  = None
	Wc.lpszClassName = u"WinMain"
	Wc.hIconSm       = None
	if not ctypes.windll.user32.RegisterClassExW(ctypes.byref(Wc)):
		raise ctypes.WinError()

	WindowRect = RECT()
	WindowRect.left   = 0
	WindowRect.top    = 0
	WindowRect.right  = 800
	WindowRect.bottom = 600
	ctypes.windll.user32.AdjustWindowRectEx(ctypes.byref(WindowRect), WS_OVERLAPPEDWINDOW , False, 0)

	WindowHandle = ctypes.windll.user32.CreateWindowExW(0, Wc.lpszClassName, u"DXGI desktop duplication sample",
		ctypes.c_int(WS_OVERLAPPEDWINDOW),
		0,0,
		WindowRect.right - WindowRect.left, WindowRect.bottom - WindowRect.top,
		None, None, ctypes.c_ulonglong(Wc.hInstance), None)

	if not WindowHandle:
		raise ctypes.WinError()

	ctypes.windll.user32.ShowWindow(WindowHandle, SW_SHOW)
	ctypes.windll.user32.UpdateWindow(WindowHandle)

	msg = MSG()
	while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
		ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
		ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

if __name__ == '__main__':
	sys.exit(WinMain())

