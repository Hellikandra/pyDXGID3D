# -*- coding: utf-8 -*-
"""Repair the vtable and naming defects the P2 tests surface.

    F-41  ID3D11VideoContext is missing two methods at slots 28 and 31, so the
          thirty slots after them dispatch to the wrong function.
    F-42  ID3D11InfoQueue stops six methods short of the SDK. A contiguous tail,
          so the declared slots are correctly aligned - just incomplete.
    F-51  IDXGIDevice1 spells both frame-latency methods 'Frameltency'.
    F-20  D3D11_INPUT_ELEMENT_DESC.InstanceDataSetRate should be
          InstanceDataStepRate.
    F-21  D3D11_BING_FLAG should be D3D11_BIND_FLAG.
    F-53  ID3D11DeviceContext::Map declares its out-parameter by value where the
          SDK declares a pointer. This one is on the capture path and it faults.
    F-55  D3D11_DEPTH_STENCILOP_DESC.StenilDepthFailOp is missing a C.

F-41 and F-53 change behaviour. The rest are naming: the
layout and the slots are right, but the Python name differs from the one MSDN
documents, so anyone copying from the documentation gets an AttributeError - or
worse, silently creates a new attribute and leaves the real field untouched.

A note on the video methods
---------------------------
The two methods added for F-41 declare `[]` for their parameters, matching every
other method on ID3D11VideoContext. That is deliberate. The interface is a set of
vtable placeholders - 56 of its 58 methods declare no parameters (finding F-49) -
and the purpose here is to restore slot alignment, not to pretend the interface
is callable. Filling in the parameters is separate work, tracked by the stub
budget in tests/test_tier1_vtable.py.

Every replacement is anchored on surrounding context. Idempotent.

Usage:  python tools/fix_vtable_defects.py [--check] [--root PATH]
"""
import io
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.pardir))

D3D11 = "Direct3D/PyIdl/d3d11.py"
SDKLAYERS = "Direct3D/PyIdl/d3d11sdklayers.py"
DXGI = "Direct3D/PyIdl/dxgi.py"
OUTPUTMGR = "OutputManager.py"

NL = "\n"

