# -*- coding: utf-8 -*-
"""Tier 1 - the translated cpp_quote macros, against the SDK's own answers.

Fourteen function-like macros in d3d12.idl and ten in d3d11.idl are emitted as
Python functions. The translation is mechanical - `&`, `|`, `<<` and `>>` mean
the same in both languages - but two things could go wrong silently and produce
a number rather than an error:

  * `&&` rewritten after `&` rather than before, turning a bitwise or into a
    logical one;
  * a C cast left in, so the expression returns a ctypes instance.

Neither would raise. Both would encode a sampler filter that is quietly the
wrong filter.

What makes this checkable is that the SDK enumerates the answers. D3D12_FILTER
lists every combination D3D12_ENCODE_BASIC_FILTER can produce, with its value,
so the macro can be checked against the header's own arithmetic rather than
against a number someone wrote down here.
"""
import pytest

from conftest import needs_comtypes, needs_windows

pytestmark = [pytest.mark.tier1, needs_windows, needs_comtypes]


@pytest.fixture(scope="module")
def d3d12():
    return pytest.importorskip("Direct3D.PyIdl.d3d12")


def test_the_macros_are_callable(d3d12):
    """Emitted as functions, not as constants that happen to parse."""
    for name in ("D3D12_ENCODE_BASIC_FILTER",
                 "D3D12_ENCODE_ANISOTROPIC_FILTER",
                 "D3D12_DECODE_MIN_FILTER",
                 "D3D12_DECODE_MAG_FILTER",
                 "D3D12_DECODE_MIP_FILTER",
                 "D3D12_DECODE_FILTER_REDUCTION",
                 "D3D12_DECODE_IS_COMPARISON_FILTER",
                 "D3D12_ENCODE_SHADER_4_COMPONENT_MAPPING",
                 "D3D12_DECODE_SHADER_4_COMPONENT_MAPPING",
                 "D3D12_MAKE_COARSE_SHADING_RATE"):
        assert callable(getattr(d3d12, name)), "%s is not callable" % name


#: (min, mag, mip, the D3D12_FILTER the SDK says that combination is).
#: Spelled out rather than generated, so the test cannot agree with the code by
#: sharing its arithmetic.
BASIC_FILTERS = [
    ("POINT", "POINT", "POINT", "D3D12_FILTER_MIN_MAG_MIP_POINT"),
    ("POINT", "POINT", "LINEAR", "D3D12_FILTER_MIN_MAG_POINT_MIP_LINEAR"),
    ("POINT", "LINEAR", "POINT", "D3D12_FILTER_MIN_POINT_MAG_LINEAR_MIP_POINT"),
    ("POINT", "LINEAR", "LINEAR", "D3D12_FILTER_MIN_POINT_MAG_MIP_LINEAR"),
    ("LINEAR", "POINT", "POINT", "D3D12_FILTER_MIN_LINEAR_MAG_MIP_POINT"),
    ("LINEAR", "POINT", "LINEAR", "D3D12_FILTER_MIN_LINEAR_MAG_POINT_MIP_LINEAR"),
    ("LINEAR", "LINEAR", "POINT", "D3D12_FILTER_MIN_MAG_LINEAR_MIP_POINT"),
    ("LINEAR", "LINEAR", "LINEAR", "D3D12_FILTER_MIN_MAG_MIP_LINEAR"),
]


@pytest.mark.parametrize("minimum,magnify,mip,expected", BASIC_FILTERS)
def test_encode_basic_filter_matches_the_enum(d3d12, minimum, magnify, mip,
                                              expected):
    """All eight combinations, against the values D3D12_FILTER declares."""
    encoded = d3d12.D3D12_ENCODE_BASIC_FILTER(
        getattr(d3d12, "D3D12_FILTER_TYPE_" + minimum),
        getattr(d3d12, "D3D12_FILTER_TYPE_" + magnify),
        getattr(d3d12, "D3D12_FILTER_TYPE_" + mip),
        d3d12.D3D12_FILTER_REDUCTION_TYPE_STANDARD)
    assert encoded == getattr(d3d12, expected)
    assert isinstance(encoded, int), (
        "a cast survived the translation and this is a ctypes instance, not an "
        "int - it will not compose with | and will not match the enum")


