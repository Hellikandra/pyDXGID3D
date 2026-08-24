# -*- coding: utf-8 -*-
"""End-to-end diagnostic: does DXGI actually work on this machine?

The test suite proves the bindings match the SDK. It does not prove they drive
real hardware - tier 1 runs on WARP, the software rasteriser, precisely so it
works on a CI runner with no GPU.

This is the other half. It walks the whole capture path against your real
adapters and monitors and reports what happened at each step:

    factory -> adapters -> outputs -> device -> duplication -> a frame -> a pixel

Run it and read the output. If it prints a pixel colour, Desktop Duplication
works here, end to end, through these bindings.

    python tools/dxgi_report.py                  enumerate and capture from output 0
    python tools/dxgi_report.py --list           enumerate only, capture nothing
    python tools/dxgi_report.py --output 1       capture from a different monitor
    python tools/dxgi_report.py --frames 60      time a sustained run
    python tools/dxgi_report.py --save shot.ppm  write the frame to a file
    python tools/dxgi_report.py --benchmark      run flat out, time each stage
    python tools/dxgi_report.py --sweep          readback cost vs capture size
    python tools/dxgi_report.py --benchmark --no-readback   GPU copy only

Needs Windows, comtypes, a GPU and an interactive desktop session. It cannot
work over a disconnected RDP session or from a service - see constraint C-7.
"""
import ctypes
import sys
import time

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

import comtypes                                              # noqa: E402

from Direct3D.PyIdl.functions import CreateDXGIFactory1, D3D11CreateDevice  # noqa: E402
from Direct3D.PyIdl.status import (                          # noqa: E402
    AccessLost, DXGIError, WaitTimeout, name_of,
)
from Direct3D.PyIdl.d3dcommon import D3D_DRIVER_TYPE_UNKNOWN  # noqa: E402
from Direct3D.PyIdl.dxgi import (                            # noqa: E402
    IDXGIAdapter1, IDXGIOutput, IDXGIResource,
    DXGI_ADAPTER_DESC1, DXGI_OUTPUT_DESC,
)
from Direct3D.PyIdl.dxgi1_2 import (                         # noqa: E402
    IDXGIOutput1, IDXGIOutputDuplication, DXGI_OUTDUPL_FRAME_INFO,
)
from Direct3D.PyIdl.d3d11 import (                           # noqa: E402
    ID3D11Texture2D, ID3D11Resource, D3D11_TEXTURE2D_DESC,
    D3D11_MAPPED_SUBRESOURCE, D3D11_USAGE_STAGING, D3D11_BOX,
    D3D11_CPU_ACCESS_READ, D3D11_MAP_READ,
)

ROTATION = {0: "unspecified", 1: "none", 2: "90", 3: "180", 4: "270"}


def _v(constant):
    return constant.value if hasattr(constant, "value") else constant


def rule(title):
    print()
    print(title)
    print("-" * len(title))


def enumerate_hardware():
    """[(adapter, adapter_desc, [(index, output, output_desc), ...]), ...]

    Enumeration is per adapter on purpose. An output belongs to exactly one
    adapter, and DuplicateOutput fails if the device was created on a different
    one - which is the normal situation on a hybrid laptop, where the panel
    hangs off the integrated GPU while games run on the discrete one (C-4).
    """
    factory = CreateDXGIFactory1()
    result = []
    index = 0
    while True:
        adapter = ctypes.POINTER(IDXGIAdapter1)()
        try:
            factory.EnumAdapters1(index, ctypes.byref(adapter))
        except comtypes.COMError:
            break                      # DXGI_ERROR_NOT_FOUND terminates the walk
        if not adapter:
            break

        desc = DXGI_ADAPTER_DESC1()
        adapter.GetDesc1(ctypes.byref(desc))

        outputs, out_index = [], 0
        while True:
            output = ctypes.POINTER(IDXGIOutput)()
            try:
                adapter.EnumOutputs(out_index, ctypes.byref(output))
            except comtypes.COMError:
                break
            if not output:
                break
            odesc = DXGI_OUTPUT_DESC()
            output.GetDesc(ctypes.byref(odesc))
            outputs.append((out_index, output, odesc))
            out_index += 1

        result.append((adapter, desc, outputs))
        index += 1
    return result


