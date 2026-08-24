# -*- coding: utf-8 -*-
"""What to capture, and what to do when it goes wrong.

Everything is validated in ``__init__``. A capture that is going to fail because
the region is off-screen should fail at construction, where the traceback points
at the caller's own line, rather than three frames into a loop.
"""

#: What DesktopCapture does when the duplication is invalidated. A mode change,
#: a resolution change, a fullscreen-exclusive application taking the display, a
#: UAC prompt, a session lock - all of them raise DXGI_ERROR_ACCESS_LOST and all
#: of them are recoverable by rebuilding. 'rebuild' is the default because the
#: alternative is every caller writing the same try/except.
ACCESS_LOST_POLICIES = ("rebuild", "raise")


class CaptureOptions(object):
    """Immutable once constructed.

    Deliberately absent, each for a reason worth stating:

    ``scale_to``
        A GPU downscale needs a render target, a sampler and a fullscreen pass.
        Measured, cropping to 256x256 from a full 1920x1200 frame removes 35x
        the bytes and only 2.2x the time, because a fixed ~1 ms Map/Unmap cost
        dominates below 1 MB. ``region`` gets that 2.2x with no shader at all,
        via CopySubresourceRegion. The shader would be added on top for a
        benefit nobody has measured.

    ``format``
        Desktop Duplication delivers BGRA and does not negotiate.

    ``deliver='gpu'``
        Shared handle and keyed mutex. Real, but useless until a consumer does
        its own GPU work, and the contract can gain it later without breaking.
    """

    __slots__ = ("output", "region", "cursor", "timeout_ms", "skip_unchanged",
                 "on_access_lost", "max_rebuilds")

    def __init__(self,
                 output=0,
                 region=None,
                 cursor=False,
                 timeout_ms=100,
                 skip_unchanged=True,
                 on_access_lost="rebuild",
                 max_rebuilds=None):
        self.output = output
        self.region = None if region is None else tuple(region)
        self.cursor = bool(cursor)
        self.timeout_ms = timeout_ms
        self.skip_unchanged = bool(skip_unchanged)
        self.on_access_lost = on_access_lost
        self.max_rebuilds = max_rebuilds
        self._validate()

    def _validate(self):
        if not isinstance(self.timeout_ms, int) or isinstance(self.timeout_ms, bool):
            raise TypeError("timeout_ms must be an int, not %s"
                            % type(self.timeout_ms).__name__)
        if self.timeout_ms < 0:
            raise ValueError("timeout_ms must not be negative, got %d"
                             % self.timeout_ms)

        if self.on_access_lost not in ACCESS_LOST_POLICIES:
            raise ValueError("on_access_lost must be one of %s, got %r"
                             % (" or ".join(map(repr, ACCESS_LOST_POLICIES)),
                                self.on_access_lost))

        if self.max_rebuilds is not None:
            if not isinstance(self.max_rebuilds, int) or isinstance(self.max_rebuilds, bool):
                raise TypeError("max_rebuilds must be an int or None, not %s"
                                % type(self.max_rebuilds).__name__)
            if self.max_rebuilds < 0:
                raise ValueError("max_rebuilds must not be negative, got %d"
                                 % self.max_rebuilds)

        if self.cursor:
            # GetFramePointerShape is bound but nothing composites the cursor
            # into the frame yet. Saying so is better than silently ignoring it.
            raise NotImplementedError(
                "cursor=True is not implemented. IDXGIOutputDuplication "
                "delivers the pointer shape separately and compositing it into "
                "the frame is deferred; the bindings for it exist.")

        if self.region is None:
            return
        if len(self.region) != 4:
            raise ValueError("region must be (left, top, right, bottom), got %d "
                             "value(s): %r" % (len(self.region), self.region))
        for name, value in zip(("left", "top", "right", "bottom"), self.region):
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError("region %s must be an int, not %s"
                                % (name, type(value).__name__))
        left, top, right, bottom = self.region
        if right <= left or bottom <= top:
            raise ValueError(
                "region must have positive width and height; "
                "(%d, %d, %d, %d) is %dx%d"
                % (left, top, right, bottom, right - left, bottom - top))

    def region_within(self, output):
        """The region in *output-local* coordinates, checked against its bounds.

        ``region`` is given in desktop coordinates, because that is what the
        caller sees and what ``Output.bounds`` reports. The staging copy needs
        it relative to the output's own top-left corner, and a second monitor
        placed to the right of the first starts at x=1920, not x=0. Getting that
        wrong produces a black frame rather than an error, so it is done in one
        place with the bounds asserted.
        """
        if self.region is None:
            return (0, 0, output.width, output.height)

        left, top, right, bottom = self.region
        if (left < output.left or top < output.top
                or right > output.right or bottom > output.bottom):
            raise ValueError(
                "region (%d, %d, %d, %d) is not inside output %d, which covers "
                "(%d, %d, %d, %d). Regions are in desktop coordinates."
                % (left, top, right, bottom, output.index,
                   output.left, output.top, output.right, output.bottom))
        return (left - output.left, top - output.top,
                right - output.left, bottom - output.top)

    def __repr__(self):
        return ("CaptureOptions(output=%r, region=%r, timeout_ms=%d, "
                "skip_unchanged=%r, on_access_lost=%r)"
                % (self.output, self.region, self.timeout_ms,
                   self.skip_unchanged, self.on_access_lost))
