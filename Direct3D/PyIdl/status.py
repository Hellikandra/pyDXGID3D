# -*- coding: utf-8 -*-
"""DXGI and Direct3D HRESULT codes, and the exception hierarchy built on them.

Auto-generated from the Windows SDK by tools/gen_status.py - do not edit by hand.

Source SDK : 10.0.26100.0
Codes read : 51 from shared/winerror.h, plus 12 generic COM codes

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


def MAKE_HRESULT(severity, facility, code):
    """The Windows macro of the same name, which no .idl declares.

    d3d11.idl builds its own status codes out of it:

        cpp_quote( "#define MAKE_D3D11_HRESULT( code )  MAKE_HRESULT( 1, _FACD3D11, code )" )

    winerror.h defines it and the IDLs assume it, the same way they assume LUID
    and SECURITY_ATTRIBUTES. It lives here rather than in typemap.py because it
    constructs an HRESULT, which is what this module is for.
    """
    return _hr((severity << 31) | (facility << 16) | code)


def MAKE_STATUS(facility, code):
    """MAKE_HRESULT with severity 0 - a success code rather than a failure."""
    return MAKE_HRESULT(0, facility, code)


def succeeded(hr):
    """True if the HRESULT indicates success. Note S_FALSE and the DXGI_STATUS_*
    codes are successes, so testing `hr == 0` is not the same thing."""
    return _hr(hr) < 0x80000000


def failed(hr):
    return _hr(hr) >= 0x80000000


# ------------------------------------------------------- generic COM ----
S_OK                               = 0x00000000
S_FALSE                            = 0x00000001
E_UNEXPECTED                       = 0x8000FFFF
E_NOTIMPL                          = 0x80004001
E_OUTOFMEMORY                      = 0x8007000E
E_INVALIDARG                       = 0x80070057
E_NOINTERFACE                      = 0x80004002
E_POINTER                          = 0x80004003
E_HANDLE                           = 0x80070006
E_ABORT                            = 0x80004004
E_FAIL                             = 0x80004005
E_ACCESSDENIED                     = 0x80070005


# ------------------------- DXGI success codes - these are NOT failures
DXGI_STATUS_OCCLUDED                       = 0x087A0001
DXGI_STATUS_CLIPPED                        = 0x087A0002
DXGI_STATUS_NO_REDIRECTION                 = 0x087A0004
DXGI_STATUS_NO_DESKTOP_ACCESS              = 0x087A0005
DXGI_STATUS_GRAPHICS_VIDPN_SOURCE_IN_USE   = 0x087A0006
DXGI_STATUS_MODE_CHANGED                   = 0x087A0007
DXGI_STATUS_MODE_CHANGE_IN_PROGRESS        = 0x087A0008
DXGI_STATUS_UNOCCLUDED                     = 0x087A0009
DXGI_STATUS_DDA_WAS_STILL_DRAWING          = 0x087A000A
DXGI_STATUS_PRESENT_REQUIRED               = 0x087A002F


# ---------------------------------------------------- DXGI error codes
DXGI_ERROR_INVALID_CALL                    = 0x887A0001
DXGI_ERROR_NOT_FOUND                       = 0x887A0002
DXGI_ERROR_MORE_DATA                       = 0x887A0003
DXGI_ERROR_UNSUPPORTED                     = 0x887A0004
DXGI_ERROR_DEVICE_REMOVED                  = 0x887A0005
DXGI_ERROR_DEVICE_HUNG                     = 0x887A0006
DXGI_ERROR_DEVICE_RESET                    = 0x887A0007
DXGI_ERROR_WAS_STILL_DRAWING               = 0x887A000A
DXGI_ERROR_FRAME_STATISTICS_DISJOINT       = 0x887A000B
DXGI_ERROR_GRAPHICS_VIDPN_SOURCE_IN_USE    = 0x887A000C
DXGI_ERROR_DRIVER_INTERNAL_ERROR           = 0x887A0020
DXGI_ERROR_NONEXCLUSIVE                    = 0x887A0021
DXGI_ERROR_NOT_CURRENTLY_AVAILABLE         = 0x887A0022
DXGI_ERROR_REMOTE_CLIENT_DISCONNECTED      = 0x887A0023
DXGI_ERROR_REMOTE_OUTOFMEMORY              = 0x887A0024
DXGI_ERROR_MODE_CHANGE_IN_PROGRESS         = 0x887A0025
DXGI_ERROR_ACCESS_LOST                     = 0x887A0026
DXGI_ERROR_WAIT_TIMEOUT                    = 0x887A0027
DXGI_ERROR_SESSION_DISCONNECTED            = 0x887A0028
DXGI_ERROR_RESTRICT_TO_OUTPUT_STALE        = 0x887A0029
DXGI_ERROR_CANNOT_PROTECT_CONTENT          = 0x887A002A
DXGI_ERROR_ACCESS_DENIED                   = 0x887A002B
DXGI_ERROR_NAME_ALREADY_EXISTS             = 0x887A002C
DXGI_ERROR_SDK_COMPONENT_MISSING           = 0x887A002D
DXGI_ERROR_NOT_CURRENT                     = 0x887A002E
DXGI_ERROR_HW_PROTECTION_OUTOFMEMORY       = 0x887A0030
DXGI_ERROR_DYNAMIC_CODE_POLICY_VIOLATION   = 0x887A0031
DXGI_ERROR_NON_COMPOSITED_UI               = 0x887A0032
DXGI_ERROR_CACHE_CORRUPT                   = 0x887A0033
DXGI_ERROR_CACHE_FULL                      = 0x887A0034
DXGI_ERROR_CACHE_HASH_COLLISION            = 0x887A0035
DXGI_ERROR_ALREADY_EXISTS                  = 0x887A0036
DXGI_ERROR_MPO_UNPINNED                    = 0x887A0064
DXGI_ERROR_SETDISPLAYMODE_REQUIRED         = 0x887A0065


# --------------------------------------------- Direct3D 11 error codes
D3D11_ERROR_TOO_MANY_UNIQUE_STATE_OBJECTS  = 0x887C0001
D3D11_ERROR_FILE_NOT_FOUND                 = 0x887C0002
D3D11_ERROR_TOO_MANY_UNIQUE_VIEW_OBJECTS   = 0x887C0003
D3D11_ERROR_DEFERRED_CONTEXT_MAP_WITHOUT_INITIAL_DISCARD = 0x887C0004


# --------------------------------------------- Direct3D 12 error codes
D3D12_ERROR_ADAPTER_NOT_FOUND              = 0x887E0001
D3D12_ERROR_DRIVER_VERSION_MISMATCH        = 0x887E0002
D3D12_ERROR_INVALID_REDIST                 = 0x887E0003


# ------------------------------------------------------------- table ----
#: Every code this module defines, name -> value.
_ALL = {
    "S_OK"                                    : S_OK,
    "S_FALSE"                                 : S_FALSE,
    "E_UNEXPECTED"                            : E_UNEXPECTED,
    "E_NOTIMPL"                               : E_NOTIMPL,
    "E_OUTOFMEMORY"                           : E_OUTOFMEMORY,
    "E_INVALIDARG"                            : E_INVALIDARG,
    "E_NOINTERFACE"                           : E_NOINTERFACE,
    "E_POINTER"                               : E_POINTER,
    "E_HANDLE"                                : E_HANDLE,
    "E_ABORT"                                 : E_ABORT,
    "E_FAIL"                                  : E_FAIL,
    "E_ACCESSDENIED"                          : E_ACCESSDENIED,
    "DXGI_STATUS_OCCLUDED"                    : DXGI_STATUS_OCCLUDED,
    "DXGI_STATUS_CLIPPED"                     : DXGI_STATUS_CLIPPED,
    "DXGI_STATUS_NO_REDIRECTION"              : DXGI_STATUS_NO_REDIRECTION,
    "DXGI_STATUS_NO_DESKTOP_ACCESS"           : DXGI_STATUS_NO_DESKTOP_ACCESS,
    "DXGI_STATUS_GRAPHICS_VIDPN_SOURCE_IN_USE": DXGI_STATUS_GRAPHICS_VIDPN_SOURCE_IN_USE,
    "DXGI_STATUS_MODE_CHANGED"                : DXGI_STATUS_MODE_CHANGED,
    "DXGI_STATUS_MODE_CHANGE_IN_PROGRESS"     : DXGI_STATUS_MODE_CHANGE_IN_PROGRESS,
    "DXGI_STATUS_UNOCCLUDED"                  : DXGI_STATUS_UNOCCLUDED,
    "DXGI_STATUS_DDA_WAS_STILL_DRAWING"       : DXGI_STATUS_DDA_WAS_STILL_DRAWING,
    "DXGI_STATUS_PRESENT_REQUIRED"            : DXGI_STATUS_PRESENT_REQUIRED,
    "DXGI_ERROR_INVALID_CALL"                 : DXGI_ERROR_INVALID_CALL,
    "DXGI_ERROR_NOT_FOUND"                    : DXGI_ERROR_NOT_FOUND,
    "DXGI_ERROR_MORE_DATA"                    : DXGI_ERROR_MORE_DATA,
    "DXGI_ERROR_UNSUPPORTED"                  : DXGI_ERROR_UNSUPPORTED,
    "DXGI_ERROR_DEVICE_REMOVED"               : DXGI_ERROR_DEVICE_REMOVED,
    "DXGI_ERROR_DEVICE_HUNG"                  : DXGI_ERROR_DEVICE_HUNG,
    "DXGI_ERROR_DEVICE_RESET"                 : DXGI_ERROR_DEVICE_RESET,
    "DXGI_ERROR_WAS_STILL_DRAWING"            : DXGI_ERROR_WAS_STILL_DRAWING,
    "DXGI_ERROR_FRAME_STATISTICS_DISJOINT"    : DXGI_ERROR_FRAME_STATISTICS_DISJOINT,
    "DXGI_ERROR_GRAPHICS_VIDPN_SOURCE_IN_USE" : DXGI_ERROR_GRAPHICS_VIDPN_SOURCE_IN_USE,
    "DXGI_ERROR_DRIVER_INTERNAL_ERROR"        : DXGI_ERROR_DRIVER_INTERNAL_ERROR,
    "DXGI_ERROR_NONEXCLUSIVE"                 : DXGI_ERROR_NONEXCLUSIVE,
    "DXGI_ERROR_NOT_CURRENTLY_AVAILABLE"      : DXGI_ERROR_NOT_CURRENTLY_AVAILABLE,
    "DXGI_ERROR_REMOTE_CLIENT_DISCONNECTED"   : DXGI_ERROR_REMOTE_CLIENT_DISCONNECTED,
    "DXGI_ERROR_REMOTE_OUTOFMEMORY"           : DXGI_ERROR_REMOTE_OUTOFMEMORY,
    "DXGI_ERROR_MODE_CHANGE_IN_PROGRESS"      : DXGI_ERROR_MODE_CHANGE_IN_PROGRESS,
    "DXGI_ERROR_ACCESS_LOST"                  : DXGI_ERROR_ACCESS_LOST,
    "DXGI_ERROR_WAIT_TIMEOUT"                 : DXGI_ERROR_WAIT_TIMEOUT,
    "DXGI_ERROR_SESSION_DISCONNECTED"         : DXGI_ERROR_SESSION_DISCONNECTED,
    "DXGI_ERROR_RESTRICT_TO_OUTPUT_STALE"     : DXGI_ERROR_RESTRICT_TO_OUTPUT_STALE,
    "DXGI_ERROR_CANNOT_PROTECT_CONTENT"       : DXGI_ERROR_CANNOT_PROTECT_CONTENT,
    "DXGI_ERROR_ACCESS_DENIED"                : DXGI_ERROR_ACCESS_DENIED,
    "DXGI_ERROR_NAME_ALREADY_EXISTS"          : DXGI_ERROR_NAME_ALREADY_EXISTS,
    "DXGI_ERROR_SDK_COMPONENT_MISSING"        : DXGI_ERROR_SDK_COMPONENT_MISSING,
    "DXGI_ERROR_NOT_CURRENT"                  : DXGI_ERROR_NOT_CURRENT,
    "DXGI_ERROR_HW_PROTECTION_OUTOFMEMORY"    : DXGI_ERROR_HW_PROTECTION_OUTOFMEMORY,
    "DXGI_ERROR_DYNAMIC_CODE_POLICY_VIOLATION": DXGI_ERROR_DYNAMIC_CODE_POLICY_VIOLATION,
    "DXGI_ERROR_NON_COMPOSITED_UI"            : DXGI_ERROR_NON_COMPOSITED_UI,
    "DXGI_ERROR_CACHE_CORRUPT"                : DXGI_ERROR_CACHE_CORRUPT,
    "DXGI_ERROR_CACHE_FULL"                   : DXGI_ERROR_CACHE_FULL,
    "DXGI_ERROR_CACHE_HASH_COLLISION"         : DXGI_ERROR_CACHE_HASH_COLLISION,
    "DXGI_ERROR_ALREADY_EXISTS"               : DXGI_ERROR_ALREADY_EXISTS,
    "DXGI_ERROR_MPO_UNPINNED"                 : DXGI_ERROR_MPO_UNPINNED,
    "DXGI_ERROR_SETDISPLAYMODE_REQUIRED"      : DXGI_ERROR_SETDISPLAYMODE_REQUIRED,
    "D3D11_ERROR_TOO_MANY_UNIQUE_STATE_OBJECTS": D3D11_ERROR_TOO_MANY_UNIQUE_STATE_OBJECTS,
    "D3D11_ERROR_FILE_NOT_FOUND"              : D3D11_ERROR_FILE_NOT_FOUND,
    "D3D11_ERROR_TOO_MANY_UNIQUE_VIEW_OBJECTS": D3D11_ERROR_TOO_MANY_UNIQUE_VIEW_OBJECTS,
    "D3D11_ERROR_DEFERRED_CONTEXT_MAP_WITHOUT_INITIAL_DISCARD": D3D11_ERROR_DEFERRED_CONTEXT_MAP_WITHOUT_INITIAL_DISCARD,
    "D3D12_ERROR_ADAPTER_NOT_FOUND"           : D3D12_ERROR_ADAPTER_NOT_FOUND,
    "D3D12_ERROR_DRIVER_VERSION_MISMATCH"     : D3D12_ERROR_DRIVER_VERSION_MISMATCH,
    "D3D12_ERROR_INVALID_REDIST"              : D3D12_ERROR_INVALID_REDIST,
}


# ---------------------------------------------------------------- lookup ----
#: HRESULT -> symbolic name, for messages and logging.
NAMES = {_hr(v): k for k, v in sorted(_ALL.items(), key=lambda kv: kv[0])}


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


class WaitTimeout(DXGIError):
    """AcquireNextFrame timed out. Routine - the desktop simply did not change."""


class AccessLost(DXGIError):
    """The duplication object is invalid. Routine: alt-tab, a mode change, the
    secure desktop, or a driver reset. Recover by rebuilding the chain."""


class DeviceRemoved(DXGIError):
    """The GPU was physically removed or the driver was reset. Fatal - the device
    and everything created from it must be recreated."""


class DeviceHung(DXGIError):
    """The application submitted invalid work and the device hung. Fatal."""


class DeviceReset(DXGIError):
    """The device failed for a reason unrelated to this application. Fatal."""


class Unsupported(DXGIError):
    """The requested functionality is not supported by the device or driver."""


class NotFound(DXGIError):
    """The requested item was not found. EnumOutputs and EnumAdapters return this
    to signal the end of enumeration - it is a terminator, not a failure."""


class MoreData(DXGIError):
    """The supplied buffer was too small."""


class InvalidCall(DXGIError):
    """The method was called with invalid parameters. A bug in the caller."""


class AccessDenied(DXGIError):
    """Insufficient privilege, or another process holds exclusive access."""


class SessionDisconnected(DXGIError):
    """The session was disconnected - the workstation locked, or RDP detached."""


class NotCurrentlyAvailable(DXGIError):
    """The resource is not available right now. Usually worth retrying."""


#: HRESULT -> exception class, consulted by check().
_EXCEPTION_MAP = {
    DXGI_ERROR_WAIT_TIMEOUT                   : WaitTimeout,
    DXGI_ERROR_ACCESS_LOST                    : AccessLost,
    DXGI_ERROR_DEVICE_REMOVED                 : DeviceRemoved,
    DXGI_ERROR_DEVICE_HUNG                    : DeviceHung,
    DXGI_ERROR_DEVICE_RESET                   : DeviceReset,
    DXGI_ERROR_UNSUPPORTED                    : Unsupported,
    DXGI_ERROR_NOT_FOUND                      : NotFound,
    DXGI_ERROR_MORE_DATA                      : MoreData,
    DXGI_ERROR_INVALID_CALL                   : InvalidCall,
    DXGI_ERROR_ACCESS_DENIED                  : AccessDenied,
    DXGI_ERROR_SESSION_DISCONNECTED           : SessionDisconnected,
    DXGI_ERROR_NOT_CURRENTLY_AVAILABLE        : NotCurrentlyAvailable,
}


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
