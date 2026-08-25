# -*- coding: utf-8 -*-
"""Tier 1 - every method's return type, against the IDL.

Two defects in P6 were both a wrong `restype`, and neither was reachable by any
test that existed:

    F-58  27 methods declared a Structure as their restype. On x64 a COM method
          returning a structure by value takes a hidden pointer to the caller's
          storage as its first argument; declaring the structure makes ctypes
          read a register holding something else and write through it. Every one
          faulted the interpreter rather than raising.

    F-59  ID3D10Blob::GetBufferPointer was declared `None` where the SDK says
          `LPVOID`, so it returned None and the bytes of every blob were
          unreachable - and a blob is how the root signature serialiser and
          every shader compiler hand back their output.

Both are invisible to reading, invisible to the vtable test (which checks order
and parameter counts) and invisible to the layout probe (which checks
structures). They are only visible by comparing the declaration against the
source of truth, which is what this file does.
"""
import ctypes
import importlib
import os
import sys

import pytest

from conftest import REPO_ROOT, needs_comtypes, needs_windows

sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
import idl  # noqa: E402

pytestmark = [pytest.mark.tier1, needs_windows, needs_comtypes]

#: module -> the IDL it is translated from.
MODULE_IDL = {
    "dxgi": "dxgi.idl",
    "dxgi1_2": "dxgi1_2.idl",
    "dxgi1_3": "dxgi1_3.idl",
    "dxgi1_4": "dxgi1_4.idl",
    "dxgi1_5": "dxgi1_5.idl",
    "dxgi1_6": "dxgi1_6.idl",
    "d3d11": "d3d11.idl",
    "d3d11_1": "d3d11_1.idl",
    "d3d11_2": "d3d11_2.idl",
    "d3d11_3": "d3d11_3.idl",
    "d3d11_4": "d3d11_4.idl",
    "d3d11sdklayers": "d3d11sdklayers.idl",
    "d3dcommon": "d3dcommon.idl",
    "d3d12": "d3d12.idl",
    "d3d12sdklayers": "d3d12sdklayers.idl",
    "d3d12video": "d3d12video.idl",
    "d3d11on12": "d3d11on12.idl",
    "d3d12compatibility": "d3d12compatibility.idl",
}


def _declared(module):
    """{(interface, method): restype} for everything the module declares."""
    binding = importlib.import_module("Direct3D.PyIdl." + module)
    out = {}
    for name, obj in vars(binding).items():
        if not (isinstance(obj, type) and hasattr(obj, "_iid_")):
            continue
        if getattr(obj, "__module__", None) != "Direct3D.PyIdl." + module:
            continue
        for spec in getattr(obj, "_methods_", []):
            out[(name, spec.name)] = spec.restype
    return out


def _is_void(restype):
    return restype is None


def _is_hresult(restype):
    return restype in (ctypes.c_long, ctypes.c_int32) or \
        getattr(restype, "__name__", "") == "HRESULT"


def _points_at(restype, target_name):
    """True if restype is POINTER(<something called target_name>)."""
    inner = getattr(restype, "_type_", None)
    return inner is not None and getattr(inner, "__name__", None) == target_name


@pytest.mark.parametrize("module", sorted(MODULE_IDL))
def test_no_method_returns_a_structure_by_value(module, sdk_include):
    """F-58, as a ratchet.

    A structure declared as the restype is always wrong on x64, whatever the IDL
    says, because the ABI passes a hidden pointer instead. The correct
    declaration is POINTER(that structure) with the same pointer prepended to
    the argument list.
    """
    declared = _declared(module)
    if not declared:
        pytest.skip("%s declares no interfaces" % module)

    offenders = []
    for (interface, method), restype in sorted(declared.items()):
        if isinstance(restype, type) and issubclass(
                restype, (ctypes.Structure, ctypes.Union)):
            offenders.append("%s::%s returns %s by value"
                             % (interface, method, restype.__name__))

    assert not offenders, (
        "a structure as the restype faults on x64 - the ABI passes a hidden "
        "pointer to the caller's storage as the first argument instead. "
        "Declare POINTER(struct) and prepend the same pointer to argtypes:\n  "
        + "\n  ".join(offenders))


@pytest.mark.parametrize("module", sorted(MODULE_IDL))
def test_struct_returning_methods_take_the_hidden_pointer(module, sdk_include):
    """The other half of F-58: the fix must be complete, not half applied.

    A method the IDL says returns a structure must declare POINTER(struct) as
    its restype AND carry that same pointer as its first argument. Declaring
    only the restype would silently drop the hidden argument and corrupt the
    stack.
    """
    interfaces, _structs = idl.load(sdk_include, MODULE_IDL[module])
    if interfaces is None:
        pytest.skip("%s not present in this SDK" % MODULE_IDL[module])

    parsed = idl.module_constructs(sdk_include, MODULE_IDL[module])
    declared = _declared(module)

    problems = []
    for interface, spec in parsed["interfaces"].items():
        for method, (restype, _params) in spec.get("signatures", {}).items():
            if restype.endswith("*") or restype not in parsed["structs"]:
                continue
            binding = importlib.import_module("Direct3D.PyIdl." + module)
            found = None
            for candidate in getattr(getattr(binding, interface, None),
                                     "_methods_", []):
                if candidate.name == method:
                    found = candidate
                    break
            if found is None:
                continue
            if not _points_at(found.restype, restype):
                problems.append("%s::%s restype is %r, expected POINTER(%s)"
                                % (interface, method, found.restype, restype))
                continue
            if not found.argtypes or not _points_at(found.argtypes[0], restype):
                problems.append(
                    "%s::%s returns %s but its first argument is not the "
                    "hidden pointer - the ABI needs both"
                    % (interface, method, restype))

    assert not problems, (
        "the x64 struct-return convention is only half declared:\n  "
        + "\n  ".join(problems))


@pytest.mark.parametrize("module", sorted(MODULE_IDL))
def test_no_method_that_returns_something_is_declared_void(module, sdk_include):
    """F-59: a method whose IDL return type is not `void`, declared as void.

    comtypes accepts it, the call succeeds, and the caller gets None. That is
    how GetBufferPointer made every blob's contents unreachable while looking
    perfectly healthy.
    """
    interfaces, _structs = idl.load(sdk_include, MODULE_IDL[module])
    if interfaces is None:
        pytest.skip("%s not present in this SDK" % MODULE_IDL[module])

    parsed = idl.module_constructs(sdk_include, MODULE_IDL[module])
    binding = importlib.import_module("Direct3D.PyIdl." + module)

    problems = []
    for interface, spec in parsed["interfaces"].items():
        klass = getattr(binding, interface, None)
        if klass is None or getattr(klass, "__module__", None) != \
                "Direct3D.PyIdl." + module:
            continue
        signatures = spec.get("signatures", {})
        for candidate in getattr(klass, "_methods_", []):
            expected = signatures.get(candidate.name, (None, []))[0]
            if expected is None or expected in ("void", "VOID"):
                continue
            if _is_void(candidate.restype):
                problems.append("%s::%s is declared void; the SDK says %s"
                                % (interface, candidate.name, expected))

    assert not problems, (
        "declared void where the SDK returns a value - the call will succeed "
        "and hand the caller None:\n  " + "\n  ".join(problems))
