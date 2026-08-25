##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.26100.0
##
##   Generated from d3d12sdklayers.idl by tools/generate.py - do not edit by hand.
##   Regenerate with:  python tools/generate.py d3d12sdklayers.idl
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

# LUID and SECURITY_ATTRIBUTES live in the canonical type table, not in
# any IDL - they are Windows types the IDLs reference without declaring.
from Direct3D.PyIdl.typemap import LUID, SECURITY_ATTRIBUTES



from Direct3D.PyIdl.d3d12 import *


## ---------------------------------------------- constants ----
D3D12_INFO_QUEUE_DEFAULT_MESSAGE_COUNT_LIMIT   = 1024


## -------------------------------------------- enumerations ----

D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE = ctypes.c_uint
D3D12_DEBUG_COMMAND_LIST_PARAMETER_GPU_BASED_VALIDATION_SETTINGS = D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE().value

D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_MODE = ctypes.c_uint
D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_DISABLED           = D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_MODE().value
D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_WHEN_HASH_BYPASSED = D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_MODE().value
D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_ALL_BYTECODE       = D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_MODE().value
D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_MODE_DEFAULT       = D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_MODE(D3D12_DEBUG_DEVICE_BYTECODE_VALIDATION_WHEN_HASH_BYPASSED).value

D3D12_DEBUG_DEVICE_PARAMETER_TYPE = ctypes.c_uint
D3D12_DEBUG_DEVICE_PARAMETER_FEATURE_FLAGS                   = D3D12_DEBUG_DEVICE_PARAMETER_TYPE().value
D3D12_DEBUG_DEVICE_PARAMETER_GPU_BASED_VALIDATION_SETTINGS   = D3D12_DEBUG_DEVICE_PARAMETER_TYPE().value
D3D12_DEBUG_DEVICE_PARAMETER_GPU_SLOWDOWN_PERFORMANCE_FACTOR = D3D12_DEBUG_DEVICE_PARAMETER_TYPE().value
D3D12_DEBUG_DEVICE_PARAMETER_BYTECODE_VALIDATION_MODE        = D3D12_DEBUG_DEVICE_PARAMETER_TYPE().value

D3D12_DEBUG_FEATURE = ctypes.c_uint
D3D12_DEBUG_FEATURE_NONE                                   = D3D12_DEBUG_FEATURE(0x00).value
D3D12_DEBUG_FEATURE_ALLOW_BEHAVIOR_CHANGING_DEBUG_AIDS     = D3D12_DEBUG_FEATURE(0x01).value
D3D12_DEBUG_FEATURE_CONSERVATIVE_RESOURCE_STATE_TRACKING   = D3D12_DEBUG_FEATURE(0x02).value
D3D12_DEBUG_FEATURE_DISABLE_VIRTUALIZED_BUNDLES_VALIDATION = D3D12_DEBUG_FEATURE(0x04).value
D3D12_DEBUG_FEATURE_EMULATE_WINDOWS7                       = D3D12_DEBUG_FEATURE(0x08).value

D3D12_GPU_BASED_VALIDATION_FLAGS = ctypes.c_uint
D3D12_GPU_BASED_VALIDATION_FLAGS_NONE                   = D3D12_GPU_BASED_VALIDATION_FLAGS(0x00).value
D3D12_GPU_BASED_VALIDATION_FLAGS_DISABLE_STATE_TRACKING = D3D12_GPU_BASED_VALIDATION_FLAGS(0x01).value

D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS = ctypes.c_uint
D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAG_NONE                                           = D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS(0x00).value
D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAG_FRONT_LOAD_CREATE_TRACKING_ONLY_SHADERS        = D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS(0x01).value
D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAG_FRONT_LOAD_CREATE_UNGUARDED_VALIDATION_SHADERS = D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS(0x02).value
D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAG_FRONT_LOAD_CREATE_GUARDED_VALIDATION_SHADERS   = D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS(0x04).value
D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS_VALID_MASK                                    = D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS(0x07).value

D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE = ctypes.c_uint
D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE_NONE                 = D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE().value
D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE_STATE_TRACKING_ONLY  = D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE().value
D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE_UNGUARDED_VALIDATION = D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE().value
D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE_GUARDED_VALIDATION   = D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE().value
NUM_D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODES                 = D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE().value

D3D12_MESSAGE_CALLBACK_FLAGS = ctypes.c_uint
D3D12_MESSAGE_CALLBACK_FLAG_NONE      = D3D12_MESSAGE_CALLBACK_FLAGS(0x00).value
D3D12_MESSAGE_CALLBACK_IGNORE_FILTERS = D3D12_MESSAGE_CALLBACK_FLAGS(0x01).value

D3D12_MESSAGE_CATEGORY = ctypes.c_uint
D3D12_MESSAGE_CATEGORY_APPLICATION_DEFINED   = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_MISCELLANEOUS         = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_INITIALIZATION        = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_CLEANUP               = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_COMPILATION           = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_STATE_CREATION        = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_STATE_SETTING         = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_STATE_GETTING         = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_RESOURCE_MANIPULATION = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_EXECUTION             = D3D12_MESSAGE_CATEGORY().value
D3D12_MESSAGE_CATEGORY_SHADER                = D3D12_MESSAGE_CATEGORY().value

