# Changelog

## 0.2.0

The port is complete and the capture API works. First release worth a version
number.

### Bindings

**Every interface in the target set is translated: 251 of 251, and 1,043 of 1,043
methods.** Measured against the `.idl` files in Windows SDK 10.0.26100.0 by
`tools/idl.py`, not counted by hand.

- DXGI 1.0 – 1.6, and the header-only debug interfaces
- Direct3D 11.0 – 11.4, SDK layers, and D3D common
- Direct3D 12, its debug layer and its video interfaces
- `d3d11on12` and `d3d12compatibility`

Fourteen of the binding modules are **generated** from the SDK `.idl` files by
`tools/generate.py`, and regenerating one that is already current produces a
byte-identical file — so a diff is always the change and never the tooling.

**Structure layout is checked against a compiled measurement.**
`tools/layout_probe.py` builds a C program that includes the SDK headers and
prints `sizeof` and `offsetof` for every structure. All **649 structures and
2,480 field offsets** match.

### Capture

`Direct3D.Capture` — three names, and nothing else needs importing:

```python
from Direct3D.Capture import enumerate_outputs, CaptureOptions, DesktopCapture
```

- Outputs are enumerated **with the adapter that drives them**, so a device is
  created on the right GPU by construction. On a hybrid laptop the panel hangs
  off the integrated GPU and a device on the discrete one cannot duplicate it.
- Region cropping, done GPU-side with `CopySubresourceRegion`.
- Recovery from `DXGI_ERROR_ACCESS_LOST` with progressive back-off, so a screen
  lock or a mode change does not end the capture.
- **Zero steady-state allocation** — asserted, not claimed.
- Frames are borrowed, not given. Using one after its iteration raises
  `StaleFrameError` rather than reading freed memory.

Measured on the development machine at 1920×1200 BGRA: 60 fps sustained, with
`frame.array` costing 2.6 ms per frame as a zero-copy view and
`frame.copy_into(buffer)` 3.8 ms into an array you reuse.

### DLL entry points

`Direct3D.PyIdl.functions` declares fifteen exports with explicit `argtypes` and
`restype`, and routes every failure through `Direct3D.PyIdl.status` as a named
exception. Reaching into `ctypes.windll` yourself truncates handles on a 64-bit
build; this exists so nobody has to.

### Examples

`examples/` — screenshot, region capture, display enumeration, window capture,
recording to H.264 via ffmpeg, and a Direct3D 12 device. They need nothing
installed beyond the package: the PNG writer is forty lines of `zlib`.

### Tests

**290 tests in four tiers.** Tier 0 is static and runs anywhere; tier 1 needs
comtypes and uses WARP, so it runs on a machine with no GPU; tier 2 needs a real
display; tier 3 covers throughput and packaging.

Notable ones:

- `tools/layout_probe.py` — every structure against MSVC
- `tools/render_probe.py` — renders a known colour and captures it back, which
  is the only check that the frame contains what was on screen rather than
  merely being the right shape
- `tools/exercise.py` — calls every method that cannot change anything and
  reports how much of the API has actually been executed
- `tests/test_tier3_packaging.py` — builds a wheel, installs it into a throwaway
  virtual environment and captures a frame from outside the repository

### Known limits

- **Fullscreen-exclusive applications cannot be captured.** `DuplicateOutput`
  raises `Unsupported`. Borderless windowed works and captures exactly. Run
  `python tools/dxgi_report.py --game` to be told which case you are in.
- **Window capture is approximate.** Desktop Duplication returns the composed
  desktop, so cropping to a window's rectangle also captures anything drawn on
  top of it.
- **Nothing renders with Direct3D 12.** It is correctly declared and lightly
  exercised; no pipeline state is built and `d3d12video` has never been run.
- No GPU-side frame delivery, and the cursor is not composited into frames.
  Both are designed and neither is built.

### Requires

Windows 10 or 11, Python 3.8 or later, and `comtypes`. `numpy` is an optional
extra — `pip install pyDXGID3D[numpy]` — needed only for `frame.array` and
`frame.copy()`.

---

## 0.0.1

Initial internal implementation: hand-translated DXGI and Direct3D 11 interface
definitions, and a partial port of Microsoft's C++ desktop duplication sample.
The sample never ran and was removed before 0.2.0.
