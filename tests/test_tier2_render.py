# -*- coding: utf-8 -*-
"""Tier 2 - render a known colour and capture it back.

Every other capture test asserts SHAPE. The frame is the right size, the pitch is
at least width * 4, a crop matches the same region of a full frame. A capture
path that returned the PREVIOUS frame, or one offset by a row, or a stale
staging buffer, would pass all of them.

This is the first test of content against ground truth: draw a specific colour,
capture that rectangle, compare the pixels.

It is also the only thing here that renders, which is how F-60 was found - ten
parameters declared as a scalar where the SDK declares an array, every one on the
rendering path, and unreachable by anything that only captures.

Needs a display and a compositing desktop, so it skips like the rest of tier 2.
"""
import os
import sys

import pytest

from conftest import REPO_ROOT, needs_comtypes, needs_windows

sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

pytestmark = [pytest.mark.tier2, needs_windows, needs_comtypes]

#: Per channel. The desktop compositor is not obliged to be lossless - a colour
#: profile or a scaling factor can shift a value by one or two. Zero drift is
#: what actually happens on the development machine; this leaves room.
TOLERANCE = 4


@pytest.fixture(scope="module")
def probe():
    render_probe = pytest.importorskip("render_probe")
    try:
        instance = render_probe.Probe()
    except Exception as exc:
        pytest.skip("could not create a window and swap chain: %s" % exc)
    yield instance, render_probe
    instance.close()


def test_the_render_path_builds(probe):
    """Window, swap chain, back buffer, render target view.

    Four things this repository could not do before P8, and the whole reason a
    class of defect was unreachable.
    """
    instance, _module = probe
    assert instance.hwnd
    assert instance.swapchain
    assert instance.device
    assert instance.rtv
    assert instance.feature_level.value >= 0xB000


def test_clear_render_target_view_can_be_called(probe):
    """F-60 itself.

    `const FLOAT ColorRGBA[4]` was bound as a single c_float, so this call
    raised ArgumentError - "must be real number, not c_float_Array_4" - and the
    method was impossible to make.
    """
    instance, _module = probe
    instance.clear((10, 20, 30))          # raises if the signature is wrong


@pytest.mark.parametrize("colour", [
    (33, 196, 92),        # the default: green, unlikely on a desktop
    (200, 40, 120),       # magenta, to prove the first was not a coincidence
    (0, 0, 0),            # the edges of the range
    (255, 255, 255),
])
def test_what_was_rendered_is_what_was_captured(probe, colour):
    """The assertion this project did not previously have."""
    instance, module = probe
    got, region = module.sample(instance, colour)

    drift = max(abs(a - b) for a, b in zip(got, colour))
    assert drift <= TOLERANCE, (
        "rendered %s, captured %s from %r - worst channel off by %d. Either the "
        "capture is not returning this window's pixels, or something is drawn "
        "on top of it." % (colour, got, region, drift))


def test_two_colours_in_a_row_are_not_the_same_frame(probe):
    """Guards against the strongest false pass available here.

    If capture returned a stale buffer, every colour would come back as
    whatever was captured first - and each individual comparison above would
    fail, but a single-colour test would have passed. Changing the colour and
    re-reading proves the frame is fresh.
    """
    instance, module = probe

    first, _region = module.sample(instance, (255, 0, 0))
    second, _region = module.sample(instance, (0, 0, 255))

    assert first != second, (
        "two different renders produced identical pixels %s - the capture is "
        "returning a stale frame" % (first,))
    assert abs(first[0] - 255) <= TOLERANCE and abs(first[2] - 0) <= TOLERANCE
    assert abs(second[2] - 255) <= TOLERANCE and abs(second[0] - 0) <= TOLERANCE
