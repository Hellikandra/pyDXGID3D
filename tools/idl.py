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
import io
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

        out[name] = {"base": base, "uuid": uuid, "methods": methods,
                     "signatures": parse_signatures(body)}
    return out


_TYPEDEF_NAME_RE = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*[,;]")

_UNION_RE = re.compile(
    r"typedef\s+union\s+([A-Za-z_][A-Za-z0-9_]*)\s*\n?\s*\{", re.M)
_NAMED_STRUCT_RE = re.compile(r"\bstruct\b[^{]*\{")


def parse_unions(text):
    """Top-level `typedef union` declarations.

    Rare - one in d3d11.idl and one in d3d12.idl across the whole target set -
    but D3D11_AUTHENTICATED_PROTECTION_FLAGS is referenced by several structures,
    so missing it makes the generated module fail to import rather than merely
    lose a type.

    It is also the most nested construct in the set: a union containing a NAMED
    struct of bitfields alongside a plain UINT, which is the classic
    flags-or-value overlay.

        {name: {'members': [(type, fname, bounds, bits), ...],
                'nested':  [(fieldname, [(type, fname, bounds, bits), ...])]}}
    """
    text = strip_comments(text)
    out = {}
    for match in _UNION_RE.finditer(text):
        tag = match.group(1)
        open_index = text.index("{", match.start())
        body, close_index = _balanced_body(text, open_index)

        trailing = _TYPEDEF_NAME_RE.match(text, close_index + 1)
        name = trailing.group(1) if trailing else tag

        out[name] = dict(split_union_body(body), tag=tag)
    return out


def split_union_body(body):
    """A union body split into plain members and named nested structures.

        {'members': [(type, name, bounds, bits), ...],
         'nested':  [(field_name, [(type, name, bounds, bits), ...]), ...]}

    Used for both shapes this SDK produces: the top-level
    D3D11_AUTHENTICATED_PROTECTION_FLAGS, which overlays one named bitfield
    struct on a UINT, and the anonymous union inside
    D3D12_INDIRECT_ARGUMENT_DESC, which holds six named structs and no plain
    members at all.
    """
    nested, remainder = [], body
    while True:
        inner = _NAMED_STRUCT_RE.search(remainder)
        if not inner:
            break
        brace = remainder.index("{", inner.start())
        fields_text, end = _balanced_body(remainder, brace)
        after = remainder[end + 1:]
        label = _TYPEDEF_NAME_RE.match(after)
        nested.append((label.group(1) if label else "s%d" % len(nested),
                       parse_struct_fields(fields_text)))
        # Cut the nested definition out and keep scanning what surrounds it, so
        # a plain member declared after the struct is not lost. The parentheses
        # matter: without them the conditional swallows the concatenation and
        # everything before an unlabelled struct is discarded.
        remainder = (remainder[:inner.start()] + after[label.end():]) \
            if label else (remainder[:inner.start()] + after)

    return {"members": parse_struct_fields(remainder), "nested": nested}


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

        # A NESTED aggregate is what makes a structure opaque - one whose field
        # offsets cannot be read off the text. The mere word `struct` does not:
        # `const struct D3D12_AUTO_BREADCRUMB_NODE *pNext` is an elaborated type
        # specifier naming a type declared elsewhere, and treating it as a
        # nested definition emitted four D3D12 structures with no fields at all.
        # A nested aggregate is followed by a brace; a reference is not.
        nested = re.search(r"\b(?:union|struct)\b[^;{}]*\{", body)
        opaque = bool(nested)

        segments = None
        if opaque and re.search(r"\bunion\b[^;{}]*\{", body):
            # Anonymous unions inside a structure. The SDK writes
            #     union { D3D11_BUFFER_RTV Buffer; ... } ;
            # and ctypes expresses it as a nested class plus _anonymous_ - the
            # shape the hand-written D3D11_RENDER_TARGET_VIEW_DESC already uses.
            #
            # The body is cut into ordered segments so field ORDER survives,
            # which matters because every offset after a union depends on where
            # it sits. There can be more than one: D3D11_BUFFER_SRV carries two
            # back to back, and handling only the first silently flattened the
            # second into plain fields - eight bytes of structure emitted as
            # twelve.
            segments, rest = [], body
            while True:
                found = re.search(r"\bunion\b[^;{}]*\{", rest)
                if not found:
                    break
                open_u = rest.index("{", found.start())
                inner, close_u = _balanced_body(rest, open_u)
                segments.append(("fields", parse_struct_fields(rest[:found.start()])))
                # The union body may itself hold NAMED structures:
                # D3D12_INDIRECT_ARGUMENT_DESC overlays six of them. Parsed with
                # the same helper as a top-level union, so both shapes produce
                # one thing for the emitter to render.
                segments.append(("union", split_union_body(inner)))
                rest = rest[close_u + 1:]
            segments.append(("fields", parse_struct_fields(rest)))
            opaque = False

        fields = []
        if not opaque and segments is None:
            for found in _FIELD_RE.finditer(body):
                ftype, fname, bound = found.groups()
                fields.append((ftype.replace(" ", ""), fname, bound))
        out[name] = {"tag": tag, "fields": fields, "opaque": opaque,
                     "segments": segments,
                     "parsed_fields": ([] if (opaque or segments)
                                       else parse_struct_fields(body))}
    return out


