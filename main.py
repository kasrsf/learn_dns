import argparse
import socket

from learn_dns import DNSPacket
from learn_dns.consts import TYPE_A
from learn_dns.dns import build_query
from learn_dns.dns import send_query
from learn_dns.utils import ip_to_string


def lookup_domain(domain_name):
    # TODO: address bugs:
    #     - poetry run python main.py www.metafilter.com gives 192.16
    #     - poetry run python main.py www.facebook.com gives 9.115.116.97.114.45.109.105.110.105.4.99.49.48.114.192.16
    # hint: look at the record type!
    query = build_query(domain_name, 1)

    # create a UDP socket
    # `socket.AF_INET` means we're connecting to the internet
    #   (as opposed to a Unix domain socket `AF_UNIX` for example)
    # `socket.SOCK_DGRAM` means "UDP"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send our query to 8.8.8.8, port 53. port 53 is the DNS port.
    sock.sendto(query, ("8.8.8.8", 53))

    # read the response. UDP DNS response are usually less than 512 bytes
    # so reading 1024 bytes is enough
    data, _ = sock.recvfrom(1024)
    response = DNSPacket.from_bytes(data)
    return ip_to_string(response.answers[0].data)


def resolve(domain_name: str, record_type: int):
    nameserver = "198.41.0.4"
    while True:
        print(f"Querying {nameserver} for {domain_name}")
        response = send_query(nameserver, domain_name, record_type)
        if ip := response.get_answer():
            return ip
        elif nsIP := response.get_nameserver_ip():
            nameserver = nsIP
        # look up the nameserver's IP address if there is one
        elif ns_domain := response.get_nameserver():
            nameserver = resolve(ns_domain, TYPE_A)
        else:
            raise Exception("something went wrong")


def main():
    parser = argparse.ArgumentParser(description="Look up the IP address of a domain.")
    parser.add_argument("domain_name", type=str, help="The domain name to look up.")
    args = parser.parse_args()

    ip_address = lookup_domain(args.domain_name)
    print(f"The IP address of {args.domain_name} is {ip_address}")


if __name__ == "__main__":
    main()
