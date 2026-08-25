# -*- coding: utf-8 -*-
"""One frame of the desktop, written to a PNG.

    python examples/screenshot.py
    python examples/screenshot.py --output 1 --out second-monitor.png

The smallest complete thing this package does. Three names, six lines of work.
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Direct3D.Capture import CaptureOptions, DesktopCapture, enumerate_outputs

from _png import write_frame


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=int, default=0,
                        help="which monitor (see examples/displays.py)")
    parser.add_argument("--out", default="screenshot.png")
    args = parser.parse_args()

    outputs = enumerate_outputs()
    if not outputs:
        print("No attached display. Desktop Duplication needs an interactive "
              "session - it cannot run over a disconnected RDP connection or "
              "from a service.")
        return 1

    with DesktopCapture(CaptureOptions(output=args.output)) as capture:
        # The first frame after DuplicateOutput is often the whole desktop as
        # one accumulated update, which is fine for a screenshot - but if the
        # screen is idle the very first acquire can also time out repeatedly,
        # so take a few and keep the last.
        for _ in range(3):
            frame = capture.grab()

        started = time.perf_counter()
        write_frame(args.out, frame)
        elapsed = time.perf_counter() - started

    print("%s  %dx%d  (%.0f ms to encode)"
          % (args.out, frame.width, frame.height, elapsed * 1000))
    return 0


if __name__ == "__main__":
    sys.exit(main())
