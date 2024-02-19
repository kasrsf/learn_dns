from learn_dns.utils import ip_to_string


def test_ip_to_string():
    input = b']\xb8\xd8"'
    expected_output = "93.184.216.34"

    actual_output = ip_to_string(input)
    assert actual_output == expected_output
