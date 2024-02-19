import socket
import random

from learn_dns import DNSQuestion
from learn_dns import DNSHeader
from learn_dns import DNSPacket
from learn_dns.consts import CLASS_IN

random.seed(1)


def encode_dns_name(domain_name: str) -> bytes:
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded += bytes([len(part)]) + part
    return encoded + b"\x00"


def build_query(
    domain_name: str, record_type: int, enable_recursion_desired_flag: bool = True
) -> bytes:
    name = encode_dns_name(domain_name)
    id = random.randint(0, 65535)

    # if asking a DNS resolver (a cache) we set flags to RECURSION_DESIRED but if
    # asking an authoritative nameserver (the source of truth) will need to set flags=0 instead
    if enable_recursion_desired_flag:
        flags = 1 << 8
    else:
        flags = 0
    header = DNSHeader(id=id, num_questions=1, flags=flags)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header.to_bytes() + question.to_bytes()


def send_query(
    ip_address: str,
    domain_name: str,
    record_type: int,
    enable_recursion_desired_flag: bool = True,
) -> DNSPacket:
    query = build_query(
        domain_name,
        record_type,
        enable_recursion_desired_flag=enable_recursion_desired_flag,
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, (ip_address, 53))

    data, _ = sock.recvfrom(1024)
    return DNSPacket.from_bytes(data)
