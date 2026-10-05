# ⚡ DNS Spoofing — Security Lab Demonstration

[![GitHub](https://img.shields.io/badge/github-repo-3776AB?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scapy](https://img.shields.io/badge/Scapy-Network%20Packets-red?style=for-the-badge)](https://scapy.net/)
[![LAB](https://img.shields.io/badge/Security-Lab-8A2BE2?style=for-the-badge)]("https://github.com/3078756D627261/DNSpoofing/")

## ⚠️ Disclaimer

> [!WARNING]
> For authorized use only. This project demonstrates DNS packet manipulation and can alter how DNS queries are resolved. Use it only on systems, networks, and environments where you have explicit authorization. The recommended environment is an isolated virtual lab or dedicated test network.

---

## ✨ Overview

DNSpoofer is a small Python tool that uses [Scapy](https://scapy.net) to `monitor DNS queries` and `generate custom DNS responses` for domains defined by the user. The project is intentionally simple and focuses on demonstrating fundamental concepts such as:

- 📡 Packet sniffing
- 🌐 DNS query inspection
- 🧩 Packet construction
- 🔄 DNS response manipulation
- 🐍 Scapy-based network programming
- 🖥️ Command-line configuration

> [!NOTE]
> It is primarily intended as a learning and security-research project rather than a production DNS server.

---

## 💭 DNS Spoofing

DNS spoofing, also known as `DNS cache poisoning`, is a network attack in which an attacker provides or causes a `forged DNS response` so that a domain name resolves to an unintended IP address.

Normally:
```text
example.com → Legitimate IP address
```

During a DNS spoofing attack:
```text
example.com → Attacker-controlled or incorrect IP address
```
As a result, a victim may be redirected to a fraudulent website, malicious service, or another unintended destination without realizing that the DNS resolution has been manipulated.

---

### 🚀 Features

| Feature |	Description |
|---|---|
📡 Packet Sniffing |	Monitors DNS traffic on a selected interface |
🔎 DNS Inspection |	Extracts requested domain names from DNS queries |
🎯 Domain Matching |	Checks queries against a configurable domain list |
🧩 Custom Responses |	Builds DNS responses containing configured addresses |
⚡ Scapy Powered |	Uses Scapy for packet parsing and construction |
📁 File Configuration |	Domains and addresses are loaded from text files |
🎨 Colored CLI| 	Provides readable terminal output |
🛠️ CLI Arguments| 	Interface and configuration files are configurable |

---

## 🧠 How It Works

At a high level, the application follows this workflow:

                    ┌─────────────────────┐
                    │   Configuration     │
                    │   domain_list.txt   │
                    │ ipaddress_list.txt  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Validate Files    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Domain → IP Mapping │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Capture DNS     │
                    │       Queries       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Extract Domain Name │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Domain in Mapping?  │
                    └───────┬───────┬─────┘
                            │       │
                            NO     YES
                            │       │
                            ▼       ▼
                         Ignore   Build
                                  Response
                                    │
                                    ▼
                               Send packet

---

## 📦 Requirements

Before running the project, make sure you have:

- Python 3
- Scapy
- Linux or another OS capable of raw packet capture/transmission
- Appropriate privileges for packet operations
- An interface carrying the test DNS traffic

Install Scapy

```text
python3 -m pip install scapy
sudo apt-get install python3-scapy
```

Depending on your operating system, packet capture and raw packet transmission `may require elevated privileges`.

---

## 📂 Project Structure

```text
DNSpoofer/
│
├── 📄 DNSpoofer.py
├── 📄 domain_list.txt
└── 📄 ipaddress_list.txt
```

---

## ⚙️ Configuration

The tool uses two simple text files:

### 🌐 Domain List

`domain_list.txt` contains one domain per line:

```text
example.test
lab.test
internal.test
```

### 📍 IP Address List

`ipaddress_list.txt` contains one address per line:

```text
192.168.2.10
192.168.2.20
192.168.2.30
```

The entries are paired according to their position:

```text
example.test      → 192.168.2.10
lab.test          → 192.168.2.20
internal.test     → 192.168.2.30
```

> [!IMPORTANT]
> Keep the files synchronized. The first domain corresponds to the first IP address, the second domain to the second IP address, and so on.

---

## ▶️ Usage

Clone the repository and enter the project directory:

```text
git clone https://github.com/3078756D627261/DNSpoofer.git
cd DNSpoofer
```

Run the tool using its default configuration:

```
sudo python3 DNSpoofer.py
```

or custom configuration:

```text
sudo python3 DNSpoofer.py --iface eth0 --ipaddr ips.txt --domain dns.txt
```

Default values:

```text
Interface    : eth0
IP list      : ipaddress_list.txt
Domain list  : domain_list.txt
```

Command-Line Options:

| Option | Long Option | Description | Default| 
|---|---|---|---|
| -i |	--iface |	Network interface |	eth0 |
| -a |	--ipaddr |	IP address list |	ipaddress_list.txt |
| -d |	--domain |	Domain list |	domain_list.txt |

For help:

```text
python3 DNSpoofer.py --help
```

---

## 🖥️ Example

When a configured domain is observed, the program displays information similar to:

```text
╭──────────────────────────────────────────╮
│             DNS Spoofer v1.0             │
╰──────────────────────────────────────────╯

[•] Sniffing DNS packets...

Requested domain: example.test from 192.168.2.50 → Resolved to 192.168.2.10
```

---

## 🔬 Code Architecture

The project is divided into a few focused functions.

`banner()`

Displays the application banner.

`file_validation()`

Checks whether the configuration files:

- Exist
- Are not empty

`merge_files_to_dict()`

Reads the two configuration files and creates a domain-to-address mapping.

Conceptually:

```text
{
    "example.test": "192.168.2.10",
    "lab.test": "192.168.2.20"
}
```

`packet_sniffer()`

Starts Scapy's packet capture mechanism and forwards captured packets to the packet handler.

`packet_handler()`

Responsible for:

1. Detecting DNS queries
2. Extracting the requested domain
3. Looking up the domain
4. Creating a response when a match is found

`build_dns_response_packet()`

Constructs the Ethernet/IP/UDP/DNS response packet based on the captured query.

---

## 🧪 Recommended Lab Setup

For safe experimentation, use an isolated environment.

A simple virtual lab might look like:

```text
┌──────────────────┐
│   Test Client    │
│                  │
│    DNS Query     │
└────────┬─────────┘
         │
         │ Isolated Test Network
         │ 
         │
┌────────▼─────────┐
│   Security Lab   │
│                  │
│   DNS Spoofer    │
└──────────────────┘
```

Virtual machines, host-only networks, or dedicated test networks are recommended.

Using reserved documentation addresses such as `192.168.2.0/24` can also make examples clearer and safer.

---

## ⚠️ Limitations

This project is intentionally minimal and should not be considered a production DNS implementation.

Current limitations include:

- Only configured domains are handled.
- Configuration relies on matching lines between two files.
- DNS queries are filtered for UDP traffic destined for port 53.
- It does not implement recursive DNS resolution.
- It does not provide DNSSEC validation.
- It does not handle encrypted DNS such as DoH or DoT.
- DNS response construction is intentionally basic.
- Network behavior depends on the network topology and DNS resolver.
- Multiple DNS responses can lead to unpredictable resolver behavior.

---

## 🛠️ Troubleshooting

`Permission denied`

Raw packet operations often require elevated privileges.
Make sure your test environment grants the program the required packet-capture and transmission permissions.

`Wrong interface`

List available interfaces:

```text
ip link
```

Then specify the desired interface:

```text
sudo python3 DNSpoofer.py --iface <interface>
```

`Configuration file not found`

Verify the files exist:

```text
ls -la
```

You can also specify custom paths:

```text
sudo python3 DNSpoofer.py --ipaddr path/to/ipaddress_list.txt --domain path/to/domain_list.txt
```

`No DNS queries detected`

Check that:

- The selected interface carries the test traffic.
- The test client is generating DNS queries.
- The traffic uses UDP DNS.
- The requested domain exists in the configured domain list.
- The application has sufficient packet-capture permissions.

---

## 🔐 Security Considerations

DNS manipulation can affect where network applications connect and can potentially redirect users to unintended destinations.

Therefore:

- 🛑 Do not use this against networks you do not own.
- 🛑 Do not deploy it against unsuspecting users.
- 🛑 Do not use it to bypass security controls.
- ✅ Use isolated environments for testing.
- ✅ Use domains specifically created for your lab.
- ✅ Obtain authorization before performing network-security testing.

---

## 🎓 Educational Topics

This project can be useful for learning about:

```text
Networking
   │
   ├── Ethernet
   ├── IP
   ├── UDP
   └── DNS
        │
        ├── DNS Queries
        ├── DNS Responses
        └── Resource Records
   │
   └── Packet Manipulation
          │
          └── Scapy
```
It provides a practical introduction to how individual network layers can be inspected and constructed programmatically.
