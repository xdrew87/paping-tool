import socket
import time
import argparse
from termcolor import colored

def tcp_ping(host, port, timeout=2):
    try:
        start_time = time.time()
        with socket.create_connection((host, port), timeout):
            response_time = (time.time() - start_time) * 1000  # in milliseconds
        return True, response_time
    except Exception as e:
        return False, str(e)

def udp_ping(host, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
            udp_sock.settimeout(timeout)
            message = b"ping"
            start_time = time.time()
            udp_sock.sendto(message, (host, port))
            udp_sock.recvfrom(1024)  # Waiting for a response
            response_time = (time.time() - start_time) * 1000  # in milliseconds
        return True, response_time
    except socket.timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="Paping - TCP/UDP Ping Tool")
    parser.add_argument("host", help="Target hostname or IP address")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("-p", "--protocol", choices=["tcp", "udp"], default="tcp", help="Protocol to use (default: tcp)")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="Timeout in seconds (default: 2)")
    parser.add_argument("-i", "--interval", type=int, default=1, help="Interval between pings in seconds (default: 1)")

    args = parser.parse_args()
    host = args.host
    port = args.port
    protocol = args.protocol
    timeout = args.timeout
    interval = args.interval

    print(f"Pinging {colored(host, 'cyan')}:{colored(port, 'yellow')} using {colored(protocol.upper(), 'green')} with a timeout of {colored(timeout, 'magenta')} seconds...")

    while True:
        if protocol == "tcp":
            success, result = tcp_ping(host, port, timeout)
        else:  # udp
            success, result = udp_ping(host, port, timeout)

        if success:
            print(colored(f"Success! Response time: {result:.2f} ms", "green"))
        else:
            print(colored(f"Skid is offline: {host} ({result})", "red"))

        time.sleep(interval)

if __name__ == "__main__":
    main()