D3D12_MESSAGE_ID = ctypes.c_uint
D3D12_MESSAGE_ID_UNKNOWN                                                                                       = D3D12_MESSAGE_ID(0).value
D3D12_MESSAGE_ID_STRING_FROM_APPLICATION                                                                       = D3D12_MESSAGE_ID(1).value
D3D12_MESSAGE_ID_CORRUPTED_THIS                                                                                = D3D12_MESSAGE_ID(2).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER1                                                                          = D3D12_MESSAGE_ID(3).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER2                                                                          = D3D12_MESSAGE_ID(4).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER3                                                                          = D3D12_MESSAGE_ID(5).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER4                                                                          = D3D12_MESSAGE_ID(6).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER5                                                                          = D3D12_MESSAGE_ID(7).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER6                                                                          = D3D12_MESSAGE_ID(8).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER7                                                                          = D3D12_MESSAGE_ID(9).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER8                                                                          = D3D12_MESSAGE_ID(10).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER9                                                                          = D3D12_MESSAGE_ID(11).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER10                                                                         = D3D12_MESSAGE_ID(12).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER11                                                                         = D3D12_MESSAGE_ID(13).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER12                                                                         = D3D12_MESSAGE_ID(14).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER13                                                                         = D3D12_MESSAGE_ID(15).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER14                                                                         = D3D12_MESSAGE_ID(16).value
D3D12_MESSAGE_ID_CORRUPTED_PARAMETER15                                                                         = D3D12_MESSAGE_ID(17).value
D3D12_MESSAGE_ID_CORRUPTED_MULTITHREADING                                                                      = D3D12_MESSAGE_ID(18).value
D3D12_MESSAGE_ID_MESSAGE_REPORTING_OUTOFMEMORY                                                                 = D3D12_MESSAGE_ID(19).value
D3D12_MESSAGE_ID_GETPRIVATEDATA_MOREDATA                                                                       = D3D12_MESSAGE_ID(20).value
D3D12_MESSAGE_ID_SETPRIVATEDATA_INVALIDFREEDATA                                                                = D3D12_MESSAGE_ID(21).value
D3D12_MESSAGE_ID_SETPRIVATEDATA_CHANGINGPARAMS                                                                 = D3D12_MESSAGE_ID(24).value
D3D12_MESSAGE_ID_SETPRIVATEDATA_OUTOFMEMORY                                                                    = D3D12_MESSAGE_ID(25).value
D3D12_MESSAGE_ID_CREATESHADERRESOURCEVIEW_UNRECOGNIZEDFORMAT                                                   = D3D12_MESSAGE_ID(26).value
D3D12_MESSAGE_ID_CREATESHADERRESOURCEVIEW_INVALIDDESC                                                          = D3D12_MESSAGE_ID(27).value
D3D12_MESSAGE_ID_CREATESHADERRESOURCEVIEW_INVALIDFORMAT                                                        = D3D12_MESSAGE_ID(28).value
D3D12_MESSAGE_ID_CREATESHADERRESOURCEVIEW_INVALIDVIDEOPLANESLICE                                               = D3D12_MESSAGE_ID(29).value
D3D12_MESSAGE_ID_CREATESHADERRESOURCEVIEW_INVALIDPLANESLICE                                                    = D3D12_MESSAGE_ID(30).value
D3D12_MESSAGE_ID_CREATESHADERRESOURCEVIEW_INVALIDDIMENSIONS                                                    = D3D12_MESSAGE_ID(31).value
D3D12_MESSAGE_ID_CREATESHADERRESOURCEVIEW_INVALIDRESOURCE                                                      = D3D12_MESSAGE_ID(32).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_UNRECOGNIZEDFORMAT                                                     = D3D12_MESSAGE_ID(35).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_UNSUPPORTEDFORMAT                                                      = D3D12_MESSAGE_ID(36).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_INVALIDDESC                                                            = D3D12_MESSAGE_ID(37).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_INVALIDFORMAT                                                          = D3D12_MESSAGE_ID(38).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_INVALIDVIDEOPLANESLICE                                                 = D3D12_MESSAGE_ID(39).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_INVALIDPLANESLICE                                                      = D3D12_MESSAGE_ID(40).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_INVALIDDIMENSIONS                                                      = D3D12_MESSAGE_ID(41).value
D3D12_MESSAGE_ID_CREATERENDERTARGETVIEW_INVALIDRESOURCE                                                        = D3D12_MESSAGE_ID(42).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILVIEW_UNRECOGNIZEDFORMAT                                                     = D3D12_MESSAGE_ID(45).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILVIEW_INVALIDDESC                                                            = D3D12_MESSAGE_ID(46).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILVIEW_INVALIDFORMAT                                                          = D3D12_MESSAGE_ID(47).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILVIEW_INVALIDDIMENSIONS                                                      = D3D12_MESSAGE_ID(48).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILVIEW_INVALIDRESOURCE                                                        = D3D12_MESSAGE_ID(49).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_OUTOFMEMORY                                                                 = D3D12_MESSAGE_ID(52).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_TOOMANYELEMENTS                                                             = D3D12_MESSAGE_ID(53).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_INVALIDFORMAT                                                               = D3D12_MESSAGE_ID(54).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_INCOMPATIBLEFORMAT                                                          = D3D12_MESSAGE_ID(55).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_INVALIDSLOT                                                                 = D3D12_MESSAGE_ID(56).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_INVALIDINPUTSLOTCLASS                                                       = D3D12_MESSAGE_ID(57).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_STEPRATESLOTCLASSMISMATCH                                                   = D3D12_MESSAGE_ID(58).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_INVALIDSLOTCLASSCHANGE                                                      = D3D12_MESSAGE_ID(59).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_INVALIDSTEPRATECHANGE                                                       = D3D12_MESSAGE_ID(60).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_INVALIDALIGNMENT                                                            = D3D12_MESSAGE_ID(61).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_DUPLICATESEMANTIC                                                           = D3D12_MESSAGE_ID(62).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_UNPARSEABLEINPUTSIGNATURE                                                   = D3D12_MESSAGE_ID(63).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_NULLSEMANTIC                                                                = D3D12_MESSAGE_ID(64).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_MISSINGELEMENT                                                              = D3D12_MESSAGE_ID(65).value
D3D12_MESSAGE_ID_CREATEVERTEXSHADER_OUTOFMEMORY                                                                = D3D12_MESSAGE_ID(66).value
D3D12_MESSAGE_ID_CREATEVERTEXSHADER_INVALIDSHADERBYTECODE                                                      = D3D12_MESSAGE_ID(67).value
D3D12_MESSAGE_ID_CREATEVERTEXSHADER_INVALIDSHADERTYPE                                                          = D3D12_MESSAGE_ID(68).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADER_OUTOFMEMORY                                                              = D3D12_MESSAGE_ID(69).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADER_INVALIDSHADERBYTECODE                                                    = D3D12_MESSAGE_ID(70).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADER_INVALIDSHADERTYPE                                                        = D3D12_MESSAGE_ID(71).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_OUTOFMEMORY                                              = D3D12_MESSAGE_ID(72).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDSHADERBYTECODE                                    = D3D12_MESSAGE_ID(73).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDSHADERTYPE                                        = D3D12_MESSAGE_ID(74).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDNUMENTRIES                                        = D3D12_MESSAGE_ID(75).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_OUTPUTSTREAMSTRIDEUNUSED                                 = D3D12_MESSAGE_ID(76).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_OUTPUTSLOT0EXPECTED                                      = D3D12_MESSAGE_ID(79).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDOUTPUTSLOT                                        = D3D12_MESSAGE_ID(80).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_ONLYONEELEMENTPERSLOT                                    = D3D12_MESSAGE_ID(81).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDCOMPONENTCOUNT                                    = D3D12_MESSAGE_ID(82).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDSTARTCOMPONENTANDCOMPONENTCOUNT                   = D3D12_MESSAGE_ID(83).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDGAPDEFINITION                                     = D3D12_MESSAGE_ID(84).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_REPEATEDOUTPUT                                           = D3D12_MESSAGE_ID(85).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDOUTPUTSTREAMSTRIDE                                = D3D12_MESSAGE_ID(86).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_MISSINGSEMANTIC                                          = D3D12_MESSAGE_ID(87).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_MASKMISMATCH                                             = D3D12_MESSAGE_ID(88).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_CANTHAVEONLYGAPS                                         = D3D12_MESSAGE_ID(89).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_DECLTOOCOMPLEX                                           = D3D12_MESSAGE_ID(90).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_MISSINGOUTPUTSIGNATURE                                   = D3D12_MESSAGE_ID(91).value
D3D12_MESSAGE_ID_CREATEPIXELSHADER_OUTOFMEMORY                                                                 = D3D12_MESSAGE_ID(92).value
D3D12_MESSAGE_ID_CREATEPIXELSHADER_INVALIDSHADERBYTECODE                                                       = D3D12_MESSAGE_ID(93).value
D3D12_MESSAGE_ID_CREATEPIXELSHADER_INVALIDSHADERTYPE                                                           = D3D12_MESSAGE_ID(94).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_INVALIDFILLMODE                                                         = D3D12_MESSAGE_ID(95).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_INVALIDCULLMODE                                                         = D3D12_MESSAGE_ID(96).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_INVALIDDEPTHBIASCLAMP                                                   = D3D12_MESSAGE_ID(97).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_INVALIDSLOPESCALEDDEPTHBIAS                                             = D3D12_MESSAGE_ID(98).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDDEPTHWRITEMASK                                                 = D3D12_MESSAGE_ID(100).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDDEPTHFUNC                                                      = D3D12_MESSAGE_ID(101).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDFRONTFACESTENCILFAILOP                                         = D3D12_MESSAGE_ID(102).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDFRONTFACESTENCILZFAILOP                                        = D3D12_MESSAGE_ID(103).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDFRONTFACESTENCILPASSOP                                         = D3D12_MESSAGE_ID(104).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDFRONTFACESTENCILFUNC                                           = D3D12_MESSAGE_ID(105).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDBACKFACESTENCILFAILOP                                          = D3D12_MESSAGE_ID(106).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDBACKFACESTENCILZFAILOP                                         = D3D12_MESSAGE_ID(107).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDBACKFACESTENCILPASSOP                                          = D3D12_MESSAGE_ID(108).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INVALIDBACKFACESTENCILFUNC                                            = D3D12_MESSAGE_ID(109).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDSRCBLEND                                                              = D3D12_MESSAGE_ID(111).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDDESTBLEND                                                             = D3D12_MESSAGE_ID(112).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDBLENDOP                                                               = D3D12_MESSAGE_ID(113).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDSRCBLENDALPHA                                                         = D3D12_MESSAGE_ID(114).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDDESTBLENDALPHA                                                        = D3D12_MESSAGE_ID(115).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDBLENDOPALPHA                                                          = D3D12_MESSAGE_ID(116).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDRENDERTARGETWRITEMASK                                                 = D3D12_MESSAGE_ID(117).value
D3D12_MESSAGE_ID_GET_PROGRAM_IDENTIFIER_ERROR                                                                  = D3D12_MESSAGE_ID(118).value
D3D12_MESSAGE_ID_GET_WORK_GRAPH_PROPERTIES_ERROR                                                               = D3D12_MESSAGE_ID(119).value
D3D12_MESSAGE_ID_SET_PROGRAM_ERROR                                                                             = D3D12_MESSAGE_ID(120).value
D3D12_MESSAGE_ID_CLEARDEPTHSTENCILVIEW_INVALID                                                                 = D3D12_MESSAGE_ID(135).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_ROOT_SIGNATURE_NOT_SET                                                      = D3D12_MESSAGE_ID(200).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_ROOT_SIGNATURE_MISMATCH                                                     = D3D12_MESSAGE_ID(201).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_VERTEX_BUFFER_NOT_SET                                                       = D3D12_MESSAGE_ID(202).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_VERTEX_BUFFER_STRIDE_TOO_SMALL                                              = D3D12_MESSAGE_ID(209).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_VERTEX_BUFFER_TOO_SMALL                                                     = D3D12_MESSAGE_ID(210).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_INDEX_BUFFER_NOT_SET                                                        = D3D12_MESSAGE_ID(211).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_INDEX_BUFFER_FORMAT_INVALID                                                 = D3D12_MESSAGE_ID(212).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_INDEX_BUFFER_TOO_SMALL                                                      = D3D12_MESSAGE_ID(213).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_INVALID_PRIMITIVETOPOLOGY                                                   = D3D12_MESSAGE_ID(219).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_VERTEX_STRIDE_UNALIGNED                                                     = D3D12_MESSAGE_ID(221).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_INDEX_OFFSET_UNALIGNED                                                      = D3D12_MESSAGE_ID(222).value
D3D12_MESSAGE_ID_DEVICE_REMOVAL_PROCESS_AT_FAULT                                                               = D3D12_MESSAGE_ID(232).value
D3D12_MESSAGE_ID_DEVICE_REMOVAL_PROCESS_POSSIBLY_AT_FAULT                                                      = D3D12_MESSAGE_ID(233).value
D3D12_MESSAGE_ID_DEVICE_REMOVAL_PROCESS_NOT_AT_FAULT                                                           = D3D12_MESSAGE_ID(234).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_TRAILING_DIGIT_IN_SEMANTIC                                                  = D3D12_MESSAGE_ID(239).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_TRAILING_DIGIT_IN_SEMANTIC                               = D3D12_MESSAGE_ID(240).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_TYPE_MISMATCH                                                               = D3D12_MESSAGE_ID(245).value
D3D12_MESSAGE_ID_CREATEINPUTLAYOUT_EMPTY_LAYOUT                                                                = D3D12_MESSAGE_ID(253).value
D3D12_MESSAGE_ID_LIVE_OBJECT_SUMMARY                                                                           = D3D12_MESSAGE_ID(255).value
D3D12_MESSAGE_ID_LIVE_DEVICE                                                                                   = D3D12_MESSAGE_ID(274).value
D3D12_MESSAGE_ID_LIVE_SWAPCHAIN                                                                                = D3D12_MESSAGE_ID(275).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILVIEW_INVALIDFLAGS                                                           = D3D12_MESSAGE_ID(276).value
D3D12_MESSAGE_ID_CREATEVERTEXSHADER_INVALIDCLASSLINKAGE                                                        = D3D12_MESSAGE_ID(277).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADER_INVALIDCLASSLINKAGE                                                      = D3D12_MESSAGE_ID(278).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDSTREAMTORASTERIZER                                = D3D12_MESSAGE_ID(280).value
D3D12_MESSAGE_ID_CREATEPIXELSHADER_INVALIDCLASSLINKAGE                                                         = D3D12_MESSAGE_ID(283).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDSTREAM                                            = D3D12_MESSAGE_ID(284).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_UNEXPECTEDENTRIES                                        = D3D12_MESSAGE_ID(285).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_UNEXPECTEDSTRIDES                                        = D3D12_MESSAGE_ID(286).value
D3D12_MESSAGE_ID_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_INVALIDNUMSTRIDES                                        = D3D12_MESSAGE_ID(287).value
D3D12_MESSAGE_ID_CREATEHULLSHADER_OUTOFMEMORY                                                                  = D3D12_MESSAGE_ID(289).value
D3D12_MESSAGE_ID_CREATEHULLSHADER_INVALIDSHADERBYTECODE                                                        = D3D12_MESSAGE_ID(290).value
D3D12_MESSAGE_ID_CREATEHULLSHADER_INVALIDSHADERTYPE                                                            = D3D12_MESSAGE_ID(291).value
D3D12_MESSAGE_ID_CREATEHULLSHADER_INVALIDCLASSLINKAGE                                                          = D3D12_MESSAGE_ID(292).value
D3D12_MESSAGE_ID_CREATEDOMAINSHADER_OUTOFMEMORY                                                                = D3D12_MESSAGE_ID(294).value
D3D12_MESSAGE_ID_CREATEDOMAINSHADER_INVALIDSHADERBYTECODE                                                      = D3D12_MESSAGE_ID(295).value
D3D12_MESSAGE_ID_CREATEDOMAINSHADER_INVALIDSHADERTYPE                                                          = D3D12_MESSAGE_ID(296).value
D3D12_MESSAGE_ID_CREATEDOMAINSHADER_INVALIDCLASSLINKAGE                                                        = D3D12_MESSAGE_ID(297).value
D3D12_MESSAGE_ID_RESOURCE_UNMAP_NOTMAPPED                                                                      = D3D12_MESSAGE_ID(310).value
D3D12_MESSAGE_ID_DEVICE_CHECKFEATURESUPPORT_MISMATCHED_DATA_SIZE                                               = D3D12_MESSAGE_ID(318).value
D3D12_MESSAGE_ID_CREATECOMPUTESHADER_OUTOFMEMORY                                                               = D3D12_MESSAGE_ID(321).value
D3D12_MESSAGE_ID_CREATECOMPUTESHADER_INVALIDSHADERBYTECODE                                                     = D3D12_MESSAGE_ID(322).value
D3D12_MESSAGE_ID_CREATECOMPUTESHADER_INVALIDCLASSLINKAGE                                                       = D3D12_MESSAGE_ID(323).value
D3D12_MESSAGE_ID_DEVICE_CREATEVERTEXSHADER_DOUBLEFLOATOPSNOTSUPPORTED                                          = D3D12_MESSAGE_ID(331).value
D3D12_MESSAGE_ID_DEVICE_CREATEHULLSHADER_DOUBLEFLOATOPSNOTSUPPORTED                                            = D3D12_MESSAGE_ID(332).value
D3D12_MESSAGE_ID_DEVICE_CREATEDOMAINSHADER_DOUBLEFLOATOPSNOTSUPPORTED                                          = D3D12_MESSAGE_ID(333).value
D3D12_MESSAGE_ID_DEVICE_CREATEGEOMETRYSHADER_DOUBLEFLOATOPSNOTSUPPORTED                                        = D3D12_MESSAGE_ID(334).value
D3D12_MESSAGE_ID_DEVICE_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_DOUBLEFLOATOPSNOTSUPPORTED                        = D3D12_MESSAGE_ID(335).value
D3D12_MESSAGE_ID_DEVICE_CREATEPIXELSHADER_DOUBLEFLOATOPSNOTSUPPORTED                                           = D3D12_MESSAGE_ID(336).value
D3D12_MESSAGE_ID_DEVICE_CREATECOMPUTESHADER_DOUBLEFLOATOPSNOTSUPPORTED                                         = D3D12_MESSAGE_ID(337).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_INVALIDRESOURCE                                                     = D3D12_MESSAGE_ID(340).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_INVALIDDESC                                                         = D3D12_MESSAGE_ID(341).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_INVALIDFORMAT                                                       = D3D12_MESSAGE_ID(342).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_INVALIDVIDEOPLANESLICE                                              = D3D12_MESSAGE_ID(343).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_INVALIDPLANESLICE                                                   = D3D12_MESSAGE_ID(344).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_INVALIDDIMENSIONS                                                   = D3D12_MESSAGE_ID(345).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_UNRECOGNIZEDFORMAT                                                  = D3D12_MESSAGE_ID(346).value
D3D12_MESSAGE_ID_CREATEUNORDEREDACCESSVIEW_INVALIDFLAGS                                                        = D3D12_MESSAGE_ID(354).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_INVALIDFORCEDSAMPLECOUNT                                                = D3D12_MESSAGE_ID(401).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_INVALIDLOGICOPS                                                              = D3D12_MESSAGE_ID(403).value
D3D12_MESSAGE_ID_DEVICE_CREATEVERTEXSHADER_DOUBLEEXTENSIONSNOTSUPPORTED                                        = D3D12_MESSAGE_ID(410).value
D3D12_MESSAGE_ID_DEVICE_CREATEHULLSHADER_DOUBLEEXTENSIONSNOTSUPPORTED                                          = D3D12_MESSAGE_ID(412).value
D3D12_MESSAGE_ID_DEVICE_CREATEDOMAINSHADER_DOUBLEEXTENSIONSNOTSUPPORTED                                        = D3D12_MESSAGE_ID(414).value
D3D12_MESSAGE_ID_DEVICE_CREATEGEOMETRYSHADER_DOUBLEEXTENSIONSNOTSUPPORTED                                      = D3D12_MESSAGE_ID(416).value
D3D12_MESSAGE_ID_DEVICE_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_DOUBLEEXTENSIONSNOTSUPPORTED                      = D3D12_MESSAGE_ID(418).value
D3D12_MESSAGE_ID_DEVICE_CREATEPIXELSHADER_DOUBLEEXTENSIONSNOTSUPPORTED                                         = D3D12_MESSAGE_ID(420).value
D3D12_MESSAGE_ID_DEVICE_CREATECOMPUTESHADER_DOUBLEEXTENSIONSNOTSUPPORTED                                       = D3D12_MESSAGE_ID(422).value
D3D12_MESSAGE_ID_DEVICE_CREATEVERTEXSHADER_UAVSNOTSUPPORTED                                                    = D3D12_MESSAGE_ID(425).value
D3D12_MESSAGE_ID_DEVICE_CREATEHULLSHADER_UAVSNOTSUPPORTED                                                      = D3D12_MESSAGE_ID(426).value
D3D12_MESSAGE_ID_DEVICE_CREATEDOMAINSHADER_UAVSNOTSUPPORTED                                                    = D3D12_MESSAGE_ID(427).value
D3D12_MESSAGE_ID_DEVICE_CREATEGEOMETRYSHADER_UAVSNOTSUPPORTED                                                  = D3D12_MESSAGE_ID(428).value
D3D12_MESSAGE_ID_DEVICE_CREATEGEOMETRYSHADERWITHSTREAMOUTPUT_UAVSNOTSUPPORTED                                  = D3D12_MESSAGE_ID(429).value
D3D12_MESSAGE_ID_DEVICE_CREATEPIXELSHADER_UAVSNOTSUPPORTED                                                     = D3D12_MESSAGE_ID(430).value
D3D12_MESSAGE_ID_DEVICE_CREATECOMPUTESHADER_UAVSNOTSUPPORTED                                                   = D3D12_MESSAGE_ID(431).value
D3D12_MESSAGE_ID_DEVICE_CLEARVIEW_INVALIDSOURCERECT                                                            = D3D12_MESSAGE_ID(447).value
D3D12_MESSAGE_ID_DEVICE_CLEARVIEW_EMPTYRECT                                                                    = D3D12_MESSAGE_ID(448).value
D3D12_MESSAGE_ID_UPDATETILEMAPPINGS_INVALID_PARAMETER                                                          = D3D12_MESSAGE_ID(493).value
D3D12_MESSAGE_ID_COPYTILEMAPPINGS_INVALID_PARAMETER                                                            = D3D12_MESSAGE_ID(494).value
D3D12_MESSAGE_ID_CREATEDEVICE_INVALIDARGS                                                                      = D3D12_MESSAGE_ID(506).value
D3D12_MESSAGE_ID_CREATEDEVICE_WARNING                                                                          = D3D12_MESSAGE_ID(507).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_TYPE                                                                 = D3D12_MESSAGE_ID(519).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_NULL_POINTER                                                                 = D3D12_MESSAGE_ID(520).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_SUBRESOURCE                                                          = D3D12_MESSAGE_ID(521).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_RESERVED_BITS                                                                = D3D12_MESSAGE_ID(522).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_MISSING_BIND_FLAGS                                                           = D3D12_MESSAGE_ID(523).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_MISMATCHING_MISC_FLAGS                                                       = D3D12_MESSAGE_ID(524).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_MATCHING_STATES                                                              = D3D12_MESSAGE_ID(525).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_COMBINATION                                                          = D3D12_MESSAGE_ID(526).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_BEFORE_AFTER_MISMATCH                                                        = D3D12_MESSAGE_ID(527).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_RESOURCE                                                             = D3D12_MESSAGE_ID(528).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_SAMPLE_COUNT                                                                 = D3D12_MESSAGE_ID(529).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_FLAGS                                                                = D3D12_MESSAGE_ID(530).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_COMBINED_FLAGS                                                       = D3D12_MESSAGE_ID(531).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_FLAGS_FOR_FORMAT                                                     = D3D12_MESSAGE_ID(532).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_SPLIT_BARRIER                                                        = D3D12_MESSAGE_ID(533).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_UNMATCHED_END                                                                = D3D12_MESSAGE_ID(534).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_UNMATCHED_BEGIN                                                              = D3D12_MESSAGE_ID(535).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_FLAG                                                                 = D3D12_MESSAGE_ID(536).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_COMMAND_LIST_TYPE                                                    = D3D12_MESSAGE_ID(537).value
D3D12_MESSAGE_ID_INVALID_SUBRESOURCE_STATE                                                                     = D3D12_MESSAGE_ID(538).value
D3D12_MESSAGE_ID_COMMAND_ALLOCATOR_CONTENTION                                                                  = D3D12_MESSAGE_ID(540).value
D3D12_MESSAGE_ID_COMMAND_ALLOCATOR_RESET                                                                       = D3D12_MESSAGE_ID(541).value
D3D12_MESSAGE_ID_COMMAND_ALLOCATOR_RESET_BUNDLE                                                                = D3D12_MESSAGE_ID(542).value
D3D12_MESSAGE_ID_COMMAND_ALLOCATOR_CANNOT_RESET                                                                = D3D12_MESSAGE_ID(543).value
D3D12_MESSAGE_ID_COMMAND_LIST_OPEN                                                                             = D3D12_MESSAGE_ID(544).value
D3D12_MESSAGE_ID_INVALID_BUNDLE_API                                                                            = D3D12_MESSAGE_ID(546).value
D3D12_MESSAGE_ID_COMMAND_LIST_CLOSED                                                                           = D3D12_MESSAGE_ID(547).value
D3D12_MESSAGE_ID_WRONG_COMMAND_ALLOCATOR_TYPE                                                                  = D3D12_MESSAGE_ID(549).value
D3D12_MESSAGE_ID_COMMAND_ALLOCATOR_SYNC                                                                        = D3D12_MESSAGE_ID(552).value
D3D12_MESSAGE_ID_COMMAND_LIST_SYNC                                                                             = D3D12_MESSAGE_ID(553).value
D3D12_MESSAGE_ID_SET_DESCRIPTOR_HEAP_INVALID                                                                   = D3D12_MESSAGE_ID(554).value
D3D12_MESSAGE_ID_CREATE_COMMANDQUEUE                                                                           = D3D12_MESSAGE_ID(557).value
D3D12_MESSAGE_ID_CREATE_COMMANDALLOCATOR                                                                       = D3D12_MESSAGE_ID(558).value
D3D12_MESSAGE_ID_CREATE_PIPELINESTATE                                                                          = D3D12_MESSAGE_ID(559).value
D3D12_MESSAGE_ID_CREATE_COMMANDLIST12                                                                          = D3D12_MESSAGE_ID(560).value
D3D12_MESSAGE_ID_CREATE_RESOURCE                                                                               = D3D12_MESSAGE_ID(562).value
D3D12_MESSAGE_ID_CREATE_DESCRIPTORHEAP                                                                         = D3D12_MESSAGE_ID(563).value
D3D12_MESSAGE_ID_CREATE_ROOTSIGNATURE                                                                          = D3D12_MESSAGE_ID(564).value
D3D12_MESSAGE_ID_CREATE_LIBRARY                                                                                = D3D12_MESSAGE_ID(565).value
D3D12_MESSAGE_ID_CREATE_HEAP                                                                                   = D3D12_MESSAGE_ID(566).value
D3D12_MESSAGE_ID_CREATE_MONITOREDFENCE                                                                         = D3D12_MESSAGE_ID(567).value
D3D12_MESSAGE_ID_CREATE_QUERYHEAP                                                                              = D3D12_MESSAGE_ID(568).value
D3D12_MESSAGE_ID_CREATE_COMMANDSIGNATURE                                                                       = D3D12_MESSAGE_ID(569).value
D3D12_MESSAGE_ID_LIVE_COMMANDQUEUE                                                                             = D3D12_MESSAGE_ID(570).value
D3D12_MESSAGE_ID_LIVE_COMMANDALLOCATOR                                                                         = D3D12_MESSAGE_ID(571).value
D3D12_MESSAGE_ID_LIVE_PIPELINESTATE                                                                            = D3D12_MESSAGE_ID(572).value
D3D12_MESSAGE_ID_LIVE_COMMANDLIST12                                                                            = D3D12_MESSAGE_ID(573).value
D3D12_MESSAGE_ID_LIVE_RESOURCE                                                                                 = D3D12_MESSAGE_ID(575).value
D3D12_MESSAGE_ID_LIVE_DESCRIPTORHEAP                                                                           = D3D12_MESSAGE_ID(576).value
D3D12_MESSAGE_ID_LIVE_ROOTSIGNATURE                                                                            = D3D12_MESSAGE_ID(577).value
D3D12_MESSAGE_ID_LIVE_LIBRARY                                                                                  = D3D12_MESSAGE_ID(578).value
D3D12_MESSAGE_ID_LIVE_HEAP                                                                                     = D3D12_MESSAGE_ID(579).value
D3D12_MESSAGE_ID_LIVE_MONITOREDFENCE                                                                           = D3D12_MESSAGE_ID(580).value
D3D12_MESSAGE_ID_LIVE_QUERYHEAP                                                                                = D3D12_MESSAGE_ID(581).value
D3D12_MESSAGE_ID_LIVE_COMMANDSIGNATURE                                                                         = D3D12_MESSAGE_ID(582).value
D3D12_MESSAGE_ID_DESTROY_COMMANDQUEUE                                                                          = D3D12_MESSAGE_ID(583).value
D3D12_MESSAGE_ID_DESTROY_COMMANDALLOCATOR                                                                      = D3D12_MESSAGE_ID(584).value
D3D12_MESSAGE_ID_DESTROY_PIPELINESTATE                                                                         = D3D12_MESSAGE_ID(585).value
D3D12_MESSAGE_ID_DESTROY_COMMANDLIST12                                                                         = D3D12_MESSAGE_ID(586).value
D3D12_MESSAGE_ID_DESTROY_RESOURCE                                                                              = D3D12_MESSAGE_ID(588).value
D3D12_MESSAGE_ID_DESTROY_DESCRIPTORHEAP                                                                        = D3D12_MESSAGE_ID(589).value
D3D12_MESSAGE_ID_DESTROY_ROOTSIGNATURE                                                                         = D3D12_MESSAGE_ID(590).value
D3D12_MESSAGE_ID_DESTROY_LIBRARY                                                                               = D3D12_MESSAGE_ID(591).value
D3D12_MESSAGE_ID_DESTROY_HEAP                                                                                  = D3D12_MESSAGE_ID(592).value
D3D12_MESSAGE_ID_DESTROY_MONITOREDFENCE                                                                        = D3D12_MESSAGE_ID(593).value
D3D12_MESSAGE_ID_DESTROY_QUERYHEAP                                                                             = D3D12_MESSAGE_ID(594).value
D3D12_MESSAGE_ID_DESTROY_COMMANDSIGNATURE                                                                      = D3D12_MESSAGE_ID(595).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDDIMENSIONS                                                              = D3D12_MESSAGE_ID(597).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDMISCFLAGS                                                               = D3D12_MESSAGE_ID(599).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDARG_RETURN                                                              = D3D12_MESSAGE_ID(602).value
D3D12_MESSAGE_ID_CREATERESOURCE_OUTOFMEMORY_RETURN                                                             = D3D12_MESSAGE_ID(603).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDDESC                                                                    = D3D12_MESSAGE_ID(604).value
D3D12_MESSAGE_ID_POSSIBLY_INVALID_SUBRESOURCE_STATE                                                            = D3D12_MESSAGE_ID(607).value
D3D12_MESSAGE_ID_INVALID_USE_OF_NON_RESIDENT_RESOURCE                                                          = D3D12_MESSAGE_ID(608).value
D3D12_MESSAGE_ID_POSSIBLE_INVALID_USE_OF_NON_RESIDENT_RESOURCE                                                 = D3D12_MESSAGE_ID(609).value
D3D12_MESSAGE_ID_BUNDLE_PIPELINE_STATE_MISMATCH                                                                = D3D12_MESSAGE_ID(610).value
D3D12_MESSAGE_ID_PRIMITIVE_TOPOLOGY_MISMATCH_PIPELINE_STATE                                                    = D3D12_MESSAGE_ID(611).value
D3D12_MESSAGE_ID_RENDER_TARGET_FORMAT_MISMATCH_PIPELINE_STATE                                                  = D3D12_MESSAGE_ID(613).value
D3D12_MESSAGE_ID_RENDER_TARGET_SAMPLE_DESC_MISMATCH_PIPELINE_STATE                                             = D3D12_MESSAGE_ID(614).value
D3D12_MESSAGE_ID_DEPTH_STENCIL_FORMAT_MISMATCH_PIPELINE_STATE                                                  = D3D12_MESSAGE_ID(615).value
D3D12_MESSAGE_ID_DEPTH_STENCIL_SAMPLE_DESC_MISMATCH_PIPELINE_STATE                                             = D3D12_MESSAGE_ID(616).value
D3D12_MESSAGE_ID_CREATESHADER_INVALIDBYTECODE                                                                  = D3D12_MESSAGE_ID(622).value
D3D12_MESSAGE_ID_CREATEHEAP_NULLDESC                                                                           = D3D12_MESSAGE_ID(623).value
D3D12_MESSAGE_ID_CREATEHEAP_INVALIDSIZE                                                                        = D3D12_MESSAGE_ID(624).value
D3D12_MESSAGE_ID_CREATEHEAP_UNRECOGNIZEDHEAPTYPE                                                               = D3D12_MESSAGE_ID(625).value
D3D12_MESSAGE_ID_CREATEHEAP_UNRECOGNIZEDCPUPAGEPROPERTIES                                                      = D3D12_MESSAGE_ID(626).value
D3D12_MESSAGE_ID_CREATEHEAP_UNRECOGNIZEDMEMORYPOOL                                                             = D3D12_MESSAGE_ID(627).value
D3D12_MESSAGE_ID_CREATEHEAP_INVALIDPROPERTIES                                                                  = D3D12_MESSAGE_ID(628).value
D3D12_MESSAGE_ID_CREATEHEAP_INVALIDALIGNMENT                                                                   = D3D12_MESSAGE_ID(629).value
D3D12_MESSAGE_ID_CREATEHEAP_UNRECOGNIZEDMISCFLAGS                                                              = D3D12_MESSAGE_ID(630).value
D3D12_MESSAGE_ID_CREATEHEAP_INVALIDMISCFLAGS                                                                   = D3D12_MESSAGE_ID(631).value
D3D12_MESSAGE_ID_CREATEHEAP_INVALIDARG_RETURN                                                                  = D3D12_MESSAGE_ID(632).value
D3D12_MESSAGE_ID_CREATEHEAP_OUTOFMEMORY_RETURN                                                                 = D3D12_MESSAGE_ID(633).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_NULLHEAPPROPERTIES                                                      = D3D12_MESSAGE_ID(634).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_UNRECOGNIZEDHEAPTYPE                                                    = D3D12_MESSAGE_ID(635).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_UNRECOGNIZEDCPUPAGEPROPERTIES                                           = D3D12_MESSAGE_ID(636).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_UNRECOGNIZEDMEMORYPOOL                                                  = D3D12_MESSAGE_ID(637).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_INVALIDHEAPPROPERTIES                                                   = D3D12_MESSAGE_ID(638).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_UNRECOGNIZEDHEAPMISCFLAGS                                               = D3D12_MESSAGE_ID(639).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_INVALIDHEAPMISCFLAGS                                                    = D3D12_MESSAGE_ID(640).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_INVALIDARG_RETURN                                                       = D3D12_MESSAGE_ID(641).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_OUTOFMEMORY_RETURN                                                      = D3D12_MESSAGE_ID(642).value
D3D12_MESSAGE_ID_GETCUSTOMHEAPPROPERTIES_UNRECOGNIZEDHEAPTYPE                                                  = D3D12_MESSAGE_ID(643).value
D3D12_MESSAGE_ID_GETCUSTOMHEAPPROPERTIES_INVALIDHEAPTYPE                                                       = D3D12_MESSAGE_ID(644).value
D3D12_MESSAGE_ID_CREATE_DESCRIPTOR_HEAP_INVALID_DESC                                                           = D3D12_MESSAGE_ID(645).value
D3D12_MESSAGE_ID_INVALID_DESCRIPTOR_HANDLE                                                                     = D3D12_MESSAGE_ID(646).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_INVALID_CONSERVATIVERASTERMODE                                          = D3D12_MESSAGE_ID(647).value
D3D12_MESSAGE_ID_CREATE_CONSTANT_BUFFER_VIEW_INVALID_RESOURCE                                                  = D3D12_MESSAGE_ID(649).value
D3D12_MESSAGE_ID_CREATE_CONSTANT_BUFFER_VIEW_INVALID_DESC                                                      = D3D12_MESSAGE_ID(650).value
D3D12_MESSAGE_ID_CREATE_UNORDEREDACCESS_VIEW_INVALID_COUNTER_USAGE                                             = D3D12_MESSAGE_ID(652).value
D3D12_MESSAGE_ID_COPY_DESCRIPTORS_INVALID_RANGES                                                               = D3D12_MESSAGE_ID(653).value
D3D12_MESSAGE_ID_COPY_DESCRIPTORS_WRITE_ONLY_DESCRIPTOR                                                        = D3D12_MESSAGE_ID(654).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_RTV_FORMAT_NOT_UNKNOWN                                            = D3D12_MESSAGE_ID(655).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INVALID_RENDER_TARGET_COUNT                                       = D3D12_MESSAGE_ID(656).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_VERTEX_SHADER_NOT_SET                                             = D3D12_MESSAGE_ID(657).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INPUTLAYOUT_NOT_SET                                               = D3D12_MESSAGE_ID(658).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_HS_DS_SIGNATURE_MISMATCH                           = D3D12_MESSAGE_ID(659).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_REGISTERINDEX                                      = D3D12_MESSAGE_ID(660).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_COMPONENTTYPE                                      = D3D12_MESSAGE_ID(661).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_REGISTERMASK                                       = D3D12_MESSAGE_ID(662).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_SYSTEMVALUE                                        = D3D12_MESSAGE_ID(663).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_NEVERWRITTEN_ALWAYSREADS                           = D3D12_MESSAGE_ID(664).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_MINPRECISION                                       = D3D12_MESSAGE_ID(665).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_LINKAGE_SEMANTICNAME_NOT_FOUND                             = D3D12_MESSAGE_ID(666).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_HS_XOR_DS_MISMATCH                                                = D3D12_MESSAGE_ID(667).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_HULL_SHADER_INPUT_TOPOLOGY_MISMATCH                               = D3D12_MESSAGE_ID(668).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_HS_DS_CONTROL_POINT_COUNT_MISMATCH                                = D3D12_MESSAGE_ID(669).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_HS_DS_TESSELLATOR_DOMAIN_MISMATCH                                 = D3D12_MESSAGE_ID(670).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INVALID_USE_OF_CENTER_MULTISAMPLE_PATTERN                         = D3D12_MESSAGE_ID(671).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INVALID_USE_OF_FORCED_SAMPLE_COUNT                                = D3D12_MESSAGE_ID(672).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INVALID_PRIMITIVETOPOLOGY                                         = D3D12_MESSAGE_ID(673).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INVALID_SYSTEMVALUE                                               = D3D12_MESSAGE_ID(674).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_OM_DUAL_SOURCE_BLENDING_CAN_ONLY_HAVE_RENDER_TARGET_0             = D3D12_MESSAGE_ID(675).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_OM_RENDER_TARGET_DOES_NOT_SUPPORT_BLENDING                        = D3D12_MESSAGE_ID(676).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_PS_OUTPUT_TYPE_MISMATCH                                           = D3D12_MESSAGE_ID(677).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_OM_RENDER_TARGET_DOES_NOT_SUPPORT_LOGIC_OPS                       = D3D12_MESSAGE_ID(678).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_RENDERTARGETVIEW_NOT_SET                                          = D3D12_MESSAGE_ID(679).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_DEPTHSTENCILVIEW_NOT_SET                                          = D3D12_MESSAGE_ID(680).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_GS_INPUT_PRIMITIVE_MISMATCH                                       = D3D12_MESSAGE_ID(681).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_POSITION_NOT_PRESENT                                              = D3D12_MESSAGE_ID(682).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_MISSING_ROOT_SIGNATURE_FLAGS                                      = D3D12_MESSAGE_ID(683).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INVALID_INDEX_BUFFER_PROPERTIES                                   = D3D12_MESSAGE_ID(684).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INVALID_SAMPLE_DESC                                               = D3D12_MESSAGE_ID(685).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_HS_ROOT_SIGNATURE_MISMATCH                                        = D3D12_MESSAGE_ID(686).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_DS_ROOT_SIGNATURE_MISMATCH                                        = D3D12_MESSAGE_ID(687).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_VS_ROOT_SIGNATURE_MISMATCH                                        = D3D12_MESSAGE_ID(688).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_GS_ROOT_SIGNATURE_MISMATCH                                        = D3D12_MESSAGE_ID(689).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_PS_ROOT_SIGNATURE_MISMATCH                                        = D3D12_MESSAGE_ID(690).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_MISSING_ROOT_SIGNATURE                                            = D3D12_MESSAGE_ID(691).value
D3D12_MESSAGE_ID_EXECUTE_BUNDLE_OPEN_BUNDLE                                                                    = D3D12_MESSAGE_ID(692).value
D3D12_MESSAGE_ID_EXECUTE_BUNDLE_DESCRIPTOR_HEAP_MISMATCH                                                       = D3D12_MESSAGE_ID(693).value
D3D12_MESSAGE_ID_EXECUTE_BUNDLE_TYPE                                                                           = D3D12_MESSAGE_ID(694).value
D3D12_MESSAGE_ID_DRAW_EMPTY_SCISSOR_RECTANGLE                                                                  = D3D12_MESSAGE_ID(695).value
D3D12_MESSAGE_ID_CREATE_ROOT_SIGNATURE_BLOB_NOT_FOUND                                                          = D3D12_MESSAGE_ID(696).value
D3D12_MESSAGE_ID_CREATE_ROOT_SIGNATURE_DESERIALIZE_FAILED                                                      = D3D12_MESSAGE_ID(697).value
D3D12_MESSAGE_ID_CREATE_ROOT_SIGNATURE_INVALID_CONFIGURATION                                                   = D3D12_MESSAGE_ID(698).value
D3D12_MESSAGE_ID_CREATE_ROOT_SIGNATURE_NOT_SUPPORTED_ON_DEVICE                                                 = D3D12_MESSAGE_ID(699).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_NULLRESOURCEPROPERTIES                                                  = D3D12_MESSAGE_ID(700).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_NULLHEAP                                                                = D3D12_MESSAGE_ID(701).value
D3D12_MESSAGE_ID_GETRESOURCEALLOCATIONINFO_INVALIDRDESCS                                                       = D3D12_MESSAGE_ID(702).value
D3D12_MESSAGE_ID_MAKERESIDENT_NULLOBJECTARRAY                                                                  = D3D12_MESSAGE_ID(703).value
D3D12_MESSAGE_ID_EVICT_NULLOBJECTARRAY                                                                         = D3D12_MESSAGE_ID(705).value
D3D12_MESSAGE_ID_SET_DESCRIPTOR_TABLE_INVALID                                                                  = D3D12_MESSAGE_ID(708).value
D3D12_MESSAGE_ID_SET_ROOT_CONSTANT_INVALID                                                                     = D3D12_MESSAGE_ID(709).value
D3D12_MESSAGE_ID_SET_ROOT_CONSTANT_BUFFER_VIEW_INVALID                                                         = D3D12_MESSAGE_ID(710).value
D3D12_MESSAGE_ID_SET_ROOT_SHADER_RESOURCE_VIEW_INVALID                                                         = D3D12_MESSAGE_ID(711).value
D3D12_MESSAGE_ID_SET_ROOT_UNORDERED_ACCESS_VIEW_INVALID                                                        = D3D12_MESSAGE_ID(712).value
D3D12_MESSAGE_ID_SET_VERTEX_BUFFERS_INVALID_DESC                                                               = D3D12_MESSAGE_ID(713).value
D3D12_MESSAGE_ID_SET_INDEX_BUFFER_INVALID_DESC                                                                 = D3D12_MESSAGE_ID(715).value
D3D12_MESSAGE_ID_SET_STREAM_OUTPUT_BUFFERS_INVALID_DESC                                                        = D3D12_MESSAGE_ID(717).value
D3D12_MESSAGE_ID_CREATERESOURCE_UNRECOGNIZEDDIMENSIONALITY                                                     = D3D12_MESSAGE_ID(718).value
D3D12_MESSAGE_ID_CREATERESOURCE_UNRECOGNIZEDLAYOUT                                                             = D3D12_MESSAGE_ID(719).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDDIMENSIONALITY                                                          = D3D12_MESSAGE_ID(720).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDALIGNMENT                                                               = D3D12_MESSAGE_ID(721).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDMIPLEVELS                                                               = D3D12_MESSAGE_ID(722).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDSAMPLEDESC                                                              = D3D12_MESSAGE_ID(723).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDLAYOUT                                                                  = D3D12_MESSAGE_ID(724).value
D3D12_MESSAGE_ID_SET_INDEX_BUFFER_INVALID                                                                      = D3D12_MESSAGE_ID(725).value
D3D12_MESSAGE_ID_SET_VERTEX_BUFFERS_INVALID                                                                    = D3D12_MESSAGE_ID(726).value
D3D12_MESSAGE_ID_SET_STREAM_OUTPUT_BUFFERS_INVALID                                                             = D3D12_MESSAGE_ID(727).value
D3D12_MESSAGE_ID_SET_RENDER_TARGETS_INVALID                                                                    = D3D12_MESSAGE_ID(728).value
D3D12_MESSAGE_ID_CREATEQUERY_HEAP_INVALID_PARAMETERS                                                           = D3D12_MESSAGE_ID(729).value
D3D12_MESSAGE_ID_BEGIN_END_QUERY_INVALID_PARAMETERS                                                            = D3D12_MESSAGE_ID(731).value
D3D12_MESSAGE_ID_CLOSE_COMMAND_LIST_OPEN_QUERY                                                                 = D3D12_MESSAGE_ID(732).value
D3D12_MESSAGE_ID_RESOLVE_QUERY_DATA_INVALID_PARAMETERS                                                         = D3D12_MESSAGE_ID(733).value
D3D12_MESSAGE_ID_SET_PREDICATION_INVALID_PARAMETERS                                                            = D3D12_MESSAGE_ID(734).value
D3D12_MESSAGE_ID_TIMESTAMPS_NOT_SUPPORTED                                                                      = D3D12_MESSAGE_ID(735).value
D3D12_MESSAGE_ID_CREATERESOURCE_UNRECOGNIZEDFORMAT                                                             = D3D12_MESSAGE_ID(737).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDFORMAT                                                                  = D3D12_MESSAGE_ID(738).value
D3D12_MESSAGE_ID_GETCOPYABLEFOOTPRINTS_INVALIDSUBRESOURCERANGE                                                 = D3D12_MESSAGE_ID(739).value
D3D12_MESSAGE_ID_GETCOPYABLEFOOTPRINTS_INVALIDBASEOFFSET                                                       = D3D12_MESSAGE_ID(740).value
D3D12_MESSAGE_ID_GETCOPYABLELAYOUT_INVALIDSUBRESOURCERANGE                                                     = D3D12_MESSAGE_ID(739).value
D3D12_MESSAGE_ID_GETCOPYABLELAYOUT_INVALIDBASEOFFSET                                                           = D3D12_MESSAGE_ID(740).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_INVALID_HEAP                                                                 = D3D12_MESSAGE_ID(741).value
D3D12_MESSAGE_ID_CREATE_SAMPLER_INVALID                                                                        = D3D12_MESSAGE_ID(742).value
D3D12_MESSAGE_ID_CREATECOMMANDSIGNATURE_INVALID                                                                = D3D12_MESSAGE_ID(743).value
D3D12_MESSAGE_ID_EXECUTE_INDIRECT_INVALID_PARAMETERS                                                           = D3D12_MESSAGE_ID(744).value
D3D12_MESSAGE_ID_GETGPUVIRTUALADDRESS_INVALID_RESOURCE_DIMENSION                                               = D3D12_MESSAGE_ID(745).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDCLEARVALUE                                                              = D3D12_MESSAGE_ID(815).value
D3D12_MESSAGE_ID_CREATERESOURCE_UNRECOGNIZEDCLEARVALUEFORMAT                                                   = D3D12_MESSAGE_ID(816).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDCLEARVALUEFORMAT                                                        = D3D12_MESSAGE_ID(817).value
D3D12_MESSAGE_ID_CREATERESOURCE_CLEARVALUEDENORMFLUSH                                                          = D3D12_MESSAGE_ID(818).value
D3D12_MESSAGE_ID_CLEARRENDERTARGETVIEW_MISMATCHINGCLEARVALUE                                                   = D3D12_MESSAGE_ID(820).value
D3D12_MESSAGE_ID_CLEARDEPTHSTENCILVIEW_MISMATCHINGCLEARVALUE                                                   = D3D12_MESSAGE_ID(821).value
D3D12_MESSAGE_ID_MAP_INVALIDHEAP                                                                               = D3D12_MESSAGE_ID(822).value
D3D12_MESSAGE_ID_UNMAP_INVALIDHEAP                                                                             = D3D12_MESSAGE_ID(823).value
D3D12_MESSAGE_ID_MAP_INVALIDRESOURCE                                                                           = D3D12_MESSAGE_ID(824).value
D3D12_MESSAGE_ID_UNMAP_INVALIDRESOURCE                                                                         = D3D12_MESSAGE_ID(825).value
D3D12_MESSAGE_ID_MAP_INVALIDSUBRESOURCE                                                                        = D3D12_MESSAGE_ID(826).value
D3D12_MESSAGE_ID_UNMAP_INVALIDSUBRESOURCE                                                                      = D3D12_MESSAGE_ID(827).value
D3D12_MESSAGE_ID_MAP_INVALIDRANGE                                                                              = D3D12_MESSAGE_ID(828).value
D3D12_MESSAGE_ID_UNMAP_INVALIDRANGE                                                                            = D3D12_MESSAGE_ID(829).value
D3D12_MESSAGE_ID_MAP_INVALIDDATAPOINTER                                                                        = D3D12_MESSAGE_ID(832).value
D3D12_MESSAGE_ID_MAP_INVALIDARG_RETURN                                                                         = D3D12_MESSAGE_ID(833).value
D3D12_MESSAGE_ID_MAP_OUTOFMEMORY_RETURN                                                                        = D3D12_MESSAGE_ID(834).value
D3D12_MESSAGE_ID_EXECUTECOMMANDLISTS_BUNDLENOTSUPPORTED                                                        = D3D12_MESSAGE_ID(835).value
D3D12_MESSAGE_ID_EXECUTECOMMANDLISTS_COMMANDLISTMISMATCH                                                       = D3D12_MESSAGE_ID(836).value
D3D12_MESSAGE_ID_EXECUTECOMMANDLISTS_OPENCOMMANDLIST                                                           = D3D12_MESSAGE_ID(837).value
D3D12_MESSAGE_ID_EXECUTECOMMANDLISTS_FAILEDCOMMANDLIST                                                         = D3D12_MESSAGE_ID(838).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_NULLDST                                                                      = D3D12_MESSAGE_ID(839).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_INVALIDDSTRESOURCEDIMENSION                                                  = D3D12_MESSAGE_ID(840).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_DSTRANGEOUTOFBOUNDS                                                          = D3D12_MESSAGE_ID(841).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_NULLSRC                                                                      = D3D12_MESSAGE_ID(842).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_INVALIDSRCRESOURCEDIMENSION                                                  = D3D12_MESSAGE_ID(843).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_SRCRANGEOUTOFBOUNDS                                                          = D3D12_MESSAGE_ID(844).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_INVALIDCOPYFLAGS                                                             = D3D12_MESSAGE_ID(845).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_NULLDST                                                                     = D3D12_MESSAGE_ID(846).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_UNRECOGNIZEDDSTTYPE                                                         = D3D12_MESSAGE_ID(847).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTRESOURCEDIMENSION                                                 = D3D12_MESSAGE_ID(848).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTRESOURCE                                                          = D3D12_MESSAGE_ID(849).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTSUBRESOURCE                                                       = D3D12_MESSAGE_ID(850).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTOFFSET                                                            = D3D12_MESSAGE_ID(851).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_UNRECOGNIZEDDSTFORMAT                                                       = D3D12_MESSAGE_ID(852).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTFORMAT                                                            = D3D12_MESSAGE_ID(853).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTDIMENSIONS                                                        = D3D12_MESSAGE_ID(854).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTROWPITCH                                                          = D3D12_MESSAGE_ID(855).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTPLACEMENT                                                         = D3D12_MESSAGE_ID(856).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTDSPLACEDFOOTPRINTFORMAT                                           = D3D12_MESSAGE_ID(857).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_DSTREGIONOUTOFBOUNDS                                                        = D3D12_MESSAGE_ID(858).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_NULLSRC                                                                     = D3D12_MESSAGE_ID(859).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_UNRECOGNIZEDSRCTYPE                                                         = D3D12_MESSAGE_ID(860).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCRESOURCEDIMENSION                                                 = D3D12_MESSAGE_ID(861).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCRESOURCE                                                          = D3D12_MESSAGE_ID(862).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCSUBRESOURCE                                                       = D3D12_MESSAGE_ID(863).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCOFFSET                                                            = D3D12_MESSAGE_ID(864).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_UNRECOGNIZEDSRCFORMAT                                                       = D3D12_MESSAGE_ID(865).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCFORMAT                                                            = D3D12_MESSAGE_ID(866).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCDIMENSIONS                                                        = D3D12_MESSAGE_ID(867).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCROWPITCH                                                          = D3D12_MESSAGE_ID(868).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCPLACEMENT                                                         = D3D12_MESSAGE_ID(869).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCDSPLACEDFOOTPRINTFORMAT                                           = D3D12_MESSAGE_ID(870).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_SRCREGIONOUTOFBOUNDS                                                        = D3D12_MESSAGE_ID(871).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDDSTCOORDINATES                                                       = D3D12_MESSAGE_ID(872).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDSRCBOX                                                               = D3D12_MESSAGE_ID(873).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_FORMATMISMATCH                                                              = D3D12_MESSAGE_ID(874).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_EMPTYBOX                                                                    = D3D12_MESSAGE_ID(875).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_INVALIDCOPYFLAGS                                                            = D3D12_MESSAGE_ID(876).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_INVALID_SUBRESOURCE_INDEX                                                  = D3D12_MESSAGE_ID(877).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_INVALID_FORMAT                                                             = D3D12_MESSAGE_ID(878).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_RESOURCE_MISMATCH                                                          = D3D12_MESSAGE_ID(879).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_INVALID_SAMPLE_COUNT                                                       = D3D12_MESSAGE_ID(880).value
D3D12_MESSAGE_ID_CREATECOMPUTEPIPELINESTATE_INVALID_SHADER                                                     = D3D12_MESSAGE_ID(881).value
D3D12_MESSAGE_ID_CREATECOMPUTEPIPELINESTATE_CS_ROOT_SIGNATURE_MISMATCH                                         = D3D12_MESSAGE_ID(882).value
D3D12_MESSAGE_ID_CREATECOMPUTEPIPELINESTATE_MISSING_ROOT_SIGNATURE                                             = D3D12_MESSAGE_ID(883).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_INVALIDCACHEDBLOB                                                         = D3D12_MESSAGE_ID(884).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_CACHEDBLOBADAPTERMISMATCH                                                 = D3D12_MESSAGE_ID(885).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_CACHEDBLOBDRIVERVERSIONMISMATCH                                           = D3D12_MESSAGE_ID(886).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_CACHEDBLOBDESCMISMATCH                                                    = D3D12_MESSAGE_ID(887).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_CACHEDBLOBIGNORED                                                         = D3D12_MESSAGE_ID(888).value
D3D12_MESSAGE_ID_WRITETOSUBRESOURCE_INVALIDHEAP                                                                = D3D12_MESSAGE_ID(889).value
D3D12_MESSAGE_ID_WRITETOSUBRESOURCE_INVALIDRESOURCE                                                            = D3D12_MESSAGE_ID(890).value
D3D12_MESSAGE_ID_WRITETOSUBRESOURCE_INVALIDBOX                                                                 = D3D12_MESSAGE_ID(891).value
D3D12_MESSAGE_ID_WRITETOSUBRESOURCE_INVALIDSUBRESOURCE                                                         = D3D12_MESSAGE_ID(892).value
D3D12_MESSAGE_ID_WRITETOSUBRESOURCE_EMPTYBOX                                                                   = D3D12_MESSAGE_ID(893).value
D3D12_MESSAGE_ID_READFROMSUBRESOURCE_INVALIDHEAP                                                               = D3D12_MESSAGE_ID(894).value
D3D12_MESSAGE_ID_READFROMSUBRESOURCE_INVALIDRESOURCE                                                           = D3D12_MESSAGE_ID(895).value
D3D12_MESSAGE_ID_READFROMSUBRESOURCE_INVALIDBOX                                                                = D3D12_MESSAGE_ID(896).value
D3D12_MESSAGE_ID_READFROMSUBRESOURCE_INVALIDSUBRESOURCE                                                        = D3D12_MESSAGE_ID(897).value
D3D12_MESSAGE_ID_READFROMSUBRESOURCE_EMPTYBOX                                                                  = D3D12_MESSAGE_ID(898).value
D3D12_MESSAGE_ID_TOO_MANY_NODES_SPECIFIED                                                                      = D3D12_MESSAGE_ID(899).value
D3D12_MESSAGE_ID_INVALID_NODE_INDEX                                                                            = D3D12_MESSAGE_ID(900).value
D3D12_MESSAGE_ID_GETHEAPPROPERTIES_INVALIDRESOURCE                                                             = D3D12_MESSAGE_ID(901).value
D3D12_MESSAGE_ID_NODE_MASK_MISMATCH                                                                            = D3D12_MESSAGE_ID(902).value
D3D12_MESSAGE_ID_COMMAND_LIST_OUTOFMEMORY                                                                      = D3D12_MESSAGE_ID(903).value
D3D12_MESSAGE_ID_COMMAND_LIST_MULTIPLE_SWAPCHAIN_BUFFER_REFERENCES                                             = D3D12_MESSAGE_ID(904).value
D3D12_MESSAGE_ID_COMMAND_LIST_TOO_MANY_SWAPCHAIN_REFERENCES                                                    = D3D12_MESSAGE_ID(905).value
D3D12_MESSAGE_ID_COMMAND_QUEUE_TOO_MANY_SWAPCHAIN_REFERENCES                                                   = D3D12_MESSAGE_ID(906).value
D3D12_MESSAGE_ID_EXECUTECOMMANDLISTS_WRONGSWAPCHAINBUFFERREFERENCE                                             = D3D12_MESSAGE_ID(907).value
D3D12_MESSAGE_ID_COMMAND_LIST_SETRENDERTARGETS_INVALIDNUMRENDERTARGETS                                         = D3D12_MESSAGE_ID(908).value
D3D12_MESSAGE_ID_CREATE_QUEUE_INVALID_TYPE                                                                     = D3D12_MESSAGE_ID(909).value
D3D12_MESSAGE_ID_CREATE_QUEUE_INVALID_FLAGS                                                                    = D3D12_MESSAGE_ID(910).value
D3D12_MESSAGE_ID_CREATESHAREDRESOURCE_INVALIDFLAGS                                                             = D3D12_MESSAGE_ID(911).value
D3D12_MESSAGE_ID_CREATESHAREDRESOURCE_INVALIDFORMAT                                                            = D3D12_MESSAGE_ID(912).value
D3D12_MESSAGE_ID_CREATESHAREDHEAP_INVALIDFLAGS                                                                 = D3D12_MESSAGE_ID(913).value
D3D12_MESSAGE_ID_REFLECTSHAREDPROPERTIES_UNRECOGNIZEDPROPERTIES                                                = D3D12_MESSAGE_ID(914).value
D3D12_MESSAGE_ID_REFLECTSHAREDPROPERTIES_INVALIDSIZE                                                           = D3D12_MESSAGE_ID(915).value
D3D12_MESSAGE_ID_REFLECTSHAREDPROPERTIES_INVALIDOBJECT                                                         = D3D12_MESSAGE_ID(916).value
D3D12_MESSAGE_ID_KEYEDMUTEX_INVALIDOBJECT                                                                      = D3D12_MESSAGE_ID(917).value
D3D12_MESSAGE_ID_KEYEDMUTEX_INVALIDKEY                                                                         = D3D12_MESSAGE_ID(918).value
D3D12_MESSAGE_ID_KEYEDMUTEX_WRONGSTATE                                                                         = D3D12_MESSAGE_ID(919).value
D3D12_MESSAGE_ID_CREATE_QUEUE_INVALID_PRIORITY                                                                 = D3D12_MESSAGE_ID(920).value
D3D12_MESSAGE_ID_OBJECT_DELETED_WHILE_STILL_IN_USE                                                             = D3D12_MESSAGE_ID(921).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_INVALID_FLAGS                                                             = D3D12_MESSAGE_ID(922).value
D3D12_MESSAGE_ID_HEAP_ADDRESS_RANGE_HAS_NO_RESOURCE                                                            = D3D12_MESSAGE_ID(923).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_RENDER_TARGET_DELETED                                                       = D3D12_MESSAGE_ID(924).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_ALL_RENDER_TARGETS_HAVE_UNKNOWN_FORMAT                            = D3D12_MESSAGE_ID(925).value
D3D12_MESSAGE_ID_HEAP_ADDRESS_RANGE_INTERSECTS_MULTIPLE_BUFFERS                                                = D3D12_MESSAGE_ID(926).value
D3D12_MESSAGE_ID_EXECUTECOMMANDLISTS_GPU_WRITTEN_READBACK_RESOURCE_MAPPED                                      = D3D12_MESSAGE_ID(927).value
D3D12_MESSAGE_ID_UNMAP_RANGE_NOT_EMPTY                                                                         = D3D12_MESSAGE_ID(929).value
D3D12_MESSAGE_ID_MAP_INVALID_NULLRANGE                                                                         = D3D12_MESSAGE_ID(930).value
D3D12_MESSAGE_ID_UNMAP_INVALID_NULLRANGE                                                                       = D3D12_MESSAGE_ID(931).value
D3D12_MESSAGE_ID_NO_GRAPHICS_API_SUPPORT                                                                       = D3D12_MESSAGE_ID(932).value
D3D12_MESSAGE_ID_NO_COMPUTE_API_SUPPORT                                                                        = D3D12_MESSAGE_ID(933).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_RESOURCE_FLAGS_NOT_SUPPORTED                                               = D3D12_MESSAGE_ID(934).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_ROOT_ARGUMENT_UNINITIALIZED                                              = D3D12_MESSAGE_ID(935).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_DESCRIPTOR_HEAP_INDEX_OUT_OF_BOUNDS                                      = D3D12_MESSAGE_ID(936).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_DESCRIPTOR_TABLE_REGISTER_INDEX_OUT_OF_BOUNDS                            = D3D12_MESSAGE_ID(937).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_DESCRIPTOR_UNINITIALIZED                                                 = D3D12_MESSAGE_ID(938).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_DESCRIPTOR_TYPE_MISMATCH                                                 = D3D12_MESSAGE_ID(939).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_SRV_RESOURCE_DIMENSION_MISMATCH                                          = D3D12_MESSAGE_ID(940).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_UAV_RESOURCE_DIMENSION_MISMATCH                                          = D3D12_MESSAGE_ID(941).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_INCOMPATIBLE_RESOURCE_STATE                                              = D3D12_MESSAGE_ID(942).value
D3D12_MESSAGE_ID_COPYRESOURCE_NULLDST                                                                          = D3D12_MESSAGE_ID(943).value
D3D12_MESSAGE_ID_COPYRESOURCE_INVALIDDSTRESOURCE                                                               = D3D12_MESSAGE_ID(944).value
D3D12_MESSAGE_ID_COPYRESOURCE_NULLSRC                                                                          = D3D12_MESSAGE_ID(945).value
D3D12_MESSAGE_ID_COPYRESOURCE_INVALIDSRCRESOURCE                                                               = D3D12_MESSAGE_ID(946).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_NULLDST                                                                    = D3D12_MESSAGE_ID(947).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_INVALIDDSTRESOURCE                                                         = D3D12_MESSAGE_ID(948).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_NULLSRC                                                                    = D3D12_MESSAGE_ID(949).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_INVALIDSRCRESOURCE                                                         = D3D12_MESSAGE_ID(950).value
D3D12_MESSAGE_ID_PIPELINE_STATE_TYPE_MISMATCH                                                                  = D3D12_MESSAGE_ID(951).value
D3D12_MESSAGE_ID_COMMAND_LIST_DISPATCH_ROOT_SIGNATURE_NOT_SET                                                  = D3D12_MESSAGE_ID(952).value
D3D12_MESSAGE_ID_COMMAND_LIST_DISPATCH_ROOT_SIGNATURE_MISMATCH                                                 = D3D12_MESSAGE_ID(953).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_ZERO_BARRIERS                                                                = D3D12_MESSAGE_ID(954).value
D3D12_MESSAGE_ID_BEGIN_END_EVENT_MISMATCH                                                                      = D3D12_MESSAGE_ID(955).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_POSSIBLE_BEFORE_AFTER_MISMATCH                                               = D3D12_MESSAGE_ID(956).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_MISMATCHING_BEGIN_END                                                        = D3D12_MESSAGE_ID(957).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_INVALID_RESOURCE                                                         = D3D12_MESSAGE_ID(958).value
D3D12_MESSAGE_ID_USE_OF_ZERO_REFCOUNT_OBJECT                                                                   = D3D12_MESSAGE_ID(959).value
D3D12_MESSAGE_ID_OBJECT_EVICTED_WHILE_STILL_IN_USE                                                             = D3D12_MESSAGE_ID(960).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_ROOT_DESCRIPTOR_ACCESS_OUT_OF_BOUNDS                                     = D3D12_MESSAGE_ID(961).value
D3D12_MESSAGE_ID_CREATEPIPELINELIBRARY_INVALIDLIBRARYBLOB                                                      = D3D12_MESSAGE_ID(962).value
D3D12_MESSAGE_ID_CREATEPIPELINELIBRARY_DRIVERVERSIONMISMATCH                                                   = D3D12_MESSAGE_ID(963).value
D3D12_MESSAGE_ID_CREATEPIPELINELIBRARY_ADAPTERVERSIONMISMATCH                                                  = D3D12_MESSAGE_ID(964).value
D3D12_MESSAGE_ID_CREATEPIPELINELIBRARY_UNSUPPORTED                                                             = D3D12_MESSAGE_ID(965).value
D3D12_MESSAGE_ID_CREATE_PIPELINELIBRARY                                                                        = D3D12_MESSAGE_ID(966).value
D3D12_MESSAGE_ID_LIVE_PIPELINELIBRARY                                                                          = D3D12_MESSAGE_ID(967).value
D3D12_MESSAGE_ID_DESTROY_PIPELINELIBRARY                                                                       = D3D12_MESSAGE_ID(968).value
D3D12_MESSAGE_ID_STOREPIPELINE_NONAME                                                                          = D3D12_MESSAGE_ID(969).value
D3D12_MESSAGE_ID_STOREPIPELINE_DUPLICATENAME                                                                   = D3D12_MESSAGE_ID(970).value
D3D12_MESSAGE_ID_LOADPIPELINE_NAMENOTFOUND                                                                     = D3D12_MESSAGE_ID(971).value
D3D12_MESSAGE_ID_LOADPIPELINE_INVALIDDESC                                                                      = D3D12_MESSAGE_ID(972).value
D3D12_MESSAGE_ID_PIPELINELIBRARY_SERIALIZE_NOTENOUGHMEMORY                                                     = D3D12_MESSAGE_ID(973).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_PS_OUTPUT_RT_OUTPUT_MISMATCH                                      = D3D12_MESSAGE_ID(974).value
D3D12_MESSAGE_ID_SETEVENTONMULTIPLEFENCECOMPLETION_INVALIDFLAGS                                                = D3D12_MESSAGE_ID(975).value
D3D12_MESSAGE_ID_CREATE_QUEUE_VIDEO_NOT_SUPPORTED                                                              = D3D12_MESSAGE_ID(976).value
D3D12_MESSAGE_ID_CREATE_COMMAND_ALLOCATOR_VIDEO_NOT_SUPPORTED                                                  = D3D12_MESSAGE_ID(977).value
D3D12_MESSAGE_ID_CREATEQUERY_HEAP_VIDEO_DECODE_STATISTICS_NOT_SUPPORTED                                        = D3D12_MESSAGE_ID(978).value
D3D12_MESSAGE_ID_CREATE_VIDEODECODECOMMANDLIST                                                                 = D3D12_MESSAGE_ID(979).value
D3D12_MESSAGE_ID_CREATE_VIDEODECODER                                                                           = D3D12_MESSAGE_ID(980).value
D3D12_MESSAGE_ID_CREATE_VIDEODECODESTREAM                                                                      = D3D12_MESSAGE_ID(981).value
D3D12_MESSAGE_ID_LIVE_VIDEODECODECOMMANDLIST                                                                   = D3D12_MESSAGE_ID(982).value
D3D12_MESSAGE_ID_LIVE_VIDEODECODER                                                                             = D3D12_MESSAGE_ID(983).value
D3D12_MESSAGE_ID_LIVE_VIDEODECODESTREAM                                                                        = D3D12_MESSAGE_ID(984).value
D3D12_MESSAGE_ID_DESTROY_VIDEODECODECOMMANDLIST                                                                = D3D12_MESSAGE_ID(985).value
D3D12_MESSAGE_ID_DESTROY_VIDEODECODER                                                                          = D3D12_MESSAGE_ID(986).value
D3D12_MESSAGE_ID_DESTROY_VIDEODECODESTREAM                                                                     = D3D12_MESSAGE_ID(987).value
D3D12_MESSAGE_ID_DECODE_FRAME_INVALID_PARAMETERS                                                               = D3D12_MESSAGE_ID(988).value
D3D12_MESSAGE_ID_DEPRECATED_API                                                                                = D3D12_MESSAGE_ID(989).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_MISMATCHING_COMMAND_LIST_TYPE                                                = D3D12_MESSAGE_ID(990).value
D3D12_MESSAGE_ID_COMMAND_LIST_DESCRIPTOR_TABLE_NOT_SET                                                         = D3D12_MESSAGE_ID(991).value
D3D12_MESSAGE_ID_COMMAND_LIST_ROOT_CONSTANT_BUFFER_VIEW_NOT_SET                                                = D3D12_MESSAGE_ID(992).value
D3D12_MESSAGE_ID_COMMAND_LIST_ROOT_SHADER_RESOURCE_VIEW_NOT_SET                                                = D3D12_MESSAGE_ID(993).value
D3D12_MESSAGE_ID_COMMAND_LIST_ROOT_UNORDERED_ACCESS_VIEW_NOT_SET                                               = D3D12_MESSAGE_ID(994).value
D3D12_MESSAGE_ID_DISCARD_INVALID_SUBRESOURCE_RANGE                                                             = D3D12_MESSAGE_ID(995).value
D3D12_MESSAGE_ID_DISCARD_ONE_SUBRESOURCE_FOR_MIPS_WITH_RECTS                                                   = D3D12_MESSAGE_ID(996).value
D3D12_MESSAGE_ID_DISCARD_NO_RECTS_FOR_NON_TEXTURE2D                                                            = D3D12_MESSAGE_ID(997).value
D3D12_MESSAGE_ID_COPY_ON_SAME_SUBRESOURCE                                                                      = D3D12_MESSAGE_ID(998).value
D3D12_MESSAGE_ID_SETRESIDENCYPRIORITY_INVALID_PAGEABLE                                                         = D3D12_MESSAGE_ID(999).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_UNSUPPORTED                                                              = D3D12_MESSAGE_ID(1000).value
D3D12_MESSAGE_ID_STATIC_DESCRIPTOR_INVALID_DESCRIPTOR_CHANGE                                                   = D3D12_MESSAGE_ID(1001).value
D3D12_MESSAGE_ID_DATA_STATIC_DESCRIPTOR_INVALID_DATA_CHANGE                                                    = D3D12_MESSAGE_ID(1002).value
D3D12_MESSAGE_ID_DATA_STATIC_WHILE_SET_AT_EXECUTE_DESCRIPTOR_INVALID_DATA_CHANGE                               = D3D12_MESSAGE_ID(1003).value
D3D12_MESSAGE_ID_EXECUTE_BUNDLE_STATIC_DESCRIPTOR_DATA_STATIC_NOT_SET                                          = D3D12_MESSAGE_ID(1004).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_RESOURCE_ACCESS_OUT_OF_BOUNDS                                            = D3D12_MESSAGE_ID(1005).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_SAMPLER_MODE_MISMATCH                                                    = D3D12_MESSAGE_ID(1006).value
D3D12_MESSAGE_ID_CREATE_FENCE_INVALID_FLAGS                                                                    = D3D12_MESSAGE_ID(1007).value
D3D12_MESSAGE_ID_RESOURCE_BARRIER_DUPLICATE_SUBRESOURCE_TRANSITIONS                                            = D3D12_MESSAGE_ID(1008).value
D3D12_MESSAGE_ID_SETRESIDENCYPRIORITY_INVALID_PRIORITY                                                         = D3D12_MESSAGE_ID(1009).value
D3D12_MESSAGE_ID_CREATE_DESCRIPTOR_HEAP_LARGE_NUM_DESCRIPTORS                                                  = D3D12_MESSAGE_ID(1013).value
D3D12_MESSAGE_ID_BEGIN_EVENT                                                                                   = D3D12_MESSAGE_ID(1014).value
D3D12_MESSAGE_ID_END_EVENT                                                                                     = D3D12_MESSAGE_ID(1015).value
D3D12_MESSAGE_ID_CREATEDEVICE_DEBUG_LAYER_STARTUP_OPTIONS                                                      = D3D12_MESSAGE_ID(1016).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_DEPTHBOUNDSTEST_UNSUPPORTED                                           = D3D12_MESSAGE_ID(1017).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_DUPLICATE_SUBOBJECT                                                       = D3D12_MESSAGE_ID(1018).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_UNKNOWN_SUBOBJECT                                                         = D3D12_MESSAGE_ID(1019).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_ZERO_SIZE_STREAM                                                          = D3D12_MESSAGE_ID(1020).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_INVALID_STREAM                                                            = D3D12_MESSAGE_ID(1021).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_CANNOT_DEDUCE_TYPE                                                        = D3D12_MESSAGE_ID(1022).value
D3D12_MESSAGE_ID_COMMAND_LIST_STATIC_DESCRIPTOR_RESOURCE_DIMENSION_MISMATCH                                    = D3D12_MESSAGE_ID(1023).value
D3D12_MESSAGE_ID_CREATE_COMMAND_QUEUE_INSUFFICIENT_PRIVILEGE_FOR_GLOBAL_REALTIME                               = D3D12_MESSAGE_ID(1024).value
D3D12_MESSAGE_ID_CREATE_COMMAND_QUEUE_INSUFFICIENT_HARDWARE_SUPPORT_FOR_GLOBAL_REALTIME                        = D3D12_MESSAGE_ID(1025).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_ARCHITECTURE                                                         = D3D12_MESSAGE_ID(1026).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_NULL_DST                                                                     = D3D12_MESSAGE_ID(1027).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_DST_RESOURCE_DIMENSION                                               = D3D12_MESSAGE_ID(1028).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_DST_RANGE_OUT_OF_BOUNDS                                                      = D3D12_MESSAGE_ID(1029).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_NULL_SRC                                                                     = D3D12_MESSAGE_ID(1030).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_SRC_RESOURCE_DIMENSION                                               = D3D12_MESSAGE_ID(1031).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_SRC_RANGE_OUT_OF_BOUNDS                                                      = D3D12_MESSAGE_ID(1032).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_OFFSET_ALIGNMENT                                                     = D3D12_MESSAGE_ID(1033).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_NULL_DEPENDENT_RESOURCES                                                     = D3D12_MESSAGE_ID(1034).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_NULL_DEPENDENT_SUBRESOURCE_RANGES                                            = D3D12_MESSAGE_ID(1035).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_DEPENDENT_RESOURCE                                                   = D3D12_MESSAGE_ID(1036).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_DEPENDENT_SUBRESOURCE_RANGE                                          = D3D12_MESSAGE_ID(1037).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_DEPENDENT_SUBRESOURCE_OUT_OF_BOUNDS                                          = D3D12_MESSAGE_ID(1038).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_DEPENDENT_RANGE_OUT_OF_BOUNDS                                                = D3D12_MESSAGE_ID(1039).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_ZERO_DEPENDENCIES                                                            = D3D12_MESSAGE_ID(1040).value
D3D12_MESSAGE_ID_DEVICE_CREATE_SHARED_HANDLE_INVALIDARG                                                        = D3D12_MESSAGE_ID(1041).value
D3D12_MESSAGE_ID_DESCRIPTOR_HANDLE_WITH_INVALID_RESOURCE                                                       = D3D12_MESSAGE_ID(1042).value
D3D12_MESSAGE_ID_SETDEPTHBOUNDS_INVALIDARGS                                                                    = D3D12_MESSAGE_ID(1043).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_RESOURCE_STATE_IMPRECISE                                                 = D3D12_MESSAGE_ID(1044).value
D3D12_MESSAGE_ID_COMMAND_LIST_PIPELINE_STATE_NOT_SET                                                           = D3D12_MESSAGE_ID(1045).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_SHADER_MODEL_MISMATCH                                             = D3D12_MESSAGE_ID(1046).value
D3D12_MESSAGE_ID_OBJECT_ACCESSED_WHILE_STILL_IN_USE                                                            = D3D12_MESSAGE_ID(1047).value
D3D12_MESSAGE_ID_PROGRAMMABLE_MSAA_UNSUPPORTED                                                                 = D3D12_MESSAGE_ID(1048).value
D3D12_MESSAGE_ID_SETSAMPLEPOSITIONS_INVALIDARGS                                                                = D3D12_MESSAGE_ID(1049).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCEREGION_INVALID_RECT                                                         = D3D12_MESSAGE_ID(1050).value
D3D12_MESSAGE_ID_CREATE_VIDEODECODECOMMANDQUEUE                                                                = D3D12_MESSAGE_ID(1051).value
D3D12_MESSAGE_ID_CREATE_VIDEOPROCESSCOMMANDLIST                                                                = D3D12_MESSAGE_ID(1052).value
D3D12_MESSAGE_ID_CREATE_VIDEOPROCESSCOMMANDQUEUE                                                               = D3D12_MESSAGE_ID(1053).value
D3D12_MESSAGE_ID_LIVE_VIDEODECODECOMMANDQUEUE                                                                  = D3D12_MESSAGE_ID(1054).value
D3D12_MESSAGE_ID_LIVE_VIDEOPROCESSCOMMANDLIST                                                                  = D3D12_MESSAGE_ID(1055).value
D3D12_MESSAGE_ID_LIVE_VIDEOPROCESSCOMMANDQUEUE                                                                 = D3D12_MESSAGE_ID(1056).value
D3D12_MESSAGE_ID_DESTROY_VIDEODECODECOMMANDQUEUE                                                               = D3D12_MESSAGE_ID(1057).value
D3D12_MESSAGE_ID_DESTROY_VIDEOPROCESSCOMMANDLIST                                                               = D3D12_MESSAGE_ID(1058).value
D3D12_MESSAGE_ID_DESTROY_VIDEOPROCESSCOMMANDQUEUE                                                              = D3D12_MESSAGE_ID(1059).value
D3D12_MESSAGE_ID_CREATE_VIDEOPROCESSOR                                                                         = D3D12_MESSAGE_ID(1060).value
D3D12_MESSAGE_ID_CREATE_VIDEOPROCESSSTREAM                                                                     = D3D12_MESSAGE_ID(1061).value
D3D12_MESSAGE_ID_LIVE_VIDEOPROCESSOR                                                                           = D3D12_MESSAGE_ID(1062).value
D3D12_MESSAGE_ID_LIVE_VIDEOPROCESSSTREAM                                                                       = D3D12_MESSAGE_ID(1063).value
D3D12_MESSAGE_ID_DESTROY_VIDEOPROCESSOR                                                                        = D3D12_MESSAGE_ID(1064).value
D3D12_MESSAGE_ID_DESTROY_VIDEOPROCESSSTREAM                                                                    = D3D12_MESSAGE_ID(1065).value
D3D12_MESSAGE_ID_PROCESS_FRAME_INVALID_PARAMETERS                                                              = D3D12_MESSAGE_ID(1066).value
D3D12_MESSAGE_ID_COPY_INVALIDLAYOUT                                                                            = D3D12_MESSAGE_ID(1067).value
D3D12_MESSAGE_ID_CREATE_CRYPTO_SESSION                                                                         = D3D12_MESSAGE_ID(1068).value
D3D12_MESSAGE_ID_CREATE_CRYPTO_SESSION_POLICY                                                                  = D3D12_MESSAGE_ID(1069).value
D3D12_MESSAGE_ID_CREATE_PROTECTED_RESOURCE_SESSION                                                             = D3D12_MESSAGE_ID(1070).value
D3D12_MESSAGE_ID_LIVE_CRYPTO_SESSION                                                                           = D3D12_MESSAGE_ID(1071).value
D3D12_MESSAGE_ID_LIVE_CRYPTO_SESSION_POLICY                                                                    = D3D12_MESSAGE_ID(1072).value
D3D12_MESSAGE_ID_LIVE_PROTECTED_RESOURCE_SESSION                                                               = D3D12_MESSAGE_ID(1073).value
D3D12_MESSAGE_ID_DESTROY_CRYPTO_SESSION                                                                        = D3D12_MESSAGE_ID(1074).value
D3D12_MESSAGE_ID_DESTROY_CRYPTO_SESSION_POLICY                                                                 = D3D12_MESSAGE_ID(1075).value
D3D12_MESSAGE_ID_DESTROY_PROTECTED_RESOURCE_SESSION                                                            = D3D12_MESSAGE_ID(1076).value
D3D12_MESSAGE_ID_PROTECTED_RESOURCE_SESSION_UNSUPPORTED                                                        = D3D12_MESSAGE_ID(1077).value
D3D12_MESSAGE_ID_FENCE_INVALIDOPERATION                                                                        = D3D12_MESSAGE_ID(1078).value
D3D12_MESSAGE_ID_CREATEQUERY_HEAP_COPY_QUEUE_TIMESTAMPS_NOT_SUPPORTED                                          = D3D12_MESSAGE_ID(1079).value
D3D12_MESSAGE_ID_SAMPLEPOSITIONS_MISMATCH_DEFERRED                                                             = D3D12_MESSAGE_ID(1080).value
D3D12_MESSAGE_ID_SAMPLEPOSITIONS_MISMATCH_RECORDTIME_ASSUMEDFROMFIRSTUSE                                       = D3D12_MESSAGE_ID(1081).value
D3D12_MESSAGE_ID_SAMPLEPOSITIONS_MISMATCH_RECORDTIME_ASSUMEDFROMCLEAR                                          = D3D12_MESSAGE_ID(1082).value
D3D12_MESSAGE_ID_CREATE_VIDEODECODERHEAP                                                                       = D3D12_MESSAGE_ID(1083).value
D3D12_MESSAGE_ID_LIVE_VIDEODECODERHEAP                                                                         = D3D12_MESSAGE_ID(1084).value
D3D12_MESSAGE_ID_DESTROY_VIDEODECODERHEAP                                                                      = D3D12_MESSAGE_ID(1085).value
D3D12_MESSAGE_ID_OPENEXISTINGHEAP_INVALIDARG_RETURN                                                            = D3D12_MESSAGE_ID(1086).value
D3D12_MESSAGE_ID_OPENEXISTINGHEAP_OUTOFMEMORY_RETURN                                                           = D3D12_MESSAGE_ID(1087).value
D3D12_MESSAGE_ID_OPENEXISTINGHEAP_INVALIDADDRESS                                                               = D3D12_MESSAGE_ID(1088).value
D3D12_MESSAGE_ID_OPENEXISTINGHEAP_INVALIDHANDLE                                                                = D3D12_MESSAGE_ID(1089).value
D3D12_MESSAGE_ID_WRITEBUFFERIMMEDIATE_INVALID_DEST                                                             = D3D12_MESSAGE_ID(1090).value
D3D12_MESSAGE_ID_WRITEBUFFERIMMEDIATE_INVALID_MODE                                                             = D3D12_MESSAGE_ID(1091).value
D3D12_MESSAGE_ID_WRITEBUFFERIMMEDIATE_INVALID_ALIGNMENT                                                        = D3D12_MESSAGE_ID(1092).value
D3D12_MESSAGE_ID_WRITEBUFFERIMMEDIATE_NOT_SUPPORTED                                                            = D3D12_MESSAGE_ID(1093).value
D3D12_MESSAGE_ID_SETVIEWINSTANCEMASK_INVALIDARGS                                                               = D3D12_MESSAGE_ID(1094).value
D3D12_MESSAGE_ID_VIEW_INSTANCING_UNSUPPORTED                                                                   = D3D12_MESSAGE_ID(1095).value
D3D12_MESSAGE_ID_VIEW_INSTANCING_INVALIDARGS                                                                   = D3D12_MESSAGE_ID(1096).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_MISMATCH_DECODE_REFERENCE_ONLY_FLAG                                         = D3D12_MESSAGE_ID(1097).value
D3D12_MESSAGE_ID_COPYRESOURCE_MISMATCH_DECODE_REFERENCE_ONLY_FLAG                                              = D3D12_MESSAGE_ID(1098).value
D3D12_MESSAGE_ID_CREATE_VIDEO_DECODE_HEAP_CAPS_FAILURE                                                         = D3D12_MESSAGE_ID(1099).value
D3D12_MESSAGE_ID_CREATE_VIDEO_DECODE_HEAP_CAPS_UNSUPPORTED                                                     = D3D12_MESSAGE_ID(1100).value
D3D12_MESSAGE_ID_VIDEO_DECODE_SUPPORT_INVALID_INPUT                                                            = D3D12_MESSAGE_ID(1101).value
D3D12_MESSAGE_ID_CREATE_VIDEO_DECODER_UNSUPPORTED                                                              = D3D12_MESSAGE_ID(1102).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_METADATA_ERROR                                                    = D3D12_MESSAGE_ID(1103).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_VIEW_INSTANCING_VERTEX_SIZE_EXCEEDED                              = D3D12_MESSAGE_ID(1104).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_RUNTIME_INTERNAL_ERROR                                            = D3D12_MESSAGE_ID(1105).value
D3D12_MESSAGE_ID_NO_VIDEO_API_SUPPORT                                                                          = D3D12_MESSAGE_ID(1106).value
D3D12_MESSAGE_ID_VIDEO_PROCESS_SUPPORT_INVALID_INPUT                                                           = D3D12_MESSAGE_ID(1107).value
D3D12_MESSAGE_ID_CREATE_VIDEO_PROCESSOR_CAPS_FAILURE                                                           = D3D12_MESSAGE_ID(1108).value
D3D12_MESSAGE_ID_VIDEO_PROCESS_SUPPORT_UNSUPPORTED_FORMAT                                                      = D3D12_MESSAGE_ID(1109).value
D3D12_MESSAGE_ID_VIDEO_DECODE_FRAME_INVALID_ARGUMENT                                                           = D3D12_MESSAGE_ID(1110).value
D3D12_MESSAGE_ID_ENQUEUE_MAKE_RESIDENT_INVALID_FLAGS                                                           = D3D12_MESSAGE_ID(1111).value
D3D12_MESSAGE_ID_OPENEXISTINGHEAP_UNSUPPORTED                                                                  = D3D12_MESSAGE_ID(1112).value
D3D12_MESSAGE_ID_VIDEO_PROCESS_FRAMES_INVALID_ARGUMENT                                                         = D3D12_MESSAGE_ID(1113).value
D3D12_MESSAGE_ID_VIDEO_DECODE_SUPPORT_UNSUPPORTED                                                              = D3D12_MESSAGE_ID(1114).value
D3D12_MESSAGE_ID_CREATE_COMMANDRECORDER                                                                        = D3D12_MESSAGE_ID(1115).value
D3D12_MESSAGE_ID_LIVE_COMMANDRECORDER                                                                          = D3D12_MESSAGE_ID(1116).value
D3D12_MESSAGE_ID_DESTROY_COMMANDRECORDER                                                                       = D3D12_MESSAGE_ID(1117).value
D3D12_MESSAGE_ID_CREATE_COMMAND_RECORDER_VIDEO_NOT_SUPPORTED                                                   = D3D12_MESSAGE_ID(1118).value
D3D12_MESSAGE_ID_CREATE_COMMAND_RECORDER_INVALID_SUPPORT_FLAGS                                                 = D3D12_MESSAGE_ID(1119).value
D3D12_MESSAGE_ID_CREATE_COMMAND_RECORDER_INVALID_FLAGS                                                         = D3D12_MESSAGE_ID(1120).value
D3D12_MESSAGE_ID_CREATE_COMMAND_RECORDER_MORE_RECORDERS_THAN_LOGICAL_PROCESSORS                                = D3D12_MESSAGE_ID(1121).value
D3D12_MESSAGE_ID_CREATE_COMMANDPOOL                                                                            = D3D12_MESSAGE_ID(1122).value
D3D12_MESSAGE_ID_LIVE_COMMANDPOOL                                                                              = D3D12_MESSAGE_ID(1123).value
D3D12_MESSAGE_ID_DESTROY_COMMANDPOOL                                                                           = D3D12_MESSAGE_ID(1124).value
D3D12_MESSAGE_ID_CREATE_COMMAND_POOL_INVALID_FLAGS                                                             = D3D12_MESSAGE_ID(1125).value
D3D12_MESSAGE_ID_CREATE_COMMAND_LIST_VIDEO_NOT_SUPPORTED                                                       = D3D12_MESSAGE_ID(1126).value
D3D12_MESSAGE_ID_COMMAND_RECORDER_SUPPORT_FLAGS_MISMATCH                                                       = D3D12_MESSAGE_ID(1127).value
D3D12_MESSAGE_ID_COMMAND_RECORDER_CONTENTION                                                                   = D3D12_MESSAGE_ID(1128).value
D3D12_MESSAGE_ID_COMMAND_RECORDER_USAGE_WITH_CREATECOMMANDLIST_COMMAND_LIST                                    = D3D12_MESSAGE_ID(1129).value
D3D12_MESSAGE_ID_COMMAND_ALLOCATOR_USAGE_WITH_CREATECOMMANDLIST1_COMMAND_LIST                                  = D3D12_MESSAGE_ID(1130).value
D3D12_MESSAGE_ID_CANNOT_EXECUTE_EMPTY_COMMAND_LIST                                                             = D3D12_MESSAGE_ID(1131).value
D3D12_MESSAGE_ID_CANNOT_RESET_COMMAND_POOL_WITH_OPEN_COMMAND_LISTS                                             = D3D12_MESSAGE_ID(1132).value
D3D12_MESSAGE_ID_CANNOT_USE_COMMAND_RECORDER_WITHOUT_CURRENT_TARGET                                            = D3D12_MESSAGE_ID(1133).value
D3D12_MESSAGE_ID_CANNOT_CHANGE_COMMAND_RECORDER_TARGET_WHILE_RECORDING                                         = D3D12_MESSAGE_ID(1134).value
D3D12_MESSAGE_ID_COMMAND_POOL_SYNC                                                                             = D3D12_MESSAGE_ID(1135).value
D3D12_MESSAGE_ID_EVICT_UNDERFLOW                                                                               = D3D12_MESSAGE_ID(1136).value
D3D12_MESSAGE_ID_CREATE_META_COMMAND                                                                           = D3D12_MESSAGE_ID(1137).value
D3D12_MESSAGE_ID_LIVE_META_COMMAND                                                                             = D3D12_MESSAGE_ID(1138).value
D3D12_MESSAGE_ID_DESTROY_META_COMMAND                                                                          = D3D12_MESSAGE_ID(1139).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_INVALID_DST_RESOURCE                                                         = D3D12_MESSAGE_ID(1140).value
D3D12_MESSAGE_ID_COPYBUFFERREGION_INVALID_SRC_RESOURCE                                                         = D3D12_MESSAGE_ID(1141).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_DST_RESOURCE                                                         = D3D12_MESSAGE_ID(1142).value
D3D12_MESSAGE_ID_ATOMICCOPYBUFFER_INVALID_SRC_RESOURCE                                                         = D3D12_MESSAGE_ID(1143).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_NULL_BUFFER                                                      = D3D12_MESSAGE_ID(1144).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_NULL_RESOURCE_DESC                                               = D3D12_MESSAGE_ID(1145).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_UNSUPPORTED                                                      = D3D12_MESSAGE_ID(1146).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_INVALID_BUFFER_DIMENSION                                         = D3D12_MESSAGE_ID(1147).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_INVALID_BUFFER_FLAGS                                             = D3D12_MESSAGE_ID(1148).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_INVALID_BUFFER_OFFSET                                            = D3D12_MESSAGE_ID(1149).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_INVALID_RESOURCE_DIMENSION                                       = D3D12_MESSAGE_ID(1150).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_INVALID_RESOURCE_FLAGS                                           = D3D12_MESSAGE_ID(1151).value
D3D12_MESSAGE_ID_CREATEPLACEDRESOURCEONBUFFER_OUTOFMEMORY_RETURN                                               = D3D12_MESSAGE_ID(1152).value
D3D12_MESSAGE_ID_CANNOT_CREATE_GRAPHICS_AND_VIDEO_COMMAND_RECORDER                                             = D3D12_MESSAGE_ID(1153).value
D3D12_MESSAGE_ID_UPDATETILEMAPPINGS_POSSIBLY_MISMATCHING_PROPERTIES                                            = D3D12_MESSAGE_ID(1154).value
D3D12_MESSAGE_ID_CREATE_COMMAND_LIST_INVALID_COMMAND_LIST_TYPE                                                 = D3D12_MESSAGE_ID(1155).value
D3D12_MESSAGE_ID_CLEARUNORDEREDACCESSVIEW_INCOMPATIBLE_WITH_STRUCTURED_BUFFERS                                 = D3D12_MESSAGE_ID(1156).value
D3D12_MESSAGE_ID_COMPUTE_ONLY_DEVICE_OPERATION_UNSUPPORTED                                                     = D3D12_MESSAGE_ID(1157).value
D3D12_MESSAGE_ID_BUILD_RAYTRACING_ACCELERATION_STRUCTURE_INVALID                                               = D3D12_MESSAGE_ID(1158).value
D3D12_MESSAGE_ID_EMIT_RAYTRACING_ACCELERATION_STRUCTURE_POSTBUILD_INFO_INVALID                                 = D3D12_MESSAGE_ID(1159).value
D3D12_MESSAGE_ID_COPY_RAYTRACING_ACCELERATION_STRUCTURE_INVALID                                                = D3D12_MESSAGE_ID(1160).value
D3D12_MESSAGE_ID_DISPATCH_RAYS_INVALID                                                                         = D3D12_MESSAGE_ID(1161).value
D3D12_MESSAGE_ID_GET_RAYTRACING_ACCELERATION_STRUCTURE_PREBUILD_INFO_INVALID                                   = D3D12_MESSAGE_ID(1162).value
D3D12_MESSAGE_ID_CREATE_LIFETIMETRACKER                                                                        = D3D12_MESSAGE_ID(1163).value
D3D12_MESSAGE_ID_LIVE_LIFETIMETRACKER                                                                          = D3D12_MESSAGE_ID(1164).value
D3D12_MESSAGE_ID_DESTROY_LIFETIMETRACKER                                                                       = D3D12_MESSAGE_ID(1165).value
D3D12_MESSAGE_ID_DESTROYOWNEDOBJECT_OBJECTNOTOWNED                                                             = D3D12_MESSAGE_ID(1166).value
D3D12_MESSAGE_ID_CREATE_TRACKEDWORKLOAD                                                                        = D3D12_MESSAGE_ID(1167).value
D3D12_MESSAGE_ID_LIVE_TRACKEDWORKLOAD                                                                          = D3D12_MESSAGE_ID(1168).value
D3D12_MESSAGE_ID_DESTROY_TRACKEDWORKLOAD                                                                       = D3D12_MESSAGE_ID(1169).value
D3D12_MESSAGE_ID_RENDER_PASS_ERROR                                                                             = D3D12_MESSAGE_ID(1170).value
D3D12_MESSAGE_ID_META_COMMAND_ID_INVALID                                                                       = D3D12_MESSAGE_ID(1171).value
D3D12_MESSAGE_ID_META_COMMAND_UNSUPPORTED_PARAMS                                                               = D3D12_MESSAGE_ID(1172).value
D3D12_MESSAGE_ID_META_COMMAND_FAILED_ENUMERATION                                                               = D3D12_MESSAGE_ID(1173).value
D3D12_MESSAGE_ID_META_COMMAND_PARAMETER_SIZE_MISMATCH                                                          = D3D12_MESSAGE_ID(1174).value
D3D12_MESSAGE_ID_UNINITIALIZED_META_COMMAND                                                                    = D3D12_MESSAGE_ID(1175).value
D3D12_MESSAGE_ID_META_COMMAND_INVALID_GPU_VIRTUAL_ADDRESS                                                      = D3D12_MESSAGE_ID(1176).value
D3D12_MESSAGE_ID_CREATE_VIDEOENCODECOMMANDLIST                                                                 = D3D12_MESSAGE_ID(1177).value
D3D12_MESSAGE_ID_LIVE_VIDEOENCODECOMMANDLIST                                                                   = D3D12_MESSAGE_ID(1178).value
D3D12_MESSAGE_ID_DESTROY_VIDEOENCODECOMMANDLIST                                                                = D3D12_MESSAGE_ID(1179).value
D3D12_MESSAGE_ID_CREATE_VIDEOENCODECOMMANDQUEUE                                                                = D3D12_MESSAGE_ID(1180).value
D3D12_MESSAGE_ID_LIVE_VIDEOENCODECOMMANDQUEUE                                                                  = D3D12_MESSAGE_ID(1181).value
D3D12_MESSAGE_ID_DESTROY_VIDEOENCODECOMMANDQUEUE                                                               = D3D12_MESSAGE_ID(1182).value
D3D12_MESSAGE_ID_CREATE_VIDEOMOTIONESTIMATOR                                                                   = D3D12_MESSAGE_ID(1183).value
D3D12_MESSAGE_ID_LIVE_VIDEOMOTIONESTIMATOR                                                                     = D3D12_MESSAGE_ID(1184).value
D3D12_MESSAGE_ID_DESTROY_VIDEOMOTIONESTIMATOR                                                                  = D3D12_MESSAGE_ID(1185).value
D3D12_MESSAGE_ID_CREATE_VIDEOMOTIONVECTORHEAP                                                                  = D3D12_MESSAGE_ID(1186).value
D3D12_MESSAGE_ID_LIVE_VIDEOMOTIONVECTORHEAP                                                                    = D3D12_MESSAGE_ID(1187).value
D3D12_MESSAGE_ID_DESTROY_VIDEOMOTIONVECTORHEAP                                                                 = D3D12_MESSAGE_ID(1188).value
D3D12_MESSAGE_ID_MULTIPLE_TRACKED_WORKLOADS                                                                    = D3D12_MESSAGE_ID(1189).value
D3D12_MESSAGE_ID_MULTIPLE_TRACKED_WORKLOAD_PAIRS                                                               = D3D12_MESSAGE_ID(1190).value
D3D12_MESSAGE_ID_OUT_OF_ORDER_TRACKED_WORKLOAD_PAIR                                                            = D3D12_MESSAGE_ID(1191).value
D3D12_MESSAGE_ID_CANNOT_ADD_TRACKED_WORKLOAD                                                                   = D3D12_MESSAGE_ID(1192).value
D3D12_MESSAGE_ID_INCOMPLETE_TRACKED_WORKLOAD_PAIR                                                              = D3D12_MESSAGE_ID(1193).value
D3D12_MESSAGE_ID_CREATE_STATE_OBJECT_ERROR                                                                     = D3D12_MESSAGE_ID(1194).value
D3D12_MESSAGE_ID_GET_SHADER_IDENTIFIER_ERROR                                                                   = D3D12_MESSAGE_ID(1195).value
D3D12_MESSAGE_ID_GET_SHADER_STACK_SIZE_ERROR                                                                   = D3D12_MESSAGE_ID(1196).value
D3D12_MESSAGE_ID_GET_PIPELINE_STACK_SIZE_ERROR                                                                 = D3D12_MESSAGE_ID(1197).value
D3D12_MESSAGE_ID_SET_PIPELINE_STACK_SIZE_ERROR                                                                 = D3D12_MESSAGE_ID(1198).value
D3D12_MESSAGE_ID_GET_SHADER_IDENTIFIER_SIZE_INVALID                                                            = D3D12_MESSAGE_ID(1199).value
D3D12_MESSAGE_ID_CHECK_DRIVER_MATCHING_IDENTIFIER_INVALID                                                      = D3D12_MESSAGE_ID(1200).value
D3D12_MESSAGE_ID_CHECK_DRIVER_MATCHING_IDENTIFIER_DRIVER_REPORTED_ISSUE                                        = D3D12_MESSAGE_ID(1201).value
D3D12_MESSAGE_ID_RENDER_PASS_INVALID_RESOURCE_BARRIER                                                          = D3D12_MESSAGE_ID(1202).value
D3D12_MESSAGE_ID_RENDER_PASS_DISALLOWED_API_CALLED                                                             = D3D12_MESSAGE_ID(1203).value
D3D12_MESSAGE_ID_RENDER_PASS_CANNOT_NEST_RENDER_PASSES                                                         = D3D12_MESSAGE_ID(1204).value
D3D12_MESSAGE_ID_RENDER_PASS_CANNOT_END_WITHOUT_BEGIN                                                          = D3D12_MESSAGE_ID(1205).value
D3D12_MESSAGE_ID_RENDER_PASS_CANNOT_CLOSE_COMMAND_LIST                                                         = D3D12_MESSAGE_ID(1206).value
D3D12_MESSAGE_ID_RENDER_PASS_GPU_WORK_WHILE_SUSPENDED                                                          = D3D12_MESSAGE_ID(1207).value
D3D12_MESSAGE_ID_RENDER_PASS_MISMATCHING_SUSPEND_RESUME                                                        = D3D12_MESSAGE_ID(1208).value
D3D12_MESSAGE_ID_RENDER_PASS_NO_PRIOR_SUSPEND_WITHIN_EXECUTECOMMANDLISTS                                       = D3D12_MESSAGE_ID(1209).value
D3D12_MESSAGE_ID_RENDER_PASS_NO_SUBSEQUENT_RESUME_WITHIN_EXECUTECOMMANDLISTS                                   = D3D12_MESSAGE_ID(1210).value
D3D12_MESSAGE_ID_TRACKED_WORKLOAD_COMMAND_QUEUE_MISMATCH                                                       = D3D12_MESSAGE_ID(1211).value
D3D12_MESSAGE_ID_TRACKED_WORKLOAD_NOT_SUPPORTED                                                                = D3D12_MESSAGE_ID(1212).value
D3D12_MESSAGE_ID_RENDER_PASS_MISMATCHING_NO_ACCESS                                                             = D3D12_MESSAGE_ID(1213).value
D3D12_MESSAGE_ID_RENDER_PASS_UNSUPPORTED_RESOLVE                                                               = D3D12_MESSAGE_ID(1214).value
D3D12_MESSAGE_ID_CLEARUNORDEREDACCESSVIEW_INVALID_RESOURCE_PTR                                                 = D3D12_MESSAGE_ID(1215).value
D3D12_MESSAGE_ID_WINDOWS7_FENCE_OUTOFORDER_SIGNAL                                                              = D3D12_MESSAGE_ID(1216).value
D3D12_MESSAGE_ID_WINDOWS7_FENCE_OUTOFORDER_WAIT                                                                = D3D12_MESSAGE_ID(1217).value
D3D12_MESSAGE_ID_VIDEO_CREATE_MOTION_ESTIMATOR_INVALID_ARGUMENT                                                = D3D12_MESSAGE_ID(1218).value
D3D12_MESSAGE_ID_VIDEO_CREATE_MOTION_VECTOR_HEAP_INVALID_ARGUMENT                                              = D3D12_MESSAGE_ID(1219).value
D3D12_MESSAGE_ID_ESTIMATE_MOTION_INVALID_ARGUMENT                                                              = D3D12_MESSAGE_ID(1220).value
D3D12_MESSAGE_ID_RESOLVE_MOTION_VECTOR_HEAP_INVALID_ARGUMENT                                                   = D3D12_MESSAGE_ID(1221).value
D3D12_MESSAGE_ID_GETGPUVIRTUALADDRESS_INVALID_HEAP_TYPE                                                        = D3D12_MESSAGE_ID(1222).value
D3D12_MESSAGE_ID_SET_BACKGROUND_PROCESSING_MODE_INVALID_ARGUMENT                                               = D3D12_MESSAGE_ID(1223).value
D3D12_MESSAGE_ID_CREATE_COMMAND_LIST_INVALID_COMMAND_LIST_TYPE_FOR_FEATURE_LEVEL                               = D3D12_MESSAGE_ID(1224).value
D3D12_MESSAGE_ID_CREATE_VIDEOEXTENSIONCOMMAND                                                                  = D3D12_MESSAGE_ID(1225).value
D3D12_MESSAGE_ID_LIVE_VIDEOEXTENSIONCOMMAND                                                                    = D3D12_MESSAGE_ID(1226).value
D3D12_MESSAGE_ID_DESTROY_VIDEOEXTENSIONCOMMAND                                                                 = D3D12_MESSAGE_ID(1227).value
D3D12_MESSAGE_ID_INVALID_VIDEO_EXTENSION_COMMAND_ID                                                            = D3D12_MESSAGE_ID(1228).value
D3D12_MESSAGE_ID_VIDEO_EXTENSION_COMMAND_INVALID_ARGUMENT                                                      = D3D12_MESSAGE_ID(1229).value
D3D12_MESSAGE_ID_CREATE_ROOT_SIGNATURE_NOT_UNIQUE_IN_DXIL_LIBRARY                                              = D3D12_MESSAGE_ID(1230).value
D3D12_MESSAGE_ID_VARIABLE_SHADING_RATE_NOT_ALLOWED_WITH_TIR                                                    = D3D12_MESSAGE_ID(1231).value
D3D12_MESSAGE_ID_GEOMETRY_SHADER_OUTPUTTING_BOTH_VIEWPORT_ARRAY_INDEX_AND_SHADING_RATE_NOT_SUPPORTED_ON_DEVICE = D3D12_MESSAGE_ID(1232).value
D3D12_MESSAGE_ID_RSSETSHADING_RATE_INVALID_SHADING_RATE                                                        = D3D12_MESSAGE_ID(1233).value
D3D12_MESSAGE_ID_RSSETSHADING_RATE_SHADING_RATE_NOT_PERMITTED_BY_CAP                                           = D3D12_MESSAGE_ID(1234).value
D3D12_MESSAGE_ID_RSSETSHADING_RATE_INVALID_COMBINER                                                            = D3D12_MESSAGE_ID(1235).value
D3D12_MESSAGE_ID_RSSETSHADINGRATEIMAGE_REQUIRES_TIER_2                                                         = D3D12_MESSAGE_ID(1236).value
D3D12_MESSAGE_ID_RSSETSHADINGRATE_REQUIRES_TIER_1                                                              = D3D12_MESSAGE_ID(1237).value
D3D12_MESSAGE_ID_SHADING_RATE_IMAGE_INCORRECT_FORMAT                                                           = D3D12_MESSAGE_ID(1238).value
D3D12_MESSAGE_ID_SHADING_RATE_IMAGE_INCORRECT_ARRAY_SIZE                                                       = D3D12_MESSAGE_ID(1239).value
D3D12_MESSAGE_ID_SHADING_RATE_IMAGE_INCORRECT_MIP_LEVEL                                                        = D3D12_MESSAGE_ID(1240).value
D3D12_MESSAGE_ID_SHADING_RATE_IMAGE_INCORRECT_SAMPLE_COUNT                                                     = D3D12_MESSAGE_ID(1241).value
D3D12_MESSAGE_ID_SHADING_RATE_IMAGE_INCORRECT_SAMPLE_QUALITY                                                   = D3D12_MESSAGE_ID(1242).value
D3D12_MESSAGE_ID_NON_RETAIL_SHADER_MODEL_WONT_VALIDATE                                                         = D3D12_MESSAGE_ID(1243).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_AS_ROOT_SIGNATURE_MISMATCH                                        = D3D12_MESSAGE_ID(1244).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_MS_ROOT_SIGNATURE_MISMATCH                                        = D3D12_MESSAGE_ID(1245).value
D3D12_MESSAGE_ID_ADD_TO_STATE_OBJECT_ERROR                                                                     = D3D12_MESSAGE_ID(1246).value
D3D12_MESSAGE_ID_CREATE_PROTECTED_RESOURCE_SESSION_INVALID_ARGUMENT                                            = D3D12_MESSAGE_ID(1247).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_MS_PSO_DESC_MISMATCH                                              = D3D12_MESSAGE_ID(1248).value
D3D12_MESSAGE_ID_CREATEPIPELINESTATE_MS_INCOMPLETE_TYPE                                                        = D3D12_MESSAGE_ID(1249).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_AS_NOT_MS_MISMATCH                                                = D3D12_MESSAGE_ID(1250).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_MS_NOT_PS_MISMATCH                                                = D3D12_MESSAGE_ID(1251).value
D3D12_MESSAGE_ID_NONZERO_SAMPLER_FEEDBACK_MIP_REGION_WITH_INCOMPATIBLE_FORMAT                                  = D3D12_MESSAGE_ID(1252).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_INPUTLAYOUT_SHADER_MISMATCH                                       = D3D12_MESSAGE_ID(1253).value
D3D12_MESSAGE_ID_EMPTY_DISPATCH                                                                                = D3D12_MESSAGE_ID(1254).value
D3D12_MESSAGE_ID_RESOURCE_FORMAT_REQUIRES_SAMPLER_FEEDBACK_CAPABILITY                                          = D3D12_MESSAGE_ID(1255).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_MAP_INVALID_MIP_REGION                                                       = D3D12_MESSAGE_ID(1256).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_MAP_INVALID_DIMENSION                                                        = D3D12_MESSAGE_ID(1257).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_MAP_INVALID_SAMPLE_COUNT                                                     = D3D12_MESSAGE_ID(1258).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_MAP_INVALID_SAMPLE_QUALITY                                                   = D3D12_MESSAGE_ID(1259).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_MAP_INVALID_LAYOUT                                                           = D3D12_MESSAGE_ID(1260).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_MAP_REQUIRES_UNORDERED_ACCESS_FLAG                                           = D3D12_MESSAGE_ID(1261).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_CREATE_UAV_NULL_ARGUMENTS                                                    = D3D12_MESSAGE_ID(1262).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_UAV_REQUIRES_SAMPLER_FEEDBACK_CAPABILITY                                     = D3D12_MESSAGE_ID(1263).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_CREATE_UAV_REQUIRES_FEEDBACK_MAP_FORMAT                                      = D3D12_MESSAGE_ID(1264).value
D3D12_MESSAGE_ID_CREATEMESHSHADER_INVALIDSHADERBYTECODE                                                        = D3D12_MESSAGE_ID(1265).value
D3D12_MESSAGE_ID_CREATEMESHSHADER_OUTOFMEMORY                                                                  = D3D12_MESSAGE_ID(1266).value
D3D12_MESSAGE_ID_CREATEMESHSHADERWITHSTREAMOUTPUT_INVALIDSHADERTYPE                                            = D3D12_MESSAGE_ID(1267).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_SAMPLER_FEEDBACK_TRANSCODE_INVALID_FORMAT                                  = D3D12_MESSAGE_ID(1268).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_SAMPLER_FEEDBACK_INVALID_MIP_LEVEL_COUNT                                   = D3D12_MESSAGE_ID(1269).value
D3D12_MESSAGE_ID_RESOLVESUBRESOURCE_SAMPLER_FEEDBACK_TRANSCODE_ARRAY_SIZE_MISMATCH                             = D3D12_MESSAGE_ID(1270).value
D3D12_MESSAGE_ID_SAMPLER_FEEDBACK_CREATE_UAV_MISMATCHING_TARGETED_RESOURCE                                     = D3D12_MESSAGE_ID(1271).value
D3D12_MESSAGE_ID_CREATEMESHSHADER_OUTPUTEXCEEDSMAXSIZE                                                         = D3D12_MESSAGE_ID(1272).value
D3D12_MESSAGE_ID_CREATEMESHSHADER_GROUPSHAREDEXCEEDSMAXSIZE                                                    = D3D12_MESSAGE_ID(1273).value
D3D12_MESSAGE_ID_VERTEX_SHADER_OUTPUTTING_BOTH_VIEWPORT_ARRAY_INDEX_AND_SHADING_RATE_NOT_SUPPORTED_ON_DEVICE   = D3D12_MESSAGE_ID(1274).value
D3D12_MESSAGE_ID_MESH_SHADER_OUTPUTTING_BOTH_VIEWPORT_ARRAY_INDEX_AND_SHADING_RATE_NOT_SUPPORTED_ON_DEVICE     = D3D12_MESSAGE_ID(1275).value
D3D12_MESSAGE_ID_CREATEMESHSHADER_MISMATCHEDASMSPAYLOADSIZE                                                    = D3D12_MESSAGE_ID(1276).value
D3D12_MESSAGE_ID_CREATE_ROOT_SIGNATURE_UNBOUNDED_STATIC_DESCRIPTORS                                            = D3D12_MESSAGE_ID(1277).value
D3D12_MESSAGE_ID_CREATEAMPLIFICATIONSHADER_INVALIDSHADERBYTECODE                                               = D3D12_MESSAGE_ID(1278).value
D3D12_MESSAGE_ID_CREATEAMPLIFICATIONSHADER_OUTOFMEMORY                                                         = D3D12_MESSAGE_ID(1279).value
D3D12_MESSAGE_ID_CREATE_SHADERCACHESESSION                                                                     = D3D12_MESSAGE_ID(1280).value
D3D12_MESSAGE_ID_LIVE_SHADERCACHESESSION                                                                       = D3D12_MESSAGE_ID(1281).value
D3D12_MESSAGE_ID_DESTROY_SHADERCACHESESSION                                                                    = D3D12_MESSAGE_ID(1282).value
D3D12_MESSAGE_ID_CREATESHADERCACHESESSION_INVALIDARGS                                                          = D3D12_MESSAGE_ID(1283).value
D3D12_MESSAGE_ID_CREATESHADERCACHESESSION_DISABLED                                                             = D3D12_MESSAGE_ID(1284).value
D3D12_MESSAGE_ID_CREATESHADERCACHESESSION_ALREADYOPEN                                                          = D3D12_MESSAGE_ID(1285).value
D3D12_MESSAGE_ID_SHADERCACHECONTROL_DEVELOPERMODE                                                              = D3D12_MESSAGE_ID(1286).value
D3D12_MESSAGE_ID_SHADERCACHECONTROL_INVALIDFLAGS                                                               = D3D12_MESSAGE_ID(1287).value
D3D12_MESSAGE_ID_SHADERCACHECONTROL_STATEALREADYSET                                                            = D3D12_MESSAGE_ID(1288).value
D3D12_MESSAGE_ID_SHADERCACHECONTROL_IGNOREDFLAG                                                                = D3D12_MESSAGE_ID(1289).value
D3D12_MESSAGE_ID_SHADERCACHESESSION_STOREVALUE_ALREADYPRESENT                                                  = D3D12_MESSAGE_ID(1290).value
D3D12_MESSAGE_ID_SHADERCACHESESSION_STOREVALUE_HASHCOLLISION                                                   = D3D12_MESSAGE_ID(1291).value
D3D12_MESSAGE_ID_SHADERCACHESESSION_STOREVALUE_CACHEFULL                                                       = D3D12_MESSAGE_ID(1292).value
D3D12_MESSAGE_ID_SHADERCACHESESSION_FINDVALUE_NOTFOUND                                                         = D3D12_MESSAGE_ID(1293).value
D3D12_MESSAGE_ID_SHADERCACHESESSION_CORRUPT                                                                    = D3D12_MESSAGE_ID(1294).value
D3D12_MESSAGE_ID_SHADERCACHESESSION_DISABLED                                                                   = D3D12_MESSAGE_ID(1295).value
D3D12_MESSAGE_ID_OVERSIZED_DISPATCH                                                                            = D3D12_MESSAGE_ID(1296).value
D3D12_MESSAGE_ID_CREATE_VIDEOENCODER                                                                           = D3D12_MESSAGE_ID(1297).value
D3D12_MESSAGE_ID_LIVE_VIDEOENCODER                                                                             = D3D12_MESSAGE_ID(1298).value
D3D12_MESSAGE_ID_DESTROY_VIDEOENCODER                                                                          = D3D12_MESSAGE_ID(1299).value
D3D12_MESSAGE_ID_CREATE_VIDEOENCODERHEAP                                                                       = D3D12_MESSAGE_ID(1300).value
D3D12_MESSAGE_ID_LIVE_VIDEOENCODERHEAP                                                                         = D3D12_MESSAGE_ID(1301).value
D3D12_MESSAGE_ID_DESTROY_VIDEOENCODERHEAP                                                                      = D3D12_MESSAGE_ID(1302).value
D3D12_MESSAGE_ID_COPYTEXTUREREGION_MISMATCH_ENCODE_REFERENCE_ONLY_FLAG                                         = D3D12_MESSAGE_ID(1303).value
D3D12_MESSAGE_ID_COPYRESOURCE_MISMATCH_ENCODE_REFERENCE_ONLY_FLAG                                              = D3D12_MESSAGE_ID(1304).value
D3D12_MESSAGE_ID_ENCODE_FRAME_INVALID_PARAMETERS                                                               = D3D12_MESSAGE_ID(1305).value
D3D12_MESSAGE_ID_ENCODE_FRAME_UNSUPPORTED_PARAMETERS                                                           = D3D12_MESSAGE_ID(1306).value
D3D12_MESSAGE_ID_RESOLVE_ENCODER_OUTPUT_METADATA_INVALID_PARAMETERS                                            = D3D12_MESSAGE_ID(1307).value
D3D12_MESSAGE_ID_RESOLVE_ENCODER_OUTPUT_METADATA_UNSUPPORTED_PARAMETERS                                        = D3D12_MESSAGE_ID(1308).value
D3D12_MESSAGE_ID_CREATE_VIDEO_ENCODER_INVALID_PARAMETERS                                                       = D3D12_MESSAGE_ID(1309).value
D3D12_MESSAGE_ID_CREATE_VIDEO_ENCODER_UNSUPPORTED_PARAMETERS                                                   = D3D12_MESSAGE_ID(1310).value
D3D12_MESSAGE_ID_CREATE_VIDEO_ENCODER_HEAP_INVALID_PARAMETERS                                                  = D3D12_MESSAGE_ID(1311).value
D3D12_MESSAGE_ID_CREATE_VIDEO_ENCODER_HEAP_UNSUPPORTED_PARAMETERS                                              = D3D12_MESSAGE_ID(1312).value
D3D12_MESSAGE_ID_CREATECOMMANDLIST_NULL_COMMANDALLOCATOR                                                       = D3D12_MESSAGE_ID(1313).value
D3D12_MESSAGE_ID_CLEAR_UNORDERED_ACCESS_VIEW_INVALID_DESCRIPTOR_HANDLE                                         = D3D12_MESSAGE_ID(1314).value
D3D12_MESSAGE_ID_DESCRIPTOR_HEAP_NOT_SHADER_VISIBLE                                                            = D3D12_MESSAGE_ID(1315).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_BLENDOP_WARNING                                                              = D3D12_MESSAGE_ID(1316).value
D3D12_MESSAGE_ID_CREATEBLENDSTATE_BLENDOPALPHA_WARNING                                                         = D3D12_MESSAGE_ID(1317).value
D3D12_MESSAGE_ID_WRITE_COMBINE_PERFORMANCE_WARNING                                                             = D3D12_MESSAGE_ID(1318).value
D3D12_MESSAGE_ID_RESOLVE_QUERY_INVALID_QUERY_STATE                                                             = D3D12_MESSAGE_ID(1319).value
D3D12_MESSAGE_ID_SETPRIVATEDATA_NO_ACCESS                                                                      = D3D12_MESSAGE_ID(1320).value
D3D12_MESSAGE_ID_COMMAND_LIST_STATIC_DESCRIPTOR_SAMPLER_MODE_MISMATCH                                          = D3D12_MESSAGE_ID(1321).value
D3D12_MESSAGE_ID_GETCOPYABLEFOOTPRINTS_UNSUPPORTED_BUFFER_WIDTH                                                = D3D12_MESSAGE_ID(1322).value
D3D12_MESSAGE_ID_CREATEMESHSHADER_TOPOLOGY_MISMATCH                                                            = D3D12_MESSAGE_ID(1323).value
D3D12_MESSAGE_ID_VRS_SUM_COMBINER_REQUIRES_CAPABILITY                                                          = D3D12_MESSAGE_ID(1324).value
D3D12_MESSAGE_ID_SETTING_SHADING_RATE_FROM_MS_REQUIRES_CAPABILITY                                              = D3D12_MESSAGE_ID(1325).value
D3D12_MESSAGE_ID_SHADERCACHESESSION_SHADERCACHEDELETE_NOTSUPPORTED                                             = D3D12_MESSAGE_ID(1326).value
D3D12_MESSAGE_ID_SHADERCACHECONTROL_SHADERCACHECLEAR_NOTSUPPORTED                                              = D3D12_MESSAGE_ID(1327).value
D3D12_MESSAGE_ID_CREATERESOURCE_STATE_IGNORED                                                                  = D3D12_MESSAGE_ID(1328).value
D3D12_MESSAGE_ID_UNUSED_CROSS_EXECUTE_SPLIT_BARRIER                                                            = D3D12_MESSAGE_ID(1329).value
D3D12_MESSAGE_ID_DEVICE_OPEN_SHARED_HANDLE_ACCESS_DENIED                                                       = D3D12_MESSAGE_ID(1330).value
D3D12_MESSAGE_ID_INCOMPATIBLE_BARRIER_VALUES                                                                   = D3D12_MESSAGE_ID(1331).value
D3D12_MESSAGE_ID_INCOMPATIBLE_BARRIER_ACCESS                                                                   = D3D12_MESSAGE_ID(1332).value
D3D12_MESSAGE_ID_INCOMPATIBLE_BARRIER_SYNC                                                                     = D3D12_MESSAGE_ID(1333).value
D3D12_MESSAGE_ID_INCOMPATIBLE_BARRIER_LAYOUT                                                                   = D3D12_MESSAGE_ID(1334).value
D3D12_MESSAGE_ID_INCOMPATIBLE_BARRIER_TYPE                                                                     = D3D12_MESSAGE_ID(1335).value
D3D12_MESSAGE_ID_OUT_OF_BOUNDS_BARRIER_SUBRESOURCE_RANGE                                                       = D3D12_MESSAGE_ID(1336).value
D3D12_MESSAGE_ID_INCOMPATIBLE_BARRIER_RESOURCE_DIMENSION                                                       = D3D12_MESSAGE_ID(1337).value
D3D12_MESSAGE_ID_SET_SCISSOR_RECTS_INVALID_RECT                                                                = D3D12_MESSAGE_ID(1338).value
D3D12_MESSAGE_ID_SHADING_RATE_SOURCE_REQUIRES_DIMENSION_TEXTURE2D                                              = D3D12_MESSAGE_ID(1339).value
D3D12_MESSAGE_ID_BUFFER_BARRIER_SUBREGION_OUT_OF_BOUNDS                                                        = D3D12_MESSAGE_ID(1340).value
D3D12_MESSAGE_ID_UNSUPPORTED_BARRIER_LAYOUT                                                                    = D3D12_MESSAGE_ID(1341).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_INVALID_PARAMETERS                                                      = D3D12_MESSAGE_ID(1342).value
D3D12_MESSAGE_ID_ENHANCED_BARRIERS_NOT_SUPPORTED                                                               = D3D12_MESSAGE_ID(1343).value
D3D12_MESSAGE_ID_LEGACY_BARRIER_VALIDATION_FORCED_ON                                                           = D3D12_MESSAGE_ID(1346).value
D3D12_MESSAGE_ID_EMPTY_ROOT_DESCRIPTOR_TABLE                                                                   = D3D12_MESSAGE_ID(1347).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_ELEMENT_OFFSET_UNALIGNED                                                    = D3D12_MESSAGE_ID(1348).value
D3D12_MESSAGE_ID_ALPHA_BLEND_FACTOR_NOT_SUPPORTED                                                              = D3D12_MESSAGE_ID(1349).value
D3D12_MESSAGE_ID_BARRIER_INTEROP_INVALID_LAYOUT                                                                = D3D12_MESSAGE_ID(1350).value
D3D12_MESSAGE_ID_BARRIER_INTEROP_INVALID_STATE                                                                 = D3D12_MESSAGE_ID(1351).value
D3D12_MESSAGE_ID_GRAPHICS_PIPELINE_STATE_DESC_ZERO_SAMPLE_MASK                                                 = D3D12_MESSAGE_ID(1352).value
D3D12_MESSAGE_ID_INDEPENDENT_STENCIL_REF_NOT_SUPPORTED                                                         = D3D12_MESSAGE_ID(1353).value
D3D12_MESSAGE_ID_CREATEDEPTHSTENCILSTATE_INDEPENDENT_MASKS_UNSUPPORTED                                         = D3D12_MESSAGE_ID(1354).value
D3D12_MESSAGE_ID_TEXTURE_BARRIER_SUBRESOURCES_OUT_OF_BOUNDS                                                    = D3D12_MESSAGE_ID(1355).value
D3D12_MESSAGE_ID_NON_OPTIMAL_BARRIER_ONLY_EXECUTE_COMMAND_LISTS                                                = D3D12_MESSAGE_ID(1356).value
D3D12_MESSAGE_ID_EXECUTE_INDIRECT_ZERO_COMMAND_COUNT                                                           = D3D12_MESSAGE_ID(1357).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_INCOMPATIBLE_TEXTURE_LAYOUT                                              = D3D12_MESSAGE_ID(1358).value
D3D12_MESSAGE_ID_DYNAMIC_INDEX_BUFFER_STRIP_CUT_NOT_SUPPORTED                                                  = D3D12_MESSAGE_ID(1359).value
D3D12_MESSAGE_ID_PRIMITIVE_TOPOLOGY_TRIANGLE_FANS_NOT_SUPPORTED                                                = D3D12_MESSAGE_ID(1360).value
D3D12_MESSAGE_ID_CREATE_SAMPLER_COMPARISON_FUNC_IGNORED                                                        = D3D12_MESSAGE_ID(1361).value
D3D12_MESSAGE_ID_CREATEHEAP_INVALIDHEAPTYPE                                                                    = D3D12_MESSAGE_ID(1362).value
D3D12_MESSAGE_ID_CREATERESOURCEANDHEAP_INVALIDHEAPTYPE                                                         = D3D12_MESSAGE_ID(1363).value
D3D12_MESSAGE_ID_DYNAMIC_DEPTH_BIAS_NOT_SUPPORTED                                                              = D3D12_MESSAGE_ID(1364).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_NON_WHOLE_DYNAMIC_DEPTH_BIAS                                            = D3D12_MESSAGE_ID(1365).value
D3D12_MESSAGE_ID_DYNAMIC_DEPTH_BIAS_FLAG_MISSING                                                               = D3D12_MESSAGE_ID(1366).value
D3D12_MESSAGE_ID_DYNAMIC_DEPTH_BIAS_NO_PIPELINE                                                                = D3D12_MESSAGE_ID(1367).value
D3D12_MESSAGE_ID_DYNAMIC_INDEX_BUFFER_STRIP_CUT_FLAG_MISSING                                                   = D3D12_MESSAGE_ID(1368).value
D3D12_MESSAGE_ID_DYNAMIC_INDEX_BUFFER_STRIP_CUT_NO_PIPELINE                                                    = D3D12_MESSAGE_ID(1369).value
D3D12_MESSAGE_ID_NONNORMALIZED_COORDINATE_SAMPLING_NOT_SUPPORTED                                               = D3D12_MESSAGE_ID(1370).value
D3D12_MESSAGE_ID_INVALID_CAST_TARGET                                                                           = D3D12_MESSAGE_ID(1371).value
D3D12_MESSAGE_ID_RENDER_PASS_COMMANDLIST_INVALID_END_STATE                                                     = D3D12_MESSAGE_ID(1372).value
D3D12_MESSAGE_ID_RENDER_PASS_COMMANDLIST_INVALID_START_STATE                                                   = D3D12_MESSAGE_ID(1373).value
D3D12_MESSAGE_ID_RENDER_PASS_MISMATCHING_ACCESS                                                                = D3D12_MESSAGE_ID(1374).value
D3D12_MESSAGE_ID_RENDER_PASS_MISMATCHING_LOCAL_PRESERVE_PARAMETERS                                             = D3D12_MESSAGE_ID(1375).value
D3D12_MESSAGE_ID_RENDER_PASS_LOCAL_PRESERVE_RENDER_PARAMETERS_ERROR                                            = D3D12_MESSAGE_ID(1376).value
D3D12_MESSAGE_ID_RENDER_PASS_LOCAL_DEPTH_STENCIL_ERROR                                                         = D3D12_MESSAGE_ID(1377).value
D3D12_MESSAGE_ID_DRAW_POTENTIALLY_OUTSIDE_OF_VALID_RENDER_AREA                                                 = D3D12_MESSAGE_ID(1378).value
D3D12_MESSAGE_ID_CREATERASTERIZERSTATE_INVALID_LINERASTERIZATIONMODE                                           = D3D12_MESSAGE_ID(1379).value
D3D12_MESSAGE_ID_CREATERESOURCE_INVALIDALIGNMENT_SMALLRESOURCE                                                 = D3D12_MESSAGE_ID(1380).value
D3D12_MESSAGE_ID_GENERIC_DEVICE_OPERATION_UNSUPPORTED                                                          = D3D12_MESSAGE_ID(1381).value
D3D12_MESSAGE_ID_CREATEGRAPHICSPIPELINESTATE_RENDER_TARGET_WRONG_WRITE_MASK                                    = D3D12_MESSAGE_ID(1382).value
D3D12_MESSAGE_ID_PROBABLE_PIX_EVENT_LEAK                                                                       = D3D12_MESSAGE_ID(1383).value
D3D12_MESSAGE_ID_PIX_EVENT_UNDERFLOW                                                                           = D3D12_MESSAGE_ID(1384).value
D3D12_MESSAGE_ID_RECREATEAT_INVALID_TARGET                                                                     = D3D12_MESSAGE_ID(1385).value
D3D12_MESSAGE_ID_RECREATEAT_INSUFFICIENT_SUPPORT                                                               = D3D12_MESSAGE_ID(1386).value
D3D12_MESSAGE_ID_GPU_BASED_VALIDATION_STRUCTURED_BUFFER_STRIDE_MISMATCH                                        = D3D12_MESSAGE_ID(1387).value
D3D12_MESSAGE_ID_DISPATCH_GRAPH_INVALID                                                                        = D3D12_MESSAGE_ID(1388).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_TARGET_FORMAT_INVALID                                                       = D3D12_MESSAGE_ID(1389).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_TARGET_DIMENSION_INVALID                                                    = D3D12_MESSAGE_ID(1390).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_SOURCE_COLOR_FORMAT_INVALID                                                 = D3D12_MESSAGE_ID(1391).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_SOURCE_DEPTH_FORMAT_INVALID                                                 = D3D12_MESSAGE_ID(1392).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_EXPOSURE_SCALE_FORMAT_INVALID                                               = D3D12_MESSAGE_ID(1393).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_ENGINE_CREATE_FLAGS_INVALID                                                 = D3D12_MESSAGE_ID(1394).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_EXTENSION_INTERNAL_LOAD_FAILURE                                             = D3D12_MESSAGE_ID(1395).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_EXTENSION_INTERNAL_ENGINE_CREATION_ERROR                                    = D3D12_MESSAGE_ID(1396).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_EXTENSION_INTERNAL_UPSCALER_CREATION_ERROR                                  = D3D12_MESSAGE_ID(1397).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_EXTENSION_INTERNAL_UPSCALER_EXECUTION_ERROR                                 = D3D12_MESSAGE_ID(1398).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_REGION_INVALID                                             = D3D12_MESSAGE_ID(1399).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_TIME_DELTA_INVALID                                         = D3D12_MESSAGE_ID(1400).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_REQUIRED_TEXTURE_IS_NULL                                   = D3D12_MESSAGE_ID(1401).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_MOTION_VECTORS_FORMAT_INVALID                              = D3D12_MESSAGE_ID(1402).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_FLAGS_INVALID                                              = D3D12_MESSAGE_ID(1403).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_FORMAT_INVALID                                             = D3D12_MESSAGE_ID(1404).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_EXPOSURE_SCALE_TEXTURE_SIZE_INVALID                        = D3D12_MESSAGE_ID(1405).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_VARIANT_INDEX_OUT_OF_BOUNDS                                                 = D3D12_MESSAGE_ID(1406).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_VARIANT_ID_NOT_FOUND                                                        = D3D12_MESSAGE_ID(1407).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_DUPLICATE_VARIANT_ID                                                        = D3D12_MESSAGE_ID(1408).value
D3D12_MESSAGE_ID_DIRECTSR_OUT_OF_MEMORY                                                                        = D3D12_MESSAGE_ID(1409).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_UNEXPECTED_TEXTURE_IS_IGNORED                              = D3D12_MESSAGE_ID(1410).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EVICT_UNDERFLOW                                                    = D3D12_MESSAGE_ID(1411).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_OPTIONAL_TEXTURE_IS_NULL                                   = D3D12_MESSAGE_ID(1412).value
D3D12_MESSAGE_ID_DIRECTSR_SUPERRES_UPSCALER_EXECUTE_INVALID_CAMERA_JITTER                                      = D3D12_MESSAGE_ID(1413).value
D3D12_MESSAGE_ID_CREATE_STATE_OBJECT_WARNING                                                                   = D3D12_MESSAGE_ID(1414).value
D3D12_MESSAGE_ID_GUID_TEXTURE_LAYOUT_UNSUPPORTED                                                               = D3D12_MESSAGE_ID(1415).value
D3D12_MESSAGE_ID_RESOLVE_ENCODER_INPUT_PARAM_LAYOUT_INVALID_PARAMETERS                                         = D3D12_MESSAGE_ID(1416).value
D3D12_MESSAGE_ID_INVALID_BARRIER_ACCESS                                                                        = D3D12_MESSAGE_ID(1417).value
D3D12_MESSAGE_ID_COMMAND_LIST_DRAW_INSTANCE_COUNT_ZERO                                                         = D3D12_MESSAGE_ID(1418).value
D3D12_MESSAGE_ID_DESCRIPTOR_HEAP_NOT_SET_BEFORE_ROOT_SIGNATURE_WITH_DIRECTLY_INDEXED_FLAG                      = D3D12_MESSAGE_ID(1419).value
D3D12_MESSAGE_ID_DIFFERENT_DESCRIPTOR_HEAP_SET_AFTER_ROOT_SIGNATURE_WITH_DIRECTLY_INDEXED_FLAG                 = D3D12_MESSAGE_ID(1420).value
D3D12_MESSAGE_ID_APPLICATION_SPECIFIC_DRIVER_STATE_NOT_SUPPORTED                                               = D3D12_MESSAGE_ID(1421).value
D3D12_MESSAGE_ID_RENDER_TARGET_OR_DEPTH_STENCIL_RESOUCE_NOT_INITIALIZED                                        = D3D12_MESSAGE_ID(1422).value
D3D12_MESSAGE_ID_BYTECODE_VALIDATION_ERROR                                                                     = D3D12_MESSAGE_ID(1423).value
D3D12_MESSAGE_ID_FENCE_ZERO_WAIT                                                                               = D3D12_MESSAGE_ID(1424).value
D3D12_MESSAGE_ID_NON_COMMON_RESOURCE_IN_COPY_QUEUE                                                             = D3D12_MESSAGE_ID(1425).value
D3D12_MESSAGE_ID_D3D12_MESSAGES_END                                                                            = D3D12_MESSAGE_ID().value

