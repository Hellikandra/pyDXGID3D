# pyDXGID3D

[![CI](https://github.com/Hellikandra/pyDXGID3D/actions/workflows/ci.yml/badge.svg)](https://github.com/Hellikandra/pyDXGID3D/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python `ctypes` / `comtypes` bindings for **DXGI** and **Direct3D 11**, translated from the
Windows SDK interface definition files.

> **Status: alpha.** Every DXGI and every Direct3D 11 interface in the Windows SDK is
> translated and machine-verified against it, and `Direct3D.Capture` turns that into a
> working Desktop Duplication API. The sample application in the repository root still
> does **not** run and is superseded by it. See [What works today](#what-works-today).

## What works today

Measured against the `.idl` files in Windows SDK 10.0.26100.0, by
`tools/idl.py` — not by hand:

| Area | Interfaces | Methods | Status |
| --- | --- | --- | --- |
| DXGI 1.0 – 1.6 | 43 / 43 | 148 / 148 | complete |
| DXGI debug (`dxgidebug.h`) | 3 / 3 | — | complete |
| Direct3D 11.0 – 11.4 | 69 / 69 | 381 / 381 | complete |
| D3D11 SDK layers + common | 8 / 8 | 54 / 54 | complete |
| Direct3D 12 | 100 / 100 | 350 / 350 | declared |
| D3D12 video | 27 / 27 | 101 / 101 | declared |
| Interop (`d3d11on12`, `d3d12compatibility`) | 4 / 4 | 9 / 9 | declared |
| **Total** | **251 / 251** | **1043 / 1043** | |

**Every interface in the target set is translated.** There is nothing left to port.

Every implemented interface carries a verified IID, and every method sits at the vtable slot
the SDK gives it — asserted, not assumed.

**Structure layout is checked against a compiled measurement.** `tools/layout_probe.py`
builds a C program that includes the SDK headers and prints `sizeof` and `offsetof` for
every structure; the result is committed as `tests/data/struct_layout.json`. All **649
structures and 2480 field offsets** match.

### "Complete" means two different things in that table

**DXGI and Direct3D 11 are complete and exercised.** `Direct3D.Capture` drives them against
real hardware, and the test suite captures frames from an actual display.

**Direct3D 12 is complete and declared.** Every interface, method signature, structure and
enumeration matches the SDK — checked by the same instruments — but *no D3D12 code in this
repository has ever been executed*. Nothing here creates a D3D12 device. Treat it as a
correct transcription rather than as a tested binding, and expect to be the first person to
call any given method.

### The bindings, checked end to end

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

Fourteen of the binding modules are generated from the SDK `.idl` files by `tools/generate.py`. Regenerate any of them with:

```bash
python tools/generate.py d3d11.idl -o Direct3D/PyIdl/d3d11.py
```

The output is idempotent: regenerating a module that is already current produces a byte
-identical file, so the diff is always the change and never the tooling.

## Capturing the screen

```python
from Direct3D.Capture import enumerate_outputs, CaptureOptions, DesktopCapture

for output in enumerate_outputs():
    print(output)          # <Output 0 \\.\DISPLAY1 1920x1200 at (0,0) on 'Intel Iris Xe'>

options = CaptureOptions(output=0, region=(320, 180, 1600, 900))

with DesktopCapture(options) as capture:
    for frame in capture:
        process(frame.array)          # zero-copy view, this iteration only
```

Three names are the whole contract. Reaching past them into `Direct3D.PyIdl` means this
layer is missing something.

### Getting the pixels out

`frame.array` is a view over memory Direct3D mapped for one iteration. It stops being valid
the moment the loop moves on, and touching it afterwards raises `StaleFrameError` rather
than reading freed pages.

To keep a frame, copy it — and if you are capturing in a loop, hold one destination and
reuse it:

```python
import numpy

buffer = numpy.empty((capture.height, capture.width, 4), numpy.uint8)
with DesktopCapture(options) as capture:
    for frame in capture:
        process(frame.copy_into(buffer))
```

Measured at 1920×1200 BGRA (8.79 MB), timed as `Map` → deliver → `Unmap`:

| | ms/frame | pipeline capacity |
| --- | ---: | ---: |
| `frame.array` — zero copy | 2.63 | 353 fps |
| `frame.copy_into(buffer)` — reused destination | 3.76 | 253 fps |
| `frame.copy()` — allocates | 7.62 | 128 fps |

The gap between the last two is **not the copy**. It is page faults on a fresh 8.79 MB
allocation, about 3.9 ms of them, every frame. That is the entire reason `copy_into` exists.

`frame.memoryview` gives the same bytes with no numpy at all, padding included.

### What a frame carries

`width`, `height`, `pitch`, `format`, `shape`, `padded`, `timestamp_qpc` (the SDK's
`LastPresentTime`) and `accumulated`. Watch `accumulated`: a steady `1` means the loop is
keeping up, and anything higher means the desktop composed frames that were coalesced before
you got to them.

`pitch` is not `width * 4`. The driver rounds rows up to its own alignment.

### Recovering

A mode change, a resolution change, a session lock or a UAC prompt invalidates the
duplication and raises `DXGI_ERROR_ACCESS_LOST`. By default the capture rebuilds itself with
progressive back-off and carries on; `capture.rebuilds` counts how often. Pass
`on_access_lost='raise'` to handle it yourself, or `max_rebuilds=N` to give up eventually.

A removed device is not recoverable this way and raises `DeviceRemoved` immediately.

### Two things that stop it working

- **A fullscreen-exclusive application owns the display.** `DuplicateOutput` raises
  `Unsupported`. Borderless windowed is the fix.
- **There is no interactive desktop** — a disconnected RDP session, or a service. In that
  case `enumerate_outputs()` returns nothing at all.

### The frame rate is the display's

Desktop Duplication produces a frame when the desktop composes one, so a 60 Hz panel gives
at most 60 per second no matter how fast the game runs. On 144 Hz you get up to 144. If the
goal is more frames than the monitor shows, no desktop-level capture API can do it.

## Using this from your own project

```bash
pip install pyDXGID3D[numpy]
```

```python
from Direct3D.Capture import enumerate_outputs, CaptureOptions, DesktopCapture
```

**Those three names are the whole contract.** If you find yourself importing from
`Direct3D.PyIdl` to do something the capture API should do for you, that is a gap in this
package rather than a workaround you should keep — please say so.

Three things to know before you build on it:

**The frame is borrowed, not given.** `frame.array` is a view over pages Direct3D mapped for
one iteration. It stops being valid the moment the loop moves on. Touching it afterwards
raises `StaleFrameError` rather than reading freed memory — but only because the check is
there, so do not remove it.

**Reuse your destination.** `frame.copy()` allocates, and the allocation costs more than the
copy: about 3.9 ms of page faults on a full 1920×1200 frame, against 3.76 ms for the copy
itself. Hold one array outside the loop:

```python
buffer = numpy.empty((capture.height, capture.width, 4), numpy.uint8)
for frame in capture:
    process(frame.copy_into(buffer))
```

That is 253 fps of pipeline capacity instead of 128, for one line.

**numpy is optional.** Without it, `frame.memoryview` gives you the same bytes and every
piece of metadata still works. `frame.array` and `frame.copy()` raise an `ImportError` that
names the extra.

The packaging is asserted, not assumed: `tests/test_tier3_packaging.py` builds a wheel,
installs it into a throwaway virtual environment and captures a frame from a directory that
is not this repository, on every CI run.

## Examples

```
examples/screenshot.py     one frame to a PNG - the smallest complete thing
examples/region.py         a fixed crop, sustained, into a buffer you keep
examples/displays.py       every monitor, and which GPU drives each
examples/window.py         the area a window occupies - read its caveats
examples/record.py         to H.264, by piping raw frames to ffmpeg
examples/d3d12_device.py   a Direct3D 12 device, and what it will accept
```

They need nothing installed beyond the package: the PNG writer is forty lines of `zlib` in
`examples/_png.py` rather than a Pillow dependency.

### Will my game capture?

```bash
python tools/dxgi_report.py --game
```

names the window in front, works out which case it is in, and says what to change.

| what you want to capture | works | how |
| --- | --- | --- |
| a **borderless windowed** game | **yes, exactly** | it covers the output, so capture the output |
| a **fullscreen exclusive** game | **no** | `DuplicateOutput` raises `Unsupported`. Switch the game to borderless windowed - by far the most common cause of failure, and a setting in the game rather than anything here |
| a **windowed** game, or any window | **approximately** | crop to its DWM frame bounds; anything drawn on top is in the frame |
| an **occluded or minimised** window | **no** | Desktop Duplication returns the composed desktop, not a window's own content |

**`window.py` is approximate and says so.** Desktop Duplication captures an *output*, so
cropping to a window's rectangle also captures anything drawn on top of it. There is no fix
within this API — `Windows.Graphics.Capture` is the one that captures a window's own
content, and this package does not bind it.

## How much of this has actually been run

The suite proves the **declarations** match the SDK — vtable order, IIDs, structure sizes,
field offsets, parameter counts, return types. That is static, and it is thorough: 649
structures and 2,480 field offsets against a compiled measurement.

It is not the same as the code having been executed. `tools/exercise.py` measures that half:

```bash
python tools/exercise.py
```

It builds every COM object this machine can produce and calls every method that can be
called without changing anything — the `Get`, `Check`, `Is`, `Query` and `Enum` families —
reporting what worked. On the development machine that is 44 of the 68 interrogative methods
across 14 interfaces; the rest need an argument the tool will not invent, such as a real
resource or a named GUID.

That distinction matters. The two worst defects this project has had — 27 methods that
faulted the interpreter, and one that made every shader blob unreadable — were both wrong
return types, invisible to every static check, and found by calling a method rather than
reading it.

## Tests

```bash
pip install pytest comtypes
python -m pytest tests -q
```

290 tests in four tiers:

- **Tier 0** — abstract-syntax checks on the binding modules. Runs on any OS, no comtypes.
- **Tier 1** — bindings against the SDK: vtable order, method signatures, structure sizes
  and field offsets, IIDs. Needs Windows and comtypes; uses **WARP**, the software
  rasteriser, so it runs on a machine with no GPU.
- **Tier 2** — a real adapter and a real display.
- **Tier 3** — throughput, and the packaging check that builds a wheel and
  imports it from outside the repository.

Two are worth knowing about because they check what the others cannot.
`tools/render_probe.py` renders a known colour and captures it back — the only test that
the frame contains what was on screen rather than merely being the right shape. And
`tools/exercise.py` calls every method that cannot change anything, reporting how much of
the API has actually been executed as opposed to declared.

## What does not work

- **There is no GPU-side delivery.** `deliver='gpu'` — a shared handle and keyed mutex for a
  consumer doing its own GPU work — is designed but not built. Every frame comes back
  through system memory.
- **The cursor is not composited into the frame.** `IDXGIOutputDuplication` delivers the
  pointer shape separately; the bindings for it exist and nothing uses them yet.
  `CaptureOptions(cursor=True)` says so rather than silently ignoring the flag.
- **Nothing renders.** Direct3D 12 is bound and a device can be created, but no code here
  draws a triangle or encodes a video on the GPU. `d3d12video` in particular — hardware
  encode and decode — is declared and has never been executed.
- **Exact window capture is not possible with this API.** Cropping to a window's rectangle
  also captures whatever is drawn on top of it. See `examples/window.py`.

## Planned

In priority order:

- **A rendered frame.** `examples/d3d12_device.py` creates a device, queues, heaps and a root
  signature; nothing yet builds a pipeline state and draws. That is the step which would
  exercise the parts of Direct3D 12 that `tools/exercise.py` currently reports as untouched.
- **GPU-side delivery** — `deliver='gpu'`, a shared handle and keyed mutex, for a consumer
  that does its own GPU work rather than reading pixels back to system memory.
- **Cursor compositing**, using the pointer-shape interfaces that are already bound.

**Direct3D 10 and Direct3D 9 are deliberately out of scope.** So is
`Windows.Graphics.Capture`: it is the right API for exact window capture and it is a
different family (WinRT) that would double the surface of this package.

## Requirements

- Windows 10 or 11
- Python 3.8 or later
- [`comtypes`](https://pypi.org/project/comtypes/) 1.2 or later

```bash
pip install comtypes
```

## Layout

```
examples/           Runnable examples - see Examples above

Direct3D/Capture/   The capture API - this is what you import
  __init__.py         enumerate_outputs, CaptureOptions, DesktopCapture
  enumerate.py        outputs, each paired with the adapter that drives it
  options.py          CaptureOptions, validated at construction
  capture.py          DesktopCapture: the device, the duplication, the loop
  frame.py            Frame: array, copy, copy_into, metadata

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
  d3d12.py            d3d12.idl          - generated
  d3d12sdklayers.py   d3d12sdklayers.idl - generated
  d3d12video.py       d3d12video.idl     - generated
  d3d11on12.py        d3d11on12.idl      - generated
  d3d12compatibility.py                  - generated
  d3d11sdklayers.py   d3d11sdklayers.idl
  d3dcommon.py        d3dcommon.idl
  functions.py        DLL entry points
  status.py           HRESULTs as named exceptions
  typemap.py          the canonical IDL-to-ctypes type table

tools/              Generator, SDK parser, layout probe, diagnostics
  exercise.py         calls the API and reports what actually ran
  render_probe.py     renders a known colour and captures it back
  dxgi_report.py      end-to-end diagnostic and benchmark
  tier0_sandbox.py    runs tier 0 as a bare CI runner sees it
tests/              Four tiers - see Tests above

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
