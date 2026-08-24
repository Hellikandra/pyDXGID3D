# -*- coding: utf-8 -*-
"""Shared fixtures and tier gating.

Tier 0  static checks   - any OS, no comtypes, no GPU
Tier 1  binding checks  - Windows + comtypes; WARP suffices, no GPU
Tier 2  capture checks  - real GPU and an interactive desktop session
Tier 3  performance     - as tier 2, plus a quiet machine

Tiers 1 and above skip themselves rather than failing when their prerequisites
are absent, so a single `pytest` run is meaningful on any machine.
"""
import os
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

ON_WINDOWS = sys.platform == "win32"

try:
    import comtypes  # noqa: F401
    HAVE_COMTYPES = True
except ImportError:
    HAVE_COMTYPES = False


needs_windows = pytest.mark.skipif(
    not ON_WINDOWS,
    reason="Windows only - these bindings call into dxgi.dll / d3d11.dll")
needs_comtypes = pytest.mark.skipif(
    not HAVE_COMTYPES, reason="comtypes is not installed")


@pytest.fixture(scope="session")
def sdk_include():
    """Path to the Windows SDK Include directory, or skip.

    Honours WINSDK_INCLUDE so a machine with several kits can pin one.
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
            if os.path.isfile(os.path.join(candidate, "shared", "dxgi.idl")):
                best = candidate
    if not best:
        pytest.skip("no Windows SDK Include directory found")
    return best


@pytest.fixture(scope="session")
def warp_device():
    """A WARP Direct3D 11 device, or skip.

    Session-scoped because device creation is the expensive part of tier 1.
    WARP is the software rasteriser, so this works on a hosted CI runner with no
    GPU at all.
    """
    if not (ON_WINDOWS and HAVE_COMTYPES):
        pytest.skip("needs Windows and comtypes")
    from Direct3D.PyIdl.functions import D3D11CreateDevice
    from Direct3D.PyIdl.d3dcommon import D3D_DRIVER_TYPE_WARP

    device, level, context = D3D11CreateDevice(driver_type=D3D_DRIVER_TYPE_WARP)
    yield device, level, context
    for obj in (context, device):
        if obj:
            obj.Release()