def report_hardware(hardware):
    rule("Adapters and outputs")
    if not hardware:
        print("  none found - that alone is a finding")
        return []

    flat = []
    for adapter_index, (_adapter, desc, outputs) in enumerate(hardware):
        software = " [software]" if desc.Flags & 0x2 else ""
        print("  adapter %d: %s%s" % (adapter_index, desc.Description, software))
        print("      vendor 0x%04X  device 0x%04X  LUID %d:%d"
              % (desc.VendorId, desc.DeviceId,
                 desc.AdapterLuid.HighPart, desc.AdapterLuid.LowPart))
        print("      dedicated video %6.0f MB   shared system %6.0f MB"
              % (desc.DedicatedVideoMemory / 1048576.0,
                 desc.SharedSystemMemory / 1048576.0))
        if not outputs:
            print("      no outputs attached")
        for out_index, output, odesc in outputs:
            box = odesc.DesktopCoordinates
            print("      output %d: %s  %dx%d at (%d,%d)  rotation %s  attached=%s"
                  % (out_index, odesc.DeviceName,
                     box.right - box.left, box.bottom - box.top,
                     box.left, box.top,
                     ROTATION.get(_v(odesc.Rotation), "?"),
                     bool(odesc.AttachedToDesktop)))
            flat.append((adapter_index, out_index, _adapter, output, odesc))
    return flat