EDITS = [
    # -------------------------------------------------------------- F-41 ----
    (D3D11,
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamPixelAspectRatio", []),' + NL +
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamStereoFormat", []),',
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamPixelAspectRatio", []),' + NL +
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamLumaKey", []),' + NL +
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamStereoFormat", []),',
     "F-41: insert VideoProcessorSetStreamLumaKey at SDK slot 28."),

    (D3D11,
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamAutoProcessingMode", []),' + NL +
     '        comtypes.STDMETHOD(APP_DEPRECATED_HRESULT, "VideoProcessorSetStreamExtension", []),',
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamAutoProcessingMode", []),' + NL +
     '        comtypes.STDMETHOD(None, "VideoProcessorSetStreamFilter", []),' + NL +
     '        comtypes.STDMETHOD(APP_DEPRECATED_HRESULT, "VideoProcessorSetStreamExtension", []),',
     "F-41: insert VideoProcessorSetStreamFilter at SDK slot 31."),

    # -------------------------------------------------------------- F-53 ----
    (D3D11,
     '        comtypes.STDMETHOD(comtypes.HRESULT, "Map", [' + NL +
     "            ctypes.POINTER(ID3D11Resource)," + NL +
     "            ctypes.c_uint," + NL +
     "            D3D11_MAP," + NL +
     "            ctypes.c_uint," + NL +
     "            D3D11_MAPPED_SUBRESOURCE," + NL +
     "            ]),",
     '        comtypes.STDMETHOD(comtypes.HRESULT, "Map", [' + NL +
     "            ctypes.POINTER(ID3D11Resource)," + NL +
     "            ctypes.c_uint," + NL +
     "            D3D11_MAP," + NL +
     "            ctypes.c_uint," + NL +
     "            ctypes.POINTER(D3D11_MAPPED_SUBRESOURCE)," + NL +
     "            ]),",
     "F-53: Map takes D3D11_MAPPED_SUBRESOURCE* - an OUT parameter - and the "
     "binding declared the structure by value. Passing byref() marshals wrongly "
     "and D3D writes through a bad address: access violation, on the exact call "
     "the capture readback depends on."),

    # -------------------------------------------------------------- F-42 ----
    (SDKLAYERS,
     '        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnSeverity", [' + NL +
     "            D3D11_MESSAGE_SEVERITY, # _In_ D3D11_MESSAGE_SEVERITY Severity" + NL +
     "            wintypes.BOOL,          # _In_ BOOL bEnable" + NL +
     "            ])," + NL +
     NL +
     "    ]",
     '        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnSeverity", [' + NL +
     "            D3D11_MESSAGE_SEVERITY, # _In_ D3D11_MESSAGE_SEVERITY Severity" + NL +
     "            wintypes.BOOL,          # _In_ BOOL bEnable" + NL +
     "            ])," + NL +
     '        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnID", [' + NL +
     "            D3D11_MESSAGE_ID,       # _In_ D3D11_MESSAGE_ID ID" + NL +
     "            wintypes.BOOL,          # _In_ BOOL bEnable" + NL +
     "            ])," + NL +
     '        comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnCategory", [' + NL +
     "            D3D11_MESSAGE_CATEGORY, # _In_ D3D11_MESSAGE_CATEGORY Category" + NL +
     "            ])," + NL +
     '        comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnSeverity", [' + NL +
     "            D3D11_MESSAGE_SEVERITY, # _In_ D3D11_MESSAGE_SEVERITY Severity" + NL +
     "            ])," + NL +
     '        comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnID", [' + NL +
     "            D3D11_MESSAGE_ID,       # _In_ D3D11_MESSAGE_ID ID" + NL +
     "            ])," + NL +
     '        comtypes.STDMETHOD(None, "SetMuteDebugOutput", [' + NL +
     "            wintypes.BOOL,          # _In_ BOOL bMute" + NL +
     "            ])," + NL +
     '        comtypes.STDMETHOD(wintypes.BOOL, "GetMuteDebugOutput", []),' + NL +
     NL +
     "    ]",
     "F-42: append the six missing ID3D11InfoQueue methods, slots 29-34."),

    # -------------------------------------------------------------- F-55 ----
    (D3D11,
     "                ('StenilDepthFailOp', D3D11_STENCIL_OP),",
     "                ('StencilDepthFailOp', D3D11_STENCIL_OP),",
     "F-55: D3D11_DEPTH_STENCILOP_DESC.StenilDepthFailOp is missing a C. The "
     "offset is correct, so nothing has ever failed - but anyone setting "
     "StencilDepthFailOp from the documentation creates a new Python attribute "
     "and leaves the real field at zero."),

    # -------------------------------------------------------------- F-51 ----
    (DXGI,
     '        comtypes.STDMETHOD(comtypes.HRESULT, "SetMaximumFrameltency", [',
     '        comtypes.STDMETHOD(comtypes.HRESULT, "SetMaximumFrameLatency", [',
     "F-51: IDXGIDevice1::SetMaximumFrameltency is missing an A and an L."),

    (DXGI,
     '        comtypes.STDMETHOD(comtypes.HRESULT, "GetMaximumFrameltency", [',
     '        comtypes.STDMETHOD(comtypes.HRESULT, "GetMaximumFrameLatency", [',
     "F-51: the same typo on GetMaximumFrameltency."),

    # -------------------------------------------------------------- F-20 ----
    (D3D11,
     "                ('InstanceDataSetRate', wintypes.UINT),",
     "                ('InstanceDataStepRate', wintypes.UINT),",
     "F-20: D3D11_INPUT_ELEMENT_DESC.InstanceDataSetRate is InstanceDataStepRate "
     "in the SDK. The offset is right; only the name is wrong, which is why it "
     "has never failed."),

    (OUTPUTMGR,
     "        tmp[0].InstanceDataSetRate = 0",
     "        tmp[0].InstanceDataStepRate = 0",
     "F-20: caller, element 0."),

    (OUTPUTMGR,
     "        tmp[1].InstanceDataSetRate = 0",
     "        tmp[1].InstanceDataStepRate = 0",
     "F-20: caller, element 1."),
]

#: Plain token renames, applied everywhere they occur. Safe because each token is
#: unique to the defect and appears nowhere else.
RENAMES = [
    (D3D11, "D3D11_BING_FLAG", "D3D11_BIND_FLAG",
     "F-21: the enum type is D3D11_BIND_FLAG. Its members were already spelled "
     "correctly - only the type name carried the typo."),
]


def main():
    argv = sys.argv[1:]
    check_only = "--check" in argv
    root = ROOT
    if "--root" in argv:
        root = os.path.abspath(argv[argv.index("--root") + 1])

    changed, already, missing = [], [], []
    per_file = {}

    for path, old, new, why in EDITS:
        per_file.setdefault(path, {"edits": [], "renames": []})["edits"].append(
            (old, new, why))
    for path, old, new, why in RENAMES:
        per_file.setdefault(path, {"edits": [], "renames": []})["renames"].append(
            (old, new, why))

    for path, work in sorted(per_file.items()):
        full = os.path.join(root, path)
        if not os.path.isfile(full):
            missing.extend((path, why) for _o, _n, why in
                           work["edits"] + work["renames"])
            continue
        text = io.open(full, encoding="utf-8").read()
        original = text

        for old, new, why in work["edits"]:
            if old in text:
                text = text.replace(old, new, 1)
                changed.append((path, why))
            elif new in text:
                already.append((path, why))
            else:
                missing.append((path, why))

        for old, new, why in work["renames"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changed.append((path, "%s (%d occurrences)" % (why, count)))
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
        print("An anchor did not match. Re-check those sites by hand rather than "
              "loosening the anchors.")
        return 2
    if check_only and changed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
