from learn_dns.dns import encode_dns_name
from learn_dns.dns import build_query
from learn_dns.dns import TYPE_A


def test_encode_dns_name():
    input = "google.com"
    expected_output = b"\x06google\x03com\x00"

    output = encode_dns_name(input)
    assert output == expected_output


def test_build_query():
    input_args = {"domain_name": "example.com", "record_type": TYPE_A}
    expected_output = b"D\xcb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"

    output = build_query(**input_args)
    assert output == expected_output
