#define DEBUG
#pragma region Includes
#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include <d3d11.h>

#pragma comment (lib, "dxgi.lib")
#pragma comment (lib, "d3d11.lib")
#pragma endregion

// Release COM object
#define SAFE_RELEASE(P) if(P){ P->Release(); P = NULL;}

#pragma region Window Proc
LRESULT CALLBACK WndProc(HWND hWnd, UINT uMessage, WPARAM wParam, LPARAM lParam) {
    PAINTSTRUCT vPainStruct = { 0 };
    HDC vDc(nullptr);

    switch(uMessage) {
        case WM_PAINT:
            vDc = BeginPaint(hWnd, &vPainStruct);
            EndPaint(hWnd, &vPainStruct);
            return FALSE;
            break;
        case WM_ERASEBKGND:
            // Don't erase background!
            return TRUE;
            break;
        case WM_CLOSE:
            DestroyWindow(hWnd);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        default:
            break;
    }

    return DefWindowProc(hWnd, uMessage, wParam, lParam);
}
#pragma endregion

int main() {
#pragma region Variables
    HINSTANCE                   vInstance = GetModuleHandle(nullptr);
    HWND                        vHwnd = nullptr;
    D3D_DRIVER_TYPE             vDriverType = D3D_DRIVER_TYPE_UNKNOWN;
    D3D_FEATURE_LEVEL           vFeatureLevel = D3D_FEATURE_LEVEL_11_0;
    IDXGIFactory                *vDxgiFactory = NULL;
    IDXGIAdapter                *vDxgiAdapter = nullptr;
    ID3D11Device                *vD3dDevice = nullptr;
    ID3D11DeviceContext         *vD3dContext = nullptr;
    IDXGISwapChain              *vSwapChain = nullptr;
    ID3D11Texture2D             *vBackBuffer = NULL;
    ID3D11RenderTargetView      *vRenderTargetView = nullptr;
#ifdef _DEBUG
    ID3D11Debug                 *vDebugger = nullptr;
    ID3D11InfoQueue             *vInfoQueue = nullptr;
#endif
#pragma endregion

#pragma region Init Window
    // Register class
    WNDCLASSEX vWndClass;
    ZeroMemory(&vWndClass, sizeof(vWndClass));
    vWndClass.cbSize = sizeof(WNDCLASSEX);
    vWndClass.style = 0; // CS_HREDRAW | CS_VREDRAW (draw in loop, no need for WM_PAINT)
    vWndClass.lpfnWndProc = WndProc;
    vWndClass.cbClsExtra = 0;
    vWndClass.cbWndExtra = 0;
    vWndClass.hInstance = vInstance;
    vWndClass.hIcon = 0;
    vWndClass.hCursor = LoadCursor(nullptr, IDC_ARROW);
    vWndClass.hbrBackground = nullptr;
    vWndClass.lpszMenuName = nullptr;
    vWndClass.lpszClassName = L"D3d11Window";
    vWndClass.hIconSm = 0;
    if(!RegisterClassEx(&vWndClass)) {
        DebugBreak();
        return 0;
    }

    // Create window
    RECT vWindowRect = { 0, 0, 640, 480 };
    vHwnd = CreateWindowEx(
        0, vWndClass.lpszClassName, L"D3D11", WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT,
        vWindowRect.right - vWindowRect.left, vWindowRect.bottom - vWindowRect.top,
        nullptr, nullptr, vInstance,
        nullptr);
    if(!vHwnd) {
        DebugBreak();
        return 0;
    }

    ShowWindow(vHwnd, SW_SHOWDEFAULT);
#pragma endregion

#pragma region Initialization
    RECT vClientRect = { 0 };
    GetClientRect(vHwnd, &vClientRect);
    UINT vWidth = vClientRect.right - vClientRect.left;
    UINT vHeight = vClientRect.bottom - vClientRect.top;

    if(FAILED(CreateDXGIFactory(__uuidof(IDXGIFactory), (void**)(&vDxgiFactory)))) {
        DebugBreak();
        return 0;
    }

    if(FAILED(vDxgiFactory->EnumAdapters(0, &vDxgiAdapter))) {
        DebugBreak();
        return 0;
    }

    D3D_FEATURE_LEVEL vRequestedFeatureLevels[] = {
        D3D_FEATURE_LEVEL_11_0,
        // D3D_FEATURE_LEVEL_10_1,
        // D3D_FEATURE_LEVEL_10_0
    };

    UINT vNumFeatureLevels = ARRAYSIZE(vRequestedFeatureLevels);

    UINT vDeviceFlags = 0;
#ifdef _DEBUG
    vDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;
#endif

    if(FAILED(D3D11CreateDevice(
        vDxgiAdapter,
        vDriverType,
        nullptr,
        vDeviceFlags,
        vRequestedFeatureLevels,
        vNumFeatureLevels,
        D3D11_SDK_VERSION,
        &vD3dDevice,
        &vFeatureLevel,
        &vD3dContext))) {
        return 0;
    }

    UINT vMsaaQuality = 0;
    if(FAILED(vD3dDevice->CheckMultisampleQualityLevels(DXGI_FORMAT_R8G8B8A8_UNORM, 4, &vMsaaQuality)) || (vMsaaQuality < 1)) {
        return 0;
    }
    printf("MsaaQuality of max %d supported for count 4\r\n", vMsaaQuality);

    DXGI_SWAP_CHAIN_DESC vSwapChainDesc;
    ZeroMemory(&vSwapChainDesc, sizeof(vSwapChainDesc));
    vSwapChainDesc.BufferCount = 2;
    vSwapChainDesc.BufferDesc.Width = vWidth;
    vSwapChainDesc.BufferDesc.Height = vHeight;
    vSwapChainDesc.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    vSwapChainDesc.BufferDesc.RefreshRate.Numerator = 60;
    vSwapChainDesc.BufferDesc.RefreshRate.Denominator = 1;
    vSwapChainDesc.BufferDesc.ScanlineOrdering = DXGI_MODE_SCANLINE_ORDER_UNSPECIFIED;
    vSwapChainDesc.BufferDesc.Scaling = DXGI_MODE_SCALING_CENTERED;
    vSwapChainDesc.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    vSwapChainDesc.SampleDesc.Count = 4; // set 1 to work
    vSwapChainDesc.SampleDesc.Quality = vMsaaQuality - 1;
    vSwapChainDesc.OutputWindow = vHwnd;
    vSwapChainDesc.Windowed = true;
    vSwapChainDesc.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;
    vSwapChainDesc.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;

    if(FAILED(vDxgiFactory->CreateSwapChain(vD3dDevice, &vSwapChainDesc, &vSwapChain))) {
        return 0;
    }

    if(FAILED(vSwapChain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&vBackBuffer))) {
        return 0;
    }

    if(FAILED(vD3dDevice->CreateRenderTargetView(vBackBuffer, nullptr, &vRenderTargetView))) {
        return 0;
    }

    vD3dContext->OMSetRenderTargets(1, &vRenderTargetView, nullptr);

    D3D11_VIEWPORT vViewport = { 0 };
    vViewport.Width = static_cast<FLOAT>(vWidth);
    vViewport.Height = static_cast<FLOAT>(vHeight);
    vViewport.MinDepth = D3D11_MIN_DEPTH;
    vViewport.MaxDepth = D3D11_MAX_DEPTH;
    vViewport.TopLeftX = 0;
    vViewport.TopLeftY = 0;
    vD3dContext->RSSetViewports(1, &vViewport);
