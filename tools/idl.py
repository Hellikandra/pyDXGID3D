# -*- coding: utf-8 -*-
"""A small parser for the Windows SDK .idl files.

The SDK ships the interface definitions this project is translated from. Reading
them directly means the test suite can assert against the source of truth rather
than against a transcription of it.

Deliberately not a general MIDL parser. It handles the constructs that appear in
the twenty-one IDLs this project targets, and nothing more. Where it cannot
parse something it says so rather than guessing - `parse_structs` marks any
structure containing an anonymous union as `opaque`, because the field offsets
inside one cannot be derived from the text alone.

Used by:
    tests/test_tier1_vtable.py    method order, per interface
    tools/layout_probe.py         structure and field enumeration
    (P3) the binding generator

Usage:
    python tools/idl.py                 summary of every targeted IDL
    python tools/idl.py dxgi1_2.idl     detail for one
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))

#: The IDLs this project targets, with the SDK sub-directory each lives in.
TARGETS = [
    ("shared", "dxgicommon.idl"), ("shared", "dxgiformat.idl"),
    ("shared", "dxgitype.idl"), ("shared", "dxgi.idl"),
    ("shared", "dxgi1_2.idl"), ("shared", "dxgi1_3.idl"),
    ("shared", "dxgi1_4.idl"), ("shared", "dxgi1_5.idl"),
    ("shared", "dxgi1_6.idl"),
    ("um", "d3dcommon.idl"), ("um", "d3d11.idl"),
    ("um", "d3d11sdklayers.idl"), ("um", "d3d11_1.idl"),
    ("um", "d3d11_2.idl"), ("um", "d3d11_3.idl"), ("um", "d3d11_4.idl"),
    ("um", "d3d12.idl"), ("um", "d3d12sdklayers.idl"),
    ("um", "d3d12video.idl"), ("um", "d3d12compatibility.idl"),
    ("um", "d3d11on12.idl"),
]

#: Headers matching these have the binding module of the same stem.
MODULE_FOR_IDL = {
    "dxgi.idl": "dxgi", "dxgi1_2.idl": "dxgi1_2", "dxgicommon.idl": "dxgicommon",
    "dxgiformat.idl": "dxgiformat", "dxgitype.idl": "dxgitype",
    "d3d11.idl": "d3d11", "d3d11sdklayers.idl": "d3d11sdklayers",
    "d3dcommon.idl": "d3dcommon",
}

_IFACE_RE = re.compile(
    r"^\s*interface\s+(I[A-Za-z0-9_]+)\s*(?::\s*(I[A-Za-z0-9_]+))?\s*$", re.M)
_UUID_RE = re.compile(r"uuid\(\s*([0-9a-fA-F\-]{36})\s*\)")
_METHOD_RE = re.compile(
    r"^\s*(?:\[[^\]]*\]\s*)?"
    r"(?:const\s+)?[A-Za-z_][A-Za-z0-9_ \t\*]*?\s"
    r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.M)
_STRUCT_RE = re.compile(
    r"typedef\s+(?:\[[^\]]*\]\s*)?struct\s+([A-Za-z_][A-Za-z0-9_]*)\s*\n?\s*\{", re.M)
_FIELD_RE = re.compile(
    r"^\s*(?:\[[^\]]*\]\s*)?"                       # MIDL / SAL annotation
    r"(?:const\s+)?"
    r"([A-Za-z_][A-Za-z0-9_]*(?:\s*\*+)?)\s+"        # type
    r"([A-Za-z_][A-Za-z0-9_]*)"                      # name
    r"(?:\s*\[\s*([0-9A-Za-z_]+)\s*\])?\s*;", re.M)  # optional array bound

_SKIP_METHOD_NAMES = {
    "cpp_quote", "import", "typedef", "if", "for", "while", "switch",
    "return", "sizeof", "DEFINE_GUID", "midl_pragma", "struct", "union",
}


def find_sdk():
    """Newest Windows SDK Include directory, or None.

    WINSDK_INCLUDE overrides, for a machine with several kits installed.
    """
    env = os.environ.get("WINSDK_INCLUDE")
    if env and os.path.isdir(env):
        return env
    roots = [
        os.path.join("C:" + os.sep, "Program Files (x86)", "Windows Kits", "10", "Include"),
        os.path.join("C:" + os.sep, "Program Files", "Windows Kits", "10", "Include"),
    ]
    best = None
    for root in roots:
        if not os.path.isdir(root):
            continue
        for version in sorted(os.listdir(root)):
            candidate = os.path.join(root, version)
            if os.path.isfile(os.path.join(candidate, "shared", "dxgi.idl")):
                best = candidate
    return best


def idl_path(sdk, name):
    """Absolute path to a targeted IDL, or None if this kit does not ship it."""
    for sub, target in TARGETS:
        if target == name:
            path = os.path.join(sdk, sub, name)
            return path if os.path.isfile(path) else None
    return None


def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def _balanced_body(text, open_index):
    """Return the text between the brace at open_index and its partner."""
    depth, i = 0, open_index
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_index + 1:i], i
        i += 1
    return "", open_index


def parse_interfaces(text):
    """{name: {'base', 'uuid', 'methods': [name, ...]}} in declaration order.

    Method order is the point of this function: comtypes builds vtables by
    position, so a method missing from the middle shifts every later slot.
    """
    text = strip_comments(text)
    out = {}
    for match in _IFACE_RE.finditer(text):
        name, base = match.group(1), match.group(2)
        if not base:
            continue                       # forward declaration
        open_index = text.find("{", match.end())
        if open_index == -1:
            continue
        body, _end = _balanced_body(text, open_index)

        head = text[max(0, match.start() - 500):match.start()]
        uuid = None
        for found in _UUID_RE.finditer(head):
            uuid = found.group(1)

        methods, seen = [], set()
        for found in _METHOD_RE.finditer(body):
            method = found.group(1)
            if method in _SKIP_METHOD_NAMES or method.startswith("_"):
                continue
            if method in seen:
                continue                   # multi-line parameter lists re-match
            seen.add(method)
            methods.append(method)

        out[name] = {"base": base, "uuid": uuid, "methods": methods}
    return out


_TYPEDEF_NAME_RE = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*[,;]")


def parse_structs(text):
    """{name: {'tag', 'fields': [(type, name, array_len), ...], 'opaque': bool}}.

    `name` is the **typedef** name, not the struct tag. The two differ more often
    than one would hope:

        typedef struct _D3D11_AES_CTR_IV { ... } D3D11_AES_CTR_IV;
        typedef struct D3D11_AUTHENTICATED_QUERY_ACESSIBILITY_OUTPUT { ... }
                       D3D11_AUTHENTICATED_QUERY_ACCESSIBILITY_OUTPUT;

    Note the second: the tag is missing a C and the typedef is not. Only the
    typedef name is usable from C, and it is the name the bindings should carry.
    Keying on the tag produced a probe that would not compile, which is how this
    was found.

    `opaque` marks a structure containing an anonymous union or nested struct.
    Its total size is still worth checking, but per-field offsets cannot be
    derived from the text, so callers should skip offset assertions for it.
    """
    text = strip_comments(text)
    out = {}
    for match in _STRUCT_RE.finditer(text):
        tag = match.group(1)
        open_index = text.index("{", match.start())
        body, close_index = _balanced_body(text, open_index)

        trailing = _TYPEDEF_NAME_RE.match(text, close_index + 1)
        name = trailing.group(1) if trailing else tag

        opaque = bool(re.search(r"\bunion\b|\bstruct\b", body))
        fields = []
        if not opaque:
            for found in _FIELD_RE.finditer(body):
                ftype, fname, bound = found.groups()
                fields.append((ftype.replace(" ", ""), fname, bound))
        out[name] = {"tag": tag, "fields": fields, "opaque": opaque}
    return out


_METHOD_SIG_RE = re.compile(
    r"(?:^|\n)\s*(?:\[[^\]]*\]\s*)?"
    r"[A-Za-z_][A-Za-z0-9_ \t\*]*?\s"
    r"([A-Za-z_][A-Za-z0-9_]*)\s*\(([^;]*?)\)\s*;", re.S)


def parse_param_counts(text):
    """{(interface, method): parameter_count}, scoped per interface.

    Scoping matters: `GetType` exists on ID3D11Resource taking one parameter and
    on ID3D11DeviceContext taking none. Keying on the method name alone conflates
    them and reports the second as a stub when it is correct.
    """
    text = strip_comments(text)
    out = {}
    for match in re.finditer(
            r"^\s*interface\s+(I[A-Za-z0-9_]+)\s*:\s*I[A-Za-z0-9_]+\s*$",
            text, re.M):
        iface = match.group(1)
        open_index = text.find("{", match.end())
        if open_index == -1:
            continue
        body, _end = _balanced_body(text, open_index)
        for found in _METHOD_SIG_RE.finditer(body):
            method, params = found.group(1), found.group(2).strip()
            if method in _SKIP_METHOD_NAMES or method.startswith("_"):
                continue
            key = (iface, method)
            if key in out:
                continue
            if params in ("", "void"):
                out[key] = 0
                continue
            depth, count = 0, 1
            for char in params:
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                elif char == "," and depth == 0:
                    count += 1
            out[key] = count
    return out


def load(sdk, name):
    """Parse one targeted IDL. Returns (interfaces, structs) or (None, None)."""
    path = idl_path(sdk, name)
    if not path:
        return None, None
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    return parse_interfaces(text), parse_structs(text)


def main():
    sdk = find_sdk()
    if not sdk:
        print("No Windows SDK Include directory found.")
        return 1
    print("SDK:", sdk)

    if len(sys.argv) > 1:
        name = sys.argv[1]
        interfaces, structs = load(sdk, name)
        if interfaces is None:
            print("not a targeted IDL, or not in this kit:", name)
            return 1
        print("\n%s - %d interfaces, %d structures\n" % (
            name, len(interfaces), len(structs)))
        for iface in sorted(interfaces):
            spec = interfaces[iface]
            print("  %-40s : %-24s %2d methods" % (
                iface, spec["base"], len(spec["methods"])))
            for slot, method in enumerate(spec["methods"]):
                print("       %2d  %s" % (slot, method))
        return 0

    total_i = total_m = total_s = 0
    for _sub, name in TARGETS:
        interfaces, structs = load(sdk, name)
        if interfaces is None:
            print("  %-24s not in this kit" % name)
            continue
        methods = sum(len(v["methods"]) for v in interfaces.values())
        opaque = sum(1 for v in structs.values() if v["opaque"])
        print("  %-24s %3d interfaces %5d methods %4d structs (%d opaque)" % (
            name, len(interfaces), methods, len(structs), opaque))
        total_i += len(interfaces)
        total_m += methods
        total_s += len(structs)
    print("  %-24s %3d            %5d         %4d" % (
        "TOTAL", total_i, total_m, total_s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
