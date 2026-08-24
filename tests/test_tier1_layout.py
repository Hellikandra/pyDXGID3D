# -*- coding: utf-8 -*-
"""Tier 1 - structure layout against a compiled measurement.

`typemap.self_check()` proves the type table is consistent with itself. It cannot
prove the table matches what the Windows headers actually define - a table can be
uniformly wrong and pass every internal check.

So this asserts against `tests/data/struct_layout.json`, produced by
`tools/layout_probe.py`: a C program that includes the SDK headers and prints
`sizeof` and `offsetof` for every structure. Compiled by MSVC, against the same
headers the bindings were translated from.

The JSON is committed, so these tests need no compiler - only comtypes, to import
the bindings. Regenerate it when the target SDK changes and review the diff.

This is the check that would have caught F-09, F-47 and F-48 on the day each was
written, and it is the one that keeps them from recurring.
"""
import ctypes
import io
import json
import os

import pytest

from conftest import REPO_ROOT, needs_comtypes, needs_windows

pytestmark = [pytest.mark.tier1, needs_windows, needs_comtypes]

LAYOUT_PATH = os.path.join(REPO_ROOT, "tests", "data", "struct_layout.json")

BINDING_MODULES = [
    "Direct3D.PyIdl.dxgicommon", "Direct3D.PyIdl.dxgitype",
    "Direct3D.PyIdl.dxgi", "Direct3D.PyIdl.dxgi1_2",
    "Direct3D.PyIdl.d3dcommon", "Direct3D.PyIdl.d3d11",
    "Direct3D.PyIdl.d3d11sdklayers",
]

#: Structures the bindings deliberately do not declare, or declare under a
#: different name. Each needs a reason, not just an entry.
EXPECTED_ABSENT = {
    # The SDK's struct tag is misspelled (missing a C) while its typedef is not.
    # The bindings copied the tag. See F-50.
    "D3D11_AUTHENTICATED_QUERY_ACCESSIBILITY_OUTPUT":
        "declared under the SDK's misspelled tag ACESSIBILITY - F-50",
}


