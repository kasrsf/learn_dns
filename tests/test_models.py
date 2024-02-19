from learn_dns import DNSHeader
from learn_dns import DNSQuestion
from learn_dns import DNSRecord
from learn_dns import DNSPacket
from io import BytesIO


def test_dns_header_to_bytes():
    input_header = DNSHeader(
        id=0x1314,
        flags=0,
        num_questions=1,
        num_additionals=0,
        num_authorities=0,
        num_answers=0,
    )
    expected_output = b"\x13\x14\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"

    actual_output = input_header.to_bytes()
    assert actual_output == expected_output


def test_dns_header_from_bytes():
    input = b'`V\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00R\x9b\x00\x04]\xb8\xd8"'
    expected_output = DNSHeader(
        id=24662,
        flags=33152,
        num_questions=1,
        num_answers=1,
        num_authorities=0,
        num_additionals=0,
    )

    actual_output = DNSHeader.from_bytes(BytesIO(input))
    assert actual_output == expected_output


def test_dns_question_from_bytes():
    input = b'`V\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00R\x9b\x00\x04]\xb8\xd8"'
    expected_output = DNSQuestion(name=b"www.example.com", type_=1, class_=1)

    reader = BytesIO(input)
    DNSHeader.from_bytes(reader)
    actual_output = DNSQuestion.from_bytes(reader)

    assert actual_output == expected_output


def test_dns_record_from_bytes():
    input = b'`V\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00R\x9b\x00\x04]\xb8\xd8"'
    expected_output = DNSRecord(
        name=b"www.example.com",
        type_=1,
        class_=1,
        ttl=21147,
        data=b']\xb8\xd8"',
    )

    reader = BytesIO(input)
    DNSHeader.from_bytes(reader)
    DNSQuestion.from_bytes(reader)
    actual_output = DNSRecord.from_bytes(reader)
    assert actual_output == expected_output


def test_dns_packet_from_bytes():
    input = b'`V\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00R\x9b\x00\x04]\xb8\xd8"'
    expected_output = DNSPacket(
        header=DNSHeader(
            id=24662,
            flags=33152,
            num_questions=1,
            num_answers=1,
            num_authorities=0,
            num_additionals=0,
        ),
        questions=[DNSQuestion(name=b"www.example.com", type_=1, class_=1)],
        answers=[
            DNSRecord(
                name=b"www.example.com",
                type_=1,
                class_=1,
                ttl=21147,
                data=b']\xb8\xd8"',
            )
        ],
        authorities=[],
        additionals=[],
    )

    actual_output = DNSPacket.from_bytes(input)
    assert actual_output == expected_output
