# -*- coding: utf-8 -*-
"""Repair the four silent defects in the hand-written bindings.

    F-08  `_mehtods_`       two interfaces registered zero vtable slots
    F-09  `_flags_`         one structure reported sizeof() == 0
    F-47  `c_bool`          a one-byte type where the IDL declares four
    F-48  missing _fields_  a struct declared its nested union and nothing else

All four are single-token mistakes that ctypes and comtypes accept in complete
silence, and all four survived years of review. Win32 BOOL is a 4-byte signed
int; ctypes.c_bool is one byte, and ten sites used the latter.

Two are worse than they look:

  * ID3D11DeviceContext::GetPredication takes `BOOL *pPredicateValue`, an
    out-parameter, and the binding declared it by value - so ctypes passed a
    one-byte value where the callee expects a pointer to write through.

  * D3D11_UNORDERED_ACCESS_VIEW_DESC declared its nested union `_I1` and then
    stopped, with no `_fields_` at all. sizeof() was 0 instead of 16.

Every replacement is anchored on surrounding context, so the script cannot
silently patch the wrong line if a file moves. It is idempotent: running it twice
is a no-op.

Usage:  python tools/fix_binding_defects.py [--check] [--root PATH]

    --check      report what would change and exit non-zero if anything would,
                 without writing. Suitable for CI.
    --root PATH  repository root. Defaults to this script's parent directory,
                 which is correct once the script lives in tools/.
"""
import io
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.pardir))

D3D11 = "Direct3D/PyIdl/d3d11.py"
SDKLAYERS = "Direct3D/PyIdl/d3d11sdklayers.py"
DXGI1_2 = "Direct3D/PyIdl/dxgi1_2.py"

NL = "\n"