def _split_params(text):
    """Top-level comma split, so size_is(a, b) does not split a parameter."""
    parts, depth, current = [], 0, []
    for char in text:
        if char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        if char == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    if "".join(current).strip():
        parts.append("".join(current))
    return parts


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
            # Must be bracket-aware, not just paren-aware: every parameter
            # carries a MIDL attribute block like [in, annotation("_In_")], and
            # the comma inside it is not a parameter separator. Counting on
            # paren depth alone inflated SetPrivateData from 3 to 5.
            out[key] = len(_split_params(params))
    return out


def load(sdk, name):
    """Parse one targeted IDL. Returns (interfaces, structs) or (None, None)."""
    path = idl_path(sdk, name)
    if not path:
        return None, None
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    return parse_interfaces(text), parse_structs(text)


# ---------------------------------------------------- method signatures ----
_SIG_RE = re.compile(
    r"(?:^|\n)[ \t]*(?:\[[^\]]*\][ \t]*)?"
    r"([A-Za-z_][A-Za-z0-9_]*(?:[ \t]*\*+)?)[ \t]+"     # return type
    r"([A-Za-z_][A-Za-z0-9_]*)[ \t]*"                     # method name
    r"\(([^;]*?)\)[ \t]*;", re.S)


_PARAM_RE = re.compile(
    r"^\s*(?:\[[^\]]*\]\s*)*"                     # MIDL / SAL annotations
    r"([A-Za-z_][A-Za-z0-9_]*(?:\s*\*)*)\s*"      # type plus any pointer depth
    r"([A-Za-z_][A-Za-z0-9_]*)?"                  # name, sometimes absent
    # An array bound. CAPTURED, because in C a parameter declared as an array
    # decays to a pointer and the binding has to say so: `const FLOAT
    # ColorRGBA[4]` is a FLOAT*, not a FLOAT. Discarding it declared
    # ClearRenderTargetView as taking one float instead of four, which made the
    # method impossible to call at all - F-60, and ten parameters like it.
    r"(\s*\[\s*[0-9A-Za-z_]*\s*\])?\s*$", re.S)


def parse_signatures(body):
    """{method: (return_type, [(param_type, param_name), ...])} for one body."""
    out = {}
    for match in _SIG_RE.finditer(body):
        restype, method, params = match.groups()
        if method in _SKIP_METHOD_NAMES or method.startswith("_"):
            continue
        if method in out:
            continue
        restype = re.sub(r"\s+", "", restype)

        collected = []
        cleaned = params.strip()
        if cleaned and cleaned != "void":
            for chunk in _split_params(cleaned):
                chunk = chunk.replace("\n", " ")
                # `const` can sit anywhere in a pointer declarator - the SDK
                # writes `IDXGIResource *const *ppResources` for an array of
                # interface pointers. It carries no ctypes meaning, and leaving
                # it in made 54 signatures parse one parameter short.
                chunk = re.sub(r"\bconst\b", " ", chunk)
                found = _PARAM_RE.match(chunk)
                if not found:
                    continue
                ptype = re.sub(r"\s+", "", found.group(1))
                if found.group(3):
                    # `FLOAT ColorRGBA[4]` is a FLOAT* at the ABI. F-60.
                    ptype += "*"
                pname = found.group(2) or "arg%d" % (len(collected) + 1)
                collected.append((ptype, pname))
        out[method] = (restype, collected)
    return out


