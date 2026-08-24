# pyDXGID3D

[![CI](https://github.com/Hellikandra/pyDXGID3D/actions/workflows/ci.yml/badge.svg)](https://github.com/Hellikandra/pyDXGID3D/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python `ctypes` / `comtypes` bindings for **DXGI** and **Direct3D 11**, translated from the
Windows SDK interface definition files.

> **Status: pre-alpha.** The binding layer for DXGI 1.0–1.2 and Direct3D 11.0 is complete
> and usable. The sample application in the repository root does **not** run. See
> [What works today](#what-works-today).

## What works today

Measured against the `.idl` files in Windows SDK 10.0.26100.0:

| Area | Interfaces | Methods | Status |
| --- | --- | --- | --- |
| DXGI 1.0 (`dxgi.idl`) | 14 / 14 | 56 / 56 | ✅ complete |
| DXGI 1.2 (`dxgi1_2.idl`) | 9 / 9 | 43 / 43 | ✅ complete |
| DXGI debug (`dxgidebug.h`) | 3 / 3 | — | ✅ complete |
| Direct3D 11.0 (`d3d11.idl`) | 41 / 41 | 272 / 274 | ⚠️ near-complete |
| D3D11 SDK layers | 6 / 6 | 37 / 54 | ⚠️ partial |
| D3D common (`d3dcommon.idl`) | 2 / 2 | 4 / 4 | ✅ complete |
| **Total** | **75** | **408** | |

All implemented interfaces carry a verified IID.

`IDXGIOutputDuplication` — the Desktop Duplication API — is declared in full.

## What does not work

- **The sample application.** `DesktopDuplication.py`, `OutputManager.py` and
  `ThreadManager.py` are a partial port of Microsoft's C++ desktop duplication sample.
  Nothing calls `DuplicateOutput`, and several defects sit on the paths that execute
  first. Treat these files as work in progress, not as an example to copy.
- **There are no DLL entry points yet.** The package declares interfaces but not
  `CreateDXGIFactory` or `D3D11CreateDevice`, so callers currently have to reach into
  `ctypes.windll` themselves.
- **There is no test suite.**

## Planned

In priority order. See `.claude/analysis/` for the full plan.

- DXGI 1.3 – 1.6 — including `IDXGIOutput5::DuplicateOutput1`
- Direct3D 11.1 – 11.4 — including `ID3D11Multithread` and `ID3D11Fence`
- Direct3D 12 — `d3d12`, `d3d12sdklayers`, `d3d12video`, `d3d12compatibility` (127 interfaces)
- A desktop-duplication capture API built on top of the bindings

**Direct3D 10 and Direct3D 9 are deliberately out of scope.**

## Requirements

- Windows 10 or 11
- Python 3.8 or later
- [`comtypes`](https://pypi.org/project/comtypes/) 1.2 or later

```bash
pip install comtypes
```

## Layout

```
Direct3D/PyIdl/     Translated interface definitions, one module per .idl
  dxgi.py             dxgi.idl
  dxgi1_2.py          dxgi1_2.idl        - includes IDXGIOutputDuplication
  dxgicommon.py       dxgicommon.idl
  dxgiformat.py       dxgiformat.idl     - DXGI_FORMAT
  dxgitype.py         dxgitype.idl
  dxgidebug.py        dxgidebug.h        - header-only in the SDK
  d3d11.py            d3d11.idl
  d3d11sdklayers.py   d3d11sdklayers.idl
  d3dcommon.py        d3dcommon.idl

DesktopDuplication.py   Sample application - does not currently run
OutputManager.py        Sample application - does not currently run
ThreadManager.py        Sample application - stub
VertexShader.py         Compiled DXBC blob used by the sample
PixelShader.py          Compiled DXBC blob used by the sample
```

## Source SDK

The bindings were translated from **Windows SDK 10.0.19041.0** (version 2004, 2020-12-16)
and are verified against **10.0.26100.0**. Interface names, method order, structure layouts
and IIDs come from the SDK's `.idl` files — see [NOTICE](NOTICE).

## References

### Microsoft documentation

- [DXGI — DirectX Graphics Infrastructure](https://docs.microsoft.com/en-us/windows/win32/api/_direct3ddxgi/)
- [Direct3D 11 Graphics](https://docs.microsoft.com/en-us/windows/win32/api/_direct3d11/)
- [Direct3D 12 Graphics](https://docs.microsoft.com/en-us/windows/win32/api/_direct3d12/)

### Implementations consulted

- [SerpentAI / D3DShot](https://github.com/SerpentAI/D3DShot)
- [DXGI desktop duplication sample (C++)](https://github.com/microsoftarchive/msdn-code-gallery-microsoft/tree/master/Official%20Windows%20Platform%20Sample/DXGI%20desktop%20duplication%20sample)

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT — see [LICENSE](LICENSE). Third-party attribution is in [NOTICE](NOTICE).
