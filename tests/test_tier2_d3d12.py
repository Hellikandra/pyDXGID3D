# -*- coding: utf-8 -*-
"""Tier 2 - Direct3D 12 against a real device.

Until P6 no Direct3D 12 code in this repository had ever executed. 131
interfaces were verified against the SDK's declarations - vtable order, IIDs,
structure layout, every method's parameter list - and none of that could see
F-58, where 27 methods declared a structure as their restype and faulted the
interpreter when called.

Static checks proved the transcription. Only calling the methods proves the
bindings.

Skips where there is no Direct3D 12 device, exactly as the capture tests skip
without a display. That includes a hosted CI runner: WARP supports D3D12, but
d3d12.dll may still be absent, so the fixture asks rather than assumes.
"""
import ctypes

import pytest

from conftest import needs_comtypes, needs_windows

pytestmark = [pytest.mark.tier2, needs_windows, needs_comtypes]


def _value(constant):
    return constant.value if hasattr(constant, "value") else constant


@pytest.fixture(scope="module")
def device():
    """A Direct3D 12 device on the adapter driving the display, or skip."""
    functions = pytest.importorskip("Direct3D.PyIdl.functions")
    capture = pytest.importorskip("Direct3D.Capture")

    outputs = capture.enumerate_outputs()
    adapter = outputs[0].adapter if outputs else None
    try:
        return functions.D3D12CreateDevice(adapter)
    except Exception as exc:                 # no D3D12 driver, or no d3d12.dll
        pytest.skip("no Direct3D 12 device available: %s" % exc)


def test_the_device_answers(device):
    """The simplest possible call through a generated D3D12 vtable."""
    assert device
    assert device.GetNodeCount() >= 1


def test_a_command_queue_can_be_created(device):
    """A method taking a structure pointer and returning an interface."""
    from Direct3D.PyIdl.d3d12 import (
        D3D12_COMMAND_LIST_TYPE_DIRECT, D3D12_COMMAND_QUEUE_DESC,
        ID3D12CommandQueue,
    )

    desc = D3D12_COMMAND_QUEUE_DESC()
    desc.Type = _value(D3D12_COMMAND_LIST_TYPE_DIRECT)
    desc.Priority, desc.Flags, desc.NodeMask = 0, 0, 0

    queue = ctypes.POINTER(ID3D12CommandQueue)()
    device.CreateCommandQueue(ctypes.byref(desc), ID3D12CommandQueue._iid_,
                              ctypes.byref(queue))
    assert queue


def test_an_allocator_and_a_fence(device):
    """A method taking a plain enum, and one taking two integers."""
    from Direct3D.PyIdl.d3d12 import (
        D3D12_COMMAND_LIST_TYPE_DIRECT, ID3D12CommandAllocator, ID3D12Fence,
    )

    allocator = ctypes.POINTER(ID3D12CommandAllocator)()
    device.CreateCommandAllocator(_value(D3D12_COMMAND_LIST_TYPE_DIRECT),
                                  ID3D12CommandAllocator._iid_,
                                  ctypes.byref(allocator))
    assert allocator

    fence = ctypes.POINTER(ID3D12Fence)()
    device.CreateFence(0, 0, ID3D12Fence._iid_, ctypes.byref(fence))
    assert fence
    assert fence.GetCompletedValue() == 0


# ----------------------------------------------------------------- F-58 ----
@pytest.fixture(scope="module")
def descriptor_heap(device):
    from Direct3D.PyIdl.d3d12 import (
        D3D12_DESCRIPTOR_HEAP_DESC, D3D12_DESCRIPTOR_HEAP_TYPE_RTV,
        ID3D12DescriptorHeap,
    )

    desc = D3D12_DESCRIPTOR_HEAP_DESC()
    desc.Type = _value(D3D12_DESCRIPTOR_HEAP_TYPE_RTV)
    desc.NumDescriptors, desc.Flags, desc.NodeMask = 4, 0, 0
    heap = ctypes.POINTER(ID3D12DescriptorHeap)()
    device.CreateDescriptorHeap(ctypes.byref(desc), ID3D12DescriptorHeap._iid_,
                                ctypes.byref(heap))
    return heap


def test_a_struct_returning_method_does_not_fault(descriptor_heap):
    """F-58 itself. Before the fix this did not fail - it faulted the process.

    A descriptor handle is a single pointer-sized integer, and the surprise is
    that the x64 convention still passes a hidden pointer for it. Any nonzero
    handle means the ABI is right; the value is an opaque driver address.
    """
    from Direct3D.PyIdl.d3d12 import D3D12_CPU_DESCRIPTOR_HANDLE

    handle = D3D12_CPU_DESCRIPTOR_HANDLE()
    descriptor_heap.GetCPUDescriptorHandleForHeapStart(ctypes.byref(handle))
    assert handle.ptr != 0


def test_the_gpu_handle_too(descriptor_heap):
    from Direct3D.PyIdl.d3d12 import D3D12_GPU_DESCRIPTOR_HANDLE

    handle = D3D12_GPU_DESCRIPTOR_HANDLE()
    descriptor_heap.GetGPUDescriptorHandleForHeapStart(ctypes.byref(handle))
    assert handle.ptr != 0