D3D12_MESSAGE_SEVERITY = ctypes.c_uint
D3D12_MESSAGE_SEVERITY_CORRUPTION = D3D12_MESSAGE_SEVERITY().value
D3D12_MESSAGE_SEVERITY_ERROR      = D3D12_MESSAGE_SEVERITY().value
D3D12_MESSAGE_SEVERITY_WARNING    = D3D12_MESSAGE_SEVERITY().value
D3D12_MESSAGE_SEVERITY_INFO       = D3D12_MESSAGE_SEVERITY().value
D3D12_MESSAGE_SEVERITY_MESSAGE    = D3D12_MESSAGE_SEVERITY().value

D3D12_RLDO_FLAGS = ctypes.c_uint
D3D12_RLDO_NONE            = D3D12_RLDO_FLAGS(0x0).value
D3D12_RLDO_SUMMARY         = D3D12_RLDO_FLAGS(0x1).value
D3D12_RLDO_DETAIL          = D3D12_RLDO_FLAGS(0x2).value
D3D12_RLDO_IGNORE_INTERNAL = D3D12_RLDO_FLAGS(0x4).value


## ---------------------------------------- callback types ----


D3D12MessageFunc = ctypes.WINFUNCTYPE(
    None,                    # the return type
    D3D12_MESSAGE_CATEGORY,  # D3D12_MESSAGE_CATEGORY Category
    D3D12_MESSAGE_SEVERITY,  # D3D12_MESSAGE_SEVERITY Severity
    D3D12_MESSAGE_ID,        # D3D12_MESSAGE_ID ID
    ctypes.c_char_p,         # LPCSTR pDescription
    ctypes.c_void_p,         # void* pContext
)