# ---------------------------------------------------------------- enums ----
_ENUM_RE = re.compile(
    r"typedef\s*\n?\s*enum\s+([A-Za-z_][A-Za-z0-9_]*)\s*\n?\s*\{", re.M)
_ENUM_MEMBER_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:=\s*([^,\n]+?))?\s*(?:,|$)", re.M)


def parse_enums(text):
    """{name: {'tag', 'members': [(name, value_expression_or_None), ...]}}.

    `name` is the typedef, matching parse_structs. Values are kept as the source
    expression rather than evaluated: the SDK writes things like ( 1 << 4 ) and
    0xffffffff, and an emitter can pass those straight through to Python, which
    reads them identically.
    """
    text = strip_comments(text)
    out = {}
    for match in _ENUM_RE.finditer(text):
        tag = match.group(1)
        open_index = text.index("{", match.start())
        body, close_index = _balanced_body(text, open_index)

        trailing = _TYPEDEF_NAME_RE.match(text, close_index + 1)
        name = trailing.group(1) if trailing else tag

        members, seen = [], set()
        # Split on top-level commas rather than matching line by line: a value
        # can span lines. D3D11_COLOR_WRITE_ENABLE_ALL is written as
        #     ( D3D11_COLOR_WRITE_ENABLE_RED | ...GREEN |
        #       ...BLUE | ...ALPHA )
        # and a line-anchored pattern truncates it mid-expression, which emits
        # syntactically invalid Python.
        for chunk in _split_params(body):
            chunk = " ".join(chunk.split())
            if not chunk:
                continue
            name_part, _, value_part = chunk.partition("=")
            member = name_part.strip()
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", member) or member in seen:
                continue
            seen.add(member)
            members.append((member, value_part.strip() or None))
        out[name] = {"tag": tag, "members": members}
    return out


# --------------------------------------------------- callback typedefs ----
#: `typedef void (__stdcall *D3D12MessageFunc) (A a, B b, void* c);`
#:
#: Two exist in the whole target set - D3D12MessageFunc in d3d12sdklayers.idl
#: and PFN_DESTRUCTION_CALLBACK in d3dcommon.idl - which is why the
#: hand-written d3dcommon.py could get away with commenting its parameters out.
#: d3d12sdklayers cannot: ID3D12InfoQueue1::RegisterMessageCallback takes one,
#: and without the type the module does not import.
_CALLBACK_TYPEDEF_RE = re.compile(
    r"typedef\s+([A-Za-z_][A-Za-z0-9_]*(?:\s*\*+)?)\s*"
    r"\(\s*__stdcall\s*\*\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*"
    r"\(([^;]*?)\)\s*;", re.S)


def parse_callbacks(text):
    """[(name, return_type, [(type, param_name), ...]), ...]

    Returned separately from parse_typedefs because the emitted shape is a
    ctypes.WINFUNCTYPE rather than an alias, and because these must be emitted
    after the enumerations they name.
    """
    text = strip_comments(text)
    out = []
    for match in _CALLBACK_TYPEDEF_RE.finditer(text):
        restype, name, params = match.groups()
        collected = []
        cleaned = params.strip()
        if cleaned and cleaned != "void":
            for chunk in _split_params(cleaned):
                chunk = re.sub(r"\bconst\b", " ", chunk.replace("\n", " "))
                found = _PARAM_RE.match(chunk)
                if not found:
                    continue
                ptype = re.sub(r"\s+", "", found.group(1))
                if found.group(3):
                    ptype += "*"                      # array decays, F-60
                collected.append((ptype,
                                  found.group(2) or "arg%d" % (len(collected) + 1)))
        out.append((name, re.sub(r"\s+", "", restype), collected))
    return out


# ------------------------------------------------------ function macros ----
#: The payload of each cpp_quote, in file order.
_CPP_QUOTE_RE = re.compile(r'cpp_quote\(\s*"(.*?)"\s*\)', re.S)

#: `#define NAME(a, b) body` - the parenthesis binds directly to the name, which
#: is what tells a function-like macro from an object-like one.
_FUNCTION_MACRO_RE = re.compile(
    r"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\(([^)]*)\)\s+(.+)$")

#: One or more backslashes at the end of a cpp_quote payload. The IDL writes the
#: C line-continuation inside a C string, so it arrives here as a literal
#: backslash (sometimes two) that has to come off before the fragments are
#: joined.
_TRAILING_BACKSLASH_RE = re.compile(r"\\+\s*$")


