# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: signData.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'signData.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0esignData.proto\x12\x0fsignDataPackage\"\x19\n\x07Gesture\x12\x0e\n\x06points\x18\x01 \x03(\x02\"K\n\x0eRequestMessage\x12&\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x18.signDataPackage.Gesture\x12\x11\n\ttimestamp\x18\x02 \x01(\t\" \n\x0fResponseMessage\x12\r\n\x05reply\x18\x01 \x01(\t2m\n\x11StreamDataService\x12X\n\x13\x62iDirectionalStream\x12\x1f.signDataPackage.RequestMessage\x1a .signDataPackage.ResponseMessageb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'signData_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GESTURE']._serialized_start=35
  _globals['_GESTURE']._serialized_end=60
  _globals['_REQUESTMESSAGE']._serialized_start=62
  _globals['_REQUESTMESSAGE']._serialized_end=137
  _globals['_RESPONSEMESSAGE']._serialized_start=139
  _globals['_RESPONSEMESSAGE']._serialized_end=171
  _globals['_STREAMDATASERVICE']._serialized_start=173
  _globals['_STREAMDATASERVICE']._serialized_end=282
# @@protoc_insertion_point(module_scope)