## ---------------------------------------------- interfaces ----

## Declarations only. Vtables are assigned at the end of the file, once every
## class exists, so anything may reference anything.


class ID3D12Debug(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{344488b7-6846-474b-b989-f027448245e0}")


class ID3D12Debug1(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{affaa4ca-63fe-4d8e-b8ad-159000af4304}")


class ID3D12Debug2(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{93a665c4-a3b2-4e5d-b692-a26ae14e3374}")


class ID3D12Debug3(ID3D12Debug):
    _iid_ = comtypes.GUID("{5cf4e58f-f671-4ff1-a542-3686e3d153d1}")


class ID3D12Debug4(ID3D12Debug3):
    _iid_ = comtypes.GUID("{014b816e-9ec5-4a2f-a845-ffbe441ce13a}")


class ID3D12Debug5(ID3D12Debug4):
    _iid_ = comtypes.GUID("{548d6b12-09fa-40e0-9069-5dcd589a52c9}")


class ID3D12Debug6(ID3D12Debug5):
    _iid_ = comtypes.GUID("{82a816d6-5d01-4157-97d0-4975463fd1ed}")


class ID3D12DebugCommandList(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{09e0bf36-54ac-484f-8847-4baeeab6053f}")


class ID3D12DebugCommandList1(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{102ca951-311b-4b01-b11f-ecb83e061b37}")


class ID3D12DebugCommandList2(ID3D12DebugCommandList):
    _iid_ = comtypes.GUID("{aeb575cf-4e06-48be-ba3b-c450fc96652e}")


class ID3D12DebugCommandList3(ID3D12DebugCommandList2):
    _iid_ = comtypes.GUID("{197d5e15-4d37-4d34-af78-724cd70fdb1f}")


class ID3D12DebugCommandQueue(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{09e0bf36-54ac-484f-8847-4baeeab6053a}")


class ID3D12DebugCommandQueue1(ID3D12DebugCommandQueue):
    _iid_ = comtypes.GUID("{16be35a2-bfd6-49f2-bcae-eaae4aff862d}")


class ID3D12DebugDevice(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{3febd6dd-4973-4787-8194-e45f9e28923e}")


class ID3D12DebugDevice1(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{a9b71770-d099-4a65-a698-3dee10020f88}")


class ID3D12DebugDevice2(ID3D12DebugDevice):
    _iid_ = comtypes.GUID("{60eccbc1-378d-4df1-894c-f8ac5ce4d7dd}")


class ID3D12InfoQueue(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{0742a90b-c387-483f-b946-30a7e4e61458}")


class ID3D12InfoQueue1(ID3D12InfoQueue):
    _iid_ = comtypes.GUID("{2852dd88-b484-4c0c-b6b1-67168500e600}")


class ID3D12ManualWriteTrackingResource(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{86ca3b85-49ad-4b6e-aed5-eddb18540f41}")


class ID3D12SharingContract(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{0adf7d52-929c-4e61-addb-ffed30de66ef}")


## ---------------------------------------------- structures ----


class D3D12_DEBUG_COMMAND_LIST_GPU_BASED_VALIDATION_SETTINGS(ctypes.Structure):
    _fields_ = [('ShaderPatchMode', D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE),
    ]


class D3D12_DEBUG_DEVICE_GPU_BASED_VALIDATION_SETTINGS(ctypes.Structure):
    _fields_ = [('MaxMessagesPerCommandList', ctypes.c_uint32),
                ('DefaultShaderPatchMode',    D3D12_GPU_BASED_VALIDATION_SHADER_PATCH_MODE),
                ('PipelineStateCreateFlags',  D3D12_GPU_BASED_VALIDATION_PIPELINE_STATE_CREATE_FLAGS),
    ]


class D3D12_DEBUG_DEVICE_GPU_SLOWDOWN_PERFORMANCE_FACTOR(ctypes.Structure):
    _fields_ = [('SlowdownFactor', ctypes.c_float),
    ]


class D3D12_INFO_QUEUE_FILTER_DESC(ctypes.Structure):
    _fields_ = [('NumCategories', ctypes.c_uint32),
                ('pCategoryList', ctypes.POINTER(D3D12_MESSAGE_CATEGORY)),
                ('NumSeverities', ctypes.c_uint32),
                ('pSeverityList', ctypes.POINTER(D3D12_MESSAGE_SEVERITY)),
                ('NumIDs',        ctypes.c_uint32),
                ('pIDList',       ctypes.POINTER(D3D12_MESSAGE_ID)),
    ]


class D3D12_MESSAGE(ctypes.Structure):
    _fields_ = [('Category',              D3D12_MESSAGE_CATEGORY),
                ('Severity',              D3D12_MESSAGE_SEVERITY),
                ('ID',                    D3D12_MESSAGE_ID),
                ('pDescription',          ctypes.POINTER(ctypes.c_char)),
                ('DescriptionByteLength', ctypes.c_size_t),
    ]


class D3D12_INFO_QUEUE_FILTER(ctypes.Structure):
    _fields_ = [('AllowList', D3D12_INFO_QUEUE_FILTER_DESC),
                ('DenyList',  D3D12_INFO_QUEUE_FILTER_DESC),
    ]


## ------------------------- vtables, assigned once every class exists ----

ID3D12Debug._methods_ = [
    comtypes.STDMETHOD(None, "EnableDebugLayer", []),
]

ID3D12Debug1._methods_ = [
    comtypes.STDMETHOD(None, "EnableDebugLayer", []),
    comtypes.STDMETHOD(None, "SetEnableGPUBasedValidation", [
        wintypes.BOOL,                               # BOOL Enable
        ]),
    comtypes.STDMETHOD(None, "SetEnableSynchronizedCommandQueueValidation", [
        wintypes.BOOL,                               # BOOL Enable
        ]),
]

ID3D12Debug2._methods_ = [
    comtypes.STDMETHOD(None, "SetGPUBasedValidationFlags", [
        D3D12_GPU_BASED_VALIDATION_FLAGS,            # D3D12_GPU_BASED_VALIDATION_FLAGS Flags
        ]),
]

ID3D12Debug3._methods_ = [
    comtypes.STDMETHOD(None, "SetEnableGPUBasedValidation", [
        wintypes.BOOL,                               # BOOL Enable
        ]),
    comtypes.STDMETHOD(None, "SetEnableSynchronizedCommandQueueValidation", [
        wintypes.BOOL,                               # BOOL Enable
        ]),
    comtypes.STDMETHOD(None, "SetGPUBasedValidationFlags", [
        D3D12_GPU_BASED_VALIDATION_FLAGS,            # D3D12_GPU_BASED_VALIDATION_FLAGS Flags
        ]),
]

ID3D12Debug4._methods_ = [
    comtypes.STDMETHOD(None, "DisableDebugLayer", []),
]

ID3D12Debug5._methods_ = [
    comtypes.STDMETHOD(None, "SetEnableAutoName", [
        wintypes.BOOL,                               # BOOL Enable
        ]),
]

ID3D12Debug6._methods_ = [
    comtypes.STDMETHOD(None, "SetForceLegacyBarrierValidation", [
        wintypes.BOOL,                               # BOOL Enable
        ]),
]

ID3D12DebugCommandList._methods_ = [
    comtypes.STDMETHOD(wintypes.BOOL, "AssertResourceState", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        ctypes.c_uint32,                             # UINT State
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetFeatureMask", [
        D3D12_DEBUG_FEATURE,                         # D3D12_DEBUG_FEATURE Mask
        ]),
    comtypes.STDMETHOD(D3D12_DEBUG_FEATURE, "GetFeatureMask", []),
]

ID3D12DebugCommandList1._methods_ = [
    comtypes.STDMETHOD(wintypes.BOOL, "AssertResourceState", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        ctypes.c_uint32,                             # UINT State
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetDebugParameter", [
        D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE,     # D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDebugParameter", [
        D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE,     # D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
]

ID3D12DebugCommandList2._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SetDebugParameter", [
        D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE,     # D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDebugParameter", [
        D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE,     # D3D12_DEBUG_COMMAND_LIST_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
]

ID3D12DebugCommandList3._methods_ = [
    comtypes.STDMETHOD(None, "AssertResourceAccess", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        D3D12_BARRIER_ACCESS,                        # D3D12_BARRIER_ACCESS Access
        ]),
    comtypes.STDMETHOD(None, "AssertTextureLayout", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        D3D12_BARRIER_LAYOUT,                        # D3D12_BARRIER_LAYOUT Layout
        ]),
]

ID3D12DebugCommandQueue._methods_ = [
    comtypes.STDMETHOD(wintypes.BOOL, "AssertResourceState", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        ctypes.c_uint32,                             # UINT State
        ]),
]

ID3D12DebugCommandQueue1._methods_ = [
    comtypes.STDMETHOD(None, "AssertResourceAccess", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        D3D12_BARRIER_ACCESS,                        # D3D12_BARRIER_ACCESS Access
        ]),
    comtypes.STDMETHOD(None, "AssertTextureLayout", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        D3D12_BARRIER_LAYOUT,                        # D3D12_BARRIER_LAYOUT Layout
        ]),
]

ID3D12DebugDevice._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SetFeatureMask", [
        D3D12_DEBUG_FEATURE,                         # D3D12_DEBUG_FEATURE Mask
        ]),
    comtypes.STDMETHOD(D3D12_DEBUG_FEATURE, "GetFeatureMask", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "ReportLiveDeviceObjects", [
        D3D12_RLDO_FLAGS,                            # D3D12_RLDO_FLAGS Flags
        ]),
]

ID3D12DebugDevice1._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SetDebugParameter", [
        D3D12_DEBUG_DEVICE_PARAMETER_TYPE,           # D3D12_DEBUG_DEVICE_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDebugParameter", [
        D3D12_DEBUG_DEVICE_PARAMETER_TYPE,           # D3D12_DEBUG_DEVICE_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "ReportLiveDeviceObjects", [
        D3D12_RLDO_FLAGS,                            # D3D12_RLDO_FLAGS Flags
        ]),
]

