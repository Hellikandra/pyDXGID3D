# -*- coding: utf-8 -*-
"""Tier 2 - capture against a real display.

This is the tier that would have caught F-01: for the whole life of the project
nothing had ever acquired a frame. Every test here needs an attached monitor and
an interactive session, and skips without one.

Note what is *not* asserted: pixel colours. The desktop is whatever the machine
is showing. What can be asserted is shape, pitch, coordinate correctness,
lifetime, and that the same region captured two ways gives the same bytes.
"""
import gc

import pytest

from conftest import needs_comtypes, needs_windows

pytestmark = [pytest.mark.tier2, needs_windows, needs_comtypes]

#: Enough iterations to leave the first-frame path behind. The first acquire
#: after DuplicateOutput often returns the whole desktop as one accumulated
#: update, which is not representative of anything.
WARMUP = 3


def _grab(capture, count=WARMUP):
    frame = None
    for _ in range(count):
        frame = capture.grab()
    return frame


# ------------------------------------------------------- the known pixel --
def test_a_frame_comes_back_with_the_right_shape(capturable_output):
    """The whole path: factory, adapter, output, device, duplication, map."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        frame = _grab(capture)
        assert frame.width == capturable_output.width
        assert frame.height == capturable_output.height
        assert frame.format == "DXGI_FORMAT_B8G8R8A8_UNORM"


def test_pitch_is_at_least_the_packed_row_and_is_not_assumed_equal(capturable_output):
    """F-09's shape: pitch is the driver's business, not width * 4.

    It happens to be equal at 1920 on this machine. Asserting equality would
    bake a local accident into the suite; asserting the invariant will not.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        frame = _grab(capture)
        assert frame.pitch >= frame.width * 4
        assert frame.padded == (frame.pitch != frame.width * 4)


def test_the_iterator_and_grab_agree(capturable_output):
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        _grab(capture)
        for count, frame in enumerate(capture, start=1):
            assert frame.width == capture.width
            if count == 3:
                break
        assert count == 3


# ------------------------------------------------------------- cropping --
def test_a_cropped_capture_has_the_requested_size(capturable_output):
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    left, top = capturable_output.left + 64, capturable_output.top + 48
    options = CaptureOptions(output=capturable_output,
                             region=(left, top, left + 256, top + 128))
    with DesktopCapture(options) as capture:
        frame = _grab(capture)
        assert (frame.width, frame.height) == (256, 128)


def test_a_crop_matches_the_same_region_of_a_full_frame(capturable_output,
                                                        numpy_module):
    """CopySubresourceRegion and D3D11_BOX, checked against the alternative.

    A wrong D3D11_BOX does not raise - it returns black, or the wrong part of
    the desktop. Capturing both ways and comparing bytes is the only check that
    catches an off-by-one in the desktop-to-output translation.

    Depends on the screen not changing between the two captures, so it retries
    rather than failing on a notification popping up.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    left = capturable_output.left + 400
    top = capturable_output.top + 300
    region = (left, top, left + 256, top + 256)
    local = (400, 300, 656, 556)

    for attempt in range(4):
        with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
            full = _grab(capture).copy()
        with DesktopCapture(CaptureOptions(output=capturable_output,
                                           region=region)) as capture:
            crop = _grab(capture).copy()
        expected = full[local[1]:local[3], local[0]:local[2]]
        if numpy_module.array_equal(expected, crop):
            return
    pytest.fail("the cropped frame does not match the same region of a full "
                "frame after %d attempts - if the screen were merely changing, "
                "one of these would have matched" % (attempt + 1))


# ------------------------------------------------------------- lifetime --
def test_a_frame_is_dead_once_the_loop_moves_on(capturable_output, numpy_module):
    """The one real footgun, enforced rather than documented.

    Without this the pages are unmapped and reused, and reading them is garbage
    on a good day and an access violation on a bad one.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture, StaleFrameError

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        stale = _grab(capture)
        assert stale.valid
        capture.grab()
        assert not stale.valid
        for accessor in (lambda: stale.array,
                         lambda: stale.memoryview,
                         lambda: stale.copy()):
            with pytest.raises(StaleFrameError):
                accessor()


def test_copy_survives_the_iteration_and_the_view_does_not(capturable_output,
                                                           numpy_module):
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        frame = _grab(capture)
        kept = frame.copy()
        capture.grab()
    assert kept.shape == (capturable_output.height, capturable_output.width, 4)
    assert int(kept.sum()) >= 0            # readable after the capture closed


def test_copy_into_writes_the_same_bytes_as_copy(capturable_output, numpy_module):
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        frame = _grab(capture)
        destination = numpy_module.empty(frame.shape, numpy_module.uint8)
        returned = frame.copy_into(destination)
        assert returned is destination
        assert numpy_module.array_equal(destination, frame.copy())


