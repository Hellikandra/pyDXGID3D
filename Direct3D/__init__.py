# -*- coding: utf-8 -*-
"""Python bindings for DXGI and Direct3D, translated from the Windows SDK.

Two layers, and most callers only need the first.

    Direct3D.Capture    the desktop capture API - three names, documented
    Direct3D.PyIdl      the raw interface definitions, one module per .idl

Capturing the screen
--------------------

    from Direct3D.Capture import enumerate_outputs, CaptureOptions, DesktopCapture

    for output in enumerate_outputs():
        print(output)

    with DesktopCapture(CaptureOptions(output=0)) as capture:
        for frame in capture:
            process(frame.array)        # zero copy, valid this iteration only

Reaching past those three names into `Direct3D.PyIdl` for something the capture
API ought to do is worth reporting rather than working around.

Calling the API directly
------------------------

Every DLL entry point is in `Direct3D.PyIdl.functions`, with explicit argtypes
and a return type, and every failure raised as a named exception from
`Direct3D.PyIdl.status`:

    from Direct3D.PyIdl.functions import CreateDXGIFactory1, D3D11CreateDevice

Do NOT reach for `ctypes.windll.dxgi.CreateDXGIFactory` instead. An undeclared
call defaults its return type to a 32-bit int, which truncates every handle it
gives back on a 64-bit build - a defect that produces plausible-looking garbage
rather than an error. That is the reason `functions` exists.

What is covered
---------------

Measured against the .idl files in Windows SDK 10.0.26100.0: 251 of 251
interfaces and 1,043 of 1,043 methods, across DXGI 1.0-1.6, Direct3D 11.0-11.4,
Direct3D 12 with its video and debug layers, and the two interop headers. 649
structures match a compiled measurement of the SDK headers for total size and
for the offset of every field.

DXGI and Direct3D 11 are exercised: the capture API drives them against real
hardware and the test suite renders a known colour and reads it back. Direct3D
12 is correctly declared and lightly exercised - a device, queues, heaps and a
root signature have been created through it, and nothing here renders with it.

See README.md for the rest, and `python tools/exercise.py` for how much of the
surface has actually been called.
"""
