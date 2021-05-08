##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.19041.0
##
##   Translate in Python by J. Vnh
##
import ctypes
import ctypes.wintypes as wintypes

class DXGI_RATIONAL(ctypes.Structure):
	_fields_ = [('Numerator',    wintypes.UINT),
				('Denominator',  wintypes.UINT),
	]


# The following values are used with DXGI_SAMPLE_DESC::Quality
DXGI_STANDARD_MULTISAMPLE_QUALITY_PATTERN = 0xFFFFFFFF
DXGI_CENTER_MULTISAMPLE_QUALITY_PATTERN   = 0xFFFFFFFE


class DXGI_SAMPLE_DESC(ctypes.Structure):
	_fields_ = [('Count',    wintypes.UINT),
				('Quality',  wintypes.UINT),
	]


DXGI_COLOR_SPACE_TYPE = ctypes.c_uint
DXGI_COLOR_SPACE_RGB_FULL_G22_NONE_P709             = DXGI_COLOR_SPACE_TYPE(0)
DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709             = DXGI_COLOR_SPACE_TYPE(1)
DXGI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709           = DXGI_COLOR_SPACE_TYPE(2)
DXGI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020          = DXGI_COLOR_SPACE_TYPE(3)
DXGI_COLOR_SPACE_RESERVED                           = DXGI_COLOR_SPACE_TYPE(4)
DXGI_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601      = DXGI_COLOR_SPACE_TYPE(5)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601         = DXGI_COLOR_SPACE_TYPE(6)
DXGI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601           = DXGI_COLOR_SPACE_TYPE(7)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709         = DXGI_COLOR_SPACE_TYPE(8)
DXGI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709           = DXGI_COLOR_SPACE_TYPE(9)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020        = DXGI_COLOR_SPACE_TYPE(10)
DXGI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020          = DXGI_COLOR_SPACE_TYPE(11)
DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020          = DXGI_COLOR_SPACE_TYPE(12)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020      = DXGI_COLOR_SPACE_TYPE(13)
DXGI_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020        = DXGI_COLOR_SPACE_TYPE(14)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020     = DXGI_COLOR_SPACE_TYPE(15)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020   = DXGI_COLOR_SPACE_TYPE(16)
DXGI_COLOR_SPACE_RGB_FULL_G22_NONE_P2020            = DXGI_COLOR_SPACE_TYPE(17)
DXGI_COLOR_SPACE_YCBCR_STUDIO_GHLG_TOPLEFT_P2020    = DXGI_COLOR_SPACE_TYPE(18)
DXGI_COLOR_SPACE_YCBCR_FULL_GHLG_TOPLEFT_P2020      = DXGI_COLOR_SPACE_TYPE(19)
DXGI_COLOR_SPACE_RGB_STUDIO_G24_NONE_P709           = DXGI_COLOR_SPACE_TYPE(20)
DXGI_COLOR_SPACE_RGB_STUDIO_G24_NONE_P2020          = DXGI_COLOR_SPACE_TYPE(21)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G24_LEFT_P709         = DXGI_COLOR_SPACE_TYPE(22)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G24_LEFT_P2020        = DXGI_COLOR_SPACE_TYPE(23)
DXGI_COLOR_SPACE_YCBCR_STUDIO_G24_TOPLEFT_P2020     = DXGI_COLOR_SPACE_TYPE(24)
DXGI_COLOR_SPACE_CUSTOM                             = DXGI_COLOR_SPACE_TYPE(0xFFFFFFFF)


####### END OF FILE #######