#pragma endregion

#pragma region Game Loop
    MSG vMessage = { 0 };
    while(WM_QUIT != vMessage.message) {
        while(PeekMessage(&vMessage, 0, 0, 0, PM_REMOVE)) {
            TranslateMessage(&vMessage);
            DispatchMessage(&vMessage);
        }

        if(WM_QUIT == vMessage.message) {
            break;
        }

#pragma region Render
        float vClearColor[4] = { 1.0f, 0.0f, 0.0f, 1.0f };
        vD3dContext->ClearRenderTargetView(vRenderTargetView, vClearColor);
        vSwapChain->Present(true, 0); // vsync
#pragma endregion
    }
#pragma endregion

#pragma region Cleanup
    if(vSwapChain) {
        vSwapChain->SetFullscreenState(false, nullptr);
    }
    if(vD3dContext) {
        vD3dContext->ClearState();
    }

    SAFE_RELEASE(vRenderTargetView);
    SAFE_RELEASE(vBackBuffer);
    SAFE_RELEASE(vSwapChain);
    SAFE_RELEASE(vD3dContext);
    SAFE_RELEASE(vD3dDevice);
    SAFE_RELEASE(vDxgiFactory);
    SAFE_RELEASE(vDxgiAdapter);

#ifdef _DEBUG
    SAFE_RELEASE(vDebugger);
    SAFE_RELEASE(vInfoQueue);
#endif


#pragma endregion

    _getch();
    return (int)vMessage.wParam;
}