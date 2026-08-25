# -*- coding: utf-8 -*-
"""One captured frame.

A ``Frame`` holds no pixels. It holds a pointer into pages that Direct3D mapped
for the duration of one loop iteration, and it becomes invalid the moment the
capture unmaps them - which happens as soon as the ``for`` body returns.

That is the one real footgun in this API, so it is enforced rather than
documented: ``expire()`` clears the pointer, and every accessor that would read
freed memory raises ``StaleFrameError`` instead.

Three ways out, measured at 1920x1200 BGRA (8.79 MB) on the development machine,
timed as Map -> deliver -> Unmap:

    frame.array          2.63 ms   zero copy, valid for this iteration only
    frame.copy_into(d)   3.76 ms   one pass into a destination you keep and reuse
    frame.copy()         7.62 ms   owned, freshly allocated

The gap between the last two is not the copy. It is the page faults on a fresh
8.79 MB allocation - about 3.9 ms of them, every frame. ``numpy``'s own
``.copy()`` off the mapped view costs 7.57 ms, statistically the same as
``numpy.empty`` plus ``memmove``, because both pay for the allocation.

So a consumer that captures in a loop should hold one destination array and call
``copy_into``. That is the difference between 253 and 128 frames per second of
pipeline capacity, and it costs the caller one line.
"""
import ctypes

try:
    import numpy
except ImportError:                                  # numpy is an optional extra
    numpy = None


class StaleFrameError(RuntimeError):
    """A Frame was used after its iteration ended.

    The pages it pointed at have been unmapped and may already hold the next
    frame, or nothing at all. Reading them is undefined behaviour, which on a
    good day is garbage pixels and on a bad day is an access violation that
    takes the interpreter with it.

    Call ``frame.copy()`` or ``frame.copy_into()`` inside the loop if the data
    has to outlive it.
    """


def _require_numpy(what):
    if numpy is None:
        raise ImportError(
            "%s needs numpy. Install it with 'pip install pyDXGID3D[numpy]', "
            "or use frame.memoryview, which has no dependency." % what)


