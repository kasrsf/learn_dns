from dataclasses import dataclass
import dataclasses
import struct


@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

    def to_bytes(self):
        fields = dataclasses.astuple(self)
        # there are 6 `H`s because there are 6 fields
        return struct.pack("!HHHHHH", *fields)


@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int

    def to_bytes(self):
        return self.name + struct.pack("!HH", self.type_, self.class_)
