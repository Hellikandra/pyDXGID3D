# -*- coding: utf-8 -*-
"""Tier 1 - the capture API's contract, without capturing anything.

Everything here runs on a machine with no GPU and no display. CaptureOptions
validates in its constructor precisely so this is possible: a bad region is a
programming error and should be catchable without hardware.

enumerate_outputs() needs DXGI but not a display. On a hosted runner it returns
an empty list, which is a valid answer and is asserted as such.
"""
import pytest

from conftest import needs_comtypes, needs_windows

pytestmark = [pytest.mark.tier1, needs_windows, needs_comtypes]


# ------------------------------------------------------------ the surface --
def test_the_public_surface_is_three_names():
    """S-5: the seam with the downstream project.

    A consumer that has to import a fourth thing has found a gap in this layer.
    The supporting types are exported for annotations, but these three are the
    contract, and this test exists so that widening it is a decision rather than
    an accident.
    """
    import Direct3D.Capture as capture

    for name in ("enumerate_outputs", "CaptureOptions", "DesktopCapture"):
        assert hasattr(capture, name), "%s is missing from the public surface" % name
        assert name in capture.__all__


def test_capture_imports_nothing_from_pyidl_into_its_namespace():
    """The bindings are an implementation detail of this package.

    Not a style point: if DXGI structures leak into Direct3D.Capture's namespace,
    consumers will start using them, and the contract stops being three names.
    """
    import Direct3D.Capture as capture

    leaked = [n for n in capture.__all__ if n.startswith(("IDXGI", "ID3D11",
                                                          "DXGI_", "D3D11_"))]
    assert not leaked, "binding types leaked into the public surface: %s" % leaked


# ------------------------------------------------------------- validation --
def test_defaults_are_valid():
    from Direct3D.Capture import CaptureOptions

    options = CaptureOptions()
    assert options.output == 0
    assert options.region is None
    assert options.skip_unchanged is True
    assert options.on_access_lost == "rebuild"


@pytest.mark.parametrize("region,fragment", [
    ((10, 10, 10, 20), "positive width and height"),
    ((10, 10, 20, 10), "positive width and height"),
    ((10, 10, 5, 20), "positive width and height"),
    ((10, 10, 20), "left, top, right, bottom"),
    ((0, 0, 10, 10, 10), "left, top, right, bottom"),
])
def test_bad_region_is_rejected_at_construction(region, fragment):
    """A region that cannot work should fail on the caller's own line."""
    from Direct3D.Capture import CaptureOptions

    with pytest.raises(ValueError) as caught:
        CaptureOptions(region=region)
    assert fragment in str(caught.value)


def test_region_of_floats_is_a_type_error():
    from Direct3D.Capture import CaptureOptions

    with pytest.raises(TypeError):
        CaptureOptions(region=(0.0, 0.0, 100.0, 100.0))


def test_bad_access_lost_policy_lists_the_valid_ones():
    from Direct3D.Capture import ACCESS_LOST_POLICIES, CaptureOptions

    with pytest.raises(ValueError) as caught:
        CaptureOptions(on_access_lost="retry")
    for policy in ACCESS_LOST_POLICIES:
        assert policy in str(caught.value)


@pytest.mark.parametrize("kwargs,exc", [
    ({"timeout_ms": -1}, ValueError),
    ({"timeout_ms": 1.5}, TypeError),
    ({"timeout_ms": True}, TypeError),
    ({"max_rebuilds": -1}, ValueError),
    ({"max_rebuilds": 2.0}, TypeError),
])
def test_scalar_validation(kwargs, exc):
    from Direct3D.Capture import CaptureOptions

    with pytest.raises(exc):
        CaptureOptions(**kwargs)


def test_cursor_says_it_is_not_implemented():
    """Rather than accepting the flag and silently ignoring it."""
    from Direct3D.Capture import CaptureOptions

    with pytest.raises(NotImplementedError) as caught:
        CaptureOptions(cursor=True)
    assert "cursor" in str(caught.value)


# --------------------------------------------------- coordinate arithmetic --
class _FakeOutput(object):
    """A second monitor placed to the right of the first.

    The interesting case, and the one that fails silently when it is wrong: a
    region given in desktop coordinates has to be translated to the output's own
    frame before it reaches D3D11_BOX. Get it wrong and the capture succeeds and
    returns black.
    """
    index = 1
    left, top, right, bottom = 1920, 0, 3840, 1080

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top


def test_region_is_translated_into_output_local_coordinates():
    from Direct3D.Capture import CaptureOptions

    options = CaptureOptions(region=(2000, 100, 2256, 356))
    assert options.region_within(_FakeOutput()) == (80, 100, 336, 356)


def test_no_region_covers_the_whole_output():
    from Direct3D.Capture import CaptureOptions

    assert CaptureOptions().region_within(_FakeOutput()) == (0, 0, 1920, 1080)


def test_region_outside_the_output_names_both_rectangles():
    from Direct3D.Capture import CaptureOptions

    options = CaptureOptions(region=(0, 0, 256, 256))     # on the first monitor
    with pytest.raises(ValueError) as caught:
        options.region_within(_FakeOutput())
    message = str(caught.value)
    assert "1920" in message and "desktop coordinates" in message


# ------------------------------------------------------------ enumeration --
def test_enumerate_outputs_is_well_formed():
    """Empty is a valid answer; malformed is not."""
    from Direct3D.Capture import Adapter, Output, enumerate_outputs

    outputs = enumerate_outputs()
    assert isinstance(outputs, list)
    for index, output in enumerate(outputs):
        assert isinstance(output, Output)
        assert output.index == index, "indices must be dense and in order"
        assert isinstance(output.adapter, Adapter)
        assert output.width > 0 and output.height > 0
        assert output.right - output.left == output.width
        assert output.bottom - output.top == output.height
        assert output.bounds == (output.left, output.top,
                                 output.right, output.bottom)
        assert output.device_name


def test_every_output_carries_its_own_adapter():
    """C-4: the adapter that owns the output, not merely 'an adapter'.

    On a hybrid laptop the panel hangs off the integrated GPU while the discrete
    one has no outputs at all. Creating the device on the wrong adapter makes
    DuplicateOutput fail, so pairing them at enumeration is what makes capture
    work at all.
    """
    from Direct3D.Capture import enumerate_outputs

    for output in enumerate_outputs():
        assert output.adapter is not None
        assert output.adapter._adapter, "the COM pointer must be kept alive"


def test_resolve_output_rejects_a_missing_index_by_listing_what_exists():
    from Direct3D.Capture import enumerate_outputs, resolve_output

    outputs = enumerate_outputs()
    if not outputs:
        pytest.skip("no attached display")
    with pytest.raises(ValueError) as caught:
        resolve_output(len(outputs) + 50, outputs)
    assert "Available" in str(caught.value)


def test_resolve_output_accepts_index_name_and_object():
    from Direct3D.Capture import enumerate_outputs, resolve_output

    outputs = enumerate_outputs()
    if not outputs:
        pytest.skip("no attached display")
    first = outputs[0]
    assert resolve_output(first, outputs) is first
    assert resolve_output(first.index, outputs) is first
    assert resolve_output(first.device_name, outputs) is first


def test_resolve_output_rejects_a_wrong_type():
    from Direct3D.Capture import resolve_output

    with pytest.raises(TypeError):
        resolve_output(1.0, [])


def test_desktop_capture_rejects_a_non_options_argument():
    from Direct3D.Capture import DesktopCapture

    with pytest.raises(TypeError):
        DesktopCapture({"output": 0})