@pytest.mark.parametrize("reduction,expected", [
    ("STANDARD", "D3D12_FILTER_ANISOTROPIC"),
    ("COMPARISON", "D3D12_FILTER_COMPARISON_ANISOTROPIC"),
    ("MINIMUM", "D3D12_FILTER_MINIMUM_ANISOTROPIC"),
    ("MAXIMUM", "D3D12_FILTER_MAXIMUM_ANISOTROPIC"),
])
def test_encode_anisotropic_filter_matches_the_enum(d3d12, reduction, expected):
    """This one calls D3D12_ENCODE_BASIC_FILTER, so it also proves a macro can
    call another macro."""
    encoded = d3d12.D3D12_ENCODE_ANISOTROPIC_FILTER(
        getattr(d3d12, "D3D12_FILTER_REDUCTION_TYPE_" + reduction))
    assert encoded == getattr(d3d12, expected)


@pytest.mark.parametrize("minimum,magnify,mip", [
    ("POINT", "LINEAR", "POINT"),
    ("LINEAR", "POINT", "LINEAR"),
    ("LINEAR", "LINEAR", "POINT"),
])
def test_decode_round_trips_encode(d3d12, minimum, magnify, mip):
    """Encode then decode returns what went in, field by field."""
    wanted = [getattr(d3d12, "D3D12_FILTER_TYPE_" + n)
              for n in (minimum, magnify, mip)]
    encoded = d3d12.D3D12_ENCODE_BASIC_FILTER(
        wanted[0], wanted[1], wanted[2],
        d3d12.D3D12_FILTER_REDUCTION_TYPE_STANDARD)
    assert d3d12.D3D12_DECODE_MIN_FILTER(encoded) == wanted[0]
    assert d3d12.D3D12_DECODE_MAG_FILTER(encoded) == wanted[1]
    assert d3d12.D3D12_DECODE_MIP_FILTER(encoded) == wanted[2]
    assert (d3d12.D3D12_DECODE_FILTER_REDUCTION(encoded)
            == d3d12.D3D12_FILTER_REDUCTION_TYPE_STANDARD)


def test_is_comparison_filter(d3d12):
    """`&&` in the source. If it were rewritten after `&`, this would still
    return a number - just the wrong one."""
    assert d3d12.D3D12_DECODE_IS_COMPARISON_FILTER(
        d3d12.D3D12_FILTER_COMPARISON_MIN_MAG_MIP_POINT)
    assert not d3d12.D3D12_DECODE_IS_COMPARISON_FILTER(
        d3d12.D3D12_FILTER_MIN_MAG_MIP_POINT)


def test_shader_component_mapping(d3d12):
    """The identity mapping, which the SDK also declares as a constant.

    D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING is itself defined as a call to this
    macro, so agreement proves the constant was evaluated with the same
    arithmetic the header intends - 0x1688.
    """
    assert (d3d12.D3D12_ENCODE_SHADER_4_COMPONENT_MAPPING(0, 1, 2, 3)
            == d3d12.D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING)
    assert d3d12.D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING == 0x1688

    for component in range(4):
        assert d3d12.D3D12_DECODE_SHADER_4_COMPONENT_MAPPING(
            component, d3d12.D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING) == component


def test_coarse_shading_rate(d3d12):
    """Two axes packed into one byte, and taken back out again."""
    for x in range(4):
        for y in range(4):
            rate = d3d12.D3D12_MAKE_COARSE_SHADING_RATE(x, y)
            assert d3d12.D3D12_GET_COARSE_SHADING_RATE_X_AXIS(rate) == x
            assert d3d12.D3D12_GET_COARSE_SHADING_RATE_Y_AXIS(rate) == y


def test_d3d11_status_macros_build_real_hresults():
    """d3d11.idl's macros are written in terms of MAKE_HRESULT, which no .idl
    declares - it comes from winerror.h and this project supplies it in
    status.py. If that import were missing the module would still import and
    only fail when called."""
    d3d11 = pytest.importorskip("Direct3D.PyIdl.d3d11")

    # _FACD3D11 is 0x87c; severity 1 makes it a failure code.
    assert d3d11.MAKE_D3D11_HRESULT(1) == 0x887C0001
    assert d3d11.MAKE_D3D11_STATUS(1) == 0x087C0001