ID3D12DebugDevice2._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SetDebugParameter", [
        D3D12_DEBUG_DEVICE_PARAMETER_TYPE,           # D3D12_DEBUG_DEVICE_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetDebugParameter", [
        D3D12_DEBUG_DEVICE_PARAMETER_TYPE,           # D3D12_DEBUG_DEVICE_PARAMETER_TYPE Type
        ctypes.c_void_p,                             # void* pData
        ctypes.c_uint32,                             # UINT DataSize
        ]),
]

ID3D12InfoQueue._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "SetMessageCountLimit", [
        ctypes.c_uint64,                             # UINT64 MessageCountLimit
        ]),
    comtypes.STDMETHOD(None, "ClearStoredMessages", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetMessage", [
        ctypes.c_uint64,                             # UINT64 MessageIndex
        ctypes.POINTER(D3D12_MESSAGE),               # D3D12_MESSAGE* pMessage
        ctypes.POINTER(ctypes.c_size_t),             # SIZE_T* pMessageByteLength
        ]),
    comtypes.STDMETHOD(ctypes.c_uint64, "GetNumMessagesAllowedByStorageFilter", []),
    comtypes.STDMETHOD(ctypes.c_uint64, "GetNumMessagesDeniedByStorageFilter", []),
    comtypes.STDMETHOD(ctypes.c_uint64, "GetNumStoredMessages", []),
    comtypes.STDMETHOD(ctypes.c_uint64, "GetNumStoredMessagesAllowedByRetrievalFilter", []),
    comtypes.STDMETHOD(ctypes.c_uint64, "GetNumMessagesDiscardedByMessageCountLimit", []),
    comtypes.STDMETHOD(ctypes.c_uint64, "GetMessageCountLimit", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "AddStorageFilterEntries", [
        ctypes.POINTER(D3D12_INFO_QUEUE_FILTER),     # D3D12_INFO_QUEUE_FILTER* pFilter
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetStorageFilter", [
        ctypes.POINTER(D3D12_INFO_QUEUE_FILTER),     # D3D12_INFO_QUEUE_FILTER* pFilter
        ctypes.POINTER(ctypes.c_size_t),             # SIZE_T* pFilterByteLength
        ]),
    comtypes.STDMETHOD(None, "ClearStorageFilter", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "PushEmptyStorageFilter", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "PushCopyOfStorageFilter", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "PushStorageFilter", [
        ctypes.POINTER(D3D12_INFO_QUEUE_FILTER),     # D3D12_INFO_QUEUE_FILTER* pFilter
        ]),
    comtypes.STDMETHOD(None, "PopStorageFilter", []),
    comtypes.STDMETHOD(ctypes.c_uint32, "GetStorageFilterStackSize", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "AddRetrievalFilterEntries", [
        ctypes.POINTER(D3D12_INFO_QUEUE_FILTER),     # D3D12_INFO_QUEUE_FILTER* pFilter
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "GetRetrievalFilter", [
        ctypes.POINTER(D3D12_INFO_QUEUE_FILTER),     # D3D12_INFO_QUEUE_FILTER* pFilter
        ctypes.POINTER(ctypes.c_size_t),             # SIZE_T* pFilterByteLength
        ]),
    comtypes.STDMETHOD(None, "ClearRetrievalFilter", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "PushEmptyRetrievalFilter", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "PushCopyOfRetrievalFilter", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "PushRetrievalFilter", [
        ctypes.POINTER(D3D12_INFO_QUEUE_FILTER),     # D3D12_INFO_QUEUE_FILTER* pFilter
        ]),
    comtypes.STDMETHOD(None, "PopRetrievalFilter", []),
    comtypes.STDMETHOD(ctypes.c_uint32, "GetRetrievalFilterStackSize", []),
    comtypes.STDMETHOD(comtypes.HRESULT, "AddMessage", [
        D3D12_MESSAGE_CATEGORY,                      # D3D12_MESSAGE_CATEGORY Category
        D3D12_MESSAGE_SEVERITY,                      # D3D12_MESSAGE_SEVERITY Severity
        D3D12_MESSAGE_ID,                            # D3D12_MESSAGE_ID ID
        ctypes.c_char_p,                             # LPCSTR pDescription
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "AddApplicationMessage", [
        D3D12_MESSAGE_SEVERITY,                      # D3D12_MESSAGE_SEVERITY Severity
        ctypes.c_char_p,                             # LPCSTR pDescription
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnCategory", [
        D3D12_MESSAGE_CATEGORY,                      # D3D12_MESSAGE_CATEGORY Category
        wintypes.BOOL,                               # BOOL bEnable
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnSeverity", [
        D3D12_MESSAGE_SEVERITY,                      # D3D12_MESSAGE_SEVERITY Severity
        wintypes.BOOL,                               # BOOL bEnable
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnID", [
        D3D12_MESSAGE_ID,                            # D3D12_MESSAGE_ID ID
        wintypes.BOOL,                               # BOOL bEnable
        ]),
    comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnCategory", [
        D3D12_MESSAGE_CATEGORY,                      # D3D12_MESSAGE_CATEGORY Category
        ]),
    comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnSeverity", [
        D3D12_MESSAGE_SEVERITY,                      # D3D12_MESSAGE_SEVERITY Severity
        ]),
    comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnID", [
        D3D12_MESSAGE_ID,                            # D3D12_MESSAGE_ID ID
        ]),
    comtypes.STDMETHOD(None, "SetMuteDebugOutput", [
        wintypes.BOOL,                               # BOOL bMute
        ]),
    comtypes.STDMETHOD(wintypes.BOOL, "GetMuteDebugOutput", []),
]

