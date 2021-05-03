import ctypes
import ctypes.wintypes as wintypes

import PyIdl.dxgicommon
import PyIdl.dxgiformat

class DXGI_RGB(ctypes.Structure):
    _fields_ = [('Red', ctypes.c_float),
                ('Green', ctypes.c_float),
                ('Blue', ctypes.c_float),
    ]


class D3DCOLORVALUE(ctypes.Structure):
    _fields_ = [('r', ctypes.c_float),
                ('g', ctypes.c_float),
                ('b', ctypes.c_float),
                ('a', ctypes.c_float),
    ]


DXGI_RGBA = D3DCOLORVALUE # typedef D3DCOLORVALUE DXGI_RGBA;


class DXGI_GAMMA_CONTROL(ctypes.Structure):
    _fields_ = [('Scale', DXGI_RGB),
                ('Offset', DXGI_RGB),
                ('GammaCurve', DXGI_RGB * 1025),
    ]


class DXGI_GAMMA_CONTROL_CAPABILITIES(ctypes.Structure):
    _fields_ = [('ScaleAndOffsetSupported', ctypes.c_bool),
                ('MaxConvertedValue', ctypes.c_float),
                ('MinConvertedValue', ctypes.c_float),
                ('NumGammaControlPoints', ctypes.c_uint),
                ('ControlPointPositions',ctypes.c_float * 1025),
    ]


DXGI_MODE_SCANLINE_ORDER = ctypes.c_int
DXGI_MODE_SCANLINE_ORDER_UNSPECIFIED = DXGI_MODE_SCANLINE_ORDER(0)
DXGI_MODE_SCANLINE_ORDER_PROGRESSIVE = DXGI_MODE_SCANLINE_ORDER(1)
DXGI_MODE_SCANLINE_ORDER_UPPER_FIELD_FIRST = DXGI_MODE_SCANLINE_ORDER(2)
DXGI_MODE_SCANLINE_ORDER_LOWER_FIELD_FIRST = DXGI_MODE_SCANLINE_ORDER(3)


DXGI_MODE_SCALING = ctypes.c_int
DXGI_MODE_SCALING_UNSPECIFIED  = DXGI_MODE_SCALING(0)
DXGI_MODE_SCALING_CENTERED     = DXGI_MODE_SCALING(1)
DXGI_MODE_SCALING_STRETCHED    = DXGI_MODE_SCALING(2)


DXGI_MODE_ROTATION = ctypes.c_int
DXGI_MODE_ROTATION_UNSPECIFIED = DXGI_MODE_ROTATION(0)
DXGI_MODE_ROTATION_IDENTITY = DXGI_MODE_ROTATION(1)
DXGI_MODE_ROTATION_ROTATE90 = DXGI_MODE_ROTATION(2)
DXGI_MODE_ROTATION_ROTATE180 = DXGI_MODE_ROTATION(3)
DXGI_MODE_ROTATION_ROTATE270 = DXGI_MODE_ROTATION(4)


class DXGI_MODE_DESC(ctypes.Structure):
    _fields_ = [('Width', ctypes.c_uint),
                ('Height', ctypes.c_uint),
                ('RefreshRate', PyIdl.dxgicommon.DXGI_RATIONAL),
                ('Format', PyIdl.dxgiformat.DXGI_FORMAT),
                ('ScanlineOrdering', DXGI_MODE_SCANLINE_ORDER),
                ('Scaling', DXGI_MODE_SCALING),
    ]


class DXGI_JPEG_DC_HUFFMAN_TABLE(ctypes.Structure):
    _fields_ = [('CodeCounts', wintypes.BYTE * 12),
                ('CodeValues', wintypes.BYTE * 12),
    ]


class DXGI_JPEG_AC_HUFFMAN_TABLE(ctypes.Structure):
    _fields_ = [('CodeCounts', wintypes.BYTE * 16),
                ('CodeValues', wintypes.BYTE * 162),
    ]


class DXGI_JPEG_QUANTIZATION_TABLE(ctypes.Structure):
    _fields_ = [('Elements', wintypes.BYTE * 64),
    ]


####### END OF FILE #######