# -*- coding: utf-8 -*-
"""Every attached monitor, and a frame from each.

    python examples/displays.py
    python examples/displays.py --save

The multi-monitor check. It also demonstrates constraint C-4, the one that makes
capture fail on a hybrid laptop: an output belongs to exactly one adapter, and a
device created on a different one cannot duplicate it. enumerate_outputs()
returns the pair, so the right device gets created by construction.
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
    parser.add_argument("--save", action="store_true",
                        help="write display-N.png for each")
    args = parser.parse_args()

    outputs = enumerate_outputs()
    if not outputs:
        print("No attached display.")
        return 1

    print("%d output%s" % (len(outputs), "" if len(outputs) == 1 else "s"))
    print()

    for output in outputs:
        adapter = output.adapter
        print("  output %d  %s" % (output.index, output.device_name))
        print("      %dx%d at (%d, %d), rotation %s"
              % (output.width, output.height, output.left, output.top,
                 output.rotation))
        print("      driven by %s" % adapter.description)
        print("          %.0f MB dedicated, vendor 0x%04X, LUID %d:%d"
              % (adapter.dedicated_video_memory / 1048576.0,
                 adapter.vendor_id, adapter.luid[0], adapter.luid[1]))

        try:
            started = time.perf_counter()
            with DesktopCapture(CaptureOptions(output=output,
                                               timeout_ms=1000)) as capture:
                for _ in range(3):
                    frame = capture.grab()
                elapsed = time.perf_counter() - started
                print("      captured %dx%d, pitch %d%s, in %.0f ms"
                      % (frame.width, frame.height, frame.pitch,
                         " (padded)" if frame.padded else "", elapsed * 1000))
                if args.save:
                    name = "display-%d.png" % output.index
                    write_frame(name, frame)
                    print("      wrote %s" % name)
        except Exception as exc:
            print("      CANNOT CAPTURE: %s" % exc)
        print()

    if len(outputs) > 1:
        print("  Each output was captured through a device created on ITS OWN")
        print("  adapter. That is constraint C-4: on a hybrid laptop the panel")
        print("  hangs off the integrated GPU while the discrete one has no")
        print("  outputs at all, and a device on the wrong adapter fails.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
