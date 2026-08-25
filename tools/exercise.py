# -*- coding: utf-8 -*-
"""Call as much of the API as can be called safely, and report what happened.

The test suite proves the DECLARATIONS match the SDK - vtable order, IIDs,
structure sizes, field offsets, parameter counts, return types. All of that is
static. Before this tool ran, roughly 28 of the 1,043 declared methods had ever
been executed.

That gap is where F-58 and F-59 lived. Both were wrong return types, both
invisible to every static check, and both found by calling a method rather than
reading it. There is no reason to think they were the last two.

So: build real objects, then call every method that can be called without
changing anything, and report per interface how many worked.

    python tools/exercise.py                 everything available here
    python tools/exercise.py --verbose       name every method and its result
    python tools/exercise.py --interface ID3D12Device

Safety
------
Only methods whose name begins with Get, Check, Is, Has, Query, Enum or Test are
called - the interrogative mood. Nothing that creates, destroys, maps, draws,
signals or sets is touched, so a run leaves no state behind.

Every out-parameter is zeroed storage the tool owns. A method whose parameters
cannot be satisfied that way is SKIPPED and counted, not guessed at.

The method name is printed BEFORE the call and the stream flushed, so if a call
takes the interpreter down the last line of output names the method that did it.
That is not hypothetical - it is exactly what a mis-declared return type does.
"""
import ctypes
import sys
import traceback

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

import comtypes                                              # noqa: E402

#: The interrogative mood. A method outside these prefixes may have side
#: effects, so it is never called.
SAFE_PREFIXES = ("Get", "Check", "Is", "Has", "Query", "Enum", "Test")

#: Even in the interrogative mood these are not safe to call blind.
#:
#: AcquireNextFrame blocks for its timeout and takes a frame the caller must
#: release. QueryInterface with zeroed storage asks for the null IID. GetDevice
#: and friends are fine; these are not.
NEVER = {
    "QueryInterface",           # a zeroed GUID is not an interface
    "AddRef", "Release",        # refcount surgery, and F-52
    "AcquireNextFrame",         # blocks, and leaves a frame held
    "GetFrameDirtyRects",       # needs a sized buffer from a held frame
    "GetFrameMoveRects",
    "GetFramePointerShape",
    "GetDisplaySurfaceData",    # needs a surface of the right size
    "GetData",                  # ID3D11DeviceContext: needs a live query
    "GetMessage",               # info queue: needs an index and a sized buffer
    "GetMessageA", "GetMessageW",
    "EnumWarningsWithSeverity",
    "GetPrivateData",           # needs a GUID and a sized buffer
    "GetWindowAssociation",     # returns an HWND into caller storage; harmless
                                # but noisy on a factory with none
}


class Result(object):
    """What happened to one interface."""

    def __init__(self, name):
        self.name = name
        self.ok = []
        self.failed = []
        self.skipped = []
        self.crashed = None

    @property
    def attempted(self):
        return len(self.ok) + len(self.failed)

    @property
    def total(self):
        return self.attempted + len(self.skipped)


def _storage_for(argtype):
    """Zeroed storage for one parameter, or None if it cannot be satisfied.

    Only two shapes are safe to invent: a pointer, which becomes storage the
    tool owns, and a plain integer, which becomes 0. Anything else - a structure
    by value, a GUID that must name something real - is a guess, and a guess is
    how a tool like this corrupts memory instead of measuring it.
    """
    if argtype is None:
        return None, False

    if getattr(argtype, "__name__", "").startswith("LP_") \
            or getattr(argtype, "__name__", "").startswith("POINTER("):
        inner = getattr(argtype, "_type_", None)
        if not isinstance(inner, type):
            inner = getattr(argtype, "__com_interface__", None)
        if not isinstance(inner, type):
            return None, False
        if inner is comtypes.GUID:
            return None, False                  # a zeroed IID names nothing
        if hasattr(inner, "_iid_"):
            # A pointer to a COM interface is an INPUT that must point at a real
            # object. Handing it freshly zeroed storage is how this tool caused
            # its own access violation in ID3D12Device::GetResourceTiling, which
            # dereferenced the "resource" it was given.
            return None, False
        try:
            return ctypes.byref(inner()), True
        except TypeError:
            return None, False

    if argtype is ctypes.c_void_p:
        return None, True                       # a null pointer is a valid "none"

    # c_char_p and c_wchar_p are _SimpleCData subclasses but they are POINTERS -
    # a caller-provided buffer, usually with a length parameter beside it. Zero
    # is not a valid one, and passing it is a TypeError at best.
    if argtype in (ctypes.c_char_p, ctypes.c_wchar_p):
        return None, False

    # Everything else that is a simple ctypes type is an integer or a float, and
    # a generated enum is an integer by another name.
    if isinstance(argtype, type) and issubclass(argtype, ctypes._SimpleCData):
        return 0, True

    return None, False