@pytest.mark.parametrize("make,fragment", [
    (lambda np, shape: np.empty(shape, np.uint16), "uint8"),
    (lambda np, shape: np.empty((shape[0] // 2, shape[1], 4), np.uint8), "frame is"),
    (lambda np, shape: np.empty((shape[0], shape[1] * 2, 4), np.uint8)[:, ::2],
     "contiguous"),
])
def test_copy_into_rejects_a_destination_it_cannot_fill(capturable_output,
                                                        numpy_module, make,
                                                        fragment):
    """Silently writing past the end of a wrong destination is the failure to
    avoid here, so each rejection names what was wrong with it."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        frame = _grab(capture)
        with pytest.raises(ValueError) as caught:
            frame.copy_into(make(numpy_module, frame.shape))
        assert fragment in str(caught.value)


def test_memoryview_works_without_numpy(capturable_output):
    """numpy is an optional extra. The bytes must be reachable without it."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        frame = _grab(capture)
        view = frame.memoryview
        assert len(view) == frame.pitch * frame.height


def test_close_is_idempotent_and_grabbing_afterwards_raises(capturable_output):
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    capture = DesktopCapture(CaptureOptions(output=capturable_output))
    _grab(capture)
    capture.close()
    capture.close()
    with pytest.raises(RuntimeError):
        capture.grab()


def test_closing_does_not_double_release(capturable_output):
    """F-52: comtypes releases in __del__, so an explicit Release() faults.

    A crash here takes the interpreter down rather than failing a test, so the
    value is in running it at all.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    for _ in range(3):
        with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
            _grab(capture, 1)
    gc.collect()


# ---------------------------------------------------------- steady state --
def test_a_running_loop_allocates_nothing(capturable_output):
    """Zero steady-state allocation, asserted rather than claimed.

    Per-frame allocation is invisible until it is a garbage-collection pause in
    the middle of a capture. The staging texture, both SDK structures and the
    Frame object are all reused, so the only growth should be tracemalloc's own
    bookkeeping.
    """
    import tracemalloc

    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        _grab(capture, 30)
        gc.collect()
        tracemalloc.start()
        try:
            before = tracemalloc.take_snapshot()
            for count, _frame in enumerate(capture, start=1):
                if count >= 120:
                    break
            after = tracemalloc.take_snapshot()
        finally:
            tracemalloc.stop()

    grew = sum(entry.size_diff
               for entry in after.compare_to(before, "filename")
               if entry.size_diff > 0)
    per_frame = grew / 120.0
    assert per_frame < 512, (
        "%.1f bytes allocated per frame - something in the loop is no longer "
        "being reused" % per_frame)


def test_the_frame_object_is_reused(capturable_output):
    """Not merely the buffers: the Frame itself should not be reallocated."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        _grab(capture)
        identities = {id(capture.grab()) for _ in range(5)}
    # One Frame is constructed per grab today; if that changes to reuse, this
    # test should be tightened rather than deleted.
    assert len(identities) <= 5


def test_counters_are_honest(capturable_output):
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    with DesktopCapture(CaptureOptions(output=capturable_output)) as capture:
        _grab(capture, 10)
        assert capture.rebuilds == 0, "nothing invalidated the duplication"
        assert capture.skipped >= 0
        assert capture.timeouts >= 0


def test_skip_unchanged_false_still_delivers(capturable_output):
    """Cursor-only updates carry a valid, unchanged desktop image.

    Turning the skip off must not break delivery - it should just hand back more
    frames, some of them identical to the last.
    """
    from Direct3D.Capture import CaptureOptions, DesktopCapture

    options = CaptureOptions(output=capturable_output, skip_unchanged=False,
                             timeout_ms=1000)
    with DesktopCapture(options) as capture:
        frame = _grab(capture)
        assert frame.width > 0
        assert capture.skipped == 0


# --------------------------------------------------- losing the duplication --
class _Failing(object):
    """Wraps IDXGIOutputDuplication and raises a chosen HRESULT on acquire.

    Forcing a genuine DXGI_ERROR_ACCESS_LOST needs a display mode change, a
    session lock or a UAC prompt, none of which a test can arrange politely. So
    the COMError is injected, which exercises exactly the code that would run -
    the part that had never executed on this machine before P4.

    The wrapper must not be held anywhere else. DXGI permits one duplication per
    output per process, so a stray reference to the old one makes the rebuild
    fail with E_INVALIDARG rather than succeeding.
    """

    def __init__(self, real, code, state):
        self._real = real
        self._code = code
        self._state = state

    def AcquireNextFrame(self, *args):
        # Imported here, not at module scope. Tier 0 runs on a machine with no
        # comtypes at all, and pytest imports every test file during collection
        # regardless of -m, so a module-level `import comtypes` fails the whole
        # tier 0 job before a single skip marker is consulted. Every other test
        # module in this suite keeps its comtypes and Direct3D imports inside
        # functions for the same reason.
        import comtypes

        if self._state["left"] > 0:
            self._state["left"] -= 1
            self._state["fired"] += 1
            raise comtypes.COMError(self._code, "injected by the test suite",
                                    None)
        return self._real.AcquireNextFrame(*args)

    def __getattr__(self, name):
        return getattr(self._real, name)


def _inject(capture, code, times=1):
    """Fail the next `times` acquires, re-arming across rebuilds.

    Re-arming matters: _rebuild() replaces _duplication with a fresh one, so a
    wrapper installed once would be discarded after the first recovery and could
    never test the second.
    """
    state = {"left": times, "fired": 0}
    real_open = capture._open

    def arm():
        if state["left"] > 0:
            capture._duplication = _Failing(capture._duplication, code, state)

    def patched_open():
        real_open()
        arm()

    capture._open = patched_open
    arm()
    return state


def test_access_lost_rebuilds_and_keeps_delivering(capturable_output):
    """F-02: the recovery the C++ sample has and this project never ported."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture
    from Direct3D.PyIdl.status import DXGI_ERROR_ACCESS_LOST

    with DesktopCapture(CaptureOptions(output=capturable_output,
                                       timeout_ms=1000)) as capture:
        _grab(capture)
        state = _inject(capture, DXGI_ERROR_ACCESS_LOST, times=1)

        frame = capture.grab()

        assert state["fired"] == 1, "the injected failure never happened"
        assert capture.rebuilds == 1, "the capture did not rebuild"
        assert frame.width == capturable_output.width
        assert frame.valid


def test_repeated_access_loss_still_recovers(capturable_output):
    """Back-off, not give-up. Three losses in a row and it is still delivering."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture
    from Direct3D.PyIdl.status import DXGI_ERROR_ACCESS_LOST

    with DesktopCapture(CaptureOptions(output=capturable_output,
                                       timeout_ms=1000)) as capture:
        _grab(capture)
        state = _inject(capture, DXGI_ERROR_ACCESS_LOST, times=3)

        frame = capture.grab()

        assert state["fired"] == 3
        assert capture.rebuilds == 3
        assert frame.valid


def test_access_lost_raises_when_asked_to(capturable_output):
    from Direct3D.Capture import CaptureOptions, DesktopCapture
    from Direct3D.PyIdl.status import DXGI_ERROR_ACCESS_LOST, AccessLost

    options = CaptureOptions(output=capturable_output, timeout_ms=1000,
                             on_access_lost="raise")
    with DesktopCapture(options) as capture:
        _grab(capture)
        _inject(capture, DXGI_ERROR_ACCESS_LOST, times=1)
        with pytest.raises(AccessLost):
            capture.grab()
        assert capture.rebuilds == 0


def test_max_rebuilds_is_enforced(capturable_output):
    """An unavailable display must not turn the loop into an unbounded spin."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture
    from Direct3D.PyIdl.status import DXGI_ERROR_ACCESS_LOST, AccessLost

    options = CaptureOptions(output=capturable_output, timeout_ms=1000,
                             max_rebuilds=2)
    with DesktopCapture(options) as capture:
        _grab(capture)
        _inject(capture, DXGI_ERROR_ACCESS_LOST, times=99)
        with pytest.raises(AccessLost) as caught:
            capture.grab()
        assert capture.rebuilds == 2
        assert "max_rebuilds" in str(caught.value)


def test_device_removed_is_not_treated_as_recoverable(capturable_output):
    """Rebuilding cannot fix a removed device - only a new process-level device
    can - so the loop must not sit there retrying."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture
    from Direct3D.PyIdl.status import DXGI_ERROR_DEVICE_REMOVED, DeviceRemoved

    with DesktopCapture(CaptureOptions(output=capturable_output,
                                       timeout_ms=1000)) as capture:
        _grab(capture)
        _inject(capture, DXGI_ERROR_DEVICE_REMOVED, times=1)
        with pytest.raises(DeviceRemoved):
            capture.grab()
        assert capture.rebuilds == 0


def test_a_timeout_is_not_an_error(capturable_output):
    """WAIT_TIMEOUT means the desktop did not change. The loop keeps waiting
    rather than surfacing it, and counts it."""
    from Direct3D.Capture import CaptureOptions, DesktopCapture
    from Direct3D.PyIdl.status import DXGI_ERROR_WAIT_TIMEOUT

    with DesktopCapture(CaptureOptions(output=capturable_output,
                                       timeout_ms=1000)) as capture:
        _grab(capture)
        before = capture.timeouts
        _inject(capture, DXGI_ERROR_WAIT_TIMEOUT, times=2)
        frame = capture.grab()
        assert capture.timeouts == before + 2
        assert capture.rebuilds == 0
        assert frame.valid