ID3D12InfoQueue1._methods_ = [
    comtypes.STDMETHOD(comtypes.HRESULT, "RegisterMessageCallback", [
        D3D12MessageFunc,                            # D3D12MessageFunc CallbackFunc
        D3D12_MESSAGE_CALLBACK_FLAGS,                # D3D12_MESSAGE_CALLBACK_FLAGS CallbackFilterFlags
        ctypes.c_void_p,                             # void* pContext
        ctypes.POINTER(ctypes.c_uint32),             # DWORD* pCallbackCookie
        ]),
    comtypes.STDMETHOD(comtypes.HRESULT, "UnregisterMessageCallback", [
        ctypes.c_uint32,                             # DWORD CallbackCookie
        ]),
]

ID3D12ManualWriteTrackingResource._methods_ = [
    comtypes.STDMETHOD(None, "TrackWrite", [
        ctypes.c_uint32,                             # UINT Subresource
        ctypes.POINTER(D3D12_RANGE),                 # D3D12_RANGE* pWrittenRange
        ]),
]

ID3D12SharingContract._methods_ = [
    comtypes.STDMETHOD(None, "Present", [
        ctypes.POINTER(ID3D12Resource),              # ID3D12Resource* pResource
        ctypes.c_uint32,                             # UINT Subresource
        ctypes.c_void_p,                             # HWND window
        ]),
    comtypes.STDMETHOD(None, "SharedFenceSignal", [
        ctypes.POINTER(ID3D12Fence),                 # ID3D12Fence* pFence
        ctypes.c_uint64,                             # UINT64 FenceValue
        ]),
    comtypes.STDMETHOD(None, "BeginCapturableWork", [
        comtypes.GUID,                               # REFGUID guid
        ]),
    comtypes.STDMETHOD(None, "EndCapturableWork", [
        comtypes.GUID,                               # REFGUID guid
        ]),
]


## -- End Of File --