def parse_macros(text):
    """[(name, [parameters], body), ...] for function-like cpp_quote macros.

    d3d12.idl declares fourteen and d3d11.idl ten. They are not decoration:
    D3D12_ENCODE_BASIC_FILTER is how a D3D12_SAMPLER_DESC gets built and
    D3D12_ENCODE_SHADER_4_COMPONENT_MAPPING is required for every SRV
    descriptor, so without them a caller is left hand-translating bit
    arithmetic out of a header they cannot read from Python.

    They span cpp_quote lines, continued with a backslash:

        cpp_quote( "#define D3D12_ENCODE_SHADER_4_COMPONENT_MAPPING(a,b,c,d) ((((a)&M)| \\\\")
        cpp_quote( "                                     (((b)&M)<<S)| \\\\")

    so the payloads are joined before anything is matched. parse_defines skips
    these because its regex requires whitespace after the name.
    """
    joined, pending = [], ""
    for payload in _CPP_QUOTE_RE.findall(text):
        if _TRAILING_BACKSLASH_RE.search(payload):
            pending += _TRAILING_BACKSLASH_RE.sub(" ", payload)
            continue
        joined.append(pending + payload)
        pending = ""
    if pending:
        joined.append(pending)

    out, seen = [], set()
    for line in joined:
        found = _FUNCTION_MACRO_RE.match(line)
        if not found:
            continue
        name, params, body = found.groups()
        if name in seen:
            continue
        seen.add(name)
        parameters = [p.strip() for p in params.split(",") if p.strip()]
        out.append((name, parameters, re.sub(r"\s+", " ", body).strip()))
    return out


# -------------------------------------------------------------- defines ----
_DEFINE_RE = re.compile(
    r'cpp_quote\(\s*"\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.+?)\s*"\s*\)')


#: `const UINT D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT = 8;` - MIDL's own way of
#: declaring a constant, as opposed to the preprocessor's. d3d11.idl writes 340
#: of them and d3d12.idl 392, and they are used as array bounds, so they are not
#: optional: without them the generated module fails to import.
_CONST_RE = re.compile(
    r"^[ \t]*const[ \t]+[A-Za-z_][A-Za-z0-9_]*[ \t]+"
    r"([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*"
    r"([^;]+);",
    re.M)


_BARE_DEFINE_RE = re.compile(
    "^[ 	]*#define[ 	]+"
    "([A-Za-z_][A-Za-z0-9_]*)[ 	]+"
    "([^\\n/]+?)[ 	]*$",
    re.M)


def parse_defines(text):
    """[(name, value_expression), ...] from cpp_quote blocks, in file order.

    Only `#define NAME value` is collected. d3d11.idl carries 1,599 cpp_quote
    lines of which just 59 are defines - the rest are the C++ CD3D11_* helper
    classes, which have no Python meaning and are deliberately skipped.
    """
    out, seen = [], set()

    def take(name, value):
        if name in seen or "(" in name:
            return
        seen.add(name)
        out.append((name, value.strip()))

    for match in _DEFINE_RE.finditer(text):
        take(match.group(1), match.group(2))

    # Not every constant hides in a cpp_quote. d3d11.idl writes some as a bare
    # preprocessor line - `#define D3D11_OMAC_SIZE 16` - and D3D11_OMAC uses it
    # as an array bound, so missing them makes the generated module fail to
    # import rather than merely lose a constant.
    for match in _BARE_DEFINE_RE.finditer(text):
        take(match.group(1), match.group(2))

    # MIDL `const` declarations. Emitted after the defines but collected in file
    # order among themselves, because they refer to each other:
    # `const UINT _FACD3D11DEBUG = _FACD3D11 + 1;`.
    for match in _CONST_RE.finditer(text):
        take(match.group(1), match.group(2))
    return out


