<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is a packet at the Network layer

> [!abstract] Short answer
> A packet is the Network layer (Layer 3) PDU: the segment (or datagram) from transport wrapped with an IP header that names source and destination IP addresses, identifies the payload protocol, limits lifetime with TTL/Hop Limit, and lets routers forward it hop by hop across many links. IP packets are best-effort — delivery, order and duplication-freedom are not guaranteed.

## IPv4 header fields worth naming

- **Version / IHL / Total Length** — layout and size of the whole datagram.
- **Identification, Flags, Fragment Offset** — IPv4 fragmentation machinery (assembled at the final receiver; DF flag enables path MTU discovery).
- **TTL** — decremented by every router; at 0 the packet is dropped and ICMP Time Exceeded is sent (this is how traceroute works).
- **Protocol** — payload type: 6 = TCP, 17 = UDP.
- **Header checksum** — covers the header only (recomputed per hop since TTL changes); removed entirely in IPv6.
- **Source/destination addresses** — 32 bits each in IPv4, 128 bits in IPv6 (RFC 8200, whose fixed header drops fragmentation and checksum fields in favor of extension headers).

```d2
direction: down
seg: "TCP segment or UDP datagram\n(layer 4 PDU)" { width: 300; height: 80; style.fill: "#fff3e0" }
ip: "IP header\nsrc IP | dst IP | TTL | protocol" { width: 320; height: 90; style.fill: "#e3f2fd" }
hop: "Router: read dst IP ->
longest-prefix match -> TTL-1" { width: 340; height: 100; style.fill: "#e8f5e9" }
frm: "Ethernet frame for the next hop\n(new MACs around the same packet)" { width: 360; height: 90; style.fill: "#f3e5f5" }
seg -> ip
ip -> hop
hop -> frm
```

**Fig. 1.** The packet is the stable unit across the path; only its frame shell changes per hop.

## What "best effort" means in practice

The network layer promises nothing about arrival. Duplicates appear (a router retransmits internally, or paths converge), order inverts (equal-cost paths), and packets die silently (TTL, queue overflow). Everything an application depends on — ordering, reliability, duplicate suppression — is built at layer 4 (TCP) or by the application over UDP; [[How do you prevent duplicate message or packet delivery]] shows the dedup mechanisms.

> [!warning] Packet vs segment vs frame — the interview's favorite mix-up
> "The router reads segments" is wrong: it reads the IP header (packet) and never opens the transport payload. "The frame travels end to end" is wrong: it is rebuilt per hop. [[What is a segment at the Transport layer]] and [[What is a frame at the Data Link layer]] complete the trio; the mapping table is in [[What PDU is associated with each OSI layer]].

> [!tip] Interview answer
> A packet is the layer-3 PDU: an IP header around a transport payload. I name the fields that carry the semantics — source/destination IP for addressing, TTL for hop limiting, Protocol for TCP vs UDP — and stress best-effort behavior: no delivery or ordering guarantees, fragmentation possible in IPv4 but moved to senders in IPv6, and per-hop re-encapsulation into fresh frames.
