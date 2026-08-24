# -*- coding: utf-8 -*-
"""Generate Direct3D/PyIdl/status.py from the Windows SDK winerror.h.

Every HRESULT value is read from the SDK rather than typed from memory. Run this
whenever the target SDK changes; the output is committed and reviewed like any
other binding module.

Usage:  python tools/gen_status.py [output_path]
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))

DEFAULT_OUTPUT = os.path.join(ROOT, "Direct3D", "PyIdl", "status.py")


def find_sdk():
    """Newest Windows SDK Include directory, or None.

    WINSDK_INCLUDE overrides, for a machine with several kits installed.
    """
    env = os.environ.get("WINSDK_INCLUDE")
    if env and os.path.isdir(env):
        return env
    roots = [r"C:\Program Files (x86)\Windows Kits\10\Include",
             r"C:\Program Files\Windows Kits\10\Include"]
    best = None
    for root in roots:
        if not os.path.isdir(root):
            continue
        for version in sorted(os.listdir(root)):
            candidate = os.path.join(root, version)
            if os.path.isfile(os.path.join(candidate, "shared", "winerror.h")):
                best = candidate
    return best

HRESULT_RE = re.compile(
    r"#define\s+((?:DXGI_ERROR|DXGI_STATUS|D3D11_ERROR|D3D12_ERROR)_[A-Z0-9_]+)\s+"
    r"_HRESULT_TYPEDEF_\(\s*0x([0-9A-Fa-f]+)L?\s*\)")

# Generic COM codes the bindings need but winerror.h spells differently.
GENERIC = [
    ("S_OK", 0x00000000), ("S_FALSE", 0x00000001),
    ("E_UNEXPECTED", 0x8000FFFF), ("E_NOTIMPL", 0x80004001),
    ("E_OUTOFMEMORY", 0x8007000E), ("E_INVALIDARG", 0x80070057),
    ("E_NOINTERFACE", 0x80004002), ("E_POINTER", 0x80004003),
    ("E_HANDLE", 0x80070006), ("E_ABORT", 0x80004004),
    ("E_FAIL", 0x80004005), ("E_ACCESSDENIED", 0x80070005),
]

# code -> (exception class, docstring). Everything else becomes DXGIError.
EXCEPTIONS = [
    ("WaitTimeout",     "DXGI_ERROR_WAIT_TIMEOUT",
     "AcquireNextFrame timed out. Routine - the desktop simply did not change."),
    ("AccessLost",      "DXGI_ERROR_ACCESS_LOST",
     "The duplication object is invalid. Routine: alt-tab, a mode change, the\n"
     "    secure desktop, or a driver reset. Recover by rebuilding the chain."),
    ("DeviceRemoved",   "DXGI_ERROR_DEVICE_REMOVED",
     "The GPU was physically removed or the driver was reset. Fatal - the device\n"
     "    and everything created from it must be recreated."),
    ("DeviceHung",      "DXGI_ERROR_DEVICE_HUNG",
     "The application submitted invalid work and the device hung. Fatal."),
    ("DeviceReset",     "DXGI_ERROR_DEVICE_RESET",
     "The device failed for a reason unrelated to this application. Fatal."),
    ("Unsupported",     "DXGI_ERROR_UNSUPPORTED",
     "The requested functionality is not supported by the device or driver."),
    ("NotFound",        "DXGI_ERROR_NOT_FOUND",
     "The requested item was not found. EnumOutputs and EnumAdapters return this\n"
     "    to signal the end of enumeration - it is a terminator, not a failure."),
    ("MoreData",        "DXGI_ERROR_MORE_DATA",
     "The supplied buffer was too small."),
    ("InvalidCall",     "DXGI_ERROR_INVALID_CALL",
     "The method was called with invalid parameters. A bug in the caller."),
    ("AccessDenied",    "DXGI_ERROR_ACCESS_DENIED",
     "Insufficient privilege, or another process holds exclusive access."),
    ("SessionDisconnected", "DXGI_ERROR_SESSION_DISCONNECTED",
     "The session was disconnected - the workstation locked, or RDP detached."),
    ("NotCurrentlyAvailable", "DXGI_ERROR_NOT_CURRENTLY_AVAILABLE",
     "The resource is not available right now. Usually worth retrying."),
]

HEADER = '''# -*- coding: utf-8 -*-
"""DXGI and Direct3D HRESULT codes, and the exception hierarchy built on them.

Auto-generated from the Windows SDK by tools/gen_status.py - do not edit by hand.

Source SDK : {sdk}
Codes read : {count} from shared/winerror.h, plus {generic} generic COM codes

Why this module exists
----------------------
An HRESULT is not merely "an error". DXGI uses it to say what the caller should
*do*: DXGI_ERROR_WAIT_TIMEOUT means try again, DXGI_ERROR_ACCESS_LOST means tear
down and rebuild, DXGI_ERROR_DEVICE_REMOVED means give up. Collapsing those into
a single failure path - or into a printed string - throws away the only
information that makes recovery possible.

Usage
-----
    from Direct3D.PyIdl.status import check, AccessLost, WaitTimeout

    try:
        check(hr)
    except WaitTimeout:
        continue                      # nothing changed on the desktop
    except AccessLost:
        self.rebuild()                # routine, not exceptional
