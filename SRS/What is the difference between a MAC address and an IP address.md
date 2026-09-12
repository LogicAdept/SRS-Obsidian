<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is the difference between a MAC address and an IP address

> [!abstract] Short answer
> A MAC address is the hardware identity of a network interface, burned in by the vendor and valid only on the local link — it answers "which NIC on this segment". An IP address is a logical, routable identity assigned by configuration or DHCP — it answers "which host in the internetwork" and persists end to end while MACs are rewritten on every hop.

## Side by side

| | MAC | IP |
|---|---|---|
| Scope | one link / broadcast domain | end-to-end across networks |
| Format | 48 bits, hex pairs (9c:b6:d0:11:22:33); EUI-64 for IPv6 derivation | IPv4: 32 bits dotted (10.0.0.5); IPv6: 128 bits (RFC 8200) |
| Assigned by | manufacturer (OUI prefix) / software override | DHCP, manual, SLAAC |
| Who uses it | switches, NICs, ARP/NDP | routers, the whole Internet |
| Changes when | hardware replaced (or spoofed) | network/moved/renewed |
| Lives at | Data Link (L2) frame header | Network (L3) packet header |

```d2
direction: right
h1: "Host A\nIP 10.0.0.5\nMAC 9c:b6:..:11" { width: 230; height: 100; style.fill: "#e3f2fd" }
r: "Router hop\nstrips frame, new MACs\nIPs unchanged" { width: 250; height: 100; style.fill: "#fff3e0" }
h2: "Server\nIP 93.184.x.x (end-to-end)\nMAC only local" { width: 260; height: 100; style.fill: "#e8f5e9" }
h1 -> r -> h2
```

**Fig. 1.** Along the path, IP addresses survive every hop; MAC addresses exist per link and die at each router.

## Why two address families exist

The separation buys independence: the network layer can route over *any* link technology (Ethernet, Wi-Fi, PPP) because it addresses hosts logically, while each link keeps its own efficient hardware addressing. ARP (IPv4) and NDP (IPv6) are the translators between the two worlds ([[What is ARP and how does it work]]). Practical consequences: DHCP leases are anchored by MACs, switch port-security filters by MACs, and NAT relies on the IP/port layer ([[What is NAT and how does it work]]), while private ranges ([[What is the difference between private and public IP addresses]]) make the logical layer re-usable per site.

> [!warning] "MAC never changes" and "IP identifies the machine" — both false
> MACs are trivially overridable per-OS (and randomized by modern phones per-network for privacy); IPs do not identify machines — one NIC can hold several IPs, and NAT shares one public IP among dozens of hosts. Also, a MAC address gives you no geo/locality information; the IP prefix hierarchy is what routing actually uses. Saying "the packet carries the destination MAC of the final server" is the flagrant version of the confusion — the frame carries the *next hop's* MAC only ([[What is a frame at the Data Link layer]]).

Companions: [[What is a packet at the Network layer]], [[What is the difference between private and public IP addresses]], and the layer vocabulary in [[What PDU is associated with each OSI layer]].

> [!tip] Interview answer
> MAC: 48-bit hardware identity of an interface, meaningful on one link only, used by switches and rewritten at every hop. IP: logical routable identity (32-bit IPv4, 128-bit IPv6), assigned by DHCP or manually, stable end to end. The one-sentence summary: MAC answers "which NIC on this segment", IP answers "which host in the world", and ARP/NDP translate between them.
