# -*- coding: utf-8 -*-
"""Record the screen to a video file, by piping raw frames to ffmpeg.

    python examples/record.py --seconds 5 --out capture.mp4
    python examples/record.py --region 0 0 1280 720 --seconds 10

Why ffmpeg and not an encoder in this package
---------------------------------------------
A 1920x1200 BGRA frame is 8.79 MB. At 60 fps that is 527 MB per second, so
compression is not optional for anything longer than a moment.

There are three ways to compress it and only one is sensible today:

  ffmpeg on a pipe        this file. About thirty lines, real video out, and
                          ffmpeg already handles every container and codec
                          question you would otherwise have to answer.

  Media Foundation        the Windows encoder API. Not bound by this package
                          and a large surface to add.

  d3d12video              hardware encode, through interfaces this package DOES
                          bind. None of them has ever been executed. It needs
                          resource heaps, command lists, bitstream buffers and
                          reference-picture management - a project, not an
                          example.

So: this writes raw BGRA to ffmpeg's stdin and lets it do the work. If ffmpeg is
not on PATH the example says so and stops rather than pretending.
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Direct3D.Capture import CaptureOptions, DesktopCapture, enumerate_outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=int, default=0)
    parser.add_argument("--region", type=int, nargs=4,
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--seconds", type=float, default=5.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--out", default="capture.mp4")
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ffmpeg is not on PATH.")
        print()
        print("This example pipes raw frames to it rather than encoding them")
        print("here - see the module docstring for why. Install it from")
        print("https://ffmpeg.org/ or with: winget install Gyan.FFmpeg")
        return 1

    outputs = enumerate_outputs()
    if not outputs:
        print("No attached display.")
        return 1
    output = outputs[args.output]
    region = tuple(args.region) if args.region else None

    options = CaptureOptions(output=output, region=region, timeout_ms=1000)
    with DesktopCapture(options) as capture:
        width, height = capture.width, capture.height
        command = [
            ffmpeg, "-y",
            "-f", "rawvideo",
            "-pix_fmt", "bgra",
            "-s", "%dx%d" % (width, height),
            "-r", str(args.fps),
            "-i", "-",                      # frames arrive on stdin
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",          # what players actually accept
            args.out,
        ]
        print("recording %dx%d for %.1f s at %d fps -> %s"
              % (width, height, args.seconds, args.fps, args.out))

        encoder = subprocess.Popen(command, stdin=subprocess.PIPE,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        packed = width * 4
        written, dropped = 0, 0
        interval = 1.0 / args.fps
        started = next_due = time.perf_counter()
        deadline = started + args.seconds

        try:
            while time.perf_counter() < deadline:
                frame = capture.grab()
                now = time.perf_counter()
                if now < next_due:
                    dropped += 1            # captured faster than the target rate
                    continue
                next_due += interval

                view = frame.memoryview
                if frame.padded:
                    # ffmpeg wants tightly packed rows; the driver pads them.
                    for y in range(height):
                        encoder.stdin.write(view[y * frame.pitch:
                                                 y * frame.pitch + packed])
                else:
                    encoder.stdin.write(view)
                written += 1
        finally:
            encoder.stdin.close()
            encoder.wait()

        elapsed = time.perf_counter() - started

    size = os.path.getsize(args.out) if os.path.isfile(args.out) else 0
    raw = written * height * packed
    print()
    print("  %d frames written in %.2f s (%d captured and dropped to hit %d fps)"
          % (written, elapsed, dropped, args.fps))
    print("  raw would have been %.1f MB; %s is %.1f MB (%.0fx smaller)"
          % (raw / 1048576.0, args.out, size / 1048576.0,
             (raw / size) if size else 0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
