from learn_dns import DNSHeader


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
