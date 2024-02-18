import socket

from learn_dns.dns import build_query


def main():
    query = build_query("www.example.com", 1)

    # create a UDP socket
    # `socket.AF_INET` means we're connecting to the internet
    #   (as opposed to a Unix domain socket `AF_UNIX` for example)
    # `socket.SOCK_DGRAM` means "UDP"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send our query to 8.8.8.8, port 53. port 53 is the DNS port.
    sock.sendto(query, ("8.8.8.8", 53))

    # read the response. UDP DNS response are usually less than 512 bytes
    # so reading 1024 bytes is enough
    response, _ = sock.recvfrom(1024)
    print(response)


if __name__ == "__main__":
    main()