class Frame(object):
    """The mapped staging texture, described.

    ``pitch`` is not ``width * 4``. The driver rounds each row up to its own
    alignment, so a 1920-pixel BGRA row is 7680 bytes here and might not be
    somewhere else. Anything walking the buffer by hand has to step by ``pitch``
    and ignore the tail of each row.
    """

    __slots__ = ("width", "height", "pitch", "format", "timestamp_qpc",
                 "accumulated", "_pointer", "_expired")

    #: Desktop Duplication delivers this and does not negotiate.
    FORMAT = "DXGI_FORMAT_B8G8R8A8_UNORM"

    def __init__(self, width, height, pitch, pointer,
                 timestamp_qpc, accumulated):
        self.width = width
        self.height = height
        self.pitch = pitch
        self.format = self.FORMAT
        #: LastPresentTime, in QueryPerformanceCounter ticks.
        self.timestamp_qpc = timestamp_qpc
        #: AccumulatedFrames. A steady 1 means the loop is keeping up; higher
        #: means the desktop composed frames that were coalesced into this one
        #: before it was acquired, so the consumer is the bottleneck.
        self.accumulated = accumulated
        self._pointer = pointer
        self._expired = False

    # ------------------------------------------------------------ lifetime --
    def expire(self):
        """Called by the capture when it unmaps. Not for callers."""
        self._expired = True
        self._pointer = None

    @property
    def valid(self):
        return not self._expired

    def _check(self, what):
        if self._expired:
            raise StaleFrameError(
                "this Frame's pixels were unmapped when the loop moved on, so "
                "%s would read freed memory. Call frame.copy() or "
                "frame.copy_into() inside the loop if you need the data "
                "afterwards." % what)

    # -------------------------------------------------------------- shape --
    @property
    def nbytes(self):
        """Bytes in the tightly packed image, ignoring row padding."""
        return self.width * self.height * 4

    @property
    def shape(self):
        return (self.height, self.width, 4)

    @property
    def padded(self):
        """True when the driver pads rows, so pitch > width * 4."""
        return self.pitch != self.width * 4

    # ----------------------------------------------------------- delivery --
    @property
    def memoryview(self):
        """The mapped pages, padding included, without numpy.

        ``height * pitch`` bytes: rows are ``pitch`` apart and only the first
        ``width * 4`` bytes of each are pixels.

        Cast to ``'B'`` on the way out. A memoryview over a ctypes array carries
        the format ``'<B'``, and Python refuses to INDEX that - ``view[0]``
        raises NotImplementedError - while slicing it works fine. So the
        no-numpy path, which is the whole reason this property exists, was half
        broken in a way that only showed when someone read a single pixel.
        See F-61.
        """
        self._check("frame.memoryview")
        buffer_type = ctypes.c_ubyte * (self.pitch * self.height)
        return memoryview(buffer_type.from_address(self._pointer)).cast("B")

    @property
    def array(self):
        """A zero-copy ``(height, width, 4)`` uint8 view. BGRA order.

        Valid for this iteration only, and the cheapest thing here - 2.63 ms
        against 2.48 for touching a single byte, so the view itself is free.
        """
        self._check("frame.array")
        _require_numpy("frame.array")
        rows = numpy.ctypeslib.as_array(
            ctypes.cast(self._pointer, ctypes.POINTER(ctypes.c_ubyte)),
            shape=(self.height, self.pitch))
        return rows[:, :self.width * 4].reshape(self.height, self.width, 4)

    def copy_into(self, destination):
        """Copy the pixels into an array you already own. Returns it.

        The fast way to keep a frame: 3.76 ms against 7.62 for ``copy()``,
        because the destination's pages are already resident. Hold one array
        outside the loop and pass it in every iteration.

            buffer = numpy.empty((h, w, 4), numpy.uint8)
            for frame in capture:
                process(frame.copy_into(buffer))

        The destination must be C-contiguous uint8 of exactly ``frame.shape``.
        """
        self._check("frame.copy_into()")
        _require_numpy("frame.copy_into()")
        if destination.dtype != numpy.uint8:
            raise ValueError("destination must be uint8, got %s"
                             % destination.dtype)
        if destination.shape != self.shape:
            raise ValueError("destination is %r, frame is %r"
                             % (destination.shape, self.shape))
        if not destination.flags["C_CONTIGUOUS"]:
            raise ValueError("destination must be C-contiguous; a slice of a "
                             "larger array usually is not")
        self._blit(destination.ctypes.data)
        return destination

    def copy(self):
        """An owned ``(height, width, 4)`` uint8 array, safe to keep.

        7.62 ms per 1920x1200 frame, of which roughly 3.9 is page faults on the
        fresh allocation rather than the copy. ``copy_into`` avoids that
        entirely; use this one for a frame you take occasionally.
        """
        self._check("frame.copy()")
        _require_numpy("frame.copy()")
        destination = numpy.empty(self.shape, dtype=numpy.uint8)
        self._blit(destination.ctypes.data)
        return destination

    def _blit(self, address):
        """One pass out of the mapped pages into `address`.

        ``ctypes.memmove`` rather than letting numpy read the source: the
        staging texture is mapped write-combined, and numpy's own copy off it
        measured about twice the cost of a streaming move for the identical
        result.
        """
        packed = self.width * 4
        if not self.padded:
            ctypes.memmove(address, self._pointer, self.nbytes)
            return
        source, target = self._pointer, address
        for _row in range(self.height):
            ctypes.memmove(target, source, packed)
            source += self.pitch
            target += packed

    def __repr__(self):
        return "<Frame %dx%d pitch=%d accumulated=%d%s>" % (
            self.width, self.height, self.pitch, self.accumulated,
            "" if self.valid else " EXPIRED")
