# -*- coding: utf-8 -*-
"""Tier 1 - vtable alignment against the Windows SDK.

comtypes builds each interface's vtable by position. A method missing from the
middle of a `_methods_` list does not raise, does not warn, and does not fail to
import: it silently shifts every later slot, so calling method N dispatches to
whatever the SDK put at slot N-1. With mismatched arguments, on the stack.

That is finding F-41, and no other kind of check can see it. Not the import smoke
test, not a size assertion, not review - the file reads perfectly.

These tests need the Windows SDK to read the .idl from. They do not need a GPU,
and only the stub check needs comtypes.
"""
import ast
import io
import os
import sys

import pytest

from conftest import REPO_ROOT

pytestmark = pytest.mark.tier1

sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
import idl  # noqa: E402

#: Binding module -> the IDL it was translated from.
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
}

#: Interfaces whose Python name differs from the SDK's, or that have no IDL.
#: dxgidebug ships as a header only, so there is nothing to diff it against.
NO_IDL = {"IDXGIDebug", "IDXGIDebug1", "IDXGIInfoQueue"}


def _method_spec(element):
    """(name, declared_param_count) for a STDMETHOD or COMMETHOD call node.

    The two put their arguments in different places, and the bindings use both:

        STDMETHOD(restype, "Name", [argtypes])          name at index 1
        COMMETHOD([idlflags], restype, "Name", *args)   name at index 2

    Reading index 1 unconditionally makes the single COMMETHOD in the bindings -
    IDXGISwapChain::GetBuffer - look like a missing method, which reports the
    whole interface as misaligned from slot 1. It is not; the extractor was.
    """
    func = element.func
    callee = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
    args = element.args
    if callee == "COMMETHOD":
        if len(args) >= 3 and isinstance(args[2], ast.Constant):
            return args[2].value, len(args) - 3
        return None, None
    if len(args) >= 2 and isinstance(args[1], ast.Constant):
        count = len(args[2].elts) if len(args) >= 3 and isinstance(args[2], ast.List) else None
        return args[1].value, count
    return None, None


def _method_names(list_node):
    names = []
    for element in list_node.elts:
        if isinstance(element, ast.Call):
            name, _count = _method_spec(element)
            if name:
                names.append(name)
    return names


def _python_methods(module):
    """{interface: [method names in declared order]} from the binding source.

    Two shapes are valid and both appear in the tree:

        class IFoo(IBar):            hand-written
            _methods_ = [...]

        class IFoo(IBar): ...        generated
        IFoo._methods_ = [...]       assigned once every class exists

    Reading only the first shape made this test pass VACUOUSLY on the generated
    modules - it found no methods, so it compared nothing and reported success.
    A test that silently checks nothing is worse than one that fails.
    """
    path = os.path.join(REPO_ROOT, "Direct3D", "PyIdl", module + ".py")
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    out = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign):
                continue
            if "_methods_" not in [t.id for t in stmt.targets
                                   if isinstance(t, ast.Name)]:
                continue
            out[node.name] = _method_names(stmt.value)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.List):
            continue
        for target in node.targets:
            if (isinstance(target, ast.Attribute)
                    and target.attr == "_methods_"
                    and isinstance(target.value, ast.Name)):
                out[target.value.id] = _method_names(node.value)
    return out


def _python_empty_params(module):
    """{(interface, method)} for methods declaring an empty parameter list."""
    path = os.path.join(REPO_ROOT, "Direct3D", "PyIdl", module + ".py")
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign):
                continue
            if "_methods_" not in [t.id for t in stmt.targets
                                   if isinstance(t, ast.Name)]:
                continue
            for element in stmt.value.elts:
                if not isinstance(element, ast.Call):
                    continue
                name, count = _method_spec(element)
                if name and count == 0:
                    out.add((node.name, name))
    return out


@pytest.mark.parametrize("module", sorted(MODULE_IDL))
def test_vtable_order_matches_idl(module, sdk_include):
    """Every method, at the position the SDK puts it.

    Reported as the FIRST divergent slot rather than a set difference, because
    that is the slot from which everything after it is wrong.
    """
    interfaces, _structs = idl.load(sdk_include, MODULE_IDL[module])
    if interfaces is None:
        pytest.skip("%s not present in this SDK" % MODULE_IDL[module])

    problems = []
    for name, declared in sorted(_python_methods(module).items()):
        if name in NO_IDL or name not in interfaces:
            continue
        expected = interfaces[name]["methods"]

        for slot, (want, got) in enumerate(zip(expected, declared)):
            if want != got:
                problems.append(
                    "%s slot %d: SDK has %r, binding has %r "
                    "- every slot from here on is misaligned"
                    % (name, slot, want, got))
                break
        else:
            if len(declared) < len(expected):
                missing = expected[len(declared):]
                problems.append(
                    "%s stops at slot %d of %d; missing tail: %s"
                    % (name, len(declared), len(expected), ", ".join(missing)))
            elif len(declared) > len(expected):
                problems.append(
                    "%s declares %d methods, SDK has %d - extra: %s"
                    % (name, len(declared), len(expected),
                       ", ".join(declared[len(expected):])))

    assert not problems, "vtable misalignment:\n  " + "\n  ".join(problems)


