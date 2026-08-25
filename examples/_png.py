# -*- coding: utf-8 -*-
"""A PNG writer in forty lines, so the examples need nothing installed.

Pillow would do this better and handle a hundred cases this does not. The point
of the examples is to show what the capture API gives you, and an example whose
first line is `pip install Pillow` teaches the reader about Pillow.

PNG is a short format if you only need one shape of it: an 8-bit RGBA image, one
IHDR, one IDAT of zlib-compressed scanlines each prefixed with a filter byte, one
IEND. That is all this writes.

The frames arrive BGRA, because that is what Desktop Duplication produces and it
does not negotiate. The channel swap happens here.
"""
import struct
import zlib


def _chunk(kind, payload):
    """length, type, payload, CRC32 of type+payload."""
    return (struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))


def write_rgba(path, rows, width, height):
    """Write 8-bit RGBA scanlines. `rows` is an iterable of `bytes`."""
    raw = bytearray()
    for row in rows:
        raw.append(0)              # filter type 0: none. Simple, slightly larger.
        raw += row

    with open(path, "wb") as handle:
        handle.write(b"\x89PNG\r\n\x1a\n")
        handle.write(_chunk(b"IHDR", struct.pack(
            ">IIBBBBB", width, height, 8, 6, 0, 0, 0)))   # 8-bit, colour type 6
        handle.write(_chunk(b"IDAT", zlib.compress(bytes(raw), 6)))
        handle.write(_chunk(b"IEND", b""))


def write_frame(path, frame):
    """Write a captured Frame as a PNG, swapping BGRA to RGBA.

    Works with or without numpy. With it, the swap is one vectorised index and
    the whole thing takes a few milliseconds; without, it is a per-row slice,
    which is slower but still not the per-pixel loop the old PPM path used.
    """
    view = frame.memoryview
    pitch, width, height = frame.pitch, frame.width, frame.height
    packed = width * 4

    try:
        import numpy
    except ImportError:
        numpy = None

    if numpy is not None:
        image = numpy.frombuffer(view, dtype=numpy.uint8)
        image = image.reshape(height, pitch)[:, :packed].reshape(height, width, 4)
        rgba = image[:, :, [2, 1, 0, 3]]                 # BGRA -> RGBA
        rows = [rgba[y].tobytes() for y in range(height)]
    else:
        rows = []
        for y in range(height):
            row = bytearray(view[y * pitch:y * pitch + packed])
            row[0::4], row[2::4] = row[2::4], row[0::4]   # swap B and R
            rows.append(bytes(row))

    write_rgba(path, rows, width, height)
    return path