# ------------------------------------------------------- richer structs ----
_FIELD_FULL_RE = re.compile(
    r"^[ \t]*(?:\[[^\]]*\][ \t]*)?"          # MIDL / SAL annotation
    r"(?:const[ \t]+)?"
    # An elaborated type specifier. d3d12.idl writes the self-reference in
    # D3D12_AUTO_BREADCRUMB_NODE as `const struct D3D12_AUTO_BREADCRUMB_NODE
    # *pNext`, and without this the keyword is read as the type and the field
    # is dropped.
    r"(?:(?:struct|union|enum)[ \t]+)?"
    r"([A-Za-z_][A-Za-z0-9_]*)"                        # type
    # The asterisks bind to the NAME in this SDK - `void *pData`,
    # `ID3D11VideoProcessorInputView **ppPastSurfaces` - so requiring
    # whitespace after them dropped every pointer field on the floor. Silently:
    # D3D11_MAPPED_SUBRESOURCE came out 8 bytes instead of 16, which is the
    # structure Desktop Duplication reads every frame through.
    #
    # They need not be contiguous, and `const` can sit between them:
    # `const D3D12_STATE_SUBOBJECT* const* ppSubobjects` is a pointer to a
    # const pointer. Only the asterisks carry ctypes meaning, so the whole
    # declarator is captured here and the count taken afterwards. Demanding
    # `\*+` lost this field and D3D12_GENERIC_PROGRAM_DESC came out 32 bytes
    # against the SDK's 40.
    r"(?:((?:[ \t]*\*[ \t]*(?:const\b[ \t]*)?)+)|[ \t]+)"
    r"([A-Za-z_][A-Za-z0-9_]*)"                        # name
    r"((?:[ \t]*\[[ \t]*[0-9A-Za-z_]+[ \t]*\])*)"      # [N], or [N][M]
    r"(?:[ \t]*:[ \t]*([0-9]+))?"                      # : bits
    r"[ \t]*;", re.M)


def parse_struct_fields(body):
    """[(type, name, array_len, bit_width), ...] for one struct body.

    array_len and bit_width are None when absent. Pointer depth is carried in
    the type string as trailing asterisks, which the emitter unwraps.
    """
    fields = []
    for found in _FIELD_FULL_RE.finditer(body):
        ftype, stars, fname, bound, bits = found.groups()
        # The declarator arrives whole - "* const * " for a pointer to a const
        # pointer. Only the asterisks mean anything to ctypes.
        ftype = ftype + re.sub(r"[^*]", "", stars or "")
        # A field can carry more than one dimension: DXGI_DISPLAY_COLOR_SPACE
        # declares FLOAT PrimaryCoordinates[8][2]. Bounds travel as a list so
        # the emitter can compose them in the right order.
        bounds = re.findall(r"\[\s*([0-9A-Za-z_]+)\s*\]", bound or "")
        fields.append((re.sub(r"\s+", "", ftype), fname,
                       bounds or None, int(bits) if bits else None))
    return fields


# ------------------------------------------------------ scalar typedefs ----
_TYPEDEF_SCALAR_RE = re.compile(
    r"^[ 	]*typedef[ 	]+(?!struct|enum|union|interface)"
    r"([A-Za-z_][A-Za-z0-9_]*(?:[ 	]*\*)*)[ 	]+"
    r"([A-Za-z_][A-Za-z0-9_]*)[ 	]*;", re.M)


def parse_typedefs(text):
    """[(alias, underlying_type), ...] for plain scalar typedefs.

    `typedef UINT DXGI_USAGE;` is neither a struct, an enum nor a define, so it
    fell through every other parser and DXGI_USAGE came out undefined. Small
    construct, and the generated dxgi.py would not import without it.
    """
    text = strip_comments(text)
    out, seen = [], set()
    for match in _TYPEDEF_SCALAR_RE.finditer(text):
        underlying, alias = match.group(1), match.group(2)
        if alias in seen:
            continue
        seen.add(alias)
        out.append((alias, re.sub(r"\s+", "", underlying)))
    return out


def module_constructs(sdk, name):
    """Everything an emitter needs for one IDL, in one call.

    Returns a dict with interfaces, structs, enums, defines and imports.
    """
    path = idl_path(sdk, name)
    if not path:
        return None
    raw = io.open(path, encoding="utf-8", errors="replace").read()
    stripped = strip_comments(raw)
    return {
        "idl": name,
        "interfaces": parse_interfaces(raw),
        "structs": parse_structs(raw),
        "unions": parse_unions(raw),
        "enums": parse_enums(raw),
        "defines": parse_defines(raw),
        "macros": parse_macros(raw),
        "callbacks": parse_callbacks(raw),
        "typedefs": parse_typedefs(raw),
        "imports": [i for i in re.findall(r'^\s*import\s+"([^"]+)"',
                                          stripped, re.M)
                    if i not in ("oaidl.idl", "ocidl.idl", "unknwn.idl",
                                 "wtypes.idl", "objidl.idl")],
    }


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
