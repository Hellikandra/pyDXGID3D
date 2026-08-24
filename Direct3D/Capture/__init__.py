# -*- coding: utf-8 -*-
"""Desktop Duplication capture, built on the DXGI and Direct3D 11 bindings.

Three names. A consumer that needs to reach past them into
``Direct3D.PyIdl`` has found something missing from this layer, and that is a
bug report rather than a workaround.

    from Direct3D.Capture import enumerate_outputs, CaptureOptions, DesktopCapture

    for output in enumerate_outputs():
        print(output)

    options = CaptureOptions(output=0, region=(320, 180, 1600, 900))
    with DesktopCapture(options) as capture:
        for frame in capture:
            process(frame.array)          # zero-copy, this iteration only

The frame rate is the display's, not the game's. Desktop Duplication produces a
frame when the desktop composes one, so a 60 Hz panel gives at most 60 per
second no matter how fast the game runs. On a 144 Hz panel you get up to 144.

Two things reliably stop it working, and neither is a defect here:

* A **fullscreen-exclusive** application owns the display. ``DuplicateOutput``
  raises ``Unsupported``. Borderless windowed is the fix.
* There is **no interactive desktop** - a disconnected RDP session, or a
  service. ``enumerate_outputs()`` returns nothing at all.
"""
from Direct3D.Capture.capture import DesktopCapture
from Direct3D.Capture.enumerate import Adapter, Output, enumerate_outputs, resolve_output
from Direct3D.Capture.frame import Frame, StaleFrameError
from Direct3D.Capture.options import ACCESS_LOST_POLICIES, CaptureOptions

__all__ = [
    "enumerate_outputs",
    "CaptureOptions",
    "DesktopCapture",
    # Supporting types. Useful for annotations and isinstance checks; you should
    # not need to construct any of them yourself.
    "Adapter",
    "Output",
    "Frame",
    "StaleFrameError",
    "resolve_output",
    "ACCESS_LOST_POLICIES",
]
