# -*- coding: utf-8 -*-
"""Tier 2 - call the API broadly and assert nothing breaks in the calling.

The rest of the suite is deep on a few paths and static everywhere else. This
is the opposite: shallow, but across every interface a real machine can produce
an instance of.

It exists because F-58 and F-59 were both wrong return types, both invisible to
every static check, and both found by calling a method rather than reading one.
The static checks now cover return types too - but the general lesson is that a
suite has a shape, and what survives it is whatever lies outside that shape.
Calling things is how you find out what you did not think to check.

`tools/exercise.py` does the work. This asserts on the result.
"""
import os
import sys

import pytest

from conftest import REPO_ROOT, needs_comtypes, needs_windows

sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

pytestmark = [pytest.mark.tier2, needs_windows, needs_comtypes]


@pytest.fixture(scope="module")
def exercised():
    """(results, exercise module) after one pass over everything available."""
    exercise = pytest.importorskip("exercise")
    try:
        live = exercise.build()
    except Exception as exc:
        pytest.skip("could not build any COM objects: %s" % exc)
    if not live:
        pytest.skip("no COM objects available on this machine")
    return [exercise.exercise(name, obj) for name, obj in live if obj], exercise


def test_objects_were_actually_built(exercised):
    results, _ = exercised
    assert results, "nothing was exercised, so nothing below means anything"


def test_no_call_broke(exercised):
    """The assertion that matters.

    A failing HRESULT is fine - the call reached the driver and came back. What
    must not happen is the CALL failing: a signature ctypes cannot marshal, or a
    method reading memory it should not. That is a binding defect every time.
    """
    results, _ = exercised
    problems = ["%s::%s  %s" % (r.name, method, why)
                for r in results for method, why in r.failed]
    assert not problems, (
        "these methods did not survive being called. A failing HRESULT would "
        "have counted as success, so each of these is a defect in the "
        "declaration rather than in the driver's answer:\n  "
        + "\n  ".join(problems))


def test_a_meaningful_number_of_methods_ran(exercised):
    """Guards against the whole thing quietly becoming a no-op.

    A test that exercises nothing passes just as loudly as one that exercises
    everything, which is how C-27 happened. The floor is deliberately well below
    what this machine manages - the point is to notice a collapse, not to pin a
    number that varies with the hardware.
    """
    results, _ = exercised
    called = sum(r.attempted for r in results)
    assert called >= 20, (
        "only %d methods were called. On a machine with a display and a D3D11 "
        "device this should be dozens; something has stopped building objects."
        % called)


def test_every_built_object_had_its_vtable_walked(exercised):
    """Inherited methods count.

    comtypes gives each class in the chain only its own _methods_, so reading
    one class finds a fraction of the vtable. If this regresses, IDXGIObject's
    methods stop being exercised on every DXGI object that inherits them.
    """
    results, _ = exercised
    empty = [r.name for r in results if r.total == 0]
    assert not empty, (
        "these objects reported no methods at all, which means the vtable walk "
        "is broken rather than that they are empty:\n  " + "\n  ".join(empty))


def test_the_capture_interfaces_are_among_them(exercised):
    """The path this project exists for should be in the sample, not adjacent
    to it."""
    results, _ = exercised
    names = {r.name for r in results}
    assert "IDXGIOutput" in names or "IDXGIOutput1" in names, (
        "no output was exercised; tier 2 needs an attached display")
    assert "ID3D11Device" in names, "no Direct3D 11 device was built"
