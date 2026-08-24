# -*- coding: utf-8 -*-
"""The canonical IDL-to-ctypes type table.

Every type decision in this project lives here, in one reviewable place. Nothing
else should decide how a Windows type maps to ctypes.

Why this module exists
----------------------
Before it, `BOOL` was translated as `wintypes.BOOL` in most places and as
`ctypes.c_bool` in ten others. `wintypes.BOOL` is a 4-byte signed int;
`ctypes.c_bool` is one byte. Where a 4-byte member happened to follow the field,
alignment hid the mistake completely - which is why it survived years of review.
Where two of them sat next to each other it did not: the structure came out four
bytes short with its last field three bytes early.

That class of defect is invisible to reading, and invisible to any test that
only counts interfaces. The fix is not vigilance, it is having exactly one table.

Two representations
-------------------
`TYPES` maps an IDL type name to the real ctypes object, for runtime use and for
the size assertions in the test suite.

`SOURCE` maps the same name to the text a generator should emit. The two are
kept in step by `self_check()`, which the test suite calls.
"""
import ctypes
import ctypes.wintypes as wintypes

import comtypes


# --------------------------------------------------------------- structs ----
class LUID(ctypes.Structure):
    """Locally unique identifier. Adapter identity, stable within a boot."""
    _fields_ = [("LowPart", wintypes.DWORD),
                ("HighPart", wintypes.LONG)]


class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("nLength", wintypes.DWORD),
                ("lpSecurityDescriptor", ctypes.c_void_p),
                ("bInheritHandle", wintypes.BOOL)]


# ----------------------------------------------------------------- table ----
#: IDL / SDK type name -> ctypes type.
#:
#: Handles map to c_void_p rather than wintypes.HANDLE deliberately: on
#: win-amd64 a handle is 64 bits, and c_void_p is the mapping that stays correct
#: both as a structure field and as a function return value.
TYPES = {
    # -- integers ---------------------------------------------------------
    "BOOL":            wintypes.BOOL,        # 4 bytes signed. NEVER c_bool.
    "BOOLEAN":         ctypes.c_ubyte,       # 1 byte. A different type to BOOL.
    "BYTE":            ctypes.c_ubyte,
    "CHAR":            ctypes.c_char,
    "WCHAR":           ctypes.c_wchar,
    "INT8":            ctypes.c_int8,
    "UINT8":           ctypes.c_uint8,
    "SHORT":           ctypes.c_int16,
    "USHORT":          ctypes.c_uint16,
    "INT16":           ctypes.c_int16,
    "UINT16":          ctypes.c_uint16,
    "WORD":            ctypes.c_uint16,
    "INT":             ctypes.c_int32,
    "INT32":           ctypes.c_int32,
    "LONG":            ctypes.c_int32,       # Win32 LONG is 4 bytes everywhere
    "UINT":            ctypes.c_uint32,
    "UINT32":          ctypes.c_uint32,
    "ULONG":           ctypes.c_uint32,
    "DWORD":           ctypes.c_uint32,
    "INT64":           ctypes.c_int64,
    "LONGLONG":        ctypes.c_int64,
    "UINT64":          ctypes.c_uint64,
    "ULONGLONG":       ctypes.c_uint64,
    "DWORDLONG":       ctypes.c_uint64,
    "LARGE_INTEGER":   ctypes.c_int64,
    "ULARGE_INTEGER":  ctypes.c_uint64,
    "SIZE_T":          ctypes.c_size_t,
    "SSIZE_T":         ctypes.c_ssize_t,

    # -- floating point ---------------------------------------------------
    "FLOAT":           ctypes.c_float,
    "DOUBLE":          ctypes.c_double,

    # -- strings ----------------------------------------------------------
    "LPSTR":           ctypes.c_char_p,
    "LPCSTR":          ctypes.c_char_p,
    "LPWSTR":          ctypes.c_wchar_p,
    "LPCWSTR":         ctypes.c_wchar_p,

    # -- handles and opaque pointers --------------------------------------
    "HANDLE":          ctypes.c_void_p,
    "HWND":            ctypes.c_void_p,
    "HDC":             ctypes.c_void_p,
    "HMONITOR":        ctypes.c_void_p,
    "HMODULE":         ctypes.c_void_p,
    "HINSTANCE":       ctypes.c_void_p,
    "LPVOID":          ctypes.c_void_p,
    "void*":           ctypes.c_void_p,

    # -- COM --------------------------------------------------------------
    "HRESULT":         comtypes.HRESULT,
    "GUID":            comtypes.GUID,
    "IID":             comtypes.GUID,
    "REFIID":          comtypes.GUID,        # const IID* - passed by reference
    "REFGUID":         comtypes.GUID,
    "CLSID":           comtypes.GUID,

    # -- aggregates -------------------------------------------------------
    "RECT":            wintypes.RECT,
    "POINT":           wintypes.POINT,
    "SIZE":            wintypes.SIZE,
    "LUID":            LUID,
    "SECURITY_ATTRIBUTES": SECURITY_ATTRIBUTES,
}

