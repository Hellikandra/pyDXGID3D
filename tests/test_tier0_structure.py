# -*- coding: utf-8 -*-
"""Tier 0 - structural checks on the binding source.

These parse the modules with `ast` and never import them, so they run on any OS
with no comtypes and no GPU.

They exist because the defects that hurt most in this codebase are invisible to
reading, and invisible to any test that only counts interfaces:

    F-08  `_mehtods_` - one transposed character left ID3D11Debug with no vtable
    F-09  `_flags_`   - left D3D11_BOX at sizeof() == 0
    F-47  `c_bool`    - a one-byte type where the IDL says four

Each survived multiple commits and several readings. None survives this file.
"""
import ast
import glob
import io
import os
import re

import pytest

from conftest import REPO_ROOT

pytestmark = pytest.mark.tier0

BINDINGS = sorted(glob.glob(os.path.join(REPO_ROOT, "Direct3D", "PyIdl", "*.py")))

#: Hand-written support modules. They are not IDL translations, so the checks
#: that assert IDL fidelity do not apply to them - typemap.py in particular has
#: to name `ctypes.c_bool` in order to document why it is never the answer.
SUPPORT = {"typemap.py", "status.py", "functions.py", "__init__.py"}

#: The IDL-translated modules, which are what the fidelity checks are about.
IDL_MODULES = [p for p in BINDINGS if os.path.basename(p) not in SUPPORT]

#: Attribute names that are nearly right, and therefore dangerous: ctypes and
#: comtypes both ignore an unrecognised class attribute in complete silence.
LOOKALIKES = {
    "_mehtods_", "_methdos_", "_metohds_", "_method_",
    "_feilds_", "_fileds_", "_field_", "_flags_",
    "_iid", "_iid__", "iid_",
}

GUID_RE = re.compile(
    r"^\{[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\}$")


def _modules():
    for path in IDL_MODULES:
        yield path, ast.parse(io.open(path, encoding="utf-8").read())


def _class_attrs(node):
    return {t.id for st in node.body
            if isinstance(st, ast.Assign)
            for t in st.targets if isinstance(t, ast.Name)}


def test_bindings_exist():
    assert BINDINGS, "no binding modules found under Direct3D/PyIdl"


def test_all_modules_parse():
    for path, tree in _modules():
        assert tree is not None, path


def test_no_lookalike_attributes():
    """F-08, F-09: a misspelled special attribute is accepted in silence."""
    bad = []
    for path, tree in _modules():
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for attr in sorted(_class_attrs(node) & LOOKALIKES):
                    bad.append("%s:%d %s.%s" % (
                        os.path.basename(path), node.lineno, node.name, attr))
    assert not bad, "misspelled special attribute:\n  " + "\n  ".join(bad)


#: Interfaces the SDK really does declare with an empty body - they exist only
#: to give a resource a distinct type. Verified against d3d11.h, where each
#: appears as `MIDL_INTERFACE(...) IFoo : public IBar { public: };`.
#:
#: The set is asserted exactly, so a NEW interface without _methods_ fails and
#: has to be added here deliberately. That turns "no methods" from an oversight
#: into a decision someone made on purpose.
EMPTY_BY_DESIGN = {
    "ID3D11VertexShader", "ID3D11HullShader", "ID3D11DomainShader",
    "ID3D11GeometryShader", "ID3D11PixelShader", "ID3D11ComputeShader",
    "ID3D11InputLayout", "ID3D11Predicate",
    # d3d11_1.idl: `interface ID3DDeviceContextState : ID3D11DeviceChild {};`
    # A handle you pass to SwapDeviceContextState, nothing more.
    "ID3DDeviceContextState",
    # d3d12.idl declares five the same way. ID3D12Pageable is the interesting
    # one: it is the base of eleven other interfaces, so it must still be given
    # `_methods_ = []` for comtypes to build any of their vtables - see C-39.
    "ID3D12Pageable", "ID3D12RootSignature", "ID3D12QueryHeap",
    "ID3D12CommandSignature", "ID3D12StateObject",
}


def _deferred_methods(tree):
    """Interfaces given their vtable at module level: `IFoo._methods_ = [...]`.

    Generated modules assign vtables after every class exists, because an
    interface can name another declared later in the same file - IDXGIOutput
    takes an IDXGISurface*, and IDXGISurface comes after it. Assigning inline
    raises NameError; that is the general form of F-56.

    So "declares a vtable" has two valid shapes, and this test has to know both.

    An EMPTY list does not count. `IFoo._methods_ = []` registers no vtable
    slots, so as far as this test is concerned it is the same as declaring
    nothing - and it has to be written that way regardless, because comtypes
    refuses to build a vtable for a class whose base has no `_methods_` at all.
    Treating the empty list as a declaration would let a genuinely missing
    vtable hide behind one.
    """
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if isinstance(node.value, ast.List) and not node.value.elts:
            continue
        for target in node.targets:
            if (isinstance(target, ast.Attribute)
                    and target.attr == "_methods_"
                    and isinstance(target.value, ast.Name)):
                out.add(target.value.id)
    return out