def _all_methods(obj):
    """Every method on an interface pointer, inherited ones included.

    comtypes gives each class in the chain only its OWN _methods_, and the
    pointer type carries the interface on __com_interface__ rather than on
    _type_ - which is the string 'P'. So the whole vtable means walking the MRO
    from the base down, which also means IDXGIObject::GetParent is exercised on
    every DXGI object rather than only where it was declared.
    """
    seen, out = set(), []
    for klass in reversed(type(obj).__mro__):
        for spec in getattr(klass, "_methods_", []) or []:
            if spec.name in seen:
                continue
            seen.add(spec.name)
            out.append(spec)
    return out


def exercise(name, obj, verbose=False, only=None):
    """Call every safe method on one live object."""
    result = Result(name)
    if only and only != name:
        return result

    for spec in _all_methods(obj):
        method = spec.name
        if method in NEVER or not method.startswith(SAFE_PREFIXES):
            result.skipped.append((method, "not interrogative"))
            continue

        arguments, satisfied = [], True
        for argtype in (spec.argtypes or ()):
            value, ok = _storage_for(argtype)
            if not ok:
                satisfied = False
                break
            arguments.append(value)
        if not satisfied:
            result.skipped.append((method, "arguments cannot be invented"))
            continue

        # Named BEFORE the call, and flushed. If this faults, the last line of
        # output is the culprit.
        if verbose:
            sys.stdout.write("      %s.%s ... " % (name, method))
            sys.stdout.flush()
        result.crashed = "%s::%s" % (name, method)

        try:
            getattr(obj, method)(*arguments)
            result.ok.append(method)
            if verbose:
                print("ok")
        except comtypes.COMError as exc:
            # An HRESULT is an answer. The call reached the driver and came
            # back, which is what this tool is measuring.
            result.ok.append(method)
            if verbose:
                print("HRESULT 0x%08X" % (exc.hresult & 0xFFFFFFFF))
        except Exception as exc:
            result.failed.append((method, "%s: %s" % (type(exc).__name__, exc)))
            if verbose:
                print("FAILED %s: %s" % (type(exc).__name__, exc))
        result.crashed = None

    return result


def build():
    """Every live object this machine can produce, as (name, instance).

    Ordered so that a failure to build one does not prevent the rest: a machine
    with no D3D12 driver should still exercise DXGI and Direct3D 11.
    """
    from Direct3D.PyIdl.functions import CreateDXGIFactory1, D3D11CreateDevice
    from Direct3D.PyIdl.d3dcommon import D3D_DRIVER_TYPE_UNKNOWN
    from Direct3D.PyIdl.dxgi import (
        IDXGIAdapter1, IDXGIDevice, IDXGIOutput,
    )
    from Direct3D.PyIdl.dxgi1_2 import IDXGIOutput1, IDXGIOutputDuplication
    from Direct3D.PyIdl.d3d11 import (
        ID3D11Device, ID3D11DeviceContext, ID3D11Texture2D,
        D3D11_TEXTURE2D_DESC, D3D11_USAGE_STAGING, D3D11_CPU_ACCESS_READ,
    )

    live = []

    factory = CreateDXGIFactory1()
    live.append(("IDXGIFactory1", factory))

    adapter = ctypes.POINTER(IDXGIAdapter1)()
    factory.EnumAdapters1(0, ctypes.byref(adapter))
    if adapter:
        live.append(("IDXGIAdapter1", adapter))

    output = ctypes.POINTER(IDXGIOutput)()
    if adapter:
        try:
            adapter.EnumOutputs(0, ctypes.byref(output))
        except comtypes.COMError:
            output = None
    if output:
        live.append(("IDXGIOutput", output))
        try:
            live.append(("IDXGIOutput1", output.QueryInterface(IDXGIOutput1)))
        except Exception:
            pass

    device = context = None
    if adapter:
        try:
            device, _level, context = D3D11CreateDevice(
                adapter=adapter, driver_type=D3D_DRIVER_TYPE_UNKNOWN)
        except Exception:
            device = context = None
    if device:
        live.append(("ID3D11Device", device))
        live.append(("ID3D11DeviceContext", context))
        try:
            live.append(("IDXGIDevice", device.QueryInterface(IDXGIDevice)))
        except Exception:
            pass

        desc = D3D11_TEXTURE2D_DESC()
        ctypes.memset(ctypes.byref(desc), 0, ctypes.sizeof(desc))
        desc.Width = desc.Height = 16
        desc.MipLevels = desc.ArraySize = 1
        desc.Format = 87                       # B8G8R8A8_UNORM
        desc.SampleDesc.Count = 1
        desc.Usage = getattr(D3D11_USAGE_STAGING, "value", D3D11_USAGE_STAGING)
        desc.CPUAccessFlags = getattr(D3D11_CPU_ACCESS_READ, "value",
                                      D3D11_CPU_ACCESS_READ)
        texture = ctypes.POINTER(ID3D11Texture2D)()
        try:
            device.CreateTexture2D(ctypes.byref(desc), None, ctypes.byref(texture))
            live.append(("ID3D11Texture2D", texture))
        except Exception:
            pass

    if output is not None and device is not None:
        try:
            output1 = output.QueryInterface(IDXGIOutput1)
            duplication = ctypes.POINTER(IDXGIOutputDuplication)()
            output1.DuplicateOutput(device, ctypes.byref(duplication))
            live.append(("IDXGIOutputDuplication", duplication))
        except Exception:
            pass

    live.extend(_build_d3d12())
    return live