@pytest.fixture(scope="session")
def layout():
    if not os.path.isfile(LAYOUT_PATH):
        pytest.skip("tests/data/struct_layout.json missing - "
                    "run tools/layout_probe.py on a machine with MSVC")
    with io.open(LAYOUT_PATH, encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture(scope="session")
def bound_structs():
    """{name: ctypes.Structure} for every structure the bindings declare."""
    import importlib
    out = {}
    for module_name in BINDING_MODULES:
        module = importlib.import_module(module_name)
        for name, obj in vars(module).items():
            if (isinstance(obj, type)
                    and issubclass(obj, ctypes.Structure)
                    and obj is not ctypes.Structure
                    and name not in out):
                out[name] = obj
    return out


def test_layout_data_is_present(layout):
    assert layout["structs"], "no structures in the layout data"
    assert layout["pointer_bits"] == 64, (
        "the layout data was measured on a %d-bit build; these bindings target "
        "win-amd64" % layout["pointer_bits"])


def test_pointer_width_matches_layout_data(layout):
    """A 32-bit interpreter cannot satisfy 64-bit offsets. Fail loudly."""
    assert ctypes.sizeof(ctypes.c_void_p) * 8 == layout["pointer_bits"], (
        "running a %d-bit interpreter against %d-bit layout data"
        % (ctypes.sizeof(ctypes.c_void_p) * 8, layout["pointer_bits"]))


#: Structures whose layout is known-wrong, with the reason. Each is a finding.
#: The dict is asserted exactly: a NEW mismatch fails, and fixing one requires
#: deleting its entry. Ratchet downwards only.
KNOWN_SIZE_MISMATCH = {
    "D3D11_VIDEO_PROCESSOR_COLOR_SPACE":
        "F-54: six SDK bitfields totalling 32 bits, declared as six full UINTs",
    "D3D11_AUTHENTICATED_CONFIGURE_PROTECTION_INPUT":
        "F-54: contains a bitfield union declared as plain fields",
    "D3D11_AUTHENTICATED_QUERY_PROTECTION_OUTPUT":
        "F-54: contains a bitfield union declared as plain fields",
    "D3D11_VIDEO_PROCESSOR_STREAM":
        "F-56: six pointer fields commented out pending a forward reference",
}

#: Field names that differ from the SDK, with the reason. Same ratchet.
KNOWN_NAME_MISMATCH = {
    "D3D11_AUTHENTICATED_QUERY_CHANNEL_TYPE_OUTPUT": "F-55: copy-paste from a sibling struct",
    "D3D11_AUTHENTICATED_QUERY_OUTPUT_ID_COUNT_INPUT": "F-55: copy-paste from a sibling struct",
    "D3D11_AUTHENTICATED_QUERY_RESTRICTED_SHARED_RESOURCE_PROCESS_COUNT_OUTPUT":
        "F-55: copy-paste from a sibling struct",
}


def test_structure_sizes(layout, bound_structs):
    """sizeof() for every structure the bindings and the SDK share."""
    problems = []
    for name, spec in sorted(layout["structs"].items()):
        struct = bound_structs.get(name)
        if struct is None:
            continue
        actual = ctypes.sizeof(struct)
        if actual != spec["size"]:
            if name in KNOWN_SIZE_MISMATCH:
                continue
            problems.append("%s is %d bytes, SDK says %d"
                            % (name, actual, spec["size"]))
        elif name in KNOWN_SIZE_MISMATCH:
            problems.append(
                "%s now matches the SDK - delete its KNOWN_SIZE_MISMATCH entry"
                % name)
    assert not problems, "structure size mismatch:\n  " + "\n  ".join(problems)


def test_field_offsets(layout, bound_structs):
    """Every field, at the byte the compiler puts it.

    Reported per field rather than per structure: a single wrong offset is
    usually one wrong type, and knowing which field points straight at it.
    """
    problems = []
    for name, spec in sorted(layout["structs"].items()):
        struct = bound_structs.get(name)
        if struct is None or not spec["fields"]:
            continue
        for field, expected in sorted(spec["fields"].items()):
            descriptor = getattr(struct, field, None)
            if descriptor is None or not hasattr(descriptor, "offset"):
                continue        # name mismatches are the next test's business
            if descriptor.offset != expected:
                problems.append("%s.%s is at %d, SDK puts it at %d"
                                % (name, field, descriptor.offset, expected))
    assert not problems, "field offset mismatch:\n  " + "\n  ".join(problems)


def test_field_names_match_the_sdk(layout, bound_structs):
    """F-20: a field spelled differently to the SDK.

    The layout can be perfectly correct and the name still wrong - which is worse
    than it sounds. Anyone copying from MSDN sets the SDK's name, silently
    creates a new Python attribute, and leaves the real field at whatever memset
    left behind. No error, no warning, wrong value.
    """
    problems = []
    for name, spec in sorted(layout["structs"].items()):
        struct = bound_structs.get(name)
        if struct is None or not spec["fields"]:
            continue
        if name in KNOWN_NAME_MISMATCH:
            continue
        declared = [f[0] for f in getattr(struct, "_fields_", [])]
        if len(declared) != len(spec["fields"]):
            continue        # a count mismatch is a different fault
        for field in sorted(spec["fields"]):
            if field not in declared:
                problems.append(
                    "%s: SDK field %r is not declared; binding has %s"
                    % (name, field, ", ".join(repr(d) for d in declared)))
    assert not problems, "field name mismatch:\n  " + "\n  ".join(problems)


def test_every_measured_struct_is_bound(layout, bound_structs):
    """Coverage in the other direction: what the SDK has and the bindings lack.

    Not a failure in itself - the bindings do not claim to be complete - but an
    unexplained absence should become an explained one, so the exceptions carry
    a reason.
    """
    missing = [name for name in sorted(layout["structs"])
               if name not in bound_structs and name not in EXPECTED_ABSENT]
    # Recorded, not asserted to zero: completing the structure set is P4-P6 work.
    if missing:
        pytest.skip("%d SDK structures not yet bound (expected during the port): "
                    "%s%s" % (len(missing), ", ".join(missing[:8]),
                              " ..." if len(missing) > 8 else ""))