#: The same table as generator-emittable source text.
SOURCE = {
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
    "void*": "ctypes.c_void_p",
    "HRESULT": "comtypes.HRESULT", "GUID": "comtypes.GUID", "IID": "comtypes.GUID",
    "REFIID": "comtypes.GUID", "REFGUID": "comtypes.GUID", "CLSID": "comtypes.GUID",
    "RECT": "wintypes.RECT", "POINT": "wintypes.POINT", "SIZE": "wintypes.SIZE",
    "LUID": "LUID", "SECURITY_ATTRIBUTES": "SECURITY_ATTRIBUTES",
}

#: Expected sizes on win-amd64. Asserted by the test suite, so a wrong mapping
#: fails loudly rather than silently shifting a structure.
EXPECTED_SIZES = {
    "BOOL": 4, "BOOLEAN": 1, "BYTE": 1, "CHAR": 1, "WCHAR": 2,
    "INT8": 1, "UINT8": 1, "SHORT": 2, "USHORT": 2, "INT16": 2, "UINT16": 2,
    "WORD": 2, "INT": 4, "INT32": 4, "LONG": 4, "UINT": 4, "UINT32": 4,
    "ULONG": 4, "DWORD": 4, "INT64": 8, "LONGLONG": 8, "UINT64": 8,
    "ULONGLONG": 8, "DWORDLONG": 8, "LARGE_INTEGER": 8, "ULARGE_INTEGER": 8,
    "FLOAT": 4, "DOUBLE": 8, "GUID": 16, "IID": 16, "REFIID": 16, "REFGUID": 16,
    "CLSID": 16, "LUID": 8, "RECT": 16, "POINT": 8,
}

#: Types whose size follows the pointer width.
POINTER_SIZED = ("SIZE_T", "SSIZE_T", "HANDLE", "HWND", "HDC", "HMONITOR",
                 "HMODULE", "HINSTANCE", "LPVOID", "void*",
                 "LPSTR", "LPCSTR", "LPWSTR", "LPCWSTR")

#: IDL spellings for "returns nothing". comtypes wants None, not c_void_p - the
#: two are not interchangeable, and mixing them is finding F-39.
VOID_RETURN = ("void", "VOID")


def resolve(idl_type, pointer_depth=0, array_length=None):
    """Map an IDL type name to a ctypes type.

    >>> resolve("UINT") is ctypes.c_uint32
    True
    >>> ctypes.sizeof(resolve("BOOL"))
    4
    >>> resolve("FLOAT", array_length=4)._length_
    4

    `array_length` builds a fixed array, `pointer_depth` wraps in POINTER().
    Arrays are applied first, matching C declaration order.
    """
    if idl_type in VOID_RETURN and pointer_depth == 0:
        return None
    base = TYPES.get(idl_type)
    if base is None:
        raise KeyError(
            "no mapping for IDL type %r - add it to typemap.TYPES rather than "
            "guessing at the call site" % (idl_type,))
    if array_length is not None:
        base = base * array_length
    for _ in range(pointer_depth):
        base = ctypes.POINTER(base)
    return base


def self_check():
    """Verify the table against itself and against the running interpreter.

    Returns a list of problem strings; empty means healthy. The test suite calls
    this, and it is importable so it can also be run by hand:

        python -c "from Direct3D.PyIdl import typemap; print(typemap.self_check())"
    """
    problems = []
    ptr = ctypes.sizeof(ctypes.c_void_p)

    missing = set(TYPES) - set(SOURCE)
    if missing:
        problems.append("in TYPES but not SOURCE: %s" % sorted(missing))
    extra = set(SOURCE) - set(TYPES)
    if extra:
        problems.append("in SOURCE but not TYPES: %s" % sorted(extra))

    for name, expected in EXPECTED_SIZES.items():
        actual = ctypes.sizeof(TYPES[name])
        if actual != expected:
            problems.append("%s is %d bytes, expected %d" % (name, actual, expected))

    for name in POINTER_SIZED:
        actual = ctypes.sizeof(TYPES[name])
        if actual != ptr:
            problems.append("%s is %d bytes, expected pointer width %d"
                            % (name, actual, ptr))

    # The specific mistake this module exists to prevent.
    if TYPES["BOOL"] is ctypes.c_bool or ctypes.sizeof(TYPES["BOOL"]) == 1:
        problems.append("BOOL has been mapped to a one-byte type again - F-47")

    return problems


if __name__ == "__main__":
    found = self_check()
    if found:
        for problem in found:
            print("PROBLEM:", problem)
        raise SystemExit(1)
    print("typemap self-check passed: %d types, pointer width %d bytes"
          % (len(TYPES), ctypes.sizeof(ctypes.c_void_p)))