@pytest.mark.parametrize("module", sorted(MODULE_IDL))
def test_interface_iid_matches_idl(module, sdk_include):
    """The IID identifies the vtable. A wrong one QIs to the wrong interface."""
    interfaces, _structs = idl.load(sdk_include, MODULE_IDL[module])
    if interfaces is None:
        pytest.skip("%s not present in this SDK" % MODULE_IDL[module])

    path = os.path.join(REPO_ROOT, "Direct3D", "PyIdl", module + ".py")
    tree = ast.parse(io.open(path, encoding="utf-8").read())

    problems = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or node.name not in interfaces:
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign):
                continue
            if "_iid_" not in [t.id for t in stmt.targets
                               if isinstance(t, ast.Name)]:
                continue
            try:
                value = stmt.value.args[0].value.strip("{}").lower()
            except (AttributeError, IndexError):
                problems.append("%s: _iid_ is not a GUID literal" % node.name)
                continue
            expected = (interfaces[node.name]["uuid"] or "").lower()
            if expected and value != expected:
                problems.append("%s: binding %s, SDK %s"
                                % (node.name, value, expected))

    assert not problems, "IID mismatch:\n  " + "\n  ".join(problems)


@pytest.mark.parametrize("module", sorted(MODULE_IDL))
def test_no_new_parameterless_stubs(module, sdk_include):
    """F-49: a method declaring `[]` where the SDK declares parameters.

    Such a method occupies its vtable slot correctly - alignment is fine - but it
    cannot be called: comtypes will pass no arguments at all. It is a placeholder
    wearing a binding's clothes.

    82 of these exist today, almost entirely in the video and debug interfaces
    that nothing uses. The budget below freezes that number so the count can only
    go down. Lower it as they are filled in.
    """
    interfaces, _structs = idl.load(sdk_include, MODULE_IDL[module])
    if interfaces is None:
        pytest.skip("%s not present in this SDK" % MODULE_IDL[module])

    path = idl.idl_path(sdk_include, MODULE_IDL[module])
    text = idl.strip_comments(io.open(path, encoding="utf-8",
                                      errors="replace").read())
    counts = idl.parse_param_counts(text)

    stubs = []
    for iface, method in sorted(_python_empty_params(module)):
        expected = counts.get((iface, method))
        if expected:
            stubs.append("%s::%s declares [] but the SDK gives it %d parameter(s)"
                         % (iface, method, expected))

    budget = STUB_BUDGET[module]
    assert len(stubs) <= budget, (
        "%d parameterless stubs in %s, budget is %d. New ones are not "
        "acceptable:\n  %s" % (len(stubs), module, budget, "\n  ".join(stubs)))
    assert len(stubs) == budget, (
        "%s has %d parameterless stubs but its budget is still %d. Lower it: a "
        "budget above the real count is a ratchet that has come loose, and it "
        "would silently absorb the next %d regressions."
        % (module, len(stubs), budget, budget - len(stubs)))


#: Frozen at the count measured when this test was written. Ratchet downwards
#: only - raising a number here means a regression was accepted.
STUB_BUDGET = {
    # Was 74 - ID3D11VideoContext 56, ID3D11VideoDevice 16, and two others.
    # Generating d3d11.py from the IDL took every one of them to a real
    # parameter list, so the whole of F-49 is gone from this module.
    "d3d11": 0,
    "d3d11_1": 0,
    "d3d11_2": 0,
    "d3d11_3": 0,
    "d3d11_4": 0,
    "d3d11sdklayers": 9,     # ID3D11InfoQueue 8, ID3D11TracingDevice 1
    "d3dcommon": 1,          # ID3DDestructionNotifier
    "dxgi": 0,
    "dxgi1_2": 0,
    "dxgi1_3": 0,
    "dxgi1_4": 0,
    "dxgi1_5": 0,
    "dxgi1_6": 0,
}


def test_capture_path_has_no_stubs(sdk_include):
    """The interfaces the capture work depends on must be fully declared.

    Separate from the budget test on purpose: the budget tolerates the historical
    debt in the video interfaces, this one does not tolerate any debt at all on
    the path that matters.
    """
    critical = {
        "d3d11": ["ID3D11Device", "ID3D11DeviceContext", "ID3D11Texture2D",
                  "ID3D11Resource"],
        "dxgi": ["IDXGIFactory1", "IDXGIAdapter", "IDXGIOutput", "IDXGIDevice",
                 "IDXGIResource", "IDXGIKeyedMutex", "IDXGISurface"],
        "dxgi1_2": ["IDXGIFactory2", "IDXGIOutput1", "IDXGIOutputDuplication",
                    "IDXGIResource1", "IDXGISwapChain1"],
    }
    problems = []
    for module, names in sorted(critical.items()):
        path = idl.idl_path(sdk_include, MODULE_IDL[module])
        if not path:
            continue
        text = idl.strip_comments(io.open(path, encoding="utf-8",
                                          errors="replace").read())
        counts = idl.parse_param_counts(text)
        empty = _python_empty_params(module)
        for iface, method in sorted(empty):
            if iface in names and counts.get((iface, method)):
                problems.append("%s::%s declares [] but takes %d parameter(s)"
                                % (iface, method, counts[(iface, method)]))

    assert not problems, (
        "a capture-path interface has a parameterless stub:\n  "
        + "\n  ".join(problems))
