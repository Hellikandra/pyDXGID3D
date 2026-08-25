# -*- coding: utf-8 -*-
"""Create a Direct3D 12 device and ask it what it can do.

    python examples/d3d12_device.py
    python examples/d3d12_device.py --adapter 1

Direct3D 12 in this package is COMPLETE and LIGHTLY EXERCISED. Every interface,
method signature, structure and enumeration matches the SDK and is asserted
against it - but far less D3D12 code has been run than DXGI or Direct3D 11 code.
This example is the part that has been run.

It creates nothing that draws. Device, command queue, allocator, fence and
descriptor heap are the objects every D3D12 program starts with, and the feature
queries are how you find out what the hardware will accept.
"""
import argparse
import ctypes
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Direct3D.Capture import enumerate_outputs
from Direct3D.PyIdl import d3d12
from Direct3D.PyIdl.functions import D3D12CreateDevice
from Direct3D.PyIdl.status import DXGIError


def value(constant):
    return constant.value if hasattr(constant, "value") else constant


FEATURE_LEVELS = [
    ("12_2", 0xc200), ("12_1", 0xc100), ("12_0", 0xc000),
    ("11_1", 0xb100), ("11_0", 0xb000),
]

HEAPS = [
    ("CBV/SRV/UAV", d3d12.D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV),
    ("Sampler", d3d12.D3D12_DESCRIPTOR_HEAP_TYPE_SAMPLER),
    ("RTV", d3d12.D3D12_DESCRIPTOR_HEAP_TYPE_RTV),
    ("DSV", d3d12.D3D12_DESCRIPTOR_HEAP_TYPE_DSV),
]

QUEUES = [
    ("direct", d3d12.D3D12_COMMAND_LIST_TYPE_DIRECT),
    ("compute", d3d12.D3D12_COMMAND_LIST_TYPE_COMPUTE),
    ("copy", d3d12.D3D12_COMMAND_LIST_TYPE_COPY),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--adapter", type=int, default=None,
                        help="index into the adapters that drive a display")
    args = parser.parse_args()

    outputs = enumerate_outputs()
    adapters, seen = [], set()
    for output in outputs:
        if output.adapter.luid not in seen:
            seen.add(output.adapter.luid)
            adapters.append(output.adapter)

    adapter = None
    if adapters:
        adapter = adapters[args.adapter or 0]
        print("adapter : %s" % adapter.description)
    else:
        print("adapter : default (no display-driving adapter found)")

    try:
        device = D3D12CreateDevice(adapter)
    except (DXGIError, OSError) as exc:
        print("Could not create a Direct3D 12 device: %s" % exc)
        print("Direct3D 12 needs Windows 10 or later and a driver that supports it.")
        return 1

    print("device  : created, %d node%s"
          % (device.GetNodeCount(), "" if device.GetNodeCount() == 1 else "s"))
    print()

    print("  highest feature level accepted")
    for name, level in FEATURE_LEVELS:
        try:
            probe = D3D12CreateDevice(adapter, minimum_feature_level=level)
            print("      %s  yes" % name)
            del probe
            break
        except (DXGIError, OSError):
            print("      %s  no" % name)

    print()
    print("  descriptor sizes")
    for name, kind in HEAPS:
        size = device.GetDescriptorHandleIncrementSize(value(kind))
        print("      %-12s %3d bytes" % (name, size))

    print()
    print("  command queues")
    for name, kind in QUEUES:
        desc = d3d12.D3D12_COMMAND_QUEUE_DESC()
        desc.Type = value(kind)
        desc.Priority = desc.Flags = desc.NodeMask = 0
        queue = ctypes.POINTER(d3d12.ID3D12CommandQueue)()
        try:
            device.CreateCommandQueue(ctypes.byref(desc),
                                      d3d12.ID3D12CommandQueue._iid_,
                                      ctypes.byref(queue))
            # GetDesc returns a structure BY VALUE, which on x64 means a hidden
            # out-pointer rather than a register. That was F-58, and it faulted
            # the interpreter until P6.
            back = d3d12.D3D12_COMMAND_QUEUE_DESC()
            queue.GetDesc(ctypes.byref(back))
            print("      %-8s created, GetDesc reports type %d" % (name, back.Type))
        except (DXGIError, OSError) as exc:
            print("      %-8s FAILED: %s" % (name, exc))

    print()
    print("  a root signature, serialised and read back")
    desc = d3d12.D3D12_ROOT_SIGNATURE_DESC()
    desc.NumParameters, desc.pParameters = 0, None
    desc.NumStaticSamplers, desc.pStaticSamplers = 0, None
    desc.Flags = 1                       # ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT
    from Direct3D.PyIdl.functions import D3D12SerializeRootSignature
    blob = D3D12SerializeRootSignature(desc)
    raw = ctypes.string_at(blob.GetBufferPointer(), blob.GetBufferSize())
    print("      %d bytes, container %r" % (len(raw), raw[:4].decode("ascii")))

    signature = ctypes.POINTER(d3d12.ID3D12RootSignature)()
    device.CreateRootSignature(0, blob.GetBufferPointer(), blob.GetBufferSize(),
                               d3d12.ID3D12RootSignature._iid_,
                               ctypes.byref(signature))
    print("      CreateRootSignature accepted it")

    print()
    print("  Every call above went through the generated bindings. What is NOT")
    print("  shown is a frame: this package binds Direct3D 12 but nothing here")
    print("  renders. Use tools/exercise.py to see how much of the surface has")
    print("  actually been called.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
