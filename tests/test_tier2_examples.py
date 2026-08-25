# -*- coding: utf-8 -*-
"""Tier 0 and 2 - the examples parse, and the ones that can run do run.

An example that no longer works is worse than no example: it is documentation
that lies, and it is the first thing a new reader executes. These are cheap to
check and they break the moment the capture API changes shape, which is exactly
when someone needs to be told.

The structural checks are tier 0 and run anywhere. Actually running them needs a
display, so those are tier 2.
"""
import ast
import glob
import io
import os
import subprocess
import sys

import pytest

from conftest import REPO_ROOT, needs_comtypes, needs_windows

EXAMPLES = os.path.join(REPO_ROOT, "examples")


def _example_files():
    return sorted(p for p in glob.glob(os.path.join(EXAMPLES, "*.py"))
                  if not os.path.basename(p).startswith("_"))


# ------------------------------------------------------------- structure ----
@pytest.mark.tier0
def test_there_are_examples():
    assert _example_files(), "no examples found under examples/"


@pytest.mark.tier0
@pytest.mark.parametrize("path", _example_files(),
                         ids=lambda p: os.path.basename(p))
def test_an_example_parses_and_explains_itself(path):
    """Every example needs a module docstring and a main().

    The docstring is not decoration - it is where the constraints live.
    examples/window.py is only honest because its docstring says occlusion is
    not solved, and an example that loses its docstring loses that.
    """
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    assert ast.get_docstring(tree), "%s has no module docstring" % path

    functions = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    assert "main" in functions, "%s has no main()" % path

    source = io.open(path, encoding="utf-8").read()
    assert "__main__" in source, "%s is not runnable" % path


@pytest.mark.tier0
@pytest.mark.parametrize("path", _example_files(),
                         ids=lambda p: os.path.basename(p))
def test_an_example_uses_only_the_public_surface(path):
    """The examples are the contract, demonstrated.

    An example that reaches into Direct3D.PyIdl for something the capture API
    should provide is a sign the API is missing something. d3d12_device.py is
    exempt: Direct3D 12 has no ergonomic layer, so the bindings ARE its public
    surface.
    """
    if os.path.basename(path) == "d3d12_device.py":
        pytest.skip("d3d12 has no capture-style wrapper; the bindings are the API")

    source = io.open(path, encoding="utf-8").read()
    assert "Direct3D.PyIdl" not in source, (
        "%s reaches past Direct3D.Capture into the raw bindings. Either the "
        "example is doing something the capture API should do for it, or the "
        "capture API is missing something." % os.path.basename(path))


# ------------------------------------------------------------- execution ----
@pytest.mark.tier2
@needs_windows
@needs_comtypes
@pytest.mark.parametrize("name", ["screenshot.py", "displays.py", "region.py",
                                  "window.py", "record.py", "d3d12_device.py"])
def test_an_example_answers_help(name):
    """--help exercises the argument parser and the imports without side effects.

    Cheap, and it catches the commonest way an example rots: a rename in the
    capture API that the example still spells the old way.
    """
    completed = subprocess.run(
        [sys.executable, os.path.join(EXAMPLES, name), "--help"],
        capture_output=True, text=True, timeout=60)
    assert completed.returncode == 0, (
        "%s --help failed:\n%s" % (name, completed.stderr[-1500:]))
    assert completed.stdout.strip()


@pytest.mark.tier2
@needs_windows
@needs_comtypes
def test_the_screenshot_example_writes_a_real_png(tmp_path, capturable_output):
    """Runs it for real and decodes what it produced.

    Asserting the file exists would pass on a zero-byte file. This checks the
    PNG structure, every chunk CRC, and that the decompressed image is exactly
    the size the header claims - which is what would catch the BGRA-to-RGBA
    swap writing the wrong number of bytes.
    """
    import struct
    import zlib

    target = tmp_path / "shot.png"
    completed = subprocess.run(
        [sys.executable, os.path.join(EXAMPLES, "screenshot.py"),
         "--out", str(target)],
        capture_output=True, text=True, timeout=120)
    assert completed.returncode == 0, completed.stderr[-1500:]
    assert target.is_file()

    data = target.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"

    position, chunks = 8, {}
    while position < len(data):
        length = struct.unpack(">I", data[position:position + 4])[0]
        kind = data[position + 4:position + 8]
        payload = data[position + 8:position + 8 + length]
        crc = struct.unpack(">I", data[position + 8 + length:
                                       position + 12 + length])[0]
        assert crc == (zlib.crc32(kind + payload) & 0xFFFFFFFF), \
            "chunk %r has a bad CRC" % kind
        chunks[kind] = payload
        position += 12 + length

    assert set(chunks) == {b"IHDR", b"IDAT", b"IEND"}
    width, height, bits, colour = struct.unpack(">IIBB", chunks[b"IHDR"][:10])
    assert (width, height) == (capturable_output.width, capturable_output.height)
    assert (bits, colour) == (8, 6), "not 8-bit RGBA"

    raw = zlib.decompress(chunks[b"IDAT"])
    assert len(raw) == height * (1 + width * 4), (
        "the image data is %d bytes; %dx%d RGBA with one filter byte per row "
        "should be %d" % (len(raw), width, height, height * (1 + width * 4)))


@pytest.mark.tier2
@needs_windows
@needs_comtypes
def test_the_displays_example_names_every_output(capturable_output):
    completed = subprocess.run(
        [sys.executable, os.path.join(EXAMPLES, "displays.py")],
        capture_output=True, text=True, timeout=120)
    assert completed.returncode == 0, completed.stderr[-1500:]
    assert capturable_output.device_name in completed.stdout
    assert "captured" in completed.stdout
