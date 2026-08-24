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
}


def _deferred_methods(tree):
    """Interfaces given their vtable at module level: `IFoo._methods_ = [...]`.

    Generated modules assign vtables after every class exists, because an
    interface can name another declared later in the same file - IDXGIOutput
    takes an IDXGISurface*, and IDXGISurface comes after it. Assigning inline
    raises NameError; that is the general form of F-56.

    So "declares a vtable" has two valid shapes, and this test has to know both.
    """
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
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


def test_every_structure_declares_fields():
    """F-09: a Structure without _fields_ reports sizeof() == 0."""
    bad = []
    for path, tree in _modules():
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            bases = [b.attr if isinstance(b, ast.Attribute) else getattr(b, "id", "")
                     for b in node.bases]
            if not any(b in ("Structure", "Union") for b in bases):
                continue
            if "_fields_" not in _class_attrs(node):
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