def test_every_com_class_declares_methods():
    """F-08: a class carrying an _iid_ is a COM interface and needs a vtable,
    unless the SDK genuinely declares it empty."""
    found, where = set(), {}
    for path, tree in _modules():
        deferred = _deferred_methods(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            attrs = _class_attrs(node)
            if ("_iid_" in attrs and "_methods_" not in attrs
                    and node.name not in deferred):
                found.add(node.name)
                where[node.name] = "%s:%d" % (os.path.basename(path), node.lineno)

    unexpected = sorted(found - EMPTY_BY_DESIGN)
    assert not unexpected, (
        "COM class with _iid_ but no _methods_. comtypes registers zero vtable "
        "slots and every call raises AttributeError. If the SDK really declares "
        "it empty, add it to EMPTY_BY_DESIGN:\n  "
        + "\n  ".join("%s %s" % (where[n], n) for n in unexpected))

    vanished = sorted(EMPTY_BY_DESIGN - found)
    assert not vanished, (
        "these gained a _methods_ list - remove them from EMPTY_BY_DESIGN:\n  "
        + "\n  ".join(vanished))


def _deferred_attribute(tree, attribute):
    """Names given `attribute` at module level: `Foo.<attribute> = [...]`.

    An empty list does not count, for the same reason it does not in
    _deferred_methods: it declares nothing.
    """
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if isinstance(node.value, ast.List) and not node.value.elts:
            continue
        for target in node.targets:
            if (isinstance(target, ast.Attribute)
                    and target.attr == attribute
                    and isinstance(target.value, ast.Name)):
                out.add(target.value.id)
    return out


def test_every_structure_declares_fields():
    """F-09: a Structure without _fields_ reports sizeof() == 0.

    Two valid shapes, as with vtables. A structure that points at itself -
    D3D12_AUTO_BREADCRUMB_NODE ends with a `pNext` to its own type - cannot name
    its own class inside its body, so ctypes' documented form is to declare the
    class and assign `_fields_` afterwards. Reading class bodies alone would
    report those four as empty, which is the same false reading that made the
    vtable test vacuous in C-27.
    """
    bad = []
    for path, tree in _modules():
        deferred = _deferred_attribute(tree, "_fields_")
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            bases = [b.attr if isinstance(b, ast.Attribute) else getattr(b, "id", "")
                     for b in node.bases]
            if not any(b in ("Structure", "Union") for b in bases):
                continue
            if "_fields_" in _class_attrs(node) or node.name in deferred:
                continue
            bad.append("%s:%d %s" % (
                os.path.basename(path), node.lineno, node.name))
    assert not bad, (
        "Structure without _fields_, so sizeof() is 0:\n  " + "\n  ".join(bad))


def test_no_c_bool_anywhere():
    """F-47: Win32 BOOL is four bytes; ctypes.c_bool is one.

    No Windows type maps to c_bool, so any occurrence in the bindings is wrong.
    """
    bad = []
    for path in IDL_MODULES:
        for i, line in enumerate(io.open(path, encoding="utf-8"), 1):
            if "c_bool" in line:
                bad.append("%s:%d %s" % (
                    os.path.basename(path), i, line.strip()))
    assert not bad, (
        "ctypes.c_bool is 1 byte, Win32 BOOL is 4. Use wintypes.BOOL:\n  "
        + "\n  ".join(bad))


def test_iids_are_wellformed_and_unique():
    """A duplicated IID means two interfaces resolve to the same vtable."""
    seen, dupes, malformed = {}, [], []
    for path, tree in _modules():
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            for st in node.body:
                if not isinstance(st, ast.Assign):
                    continue
                if "_iid_" not in [t.id for t in st.targets
                                   if isinstance(t, ast.Name)]:
                    continue
                try:
                    value = st.value.args[0].value
                except (AttributeError, IndexError):
                    malformed.append("%s %s: not a GUID literal" % (
                        os.path.basename(path), node.name))
                    continue
                if not GUID_RE.match(value):
                    malformed.append("%s %s: %r" % (
                        os.path.basename(path), node.name, value))
                key = value.lower()
                if key in seen and seen[key] != node.name:
                    dupes.append("%s and %s share %s" % (
                        seen[key], node.name, value))
                seen[key] = node.name
    assert not malformed, "malformed IID:\n  " + "\n  ".join(malformed)
    assert not dupes, "duplicate IID:\n  " + "\n  ".join(dupes)


def test_no_bare_except():
    """A bare `except:` swallows KeyboardInterrupt and hides COMError detail."""
    bad = []
    for path, tree in _modules():
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                bad.append("%s:%d" % (os.path.basename(path), node.lineno))
    assert not bad, "bare except:\n  " + "\n  ".join(bad)


#: Modules a bare tier 0 runner does not have. `conftest.py` is exempt: it
#: imports comtypes inside a try/except precisely so it can define the skip
#: markers, which is the mechanism that makes every other exemption unnecessary.
UNAVAILABLE_AT_TIER_0 = ("comtypes", "Direct3D")


def _module_level_imports(tree):
    """Names imported at module scope. Imports inside functions do not count."""
    found = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            found.add(node.module.split(".")[0])
    return found


def test_no_test_module_imports_the_bindings_at_module_scope():
    """Tier 0 runs on Linux with pytest and nothing else.

    pytest imports every test file during collection regardless of `-m`, so a
    single module-level `import comtypes` fails the entire tier 0 job before one
    skip marker is consulted - and it passes locally, where comtypes is always
    installed. That is exactly how it got through: the marker
    `pytestmark = [pytest.mark.tier2, needs_comtypes]` skips the TESTS, not the
    IMPORT.

    Keep those imports inside the functions that need them.
    """
    offenders = []
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, "tests", "test_*.py"))):
        with io.open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read())
        for name in sorted(_module_level_imports(tree) & set(UNAVAILABLE_AT_TIER_0)):
            offenders.append("%s imports %s at module scope"
                             % (os.path.basename(path), name))

    assert not offenders, (
        "these would break collection on the tier 0 runner, which has neither "
        "comtypes nor a Windows DLL to load:\n  " + "\n  ".join(offenders)
        + "\n\nMove the import inside the test function. Run "
          "`python tools/tier0_sandbox.py -m tier0 -q` to check locally.")