# (file, anchored old text, new text, why)
EDITS = [
    # ------------------------------------------------------------- F-08 ----
    (SDKLAYERS,
     'class ID3D11Debug(comtypes.IUnknown):' + NL +
     '    _iid_ = comtypes.GUID("{79cf2233-7536-4948-9d36-1e4692dc5760}")' + NL +
     '    _mehtods_ = [',
     'class ID3D11Debug(comtypes.IUnknown):' + NL +
     '    _iid_ = comtypes.GUID("{79cf2233-7536-4948-9d36-1e4692dc5760}")' + NL +
     '    _methods_ = [',
     "F-08: ID3D11Debug declared its vtable as _mehtods_, so comtypes registered "
     "zero slots and every debug-layer call raised AttributeError."),

    (SDKLAYERS,
     'class ID3D11SwitchToRef(comtypes.IUnknown):' + NL +
     '    _iid_ = comtypes.GUID("{1EF337E3-58E7-4F83-A692-DB221F5ED47E}")' + NL +
     '    _mehtods_ = [',
     'class ID3D11SwitchToRef(comtypes.IUnknown):' + NL +
     '    _iid_ = comtypes.GUID("{1EF337E3-58E7-4F83-A692-DB221F5ED47E}")' + NL +
     '    _methods_ = [',
     "F-08: the same typo on ID3D11SwitchToRef."),

    # ------------------------------------------------------------- F-09 ----
    (D3D11,
     "class D3D11_BOX(ctypes.Structure):" + NL +
     "    _flags_ = [('left',   wintypes.UINT),",
     "class D3D11_BOX(ctypes.Structure):" + NL +
     "    _fields_ = [('left',   wintypes.UINT),",
     "F-09: D3D11_BOX stored its members under _flags_, which ctypes ignores. "
     "sizeof(D3D11_BOX) was 0 instead of 24."),

    # ------------------------------------------------------------- F-48 ----
    (D3D11,
     "                    ('Texture3D',      D3D11_TEX3D_UAV)," + NL +
     "        ]" + NL +
     NL +
     "class ID3D11UnorderedAccessView(ID3D11View):",
     "                    ('Texture3D',      D3D11_TEX3D_UAV)," + NL +
     "        ]" + NL +
     "    _anonymous_ = ('i1',)" + NL +
     "    _fields_ = [('Format',        DXGI_FORMAT)," + NL +
     "                ('ViewDimension', D3D11_UAV_DIMENSION)," + NL +
     "                ('i1',_I1)," + NL +
     "    ]" + NL +
     NL +
     "class ID3D11UnorderedAccessView(ID3D11View):",
     "F-48: D3D11_UNORDERED_ACCESS_VIEW_DESC declared its nested union but no "
     "_fields_ at all, so sizeof() was 0 instead of 16. The sibling "
     "D3D11_RENDER_TARGET_VIEW_DESC shows the intended shape."),

    # ------------------------------------------------------------- F-47 ----
    (D3D11,
     "    _fields_ = [('Frequency', ctypes.c_ulonglong)," + NL +
     "                ('Disjoint', ctypes.c_bool),",
     "    _fields_ = [('Frequency', ctypes.c_ulonglong)," + NL +
     "                ('Disjoint', wintypes.BOOL),",
     "F-47: D3D11_QUERY_DATA_TIMESTAMP_DISJOINT.Disjoint is BOOL."),

    (D3D11,
     '        comtypes.STDMETHOD(None, "SetPredication", [' + NL +
     "            ctypes.POINTER(ID3D11Predicate)," + NL +
     "            ctypes.c_bool,",
     '        comtypes.STDMETHOD(None, "SetPredication", [' + NL +
     "            ctypes.POINTER(ID3D11Predicate)," + NL +
     "            wintypes.BOOL,",
     "F-47: SetPredication takes BOOL PredicateValue."),

    (D3D11,
     '        comtypes.STDMETHOD(None, "ExecuteCommandList", [' + NL +
     "            ctypes.POINTER(ID3D11CommandList)," + NL +
     "            ctypes.c_bool,",
     '        comtypes.STDMETHOD(None, "ExecuteCommandList", [' + NL +
     "            ctypes.POINTER(ID3D11CommandList)," + NL +
     "            wintypes.BOOL,",
     "F-47: ExecuteCommandList takes BOOL RestoreContextState."),

    (D3D11,
     '        comtypes.STDMETHOD(None, "GetPredication", [' + NL +
     "            ctypes.POINTER(ctypes.POINTER(ID3D11Predicate))," + NL +
     "            ctypes.c_bool,",
     '        comtypes.STDMETHOD(None, "GetPredication", [' + NL +
     "            ctypes.POINTER(ctypes.POINTER(ID3D11Predicate))," + NL +
     "            ctypes.POINTER(wintypes.BOOL),",
     "F-47: GetPredication takes BOOL* pPredicateValue - an OUT parameter that "
     "was declared by value. This one was writing through a non-pointer."),

    (D3D11,
     '        comtypes.STDMETHOD(comtypes.HRESULT, "FinishCommandList", [' + NL +
     "            ctypes.c_bool,",
     '        comtypes.STDMETHOD(comtypes.HRESULT, "FinishCommandList", [' + NL +
     "            wintypes.BOOL,",
     "F-47: FinishCommandList takes BOOL RestoreDeferredContextState."),

    (D3D11,
     "    _fields_ = [('Enable', ctypes.c_bool), " + NL +
     "                ('OutputIndex', wintypes.UINT),",
     "    _fields_ = [('Enable', wintypes.BOOL), " + NL +
     "                ('OutputIndex', wintypes.UINT),",
     "F-47: D3D11_VIDEO_PROCESSOR_STREAM.Enable is BOOL."),

    (D3D11,
     "                ('AccessibleInContiguousBlocks', ctypes.c_bool)," + NL +
     "                ('AccessibleInNonContiguousBlocks', ctypes.c_bool),",
     "                ('AccessibleInContiguousBlocks', wintypes.BOOL)," + NL +
     "                ('AccessibleInNonContiguousBlocks', wintypes.BOOL),",
     "F-47: two adjacent BOOLs - the case where alignment does NOT hide the "
     "error. This structure was 44 bytes instead of 48, last field 3 bytes early."),

    (D3D11,
     "                ('ProcessHandle', wintypes.HANDLE)," + NL +
     "                ('AllowAccess', ctypes.c_bool),",
     "                ('ProcessHandle', wintypes.HANDLE)," + NL +
     "                ('AllowAccess', wintypes.BOOL),",
     "F-47: D3D11_AUTHENTICATED_CONFIGURE_ACCESSIBLE_ENCRYPTION_INPUT.AllowAccess "
     "is BOOL."),

    (DXGI1_2,
     '        comtypes.STDMETHOD(ctypes.c_bool, "IsStereoEnabled",  [ ]),',
     '        comtypes.STDMETHOD(wintypes.BOOL, "IsStereoEnabled",  [ ]),',
     "F-47: IsStereoEnabled returns BOOL. SetStereoEnabled two lines below "
     "already used wintypes.BOOL for the same type."),
]


def main():
    argv = sys.argv[1:]
    check_only = "--check" in argv
    root = ROOT
    if "--root" in argv:
        root = os.path.abspath(argv[argv.index("--root") + 1])

    changed, already, missing = [], [], []
    by_file = {}
    for path, old, new, why in EDITS:
        by_file.setdefault(path, []).append((old, new, why))

    for path, edits in sorted(by_file.items()):
        full = os.path.join(root, path)
        if not os.path.isfile(full):
            missing.extend((path, why) for _o, _n, why in edits)
            continue
        text = io.open(full, encoding="utf-8").read()
        original = text
        for old, new, why in edits:
            if old in text:
                text = text.replace(old, new, 1)
                changed.append((path, why))
            elif new in text:
                already.append((path, why))
            else:
                missing.append((path, why))
        if text != original and not check_only:
            io.open(full, "w", encoding="utf-8", newline="\n").write(text)

    verb = "WOULD FIX" if check_only else "FIXED"
    for path, why in changed:
        print("%-9s %s" % (verb, why))
        print("          in %s" % path)
    for _path, why in already:
        print("%-9s %s" % ("ok", why))
    for path, why in missing:
        print("%-9s %s" % ("NOT FOUND", why))
        print("          in %s" % path)

    print()
    print("%d changed, %d already correct, %d anchors not found"
          % (len(changed), len(already), len(missing)))

    if missing:
        print()
        print("An anchor did not match. The file has moved on since this script "
              "was written - re-check those sites by hand rather than loosening "
              "the anchors.")
        return 2
    if check_only and changed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
