# pyDXGID3D

[![CI](https://github.com/Hellikandra/pyDXGID3D/actions/workflows/ci.yml/badge.svg)](https://github.com/Hellikandra/pyDXGID3D/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python `ctypes` / `comtypes` bindings for **DXGI** and **Direct3D 11**, translated from the
Windows SDK interface definition files.

> **Status: alpha.** Every DXGI and every Direct3D 11 interface in the Windows SDK is
> translated and machine-verified against it. Desktop Duplication captures frames on real
> hardware through these bindings. The sample application in the repository root still does
> **not** run. See [What works today](#what-works-today).

## What works today

Measured against the `.idl` files in Windows SDK 10.0.26100.0, by
`tools/idl.py` — not by hand:

| Area | Interfaces | Methods | Status |
| --- | --- | --- | --- |
| DXGI 1.0 (`dxgi.idl`) | 14 / 14 | 56 / 56 | complete |
| DXGI 1.2 (`dxgi1_2.idl`) | 9 / 9 | 43 / 43 | complete |
| DXGI 1.3 (`dxgi1_3.idl`) | 8 / 8 | 25 / 25 | complete |
| DXGI 1.4 (`dxgi1_4.idl`) | 4 / 4 | 13 / 13 | complete |
| DXGI 1.5 (`dxgi1_5.idl`) | 4 / 4 | 5 / 5 | complete |
| DXGI 1.6 (`dxgi1_6.idl`) | 4 / 4 | 6 / 6 | complete |
| DXGI debug (`dxgidebug.h`) | 3 / 3 | — | complete |
| Direct3D 11.0 (`d3d11.idl`) | 41 / 41 | 274 / 274 | complete |
| Direct3D 11.1 (`d3d11_1.idl`) | 9 / 9 | 51 / 51 | complete |
| Direct3D 11.2 (`d3d11_2.idl`) | 2 / 2 | 14 / 14 | complete |
| Direct3D 11.3 (`d3d11_3.idl`) | 11 / 11 | 26 / 26 | complete |
| Direct3D 11.4 (`d3d11_4.idl`) | 6 / 6 | 16 / 16 | complete |
| D3D11 SDK layers | 6 / 6 | 50 / 50 | complete |
| D3D common (`d3dcommon.idl`) | 2 / 2 | 4 / 4 | complete |
| **Total** | **120** | **583** | |

Every implemented interface carries a verified IID, and every method sits at the vtable slot
the SDK gives it — asserted, not assumed.

**Structure layout is checked against a compiled measurement.** `tools/layout_probe.py`
builds a C program that includes the SDK headers and prints `sizeof` and `offsetof` for
every structure; the result is committed as `tests/data/struct_layout.json`. All **207
structures and 797 field offsets** match.

### Desktop Duplication captures

```
python tools/dxgi_report.py --frames 60
```

walks the whole path — factory, adapter, output, device, `DuplicateOutput`,
`AcquireNextFrame`, `CopyResource`, `Map` — and prints a real pixel value at the end. On the
development machine it sustains the panel's refresh rate with zero timeouts.

`--benchmark` reports where the time goes and what the pipeline could do without a display
in the way; `--sweep` measures readback cost against capture size.

### DLL entry points

`Direct3D/PyIdl/functions.py` binds `CreateDXGIFactory`, `CreateDXGIFactory1`,
`CreateDXGIFactory2`, `D3D11CreateDevice`, `D3D11CreateDeviceAndSwapChain`,
`DXGIGetDebugInterface`, `DXGIGetDebugInterface1` and `DXGIDeclareAdapterRemovalSupport`
with explicit `argtypes` and `restype`. `Direct3D/PyIdl/status.py` turns the HRESULTs they
return into named exceptions.

### Generated, not hand-written

`Direct3D/PyIdl/d3d11.py`, `d3d11_1.py` … `d3d11_4.py` and `dxgi1_3.py` … `dxgi1_6.py` are
generated from the SDK `.idl` files by `tools/generate.py`. Regenerate any of them with:

```bash
python tools/generate.py d3d11.idl -o Direct3D/PyIdl/d3d11.py
```

The output is idempotent: regenerating a module that is already current produces a byte
-identical file, so the diff is always the change and never the tooling.

## Tests

```bash
pip install pytest comtypes
python -m pytest tests -q
```

79 tests in four tiers:

- **Tier 0** — abstract-syntax checks on the binding modules. Runs on any OS, no comtypes.
- **Tier 1** — bindings against the SDK: vtable order, method signatures, structure sizes
  and field offsets, IIDs. Needs Windows and comtypes; uses **WARP**, the software
  rasteriser, so it runs on a machine with no GPU.
- **Tier 2** — a real adapter and a real display.
- **Tier 3** — throughput.

## What does not work

- **The sample application.** `DesktopDuplication.py`, `OutputManager.py` and
  `ThreadManager.py` are a partial port of Microsoft's C++ desktop duplication sample.
  Nothing calls `DuplicateOutput`, and several defects sit on the paths that execute
  first. Treat these files as work in progress, not as an example to copy — use
  `tools/dxgi_report.py` instead.
- **There is no capture API yet.** The bindings are complete; the ergonomic layer on top of
  them — pick an output, get frames, recover from `DXGI_ERROR_ACCESS_LOST` — is not written.

## Planned

In priority order:

- A desktop-duplication capture API built on top of the bindings
- Direct3D 12 — `d3d12`, `d3d12sdklayers`, `d3d12video`, `d3d12compatibility`
  (127 interfaces, 451 methods)

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
  dxgi1_3.py          dxgi1_3.idl        - generated
  dxgi1_4.py          dxgi1_4.idl        - generated
  dxgi1_5.py          dxgi1_5.idl        - generated
  dxgi1_6.py          dxgi1_6.idl        - generated
  dxgicommon.py       dxgicommon.idl
  dxgiformat.py       dxgiformat.idl     - DXGI_FORMAT
  dxgitype.py         dxgitype.idl
  dxgidebug.py        dxgidebug.h        - header-only in the SDK
  d3d11.py            d3d11.idl          - generated
  d3d11_1.py          d3d11_1.idl        - generated
  d3d11_2.py          d3d11_2.idl        - generated
  d3d11_3.py          d3d11_3.idl        - generated
  d3d11_4.py          d3d11_4.idl        - generated
  d3d11sdklayers.py   d3d11sdklayers.idl
  d3dcommon.py        d3dcommon.idl
  functions.py        DLL entry points
  status.py           HRESULTs as named exceptions
  typemap.py          the canonical IDL-to-ctypes type table

tools/              Generator, SDK parser, layout probe, diagnostics
tests/              Four tiers - see Tests above

DesktopDuplication.py   Sample application - does not currently run
OutputManager.py        Sample application - does not currently run
ThreadManager.py        Sample application - stub
VertexShader.py         Compiled DXBC blob used by the sample
PixelShader.py          Compiled DXBC blob used by the sample
```

## Source SDK

The hand-written modules were translated from **Windows SDK 10.0.19041.0** (version 2004,
2020-12-16). The generated modules are produced from, and every module is verified
against, **10.0.26100.0**. Interface names, method order, structure layouts
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
