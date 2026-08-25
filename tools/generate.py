# -*- coding: utf-8 -*-
"""Generate a binding module from a Windows SDK .idl file.

Why generate
------------
616 methods, 484 structures and 295 enumerations remain unported. Hand
translation has so far produced 427 correct methods and eight defects that were
invisible to reading - a misspelled dunder, a structure with no fields, a method
missing from the middle of a vtable, a one-byte type where the SDK says four.
Every one was found by a machine, none by a person.

This turns the remaining work into a diff review.

What it emits
-------------
Interfaces, structures, enumerations and the constants hidden in cpp_quote, in
the house style of the hand-written modules - because those are what people
already read.

Type decisions come from Direct3D/PyIdl/typemap.py and nowhere else. That module
exists precisely because a scattered type decision is what produced F-47.

Ordering
--------
Structures and interfaces are emitted in dependency order, worked out by a
topological sort over what references what. Where a genuine cycle exists the
class is emitted with its _iid_ first and its _methods_ assigned afterwards,
once every class object exists. The hand-written d3d11.py relies on the author
having ordered declarations by hand, which works but does not generalise - and
D3D11_VIDEO_PROCESSOR_STREAM is what happens when it fails (F-56: six fields
commented out with "Interface dependance defined after").

Usage
-----
    python tools/generate.py dxgi1_5.idl                  print to stdout
    python tools/generate.py dxgi1_5.idl -o out.py        write a file
    python tools/generate.py --all --outdir generated/    the whole target set
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

import idl  # noqa: E402

try:
    from Direct3D.PyIdl import typemap
    SOURCE = typemap.SOURCE
    VOID_RETURN = typemap.VOID_RETURN
except ImportError:                      # generation must work without comtypes
    SOURCE = None
    VOID_RETURN = ("void", "VOID")

#: Fallback used when typemap cannot be imported (no comtypes installed).
#: Kept deliberately identical to typemap.SOURCE - the test suite asserts that.
_FALLBACK_SOURCE = {
    "BOOL": "wintypes.BOOL", "BOOLEAN": "ctypes.c_ubyte", "BYTE": "ctypes.c_ubyte",
    "CHAR": "ctypes.c_char", "WCHAR": "ctypes.c_wchar",
    "INT8": "ctypes.c_int8", "UINT8": "ctypes.c_uint8",
    "SHORT": "ctypes.c_int16", "USHORT": "ctypes.c_uint16",
    "INT16": "ctypes.c_int16", "UINT16": "ctypes.c_uint16", "WORD": "ctypes.c_uint16",
    "INT": "ctypes.c_int32", "INT32": "ctypes.c_int32", "LONG": "ctypes.c_int32",
    "UINT": "ctypes.c_uint32", "UINT32": "ctypes.c_uint32",
    "ULONG": "ctypes.c_uint32", "DWORD": "ctypes.c_uint32",
    "INT64": "ctypes.c_int64", "LONGLONG": "ctypes.c_int64",
    "UINT64": "ctypes.c_uint64", "ULONGLONG": "ctypes.c_uint64",
    "DWORDLONG": "ctypes.c_uint64",
    "LARGE_INTEGER": "ctypes.c_int64", "ULARGE_INTEGER": "ctypes.c_uint64",
    "SIZE_T": "ctypes.c_size_t", "SSIZE_T": "ctypes.c_ssize_t",
    "FLOAT": "ctypes.c_float", "DOUBLE": "ctypes.c_double",
    "LPSTR": "ctypes.c_char_p", "LPCSTR": "ctypes.c_char_p",
    "LPWSTR": "ctypes.c_wchar_p", "LPCWSTR": "ctypes.c_wchar_p",
    "HANDLE": "ctypes.c_void_p", "HWND": "ctypes.c_void_p", "HDC": "ctypes.c_void_p",
    "HMONITOR": "ctypes.c_void_p", "HMODULE": "ctypes.c_void_p",
    "HINSTANCE": "ctypes.c_void_p", "LPVOID": "ctypes.c_void_p",
    "void*": "ctypes.c_void_p", "void": "ctypes.c_void_p",
    "HRESULT": "comtypes.HRESULT", "GUID": "comtypes.GUID", "IID": "comtypes.GUID",
    "REFIID": "comtypes.GUID", "REFGUID": "comtypes.GUID", "CLSID": "comtypes.GUID",
    "RECT": "wintypes.RECT", "POINT": "wintypes.POINT", "SIZE": "wintypes.SIZE",
    "LUID": "LUID", "SECURITY_ATTRIBUTES": "SECURITY_ATTRIBUTES",
}

NEWLINE = chr(10)

HEADER = '''##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version {sdk}
##
##   Generated from {idl} by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py {idl}
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES
{helpers}
'''


class Emitter(object):
    """Turns one parsed IDL into a binding module."""

    #: Plain C keywords. The IDLs use these alongside the Windows typedefs -
    #: `float r;` in D3DCOLORVALUE, `int Level` in VideoProcessorSetStreamFilter -
    #: and typemap.py covers only the typedefs. Without these the emitter passed
    #: `float` through verbatim, producing Python's builtin, which ctypes rejects
    #: with "this type has no size". typemap.py should gain them.
    C_KEYWORDS = {
        "float": "ctypes.c_float", "double": "ctypes.c_double",
        "int": "ctypes.c_int32", "unsignedint": "ctypes.c_uint32",
        "char": "ctypes.c_char", "unsignedchar": "ctypes.c_ubyte",
        "short": "ctypes.c_int16", "unsignedshort": "ctypes.c_uint16",
        "long": "ctypes.c_int32", "unsignedlong": "ctypes.c_uint32",
        "longlong": "ctypes.c_int64", "unsignedlonglong": "ctypes.c_uint64",
        "byte": "ctypes.c_ubyte", "boolean": "ctypes.c_ubyte",
        "wchar_t": "ctypes.c_wchar", "size_t": "ctypes.c_size_t",
        "__int64": "ctypes.c_int64", "unsigned__int64": "ctypes.c_uint64",
    }

    def __init__(self, sdk, name):
        self.sdk = sdk
        self.name = name
        self.parsed = idl.module_constructs(sdk, name)
        if self.parsed is None:
            raise SystemExit("not a targeted IDL, or not in this kit: %s" % name)
        self.source = SOURCE or _FALLBACK_SOURCE
        self.local = (set(self.parsed["structs"]) | set(self.parsed["enums"])
                      | set(self.parsed.get("unions", {}))
                      | {a for a, _u in self.parsed.get("typedefs", [])})
        self.interfaces = set(self.parsed["interfaces"])
        self.unmapped = set()

    # ------------------------------------------------------------ types --
    def ctype(self, raw):
        """One IDL type token to a ctypes expression.

        Pointer depth travels as trailing asterisks on the token, exactly as the
        parser leaves it.
        """
        depth = 0
        while raw.endswith("*"):
            depth += 1
            raw = raw[:-1]
        raw = raw.strip()

        if raw in VOID_RETURN and depth == 0:
            return None
        if raw in VOID_RETURN:
            base = "ctypes.c_void_p"
            depth -= 1
        elif raw == "IUnknown":
            base = "comtypes.IUnknown"      # the one interface comtypes owns
        elif raw in self.C_KEYWORDS:
            base = self.C_KEYWORDS[raw]
        elif raw in self.interfaces:
            base = raw
        elif raw in self.local:
            base = raw
        elif raw in self.source:
            base = self.source[raw]
        elif raw.startswith("I") and raw[1:2].isupper():
            base = raw                      # an interface from an imported IDL
        else:
            base = raw                      # a type from an imported IDL
            if raw not in ("IUnknown",):
                self.unmapped.add(raw)

        for _ in range(depth):
            base = "ctypes.POINTER(%s)" % base
        return base

    # ---------------------------------------------------------- ordering --
    def _struct_order(self):
        """Structures in dependency order; a cycle would raise rather than emit
        something subtly wrong."""
        structs = self.parsed["structs"]
        deps = {}
        for name, spec in structs.items():
            refs = set()
            candidates = list(spec.get("parsed_fields", []))
            for kind, payload in spec.get("segments") or []:
                # A union-carrying structure has no parsed_fields, so its
                # dependencies live in the segments. Missing these ordered
                # D3D11_DEPTH_STENCIL_VIEW_DESC before D3D11_TEX1D_DSV, which it
                # contains.
                if kind == "fields":
                    candidates += list(payload)
                    continue
                candidates += list(payload["members"])
                for _field_name, nested_fields in payload["nested"]:
                    candidates += list(nested_fields)
            for ftype, _fname, _bound, _bits in candidates:
                base = ftype.rstrip("*")
                if base in structs and base != name:
                    refs.add(base)
            deps[name] = refs

        order, placed, guard = [], set(), 0
        while len(placed) < len(structs) and guard < 5000:
            guard += 1
            progressed = False
            for name in sorted(structs):
                if name in placed:
                    continue
                if deps[name] <= placed:
                    order.append(name)
                    placed.add(name)
                    progressed = True
            if not progressed:
                remaining = sorted(set(structs) - placed)
                raise SystemExit(
                    "cycle among structures, cannot order: %s" % remaining)
        return order

    def _enum_order(self):
        """Enumerations in dependency order.

        Members are usually literals, but not always:

            D3D12_COMMAND_LIST_SUPPORT_FLAG_DIRECT = 1 << D3D12_COMMAND_LIST_TYPE_DIRECT

        is a member of one enumeration whose value is written in terms of a
        member of another. File order happens to satisfy every such reference in
        DXGI and Direct3D 11, and does not in d3d12.idl, where seven members of
        D3D12_COMMAND_LIST_SUPPORT_FLAGS name an enumeration declared later.

        Same sort as _struct_order over a different graph: an enumeration
        depends on every other whose member names appear in its values.
        """
        enums = self.parsed["enums"]
        owner = {}
        for name, spec in enums.items():
            for member, _value in spec["members"]:
                owner[member] = name

        deps = {}
        for name, spec in enums.items():
            refs = set()
            for _member, value in spec["members"]:
                if not value:
                    continue
                for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", value):
                    holder = owner.get(token)
                    if holder and holder != name:
                        refs.add(holder)
            deps[name] = refs

        order, placed, guard = [], set(), 0
        while len(placed) < len(enums) and guard < 5000:
            guard += 1
            progressed = False
            for name in sorted(enums):
                if name in placed:
                    continue
                if deps[name] <= placed:
                    order.append(name)
                    placed.add(name)
                    progressed = True
            if not progressed:
                remaining = sorted(set(enums) - placed)
                raise SystemExit(
                    "cycle among enumerations, cannot order: %s" % remaining)
        return order

    def _interface_order(self):
        """Interfaces in inheritance order, base before derived."""
        ifaces = self.parsed["interfaces"]
        order, placed, guard = [], set(), 0
        while len(placed) < len(ifaces) and guard < 5000:
            guard += 1
            progressed = False
            for name in sorted(ifaces):
                if name in placed:
                    continue
                base = ifaces[name]["base"]
                if base not in ifaces or base in placed:
                    order.append(name)
                    placed.add(name)
                    progressed = True
            if not progressed:
                order.extend(sorted(set(ifaces) - placed))
                break
        return order

    # ----------------------------------------------------------- emitters --
    @staticmethod
    def c_literal(value):
        """Turn a C constant expression into one Python reads the same way.

        The SDK writes integer literals with width suffixes - 0x00000010UL, 1L,
        0xffffffffU - and floats with a trailing f. Python rejects all of them.
        Everything else, including ( 1 << (4 + 1) ), is already valid Python and
        passes through untouched.
        """
        value = value.strip()
        value = re.sub(r"\b(0[xX][0-9a-fA-F]+|\d+)[uUlL]+\b", r"\1", value)
        value = re.sub(r"\b(\d+\.\d*(?:[eE][-+]?\d+)?)[fF]\b", r"\1", value)
        # C reads a leading zero as octal; Python 3 refuses the form outright.
        # D3D11_SPEC_DATE_MONTH = 05 is the only one that bites, and it means 5
        # either way, but 0o keeps the C meaning for any that do not.
        value = re.sub(r"(?<![\w.])0([0-7]+)\b", r"0o\1", value)
        return value

    def emit_typedefs(self, local):
        """Scalar aliases.

        Split around the structure section on purpose: `typedef UINT
        DXGI_USAGE;` can be emitted immediately, but `typedef D3DCOLORVALUE
        DXGI_RGBA;` names a structure declared later in the same file and has to
        follow it. Emitting both early produced a NameError at import.

        `local` selects which half: False for aliases of primitive types, True
        for aliases of something this module declares.
        """
        out = []
        for alias, underlying in self.parsed.get("typedefs", []):
            base = underlying.rstrip("*")
            is_local = base in (set(self.parsed["structs"])
                                | set(self.parsed["enums"])
                                | self.interfaces)
            if is_local != local:
                continue
            rendered = self.ctype(underlying)
            if rendered:
                out.append("%-34s = %s" % (alias, rendered))
        return NEWLINE.join(out)

    def emit_callback(self, name, restype, parameters):
        """A `typedef void (__stdcall *Name)(...)` as a ctypes function type.

        WINFUNCTYPE rather than CFUNCTYPE: `__stdcall` is the calling convention
        and getting it wrong corrupts the stack on the way back out, which is
        not the kind of defect that shows up as a wrong number.

        The return type comes first, matching ctypes' own argument order rather
        than C's declaration order.
        """
        rendered = self.ctype(restype)
        arguments = ["None" if rendered is None else rendered]
        comments = []
        for ptype, pname in parameters:
            arguments.append(self.ctype(ptype) or "ctypes.c_void_p")
            comments.append("%s %s" % (ptype, pname))

        lines = ["%s = ctypes.WINFUNCTYPE(" % name]
        width = max(len(a) for a in arguments)
        for index, argument in enumerate(arguments):
            note = "the return type" if index == 0 else comments[index - 1]
            lines.append("    %-*s  # %s" % (width + 1, argument + ",", note))
        lines.append(")")
        return NEWLINE.join(lines)

    #: C operators that differ from Python, longest first. `&&` MUST be
    #: rewritten before anything looks at `&`, and `||` before `|` - turning a
    #: bitwise or into a logical one produces a number that is wrong rather than
    #: an error, and D3D12_ENCODE_BASIC_FILTER is built entirely out of them.
    _OPERATOR_REWRITES = ((r"&&", " and "), (r"\|\|", " or "))

    def emit_macro(self, name, parameters, body):
        """A function-like cpp_quote macro, as a Python function.

        All 24 in the target set are pure integer arithmetic, and `&`, `|`,
        `<<`, `>>` and `==` mean the same thing in both languages. Three things
        do not survive verbatim:

          * C casts. `((D3D12_FILTER)(expr))` has to lose the cast, because the
            generated enums are ctypes types and calling one returns an instance
            rather than an int.
          * `&&` and `||`.
          * The parameter names, which are left exactly as the SDK writes them
            even where that shadows a builtin - D3D12_ENCODE_BASIC_FILTER takes
            `min`, and a caller reading MSDN should find the same word here.
        """
        translated = body
        for pattern, replacement in self._OPERATOR_REWRITES:
            translated = re.sub(pattern, replacement, translated)

        local = set(parameters)

        def strip_cast(match):
            token = match.group(1)
            if token in local:
                return match.group(0)      # a parameter, not a type
            if self._is_type_name(token):
                return ""
            return match.group(0)

        # A parenthesised identifier immediately followed by another open
        # parenthesis: that is a cast applied to an expression. `(Src0)&MASK` is
        # not one, because `&` follows rather than `(`.
        translated = re.sub(r"\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*(?=\()",
                            strip_cast, translated)
        translated = re.sub(r"\s+", " ", translated).strip()

        signature = "def %s(%s):" % (name, ", ".join(parameters))
        return "%s\n    return %s" % (signature, translated)

    def _is_type_name(self, token):
        """Does this identifier name a type, as opposed to a constant?"""
        if token in self.parsed["enums"] or token in self.parsed["structs"]:
            return True
        if token in self.parsed.get("unions", {}):
            return True
        if token in self.interfaces or token in self.C_KEYWORDS:
            return True
        return token in self.source

    def emit_defines(self):
        out = []
        for name, value in self.parsed["defines"]:
            out.append("%-46s = %s" % (name, self.c_literal(value)))
        return "\n".join(out)

    def emit_enum(self, name):
        spec = self.parsed["enums"][name]
        lines = ["%s = ctypes.c_uint" % name]
        width = max([len(m) for m, _v in spec["members"]] or [1])
        for member, value in spec["members"]:
            # `.value` on purpose, matching the hand-written modules: a flag
            # enum is meant to be composed, and ORing two ctypes instances
            # raises TypeError. Members are therefore plain ints, while the
            # source still records which enum they belong to.
            if value is None:
                lines.append("%-*s = %s().value" % (width, member, name))
            else:
                lines.append("%-*s = %s(%s).value"
                             % (width, member, name, self.c_literal(value)))
        return "\n".join(lines)


    def _render_fields(self, fields, indent):
        """`_fields_ = [...]`, aligned, at the given indentation.

        A nested class name arrives as the field type verbatim - `_VertexBuffer`
        - and must not be run through the type map, which would not find it.
        """
        pad = " " * indent
        width = max(len(f[1]) for f in fields)
        rendered = []
        for ftype, fname, bound, bits in fields:
            if ftype.startswith("_") and bound is None:
                base = ftype                       # a nested class, declared above
            else:
                base = self._field_type(ftype, bound)
            gap = " " * (width - len(fname))
            if bits:
                rendered.append("('%s',%s %s, %d)" % (fname, gap, base, bits))
            else:
                rendered.append("('%s',%s %s)" % (fname, gap, base))

        out = [pad + "_fields_ = [" + rendered[0] + ","]
        continuation = pad + " " * len("_fields_ = [")
        for item in rendered[1:]:
            out.append(continuation + item + ",")
        out.append(pad + "]")
        return out

    def _emit_struct_with_union(self, name, segments):
        """A structure carrying one or more anonymous unions.

        Emitted as nested Union classes plus _anonymous_, matching the shape the
        hand-written D3D11_RENDER_TARGET_VIEW_DESC uses - so generated and
        hand-written modules read the same way.

        The segments arrive as an ordered list rather than a before/union/after
        triple because a structure may carry more than one: D3D11_BUFFER_SRV has
        two, back to back. Handling only the first flattened the second into
        plain fields, and eight bytes of structure came out as twelve.
        """
        lines = ["class %s(ctypes.Structure):" % name]
        total = sum(1 for kind, _f in segments if kind == "union")
        outer, anonymous, index = [], [], 0

        for kind, payload in segments:
            if kind == "fields":
                outer.extend(payload)
                continue
            index += 1
            cls = "_U" if total == 1 else "_U%d" % index
            attr = "u" if total == 1 else "u%d" % index
            lines.append("    class %s(ctypes.Union):" % cls)

            # The union may hold NAMED structures of its own -
            # D3D12_INDIRECT_ARGUMENT_DESC overlays six, one per argument kind.
            # Each becomes a nested class, reached as .VertexBuffer and so on,
            # which needs no _anonymous_ because the SDK gave it a name.
            members = list(payload["members"])
            for field_name, nested_fields in payload["nested"]:
                nested_cls = "_" + field_name
                lines.append("        class %s(ctypes.Structure):" % nested_cls)
                lines.extend(self._render_fields(nested_fields, indent=12))
                members.append((nested_cls, field_name, None, None))

            if not members:
                lines.append("        _fields_ = []")
            else:
                lines.extend(self._render_fields(members, indent=8))
            outer.append(("__union__" + cls, attr, None, None))
            anonymous.append(attr)

        width = max(len(f[1]) for f in outer)
        rendered = []
        for ftype, fname, bound, bits in outer:
            if ftype.startswith("__union__"):
                rendered.append("('%s',%s %s)"
                                % (fname, " " * (width - len(fname)),
                                   ftype[len("__union__"):]))
                continue
            base = self._field_type(ftype, bound)
            if bits:
                rendered.append("('%s',%s %s, %d)"
                                % (fname, " " * (width - len(fname)), base, bits))
            else:
                rendered.append("('%s',%s %s)"
                                % (fname, " " * (width - len(fname)), base))

        lines.append("    _anonymous_ = (%s)"
                     % "".join("'%s', " % a for a in anonymous).rstrip())
        lines.append("    _fields_ = [" + rendered[0] + ",")
        for item in rendered[1:]:
            lines.append("                " + item + ",")
        lines.append("    ]")
        return NEWLINE.join(lines)

    def _field_type(self, ftype, bound):
        base = self.ctype(ftype) or "ctypes.c_void_p"
        for extent in reversed(bound or []):
            base = "%s * %s" % (base, extent)
        return base

    def emit_union(self, name):
        """A top-level `typedef union`.

        D3D11_AUTHENTICATED_PROTECTION_FLAGS overlays a named struct of bitfields
        on a plain UINT - the flags-or-value idiom. The nested struct carries a
        name in the IDL, so it needs no _anonymous_: it is reached as .Flags.
        """
        spec = self.parsed["unions"][name]
        lines = ["class %s(ctypes.Union):" % name]

        entries = []
        for fieldname, fields in spec["nested"]:
            cls = "_" + fieldname
            lines.append("    class %s(ctypes.Structure):" % cls)
            if not fields:
                lines.append("        _fields_ = []")
                entries.append((fieldname, cls))
                continue
            width = max(len(f[1]) for f in fields)
            rendered = []
            for ftype, fname, bound, bits in fields:
                base = self._field_type(ftype, bound)
                pad = " " * (width - len(fname))
                if bits:
                    rendered.append("('%s',%s %s, %d)" % (fname, pad, base, bits))
                else:
                    rendered.append("('%s',%s %s)" % (fname, pad, base))
            lines.append("        _fields_ = [" + rendered[0] + ",")
            for item in rendered[1:]:
                lines.append("                    " + item + ",")
            lines.append("        ]")
            entries.append((fieldname, cls))

        members = [(f[1], self._field_type(f[0], f[2])) for f in spec["members"]]
        members += entries
        if not members:
            lines.append("    _fields_ = []")
            return NEWLINE.join(lines)

        width = max(len(m[0]) for m in members)
        rendered = ["('%s',%s %s)" % (n, " " * (width - len(n)), t)
                    for n, t in members]
        lines.append("    _fields_ = [" + rendered[0] + ",")
        for item in rendered[1:]:
            lines.append("                " + item + ",")
        lines.append("    ]")
        return NEWLINE.join(lines)


    def emit_struct(self, name):
        spec = self.parsed["structs"][name]
        fields = spec.get("parsed_fields", [])
        lines = ["class %s(ctypes.Structure):" % name]

        if spec.get("segments"):
            return self._emit_struct_with_union(name, spec["segments"])

        if spec.get("opaque"):
            lines.append("    # contains a nested struct - not yet emitted")
            lines.append("    _fields_ = []")
            return "\n".join(lines)
        if not fields:
            lines.append("    _fields_ = []")
            return "\n".join(lines)

        width = max(len(f[1]) for f in fields)
        rendered = []
        for ftype, fname, bound, bits in fields:
            base = self.ctype(ftype) or "ctypes.c_void_p"
            if bound:
                # C declares the outermost dimension first: FLOAT x[8][2] is
                # eight pairs. ctypes composes the other way round, so the
                # bounds are applied innermost-first.
                for extent in reversed(bound):
                    base = "%s * %s" % (base, extent)
            if bits:
                rendered.append("('%s',%s %s, %d)"
                                % (fname, " " * (width - len(fname)), base, bits))
            else:
                rendered.append("('%s',%s %s)"
                                % (fname, " " * (width - len(fname)), base))
        if any(ftype.rstrip("*") == name for ftype, _n, _b, _bits in fields):
            # A structure that points at itself: D3D12_AUTO_BREADCRUMB_NODE
            # ends with `const struct D3D12_AUTO_BREADCRUMB_NODE *pNext`, which
            # is a linked list. The class object has to exist before its own
            # _fields_ can name it, so the body is assigned afterwards - the
            # same shape ctypes documents for recursive structures, and the same
            # trick the interface vtables already use.
            lines = ["class %s(ctypes.Structure):" % name,
                     "    pass",
                     "",
                     "",
                     "%s._fields_ = [" % name + rendered[0] + ","]
            pad = " " * (len(name) + len("._fields_ = ["))
            for item in rendered[1:]:
                lines.append(pad + item + ",")
            lines.append("]")
            return "\n".join(lines)

        lines.append("    _fields_ = [" + rendered[0] + ",")
        for item in rendered[1:]:
            lines.append("                " + item + ",")
        lines.append("    ]")
        return "\n".join(lines)

    def emit_interface_decl(self, name):
        """The class and its IID only.

        Every interface is declared before any vtable is assigned, which makes
        forward references between interfaces a non-problem: IDXGIOutput names
        IDXGISurface in GetDisplaySurfaceData, and IDXGISurface is declared later
        in the same IDL. Emitting the vtable inline raises NameError - the
        general form of F-56, where a hand-written structure ended up with six
        fields commented out and the note "Interface dependance defined after".
        """
        spec = self.parsed["interfaces"][name]
        base = spec["base"]
        if base == "IUnknown":
            base = "comtypes.IUnknown"
        return ('class %s(%s):%s    _iid_ = comtypes.GUID("{%s}")'
                % (name, base, NEWLINE, spec["uuid"]))

    def _returns_struct_by_value(self, restype):
        """The structure name if this return type is one BY VALUE, else None.

        A pointer return is ordinary and needs no special handling; it is the
        by-value case that carries the x64 hidden-argument convention. See F-58.
        """
        if restype.endswith("*"):
            return None
        if restype in self.parsed["structs"] or restype in self.parsed.get("unions", {}):
            return restype
        return None

    def emit_interface_methods(self, name):
        """The vtable, assigned once every class object exists."""
        spec = self.parsed["interfaces"][name]
        if not spec["methods"]:
            # An interface the SDK genuinely declares empty. ID3D11VertexShader
            # and seven siblings add nothing to ID3D11DeviceChild; they exist so
            # the type system can tell a vertex shader from a pixel shader.
            #
            # The empty list is not decoration. comtypes refuses to build a
            # vtable for a class whose base has no _methods_ - "baseinterface
            # 'ID3D12Pageable' has no _methods_" - and ID3D12Pageable is the
            # base of eleven interfaces. Every empty interface in the D3D11
            # family happens to be a leaf, so emitting a comment here worked
            # until Direct3D 12 arrived. See C-39.
            return ("## %s adds no methods to %s.%s%s._methods_ = []"
                    % (name, spec["base"], NEWLINE, name))

        lines = ["%s._methods_ = [" % name]
        for method in spec["methods"]:
            restype, params = spec.get("signatures", {}).get(method,
                                                             ("HRESULT", []))
            ret = self.ctype(restype)
            ret = "None" if ret is None else ret

            sret = self._returns_struct_by_value(restype)
            if sret:
                # F-58. On x64 a COM method returning a structure by value takes
                # a hidden pointer to the caller's storage as its FIRST argument
                # and returns that pointer; it does not hand the structure back
                # in a register. Declaring the structure as the restype makes
                # ctypes read a register holding something else and write
                # through it, which faults rather than failing.
                #
                # Proved by calling one vtable slot both ways:
                #   restype is the struct        -> access violation
                #   hidden out-pointer + byref   -> a valid handle
                # and that holds even for an eight-byte structure, which is the
                # part that catches people out.
                #
                # So the caller passes byref(out) and reads `out`. Not pretty,
                # but the alternative is a method that cannot be called.
                pointer = "ctypes.POINTER(%s)" % sret
                lines.append('    comtypes.STDMETHOD(%s, "%s", [' % (pointer, method))
                pad = " " * max(1, 44 - len(pointer))
                lines.append("        %s,%s# %s, the x64 hidden return slot"
                             % (pointer, pad, sret))
                for ptype, pname in params:
                    rendered = self.ctype(ptype) or "ctypes.c_void_p"
                    pad = " " * max(1, 44 - len(rendered))
                    lines.append("        %s,%s# %s %s"
                                 % (rendered, pad, ptype, pname))
                lines.append("        ]),")
                continue

            if not params:
                lines.append('    comtypes.STDMETHOD(%s, "%s", []),'
                             % (ret, method))
                continue
            lines.append('    comtypes.STDMETHOD(%s, "%s", [' % (ret, method))
            for ptype, pname in params:
                rendered = self.ctype(ptype) or "ctypes.c_void_p"
                pad = " " * max(1, 44 - len(rendered))
                lines.append("        %s,%s# %s %s"
                             % (rendered, pad, ptype, pname))
            lines.append("        ]),")
        lines.append("]")
        return NEWLINE.join(lines)


    # -------------------------------------------------------------- whole --
    def emit(self):
        # MAKE_HRESULT is a winerror.h macro that no .idl declares, and
        # d3d11.idl's MAKE_D3D11_HRESULT is written in terms of it. Imported
        # only where a macro actually needs it, so a module without one does not
        # carry an unused import.
        needs_hresult = any("MAKE_HRESULT" in body
                            for _n, _a, body in self.parsed.get("macros", []))
        helpers = ("from Direct3D.PyIdl.status import MAKE_HRESULT"
                   if needs_hresult else "")
        parts = [HEADER.format(sdk=os.path.basename(self.sdk), idl=self.name,
                               helpers=helpers)]

        imports = [i[:-4] for i in self.parsed["imports"]]
        if imports:
            parts.append("")
            for module in imports:
                parts.append("from Direct3D.PyIdl.%s import *" % module)

        if self.parsed.get("typedefs"):
            parts.append(NEWLINE + NEWLINE +
                         "## ------------------------------------------------ "
                         "typedefs ----")
            parts.append(self.emit_typedefs(local=False))

        if self.parsed.get("macros"):
            # Before the constants, because a constant may call one:
            # D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING is defined as
            # D3D12_ENCODE_SHADER_4_COMPONENT_MAPPING(0,1,2,3). The bodies are
            # not evaluated until called, so anything they name only has to
            # exist by then - and the SDK's own file order already guarantees
            # that for every call made at module level.
            parts.append(NEWLINE + NEWLINE +
                         "## ------------------------------------------------ "
                         "macros ----")
            parts.append(NEWLINE + "## Function-like macros from cpp_quote, as "
                         "functions. Pure integer")
            parts.append("## arithmetic in the SDK and pure integer arithmetic "
                         "here.")
            for name, parameters, body in self.parsed["macros"]:
                parts.append(NEWLINE + NEWLINE
                             + self.emit_macro(name, parameters, body))

        if self.parsed["defines"]:
            parts.append("\n\n## ---------------------------------------------- "
                         "constants ----")
            parts.append(self.emit_defines())

        if self.parsed["enums"]:
            parts.append("\n\n## -------------------------------------------- "
                         "enumerations ----")
            for name in self._enum_order():
                parts.append("\n" + self.emit_enum(name))

        if self.parsed.get("callbacks"):
            # After the enumerations, because a callback names them:
            # D3D12MessageFunc takes a D3D12_MESSAGE_CATEGORY. Unlike a macro
            # body, a WINFUNCTYPE argument list is evaluated immediately.
            parts.append(NEWLINE + NEWLINE +
                         "## ---------------------------------------- "
                         "callback types ----")
            for name, restype, parameters in self.parsed["callbacks"]:
                parts.append(NEWLINE + NEWLINE
                             + self.emit_callback(name, restype, parameters))

        # Three passes, in this order, because the references run both ways:
        #
        #   1. interface DECLARATIONS - class plus _iid_, nothing else
        #   2. structures             - some carry ID3D11Resource* fields
        #   3. interface VTABLES      - most take structures as parameters
        #
        # Emitting structures first breaks on D3D11_AUTHENTICATED_* and friends,
        # which name an interface declared later. Emitting interfaces first with
        # their vtables inline breaks the other way. Splitting the interface into
        # declaration and vtable satisfies both, and is the same trick that makes
        # forward references between interfaces work.
        if self.parsed["interfaces"]:
            parts.append("\n\n## ---------------------------------------------- "
                         "interfaces ----")
            parts.append(NEWLINE + "## Declarations only. Vtables are assigned at "
                         "the end of the file, once every")
            parts.append("## class exists, so anything may reference anything.")
            for name in self._interface_order():
                parts.append(NEWLINE + NEWLINE + self.emit_interface_decl(name))

        if self.parsed.get("unions"):
            parts.append(NEWLINE + NEWLINE +
                         "## -------------------------------------------------- "
                         "unions ----")
            for name in sorted(self.parsed["unions"]):
                parts.append(NEWLINE + NEWLINE + self.emit_union(name))

        if self.parsed["structs"]:
            parts.append("\n\n## ---------------------------------------------- "
                         "structures ----")
            for name in self._struct_order():
                parts.append("\n\n" + self.emit_struct(name))

            trailing = self.emit_typedefs(local=True)
            if trailing:
                parts.append(NEWLINE + NEWLINE + trailing)

        if self.parsed["interfaces"]:
            parts.append(NEWLINE + NEWLINE +
                         "## ------------------------- vtables, assigned once "
                         "every class exists ----")
            for name in self._interface_order():
                parts.append(NEWLINE + self.emit_interface_methods(name))

        parts.append("\n\n## -- End Of File --\n")
        return "\n".join(parts)


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1

    sdk = idl.find_sdk()
    if not sdk:
        raise SystemExit("No Windows SDK found.")

    if "--all" in argv:
        outdir = argv[argv.index("--outdir") + 1] if "--outdir" in argv else "generated"
        os.makedirs(outdir, exist_ok=True)
        for _sub, name in idl.TARGETS:
            if idl.idl_path(sdk, name) is None:
                continue
            try:
                text = Emitter(sdk, name).emit()
            except SystemExit as exc:
                print("  SKIP %-24s %s" % (name, exc))
                continue
            dst = os.path.join(outdir, name.replace(".idl", ".py"))
            io.open(dst, "w", encoding="utf-8", newline="\n").write(text)
            print("  %-24s -> %s (%d lines)"
                  % (name, dst, text.count("\n") + 1))
        return 0

    name = argv[0]
    emitter = Emitter(sdk, name)
    text = emitter.emit()
    if "-o" in argv:
        dst = argv[argv.index("-o") + 1]
        io.open(dst, "w", encoding="utf-8", newline="\n").write(text)
        print("wrote %s (%d lines)" % (dst, text.count("\n") + 1))
        if emitter.unmapped:
            print("types resolved from imported IDLs: %s"
                  % ", ".join(sorted(emitter.unmapped)))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
