#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Import smoke test for the pyDXGID3D bindings.


Imports every binding module in dependency order and reports how many COM
classes each one registered. Importing is not a formality here: comtypes builds
each interface's vtable at class-creation time, so a malformed _methods_ list
fails on import rather than at first call.

Requires Windows and comtypes. No GPU, no display.
"""
import importlib
import sys

MODULES = [
    "Direct3D.PyIdl.dxgicommon",
    "Direct3D.PyIdl.dxgiformat",
    "Direct3D.PyIdl.dxgitype",
    "Direct3D.PyIdl.dxgi",
    "Direct3D.PyIdl.dxgi1_2",
    "Direct3D.PyIdl.dxgidebug",
    "Direct3D.PyIdl.d3dcommon",
    "Direct3D.PyIdl.d3d11",
    "Direct3D.PyIdl.d3d11_1",
    "Direct3D.PyIdl.d3d11_2",
    "Direct3D.PyIdl.d3d11_3",
    "Direct3D.PyIdl.d3d11_4",
    "Direct3D.PyIdl.d3d11sdklayers",
]


def main():
    failures, total_ifaces = [], 0

    for name in MODULES:
        try:
            mod = importlib.import_module(name)
        except Exception as exc:                      # noqa: BLE001 - report, do not mask
            failures.append((name, "%s: %s" % (type(exc).__name__, exc)))
            print("FAIL %-34s %s: %s" % (name, type(exc).__name__, exc))
            continue

        ifaces = [v for v in vars(mod).values()
                  if isinstance(v, type) and hasattr(v, "_iid_")
                  and getattr(v, "__module__", None) == name]
        total_ifaces += len(ifaces)
        print("ok   %-34s %3d interfaces" % (name, len(ifaces)))

    print("-" * 60)
    print("%d/%d modules imported, %d interfaces registered"
          % (len(MODULES) - len(failures), len(MODULES), total_ifaces))

    if failures:
        print("\n%d module(s) failed to import:" % len(failures))
        for name, err in failures:
            print("  %s -> %s" % (name, err))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