def _build_d3d12():
    """The Direct3D 12 half, or nothing if this machine has no D3D12 driver."""
    try:
        from Direct3D.PyIdl.functions import D3D12CreateDevice
        from Direct3D.PyIdl.d3d12 import (
            D3D12_COMMAND_LIST_TYPE_DIRECT, D3D12_COMMAND_QUEUE_DESC,
            D3D12_DESCRIPTOR_HEAP_DESC, D3D12_DESCRIPTOR_HEAP_TYPE_RTV,
            ID3D12CommandAllocator, ID3D12CommandQueue, ID3D12DescriptorHeap,
            ID3D12Fence,
        )
        device = D3D12CreateDevice()
    except Exception:
        return []

    def value(x):
        return x.value if hasattr(x, "value") else x

    live = [("ID3D12Device", device)]

    desc = D3D12_COMMAND_QUEUE_DESC()
    desc.Type = value(D3D12_COMMAND_LIST_TYPE_DIRECT)
    desc.Priority = desc.Flags = desc.NodeMask = 0
    queue = ctypes.POINTER(ID3D12CommandQueue)()
    try:
        device.CreateCommandQueue(ctypes.byref(desc), ID3D12CommandQueue._iid_,
                                  ctypes.byref(queue))
        live.append(("ID3D12CommandQueue", queue))
    except Exception:
        pass

    allocator = ctypes.POINTER(ID3D12CommandAllocator)()
    try:
        device.CreateCommandAllocator(value(D3D12_COMMAND_LIST_TYPE_DIRECT),
                                      ID3D12CommandAllocator._iid_,
                                      ctypes.byref(allocator))
        live.append(("ID3D12CommandAllocator", allocator))
    except Exception:
        pass

    fence = ctypes.POINTER(ID3D12Fence)()
    try:
        device.CreateFence(0, 0, ID3D12Fence._iid_, ctypes.byref(fence))
        live.append(("ID3D12Fence", fence))
    except Exception:
        pass

    heap_desc = D3D12_DESCRIPTOR_HEAP_DESC()
    heap_desc.Type = value(D3D12_DESCRIPTOR_HEAP_TYPE_RTV)
    heap_desc.NumDescriptors = 4
    heap_desc.Flags = heap_desc.NodeMask = 0
    heap = ctypes.POINTER(ID3D12DescriptorHeap)()
    try:
        device.CreateDescriptorHeap(ctypes.byref(heap_desc),
                                    ID3D12DescriptorHeap._iid_,
                                    ctypes.byref(heap))
        live.append(("ID3D12DescriptorHeap", heap))
    except Exception:
        pass

    return live


def main():
    argv = sys.argv[1:]
    verbose = "--verbose" in argv or "-v" in argv
    only = argv[argv.index("--interface") + 1] if "--interface" in argv else None

    print("pyDXGID3D - exercising the API against real objects")
    print("=" * 52)
    print()
    print("The suite proves the declarations. This calls them.")
    print()

    try:
        live = build()
    except Exception:
        print("could not build any objects:")
        traceback.print_exc()
        return 1

    results = []
    for name, obj in live:
        if not obj:
            continue
        results.append(exercise(name, obj, verbose=verbose, only=only))

    print("  %-28s %7s %7s %7s %9s %9s"
          % ("interface", "called", "ok", "failed", "no args", "mutating"))
    print("  " + "-" * 74)
    called = ok = failed = unsatisfiable = mutating = 0
    for r in results:
        if not r.total:
            continue
        cannot = sum(1 for _m, why in r.skipped if why != "not interrogative")
        changes = len(r.skipped) - cannot
        print("  %-28s %7d %7d %7d %9d %9d"
              % (r.name, r.attempted, len(r.ok), len(r.failed), cannot, changes))
        called += r.attempted
        ok += len(r.ok)
        failed += len(r.failed)
        unsatisfiable += cannot
        mutating += changes
    print("  " + "-" * 74)
    print("  %-28s %7d %7d %7d %9d %9d"
          % ("TOTAL", called, ok, failed, unsatisfiable, mutating))

    interrogative = called + unsatisfiable
    if interrogative:
        print()
        print("  %d of the %d interrogative methods on these objects were called, "
              "%.0f%%." % (called, interrogative, 100.0 * called / interrogative))
        print("  The other %d need an argument this tool will not invent - a real"
              % unsatisfiable)
        print("  resource, a named GUID, a sized buffer. %d more change state and"
              % mutating)
        print("  are never called at all.")

    problems = [(r.name, m, why) for r in results for m, why in r.failed]
    if problems:
        print()
        print("  Methods that did not survive the call:")
        for iface, method, why in problems:
            print("    %s::%s" % (iface, method))
            print("        %s" % why)

    print()
    print("  'ok' includes a method that returned a failing HRESULT: the call")
    print("  reached the driver and came back, which is what is being measured.")
    print("  'failed' means the call itself broke - a wrong signature, a type")
    print("  ctypes could not marshal, or memory it should not have touched.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
