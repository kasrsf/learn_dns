from typing import List

from dataclasses import dataclass
import dataclasses
from io import BytesIO
import struct


def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result


def decode_name(reader: BytesIO):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(length, reader))
            break
        else:
            parts.append(reader.read(length))
    return b".".join(parts)


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

    @staticmethod
    def from_bytes(reader: BytesIO):
        items = struct.unpack("!HHHHHH", reader.read(12))
        return DNSHeader(*items)


@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int

    def to_bytes(self):
        return self.name + struct.pack("!HH", self.type_, self.class_)

    @staticmethod
    def from_bytes(reader: BytesIO):
        name = decode_name(reader)
        data = reader.read(4)
        type_, class_ = struct.unpack("!HH", data)
        return DNSQuestion(name, type_, class_)


@dataclass
class DNSRecord:
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes

    @staticmethod
    def from_bytes(reader: BytesIO):
        name = decode_name(reader)
        # the type, class, ttl, and data length together are 10 bytes (2 + 2 + 4 + 2 = 10)
        # so we read 10 bytes
        data = reader.read(10)
        # HHIH means 2-byte int, 2-byte int, 4-byte int, 2-byte int
        type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
        data = reader.read(data_len)
        return DNSRecord(name, type_, class_, ttl, data)


@dataclass
class DNSPacket:
    header: DNSHeader
    questions: List[DNSQuestion]
    answers: List[DNSRecord]
    authorities: List[DNSRecord]
    additionals: List[DNSRecord]

    @staticmethod
    def from_bytes(data: bytes):
        reader = BytesIO(data)
        header = DNSHeader.from_bytes(reader)
        questions = [
            DNSQuestion.from_bytes(reader) for _ in range(header.num_questions)
        ]
        answers = [DNSRecord.from_bytes(reader) for _ in range(header.num_answers)]
        authorities = [
            DNSRecord.from_bytes(reader) for _ in range(header.num_authorities)
        ]
        additionals = [
            DNSRecord.from_bytes(reader) for _ in range(header.num_additionals)
        ]

        return DNSPacket(header, questions, answers, authorities, additionals)