def test_getdesc_returns_what_was_asked_for(descriptor_heap):
    """The strongest evidence the struct-return ABI is right.

    A nonzero handle only shows something was written. GetDesc hands back a
    whole structure, and every field matching what was requested means it was
    written to the right place with the right layout.
    """
    from Direct3D.PyIdl.d3d12 import (
        D3D12_DESCRIPTOR_HEAP_DESC, D3D12_DESCRIPTOR_HEAP_TYPE_RTV,
    )

    desc = D3D12_DESCRIPTOR_HEAP_DESC()
    descriptor_heap.GetDesc(ctypes.byref(desc))
    assert desc.Type == _value(D3D12_DESCRIPTOR_HEAP_TYPE_RTV)
    assert desc.NumDescriptors == 4
    # NodeMask is NOT asserted equal to what was passed. The runtime normalises
    # 0 to 1 on a single-adapter system - "no node specified" means "node one" -
    # so asserting it would be testing D3D12's behaviour rather than this
    # binding's. Type and NumDescriptors coming back exactly is what shows the
    # structure was written to the right address with the right layout.
    assert desc.NodeMask in (0, 1)


def test_descriptor_increment_is_plausible(device):
    from Direct3D.PyIdl.d3d12 import D3D12_DESCRIPTOR_HEAP_TYPE_RTV

    size = device.GetDescriptorHandleIncrementSize(
        _value(D3D12_DESCRIPTOR_HEAP_TYPE_RTV))
    assert 0 < size <= 256, "a descriptor is a few dozen bytes, not %d" % size


# ----------------------------------------------------------------- F-59 ----
def test_the_root_signature_round_trip(device):
    """Serialise, read the bytes, deserialise, and build the real object.

    This is the path F-59 broke: ID3D10Blob::GetBufferPointer was declared void,
    so it returned None and the bytecode was unreachable. A blob is how the root
    signature serialiser and every shader compiler hand back their output, so
    that one wrong return type made all of them useless.
    """
    from Direct3D.PyIdl.functions import (
        D3D12CreateRootSignatureDeserializer, D3D12SerializeRootSignature,
    )
    from Direct3D.PyIdl.d3d12 import D3D12_ROOT_SIGNATURE_DESC, ID3D12RootSignature

    desc = D3D12_ROOT_SIGNATURE_DESC()
    desc.NumParameters, desc.pParameters = 0, None
    desc.NumStaticSamplers, desc.pStaticSamplers = 0, None
    desc.Flags = 1                    # ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT

    blob = D3D12SerializeRootSignature(desc)
    assert blob.GetBufferSize() > 0
    pointer = blob.GetBufferPointer()
    assert pointer, "GetBufferPointer returned nothing - F-59 is back"

    raw = ctypes.string_at(pointer, blob.GetBufferSize())
    assert raw[:4] == b"DXBC", "not a DXBC container: %r" % raw[:4]

    assert D3D12CreateRootSignatureDeserializer(blob)

    signature = ctypes.POINTER(ID3D12RootSignature)()
    device.CreateRootSignature(0, pointer, blob.GetBufferSize(),
                               ID3D12RootSignature._iid_,
                               ctypes.byref(signature))
    assert signature


def test_a_rejected_root_signature_raises_with_the_reason(device):
    """The serialiser's error blob carries the compiler's message, which is the
    only useful thing about a rejected signature. It belongs in the exception."""
    from Direct3D.PyIdl.functions import D3D12SerializeRootSignature
    from Direct3D.PyIdl.d3d12 import D3D12_ROOT_SIGNATURE_DESC
    from Direct3D.PyIdl.status import DXGIError

    desc = D3D12_ROOT_SIGNATURE_DESC()
    desc.NumParameters, desc.pParameters = 4, None     # a lie: no parameters
    desc.NumStaticSamplers, desc.pStaticSamplers = 0, None
    desc.Flags = 0

    with pytest.raises((DXGIError, OSError)):
        D3D12SerializeRootSignature(desc)


# ------------------------------------------------------- the entry points --
def test_the_device_can_be_made_from_a_capture_adapter():
    """The seam that matters: an Adapter from enumerate_outputs() is what a
    caller already has, and it is paired with the output it drives (C-4)."""
    functions = pytest.importorskip("Direct3D.PyIdl.functions")
    capture = pytest.importorskip("Direct3D.Capture")

    outputs = capture.enumerate_outputs()
    if not outputs:
        pytest.skip("no attached display")
    try:
        assert functions.D3D12CreateDevice(outputs[0].adapter)
    except Exception as exc:
        pytest.skip("no Direct3D 12 device on that adapter: %s" % exc)


def test_a_bad_feature_level_raises_rather_than_returning_a_number():
    """Every entry point routes through status.check(), so a failure is a typed
    exception and not a negative integer nobody looks at."""
    functions = pytest.importorskip("Direct3D.PyIdl.functions")
    from Direct3D.PyIdl.status import DXGIError

    with pytest.raises((DXGIError, OSError, ValueError)):
        # 0xFFFF is not a feature level any driver implements.
        functions.D3D12CreateDevice(minimum_feature_level=0xFFFF)
