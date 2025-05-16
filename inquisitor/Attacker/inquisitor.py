# attacker.py
import re
from scapy.all import *
import argparse
import ipaddress

def parse_args():
    parser = argparse.ArgumentParser(description="Inquisitor : MiddleMan attack tool")
    parser.add_argument("IP_src", type=str, help="Source IPv4 address")
    parser.add_argument("IP_dst", type=str, help="Destination IPv4 address")
    parser.add_argument("MAC_src", type=str, help="Source MAC address")
    parser.add_argument("MAC_dst", type=str, help="Destination MAC address")

    args = parser.parse_args()

    if not (check_ip(args.IP_src) and ipaddress.ip_address(args.IP_src).version == 4):
        parser.error("IP-src must be a valid IPv4 address.")
    if not (check_ip(args.IP_dst) and ipaddress.ip_address(args.IP_dst).version == 4):
        parser.error("IP-dst must be a valid IPv4 address.")

    def is_valid_mac(mac):
        return re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac) is not None

    if not is_valid_mac(args.MAC_src):
        parser.error("MAC-src must be a valid MAC address.")
    if not is_valid_mac(args.MAC_dst):
        parser.error("MAC-dst must be a valid MAC address.")
    return parser.parse_args()


def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def main():
    args = parse_args()

    print("[*] Starting Inquisitor...". args.IP_src,
          args.IP_dst, args.MAC_src, args.MAC_dst)


if __name__ == "__main__":
    main()
