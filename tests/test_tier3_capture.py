# -*- coding: utf-8 -*-
"""Tier 3 - throughput, and the delivery costs the API documents.

These are the project's premise, measured. The claim is that DXGI capture beats
screenshot-based approaches on frame rate; if the loop cannot keep up with the
panel, that claim is gone.

Every gate here is deliberately loose. A test that fails because the machine was
busy is a test people learn to ignore, so the thresholds sit well below what the
development machine actually does - roughly half - and are there to catch a
regression of the kind that turns 60 fps into 6, not a 10% drift.

The measured figures on the development machine, 1920x1200 BGRA (8.79 MB),
timed as Map to deliver to Unmap:

    array (zero copy)   2.63 ms
    copy_into(reused)   3.76 ms
    copy() (allocates)  7.62 ms

The gap between the last two is page faults on the fresh allocation, not the
copy itself. That is the whole reason copy_into exists.
"""
import time

import pytest

from conftest import needs_comtypes, needs_windows

pytestmark = [pytest.mark.tier3, needs_windows, needs_comtypes]

#: Long enough to average over display refreshes, short enough that a full run
#: of the suite stays tolerable.
SECONDS = 2.0

#: The loop must keep up with the display. A 60 Hz panel delivers 60; anything
#: at or below this means the loop, not the panel, is the limit.
MIN_FPS = 30.0


def _run(capture, seconds, deliver):
    """Return (frames, seconds spent inside deliver)."""
    for _ in range(10):                      # leave the first-frame path behind
        capture.grab()

    frames, spent = 0, 0.0
    deadline = time.perf_counter() + seconds
    while time.perf_counter() < deadline:
        frame = capture.grab()
        mark = time.perf_counter()
        deliver(frame)
        spent += time.perf_counter() - mark
        frames += 1
    return frames, spent


def test_the_loop_keeps_up_with_the_display(capturable_output):
    """C-1: the ceiling is the refresh rate, and the loop should reach it."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output,
                                       timeout_ms=1000)) as capture:
        started = time.perf_counter()
        frames, _ = _run(capture, SECONDS, lambda frame: None)
        elapsed = time.perf_counter() - started

    rate = frames / elapsed
    assert rate >= MIN_FPS, (
        "%.1f fps - the loop is the bottleneck, not the display. On an idle "
        "desktop some of this is waiting for the screen to change, so check "
        "that something is animating before believing a low number." % rate)


def test_the_zero_copy_view_is_nearly_free(capturable_output, numpy_module):
    """frame.array should cost almost nothing over touching one byte.

    If this regresses it means the view is copying, which would be invisible
    except as a halved frame rate under load.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output,
                                       timeout_ms=1000)) as capture:
        frames, spent = _run(capture, SECONDS, lambda frame: frame.array)

    if not frames:
        pytest.skip("no frames - the desktop is not changing")
    per_frame_ms = 1000.0 * spent / frames
    assert per_frame_ms < 2.0, (
        "frame.array costs %.2f ms - it is meant to be a view, not a copy"
        % per_frame_ms)


def test_copy_into_beats_copy(capturable_output, numpy_module):
    """The reason copy_into is in the API at all.

    Measured at 3.76 against 7.62 ms. Asserted only as 'faster', because the
    ratio depends on how the allocator feels: what must not happen is the two
    converging, which would mean the destination is being reallocated.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output,
                                       timeout_ms=1000)) as capture:
        capture.grab()
        destination = numpy_module.empty(
            (capture.height, capture.width, 4), numpy_module.uint8)
        into_frames, into_spent = _run(
            capture, SECONDS, lambda frame: frame.copy_into(destination))
        copy_frames, copy_spent = _run(
            capture, SECONDS, lambda frame: frame.copy())

    if not into_frames or not copy_frames:
        pytest.skip("no frames - the desktop is not changing")
    into_ms = 1000.0 * into_spent / into_frames
    copy_ms = 1000.0 * copy_spent / copy_frames
    assert into_ms < copy_ms, (
        "copy_into %.2f ms, copy %.2f ms. copy_into exists because it reuses "
        "the caller's destination and so avoids page-faulting a fresh "
        "allocation every frame; if it is no longer faster, it is no longer "
        "doing that." % (into_ms, copy_ms))


def test_cropping_reduces_the_delivery_cost(capturable_output, numpy_module):
    """C-5, as corrected by C-29.

    Cropping is worth about 2.2x, not the three orders of magnitude the original
    constraint claimed, because a fixed ~1 ms Map/Unmap cost dominates below
    1 MB.

    Timed with copy_into, not with frame.array: the view never touches a pixel,
    so its cost does not vary with the size of the frame and comparing views
    compares two numbers that are both noise. Copying is where the bytes are
    actually moved, and 0.25 MB against 8.79 MB is unambiguous.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    left, top = capturable_output.left, capturable_output.top
    small = CaptureOptions(output=capturable_output, timeout_ms=1000,
                           region=(left, top, left + 256, top + 256))

    def measure(options):
        with DesktopCapture(options) as capture:
            capture.grab()
            destination = numpy_module.empty(
                (capture.height, capture.width, 4), numpy_module.uint8)
            return _run(capture, SECONDS,
                        lambda frame: frame.copy_into(destination))

    full_frames, full_spent = measure(
        CaptureOptions(output=capturable_output, timeout_ms=1000))
    crop_frames, crop_spent = measure(small)

    if not full_frames or not crop_frames:
        pytest.skip("no frames - the desktop is not changing")
    full_ms = 1000.0 * full_spent / full_frames
    crop_ms = 1000.0 * crop_spent / crop_frames
    assert crop_ms < full_ms, (
        "a 256x256 crop copies in %.2f ms against %.2f for a full frame - "
        "0.25 MB against 8.79 MB should not cost the same, and if it does then "
        "CopySubresourceRegion is not actually narrowing the staging texture"
        % (crop_ms, full_ms))