def capture(adapter, output, odesc, frames, save):
    box = odesc.DesktopCoordinates
    width, height = box.right - box.left, box.bottom - box.top

    rule("Device on the adapter that owns this output")
    device, level, context = D3D11CreateDevice(
        adapter=adapter, driver_type=D3D_DRIVER_TYPE_UNKNOWN)
    print("  created, feature level 0x%X" % level.value)

    rule("Duplicating the output")
    output1 = output.QueryInterface(IDXGIOutput1)
    duplication = ctypes.POINTER(IDXGIOutputDuplication)()
    try:
        output1.DuplicateOutput(device, ctypes.byref(duplication))
    except comtypes.COMError as exc:
        code = exc.hresult & 0xFFFFFFFF
        print("  FAILED: %s" % name_of(code))
        if code == 0x887A0004:
            print("  DXGI_ERROR_UNSUPPORTED usually means a fullscreen-exclusive")
            print("  application owns the display, or the desktop is not composited.")
            print("  Set the game to borderless windowed - constraint C-2.")
        elif code == 0x887A0026:
            print("  ACCESS_LOST at creation - a mode change is in progress.")
        return False
    print("  IDXGIOutputDuplication obtained")

    staging = ctypes.POINTER(ID3D11Texture2D)()
    desc = D3D11_TEXTURE2D_DESC()
    ctypes.memset(ctypes.byref(desc), 0, ctypes.sizeof(desc))
    desc.Width, desc.Height = width, height
    desc.MipLevels = desc.ArraySize = 1
    desc.Format = 87                                     # DXGI_FORMAT_B8G8R8A8_UNORM
    desc.SampleDesc.Count = 1
    desc.Usage = _v(D3D11_USAGE_STAGING)
    desc.CPUAccessFlags = _v(D3D11_CPU_ACCESS_READ)
    device.CreateTexture2D(ctypes.byref(desc), None, ctypes.byref(staging))

    rule("Acquiring %d frame%s" % (frames, "" if frames == 1 else "s"))
    got = timeouts = 0
    accumulated = 0
    first_pixel = None
    pitch = 0
    started = time.perf_counter()

    while got < frames:
        info = DXGI_OUTDUPL_FRAME_INFO()
        resource = ctypes.POINTER(IDXGIResource)()
        try:
            duplication.AcquireNextFrame(1000, ctypes.byref(info),
                                         ctypes.byref(resource))
        except comtypes.COMError as exc:
            code = exc.hresult & 0xFFFFFFFF
            if code == 0x887A0027:                       # WAIT_TIMEOUT
                timeouts += 1
                if timeouts > 5:
                    print("  timed out %d times - the desktop is not changing."
                          % timeouts)
                    print("  Move the mouse or play a video and run this again.")
                    break
                continue
            print("  FAILED: %s" % name_of(code))
            return False

        accumulated += info.AccumulatedFrames
        if info.LastPresentTime == 0:
            # Only the cursor moved; no new desktop image. Skipping these is the
            # cheapest optimisation in the loop (constraint C-1).
            duplication.ReleaseFrame()
            continue

        texture = resource.QueryInterface(ID3D11Texture2D)
        context.CopyResource(staging.QueryInterface(ID3D11Resource),
                             texture.QueryInterface(ID3D11Resource))

        mapped = D3D11_MAPPED_SUBRESOURCE()
        context.Map(staging.QueryInterface(ID3D11Resource), 0,
                    _v(D3D11_MAP_READ), 0, ctypes.byref(mapped))
        try:
            pitch = mapped.RowPitch
            if first_pixel is None:
                buf = ctypes.cast(mapped.pData, ctypes.POINTER(ctypes.c_ubyte))
                middle = pitch * (height // 2) + (width // 2) * 4
                first_pixel = (buf[middle + 2], buf[middle + 1], buf[middle])
                if save:
                    _write_ppm(save, buf, width, height, pitch)
        finally:
            context.Unmap(staging.QueryInterface(ID3D11Resource), 0)

        duplication.ReleaseFrame()
        got += 1

    elapsed = time.perf_counter() - started

    rule("Result")
    if not got:
        print("  no frames captured")
        return False
    print("  frames captured    : %d" % got)
    print("  wall clock         : %.2f s  (%.1f fps)" % (elapsed, got / elapsed))
    print("  timeouts           : %d" % timeouts)
    print("  coalesced updates  : %d" % accumulated)
    print("  row pitch          : %d bytes (%d for %d BGRA pixels)"
          % (pitch, width * 4, width))
    print("  centre pixel RGB   : %s" % (first_pixel,))
    if save:
        print("  saved              : %s" % save)
    print()
    print("  A pixel value here means the whole path works through these")
    print("  bindings: factory, adapter, output, device, duplication,")
    print("  AcquireNextFrame, CopyResource, Map.")
    return True


def _staging(device, width, height):
    desc = D3D11_TEXTURE2D_DESC()
    ctypes.memset(ctypes.byref(desc), 0, ctypes.sizeof(desc))
    desc.Width, desc.Height = width, height
    desc.MipLevels = desc.ArraySize = 1
    desc.Format = 87                                 # DXGI_FORMAT_B8G8R8A8_UNORM
    desc.SampleDesc.Count = 1
    desc.Usage = _v(D3D11_USAGE_STAGING)
    desc.CPUAccessFlags = _v(D3D11_CPU_ACCESS_READ)
    texture = ctypes.POINTER(ID3D11Texture2D)()
    device.CreateTexture2D(ctypes.byref(desc), None, ctypes.byref(texture))
    return texture


def _open_duplication(adapter, output):
    device, level, context = D3D11CreateDevice(
        adapter=adapter, driver_type=D3D_DRIVER_TYPE_UNKNOWN)
    output1 = output.QueryInterface(IDXGIOutput1)
    duplication = ctypes.POINTER(IDXGIOutputDuplication)()
    output1.DuplicateOutput(device, ctypes.byref(duplication))
    return device, context, duplication


def benchmark(adapter, output, odesc, seconds, readback=True):
    """Run flat out and report where the time actually goes.

    Desktop Duplication caps NEW frames at the display refresh rate, so raw fps
    cannot tell you what the pipeline is capable of: a 60 Hz panel reports 60
    whether the loop has a millisecond of headroom or none at all.

    So the stages are timed separately. AcquireNextFrame is waiting; copy, map
    and release are work. Capacity is 1 / work - the rate the loop could sustain
    if frames arrived instantly, which is the number that says whether a faster
    monitor would actually buy you anything.
    """
    box = odesc.DesktopCoordinates
    width, height = box.right - box.left, box.bottom - box.top

    device, context, duplication = _open_duplication(adapter, output)
    staging_res = _staging(device, width, height).QueryInterface(ID3D11Resource)

    rule("Benchmark: %d s at %dx%d, readback %s"
         % (seconds, width, height, "on" if readback else "off"))

    t_wait = t_copy = t_map = t_release = 0.0
    frames = skipped = timeouts = 0
    deadline = time.perf_counter() + seconds
    started = time.perf_counter()

    while time.perf_counter() < deadline:
        info = DXGI_OUTDUPL_FRAME_INFO()
        resource = ctypes.POINTER(IDXGIResource)()
        mark = time.perf_counter()
        try:
            duplication.AcquireNextFrame(500, ctypes.byref(info),
                                         ctypes.byref(resource))
        except comtypes.COMError as exc:
            t_wait += time.perf_counter() - mark
            if (exc.hresult & 0xFFFFFFFF) == 0x887A0027:
                timeouts += 1
                continue
            print("  aborted: %s" % name_of(exc.hresult & 0xFFFFFFFF))
            break
        t_wait += time.perf_counter() - mark

        if info.LastPresentTime == 0:
            skipped += 1
            duplication.ReleaseFrame()
            continue

        source = (resource.QueryInterface(ID3D11Texture2D)
                  .QueryInterface(ID3D11Resource))
        mark = time.perf_counter()
        context.CopyResource(staging_res, source)
        t_copy += time.perf_counter() - mark

        if readback:
            mark = time.perf_counter()
            mapped = D3D11_MAPPED_SUBRESOURCE()
            context.Map(staging_res, 0, _v(D3D11_MAP_READ), 0,
                        ctypes.byref(mapped))
            buf = ctypes.cast(mapped.pData, ctypes.POINTER(ctypes.c_ubyte))
            _ = buf[mapped.RowPitch * (height - 1) + width * 4 - 1]
            context.Unmap(staging_res, 0)
            t_map += time.perf_counter() - mark

        mark = time.perf_counter()
        duplication.ReleaseFrame()
        t_release += time.perf_counter() - mark
        frames += 1

    elapsed = time.perf_counter() - started
    if not frames:
        print("  no frames - move the mouse or play a video, then try again")
        return False

    work = (t_copy + t_map + t_release) / frames
    megabytes = frames * width * height * 4 / 1048576.0

    print("  frames                 : %d in %.2f s" % (frames, elapsed))
    print("  cursor-only, skipped   : %d" % skipped)
    print("  timeouts               : %d" % timeouts)
    print("")
    print("  observed rate          : %6.1f fps   <- capped by the display"
          % (frames / elapsed))
    print("  waiting for a frame    : %5.1f %%    %6.2f ms each"
          % (100.0 * t_wait / elapsed, 1000.0 * t_wait / frames))
    print("  CopyResource           : %5.1f %%    %6.2f ms each"
          % (100.0 * t_copy / elapsed, 1000.0 * t_copy / frames))
    if readback:
        print("  Map + read + Unmap     : %5.1f %%    %6.2f ms each"
              % (100.0 * t_map / elapsed, 1000.0 * t_map / frames))
    print("  ReleaseFrame           : %5.1f %%    %6.2f ms each"
          % (100.0 * t_release / elapsed, 1000.0 * t_release / frames))
    print("")
    capacity = (1.0 / work) if work else 0.0
    print("  PIPELINE CAPACITY      : %6.0f fps   (1 / %.2f ms of real work)"
          % (capacity, 1000.0 * work))
    print("  readback bandwidth     : %6.0f MB/s" % (megabytes / elapsed))
    print("")
    print("  The loop spends %.0f%% of its time waiting for the display."
          % (100.0 * t_wait / elapsed))
    if capacity:
        print("  It could handle about %.0fx the current frame rate, so a faster"
              % (capacity / (frames / elapsed)))
        print("  panel would translate almost directly into more captured frames.")
    return True


def sweep(adapter, output, odesc, seconds):
    """Readback cost against capture size - constraint C-5, measured.

    A full 1080p BGRA frame is 8.3 MB. The claim is that cropping before the
    staging copy is worth orders of magnitude. CopySubresourceRegion keeps the
    source whole and varies only the region crossing to system memory, so this
    isolates the readback rather than the capture.
    """
    box = odesc.DesktopCoordinates
    full_w, full_h = box.right - box.left, box.bottom - box.top

    device, context, duplication = _open_duplication(adapter, output)

    sizes = [(full_w, full_h), (1280, 720), (640, 360), (256, 256), (128, 128)]
    sizes = [(w, h) for w, h in sizes if w <= full_w and h <= full_h]

    rule("Readback cost against capture size")
    print("  %-13s %10s %10s %12s" % ("region", "MB/frame", "ms/frame", "MB/s"))

    for width, height in sizes:
        staging_res = _staging(device, width, height).QueryInterface(ID3D11Resource)
        region = D3D11_BOX()
        region.left, region.top, region.front = 0, 0, 0
        region.right, region.bottom, region.back = width, height, 1

        total, frames = 0.0, 0
        deadline = time.perf_counter() + seconds
        while time.perf_counter() < deadline:
            info = DXGI_OUTDUPL_FRAME_INFO()
            resource = ctypes.POINTER(IDXGIResource)()
            try:
                duplication.AcquireNextFrame(500, ctypes.byref(info),
                                             ctypes.byref(resource))
            except comtypes.COMError:
                continue
            if info.LastPresentTime == 0:
                duplication.ReleaseFrame()
                continue
            source = (resource.QueryInterface(ID3D11Texture2D)
                      .QueryInterface(ID3D11Resource))
            mark = time.perf_counter()
            context.CopySubresourceRegion(staging_res, 0, 0, 0, 0,
                                          source, 0, ctypes.byref(region))
            mapped = D3D11_MAPPED_SUBRESOURCE()
            context.Map(staging_res, 0, _v(D3D11_MAP_READ), 0,
                        ctypes.byref(mapped))
            buf = ctypes.cast(mapped.pData, ctypes.POINTER(ctypes.c_ubyte))
            _ = buf[mapped.RowPitch * (height - 1) + width * 4 - 1]
            context.Unmap(staging_res, 0)
            total += time.perf_counter() - mark
            frames += 1
            duplication.ReleaseFrame()

        label = "%dx%d" % (width, height)
        if not frames:
            print("  %-13s %10s" % (label, "no frames"))
            continue
        mb = width * height * 4 / 1048576.0
        ms = 1000.0 * total / frames
        print("  %-13s %10.2f %10.2f %12.0f"
              % (label, mb, ms, mb / (total / frames)))

    print("")
    print("  This is constraint C-5 measured. Cropping before the staging copy is")
    print("  the difference between shipping the whole desktop across the bus")
    print("  every frame and shipping only the part that matters.")
    return True


def _write_ppm(path, buf, width, height, pitch):
    """Binary PPM - no dependencies, and every image viewer reads it."""
    with open(path, "wb") as handle:
        handle.write(b"P6\n%d %d\n255\n" % (width, height))
        for y in range(height):
            row = bytearray(width * 3)
            base = pitch * y
            for x in range(width):
                off = base + x * 4
                row[x * 3] = buf[off + 2]        # BGRA on disk, RGB in the file
                row[x * 3 + 1] = buf[off + 1]
                row[x * 3 + 2] = buf[off]
            handle.write(bytes(row))


def main():
    argv = sys.argv[1:]

    def opt(flag, default=None, cast=str):
        return cast(argv[argv.index(flag) + 1]) if flag in argv else default

    print("pyDXGID3D - DXGI / Direct3D 11 diagnostic")
    print("=" * 42)

    try:
        hardware = enumerate_hardware()
    except (DXGIError, comtypes.COMError) as exc:
        print("  could not enumerate: %s" % exc)
        return 1

    flat = report_hardware(hardware)
    if "--list" in argv or not flat:
        return 0

    wanted = opt("--output", 0, int)
    match = [f for f in flat if f[1] == wanted and f[4].AttachedToDesktop]
    if not match:
        match = [f for f in flat if f[4].AttachedToDesktop]
    if not match:
        print("\n  no output is attached to the desktop - nothing to capture")
        return 1

    _ai, _oi, adapter, output, odesc = match[0]

    if "--sweep" in argv:
        ok = sweep(adapter, output, odesc, opt("--seconds", 3, int))
    elif "--benchmark" in argv:
        ok = benchmark(adapter, output, odesc, opt("--seconds", 5, int),
                       readback="--no-readback" not in argv)
    else:
        ok = capture(adapter, output, odesc,
                     opt("--frames", 1, int), opt("--save"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
