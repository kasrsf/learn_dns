from learn_dns.dns import encode_dns_name
from learn_dns.dns import build_query
from learn_dns.dns import send_query
from learn_dns import DNSRecord
from learn_dns.consts import TYPE_A


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


def test_send_query():
    input_args = {
        "ip_address": "8.8.8.8",
        "domain_name": "example.com",
        "record_type": TYPE_A,
        "enable_recursion_desired_flag": True,
    }
    expected_output_record = DNSRecord(
        name=b"example.com", type_=1, class_=1, ttl=18366, data="93.184.216.34"
    )

    output = send_query(**input_args)
    output_record = output.answers[0]
    output_record.ttl = expected_output_record.ttl
    assert output.answers[0] == expected_output_record
