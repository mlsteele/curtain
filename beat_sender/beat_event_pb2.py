# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: beat_event.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='beat_event.proto',
  package='',
  serialized_pb='\n\x10\x62\x65\x61t_event.proto\")\n\tBeatEvent\x12\x0b\n\x03\x62\x61r\x18\x01 \x02(\x05\x12\x0f\n\x07sub_bar\x18\x02 \x01(\x05')




_BEATEVENT = _descriptor.Descriptor(
  name='BeatEvent',
  full_name='BeatEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bar', full_name='BeatEvent.bar', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sub_bar', full_name='BeatEvent.sub_bar', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=20,
  serialized_end=61,
)

DESCRIPTOR.message_types_by_name['BeatEvent'] = _BEATEVENT

class BeatEvent(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BEATEVENT

  # @@protoc_insertion_point(class_scope:BeatEvent)


# @@protoc_insertion_point(module_scope)