"""
import ctypes


def _hr(value):
    """Normalise an HRESULT to unsigned 32-bit.

    ctypes hands back HRESULTs as signed c_long, so 0x887A0027 arrives as
    -2005270489. Comparisons must happen in one representation; this module
    uses unsigned throughout.
    """
    return value & 0xFFFFFFFF


def succeeded(hr):
    """True if the HRESULT indicates success. Note S_FALSE and the DXGI_STATUS_*
    codes are successes, so testing `hr == 0` is not the same thing."""
    return _hr(hr) < 0x80000000


def failed(hr):
    return _hr(hr) >= 0x80000000


'''

FOOTER = '''

# ---------------------------------------------------------------- lookup ----
#: HRESULT -> symbolic name, for messages and logging.
NAMES = {{_hr(v): k for k, v in sorted(_ALL.items(), key=lambda kv: kv[0])}}


def name_of(hr):
    """Symbolic name for an HRESULT, or its hex form if unknown."""
    return NAMES.get(_hr(hr), "0x%08X" % _hr(hr))


# ------------------------------------------------------------ exceptions ----
class DXGIError(OSError):
    """Base for every DXGI / Direct3D failure.

    Carries the raw HRESULT so callers can inspect a code this module does not
    model, rather than being limited to the subclasses below.
    """

    hresult = None

    def __init__(self, hr, context=None):
        self.hresult = _hr(hr)
        self.name = name_of(hr)
        message = "%s (0x%08X)" % (self.name, self.hresult)
        if context:
            message = "%s: %s" % (context, message)
        super(DXGIError, self).__init__(message)


{exception_classes}

#: HRESULT -> exception class, consulted by check().
_EXCEPTION_MAP = {{
{exception_map}
}}


def check(hr, context=None):
    """Raise the mapped exception if `hr` is a failure; otherwise return it.

    Success codes - including S_FALSE and every DXGI_STATUS_* - are returned
    unchanged so the caller can act on them.
    """
    if succeeded(hr):
        return _hr(hr)
    raise _EXCEPTION_MAP.get(_hr(hr), DXGIError)(hr, context)


def raise_for(hr, context=None):
    """Alias for check(), for call sites where the intent reads better."""
    return check(hr, context)
'''


def main():
    sdk = find_sdk()
    if not sdk:
        print("No Windows SDK found.")
        return 1
    path = os.path.join(sdk, "shared", "winerror.h")
    text = io.open(path, encoding="utf-8", errors="replace").read()

    found = []
    seen = set()
    for m in HRESULT_RE.finditer(text):
        name, val = m.group(1), int(m.group(2), 16)
        if name in seen:
            continue
        seen.add(name)
        found.append((name, val))
    found.sort(key=lambda kv: kv[1])

    groups = {"DXGI_STATUS": [], "DXGI_ERROR": [], "D3D11_ERROR": [], "D3D12_ERROR": []}
    for name, val in found:
        for g in groups:
            if name.startswith(g + "_"):
                groups[g].append((name, val))
                break

    out = [HEADER.format(sdk=os.path.basename(sdk), count=len(found), generic=len(GENERIC))]

    out.append("# ------------------------------------------------------- generic COM ----\n")
    for name, val in GENERIC:
        out.append("%-34s = 0x%08X\n" % (name, val))

    titles = {
        "DXGI_STATUS": "DXGI success codes - these are NOT failures",
        "DXGI_ERROR": "DXGI error codes",
        "D3D11_ERROR": "Direct3D 11 error codes",
        "D3D12_ERROR": "Direct3D 12 error codes",
    }
    for g in ("DXGI_STATUS", "DXGI_ERROR", "D3D11_ERROR", "D3D12_ERROR"):
        if not groups[g]:
            continue
        out.append("\n\n# %s %s\n" % ("-" * (68 - len(titles[g])), titles[g]))
        for name, val in groups[g]:
            out.append("%-42s = 0x%08X\n" % (name, val))

    out.append("\n\n# ------------------------------------------------------------- table ----\n")
    out.append("#: Every code this module defines, name -> value.\n_ALL = {\n")
    for name, _ in GENERIC:
        out.append("    %-42s: %s,\n" % ('"%s"' % name, name))
    for g in ("DXGI_STATUS", "DXGI_ERROR", "D3D11_ERROR", "D3D12_ERROR"):
        for name, _ in groups[g]:
            out.append("    %-42s: %s,\n" % ('"%s"' % name, name))
    out.append("}\n")

    known = {n for n, _ in found}
    classes, mapping = [], []
    for cls, code, doc in EXCEPTIONS:
        if code not in known:
            print("  WARNING: %s not in this SDK; skipping %s" % (code, cls))
            continue
        classes.append('class %s(DXGIError):\n    """%s"""\n' % (cls, doc))
        mapping.append("    %-42s: %s," % (code, cls))

    out.append(FOOTER.format(exception_classes="\n\n".join(classes),
                             exception_map="\n".join(mapping)))

    dst = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT
    io.open(dst, "w", encoding="utf-8", newline="\n").write("".join(out))
    print("wrote %s" % dst)
    print("  %d SDK codes + %d generic, %d exception classes"
          % (len(found), len(GENERIC), len(classes)))
    for g in groups:
        if groups[g]:
            print("    %-12s %d" % (g, len(groups[g])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
