# -*- coding: utf-8 -*-
"""Capture a rectangle, repeatedly, into a buffer you keep.

    python examples/region.py --region 320 180 1600 900 --frames 120

This is the shape a consumer actually wants: a fixed crop, delivered into an
array allocated once. It is also the shape that makes the delivery costs visible,
so the run prints them.

Two things worth reading in the source:

  * `region` is in DESKTOP coordinates, not output-local ones. A second monitor
    placed to the right of the first starts at x=1920.
  * `frame.copy_into(buffer)` reuses your array. `frame.copy()` allocates a new
    one every time, and the allocation costs more than the copy - about 3.9 ms
    of page faults on a full 1920x1200 frame.
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Direct3D.Capture import CaptureOptions, DesktopCapture, enumerate_outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=int, default=0)
    parser.add_argument("--region", type=int, nargs=4,
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
                        help="in desktop coordinates; default is a centred 512 square")
    parser.add_argument("--frames", type=int, default=120)
    args = parser.parse_args()

    outputs = enumerate_outputs()
    if not outputs:
        print("No attached display.")
        return 1
    output = outputs[args.output]

    if args.region:
        region = tuple(args.region)
    else:
        cx = output.left + output.width // 2
        cy = output.top + output.height // 2
        region = (cx - 256, cy - 256, cx + 256, cy + 256)

    print("output %d, region %r" % (output.index, region))

    try:
        import numpy
    except ImportError:
        print("This example needs numpy: pip install pyDXGID3D[numpy]")
        return 1

    options = CaptureOptions(output=output, region=region, timeout_ms=1000)
    with DesktopCapture(options) as capture:
        buffer = numpy.empty((capture.height, capture.width, 4), numpy.uint8)
        for _ in range(5):
            capture.grab()                     # settle

        started, spent, taken = time.perf_counter(), 0.0, 0
        for frame in capture:
            mark = time.perf_counter()
            pixels = frame.copy_into(buffer)
            spent += time.perf_counter() - mark
            taken += 1
            if taken >= args.frames:
                break
        elapsed = time.perf_counter() - started

    megabytes = capture.width * capture.height * 4 / 1048576.0
    print()
    print("  %d frames of %dx%d (%.2f MB each)"
          % (taken, capture.width, capture.height, megabytes))
    print("  wall clock        %6.2f s   %.1f fps" % (elapsed, taken / elapsed))
    print("  copy_into         %6.2f ms per frame" % (1000.0 * spent / taken))
    print("  skipped           %6d  (cursor-only updates)" % capture.skipped)
    print("  rebuilds          %6d" % capture.rebuilds)
    print()
    print("  last frame centre BGRA: %s"
          % (tuple(int(v) for v in pixels[capture.height // 2,
                                          capture.width // 2]),))
    print()
    print("  The frame rate is the DISPLAY's, not the game's. Desktop")
    print("  Duplication produces a frame when the desktop composes one, so a")
    print("  60 Hz panel gives at most 60 no matter what is running.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
