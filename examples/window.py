# -*- coding: utf-8 -*-
"""Capture the area a window occupies. Approximately.

    python examples/window.py --title Notepad
    python examples/window.py --foreground --frames 60

READ THIS BEFORE USING IT
-------------------------
Desktop Duplication captures an OUTPUT, not a window. There is no window-capture
API here, and this example does not provide one - it finds where the window is
and crops the desktop to that rectangle. Three consequences, all real:

1. OCCLUSION IS NOT SOLVED. Anything on top of the target window is in your
   frame, because the desktop is what was composed. A dialog, a tooltip, another
   window - they all appear. Nothing within this API can prevent that.
   Windows.Graphics.Capture is the API that captures a window's own content, and
   it is a different family (WinRT) that this package does not bind.

2. GetWindowRect IS THE WRONG API. It includes the invisible resize border. On a
   maximised window on a 1920x1200 panel it returns (-8, -8, 1928, 1160) - a
   rectangle that is not inside the monitor at all, and CaptureOptions rejects
   it. DwmGetWindowAttribute(DWMWA_EXTENDED_FRAME_BOUNDS) returns the visible
   bounds, and that is what this uses.

3. WINDOWS MOVE. They are dragged, resized, minimised, and pushed across monitor
   boundaries. The bounds are re-read every frame and clamped to the output, and
   a minimised window has no useful rectangle at all.

If you need exact window contents, occluded or not, this is not the tool.
"""
import argparse
import ctypes
import os
import sys
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Direct3D.Capture import CaptureOptions, DesktopCapture, enumerate_outputs

from _png import write_frame

_user32 = ctypes.WinDLL("user32")
_dwmapi = ctypes.WinDLL("dwmapi")

DWMWA_EXTENDED_FRAME_BOUNDS = 9


def find_window(title):
    """The first top-level window whose title contains `title`."""
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def visit(hwnd, _lparam):
        if not _user32.IsWindowVisible(hwnd):
            return True
        length = _user32.GetWindowTextLengthW(hwnd)
        if not length:
            return True
        buffer = ctypes.create_unicode_buffer(length + 1)
        _user32.GetWindowTextW(hwnd, buffer, length + 1)
        if title.lower() in buffer.value.lower():
            found.append((hwnd, buffer.value))
            return False
        return True

    _user32.EnumWindows(visit, 0)
    return found[0] if found else (None, None)


def visible_bounds(hwnd):
    """The window's visible rectangle, without the invisible resize border.

    Falls back to GetWindowRect if DWM declines, which happens for windows that
    are not composited.
    """
    rect = wintypes.RECT()
    hr = _dwmapi.DwmGetWindowAttribute(
        wintypes.HWND(hwnd), ctypes.c_uint(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect), ctypes.sizeof(rect))
    if hr != 0:
        _user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return (rect.left, rect.top, rect.right, rect.bottom)


def clamp(region, output):
    """Intersect with the output, because a window may straddle two."""
    left = max(region[0], output.left)
    top = max(region[1], output.top)
    right = min(region[2], output.right)
    bottom = min(region[3], output.bottom)
    if right <= left or bottom <= top:
        return None
    return (left, top, right, bottom)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--title", help="substring of the window title")
    parser.add_argument("--foreground", action="store_true",
                        help="capture whatever is in front instead")
    parser.add_argument("--frames", type=int, default=1)
    parser.add_argument("--out", default="window.png")
    args = parser.parse_args()

    if args.foreground or not args.title:
        hwnd = _user32.GetForegroundWindow()
        buffer = ctypes.create_unicode_buffer(256)
        _user32.GetWindowTextW(hwnd, buffer, 256)
        name = buffer.value
    else:
        hwnd, name = find_window(args.title)
        if not hwnd:
            print("No visible window matching %r." % args.title)
            return 1

    outputs = enumerate_outputs()
    if not outputs:
        print("No attached display.")
        return 1

    raw = visible_bounds(hwnd)
    print("window   : %r" % name)
    print("bounds   : %r" % (raw,))

    if _user32.IsIconic(hwnd):
        print("It is minimised, so it has no visible rectangle to capture.")
        return 1

    output = next((o for o in outputs
                   if clamp(raw, o) is not None), None)
    if output is None:
        print("The window does not overlap any attached output.")
        return 1

    region = clamp(raw, output)
    if region != raw:
        print("clamped  : %r  (to output %d)" % (region, output.index))

    options = CaptureOptions(output=output, region=region, timeout_ms=1000)
    with DesktopCapture(options) as capture:
        for _ in range(3):
            frame = capture.grab()
        for _ in range(max(0, args.frames - 1)):
            frame = capture.grab()
        write_frame(args.out, frame)

    print("captured : %dx%d -> %s" % (frame.width, frame.height, args.out))
    print()
    print("Remember: anything drawn on top of that rectangle is in the image.")
    print("This crops the desktop; it does not capture the window's own content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
