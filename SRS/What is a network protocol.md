<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is a network protocol

> [!abstract] Short answer
> A network protocol is an agreed set of message formats and rules that two or more machines follow to exchange data: what a message looks like (syntax), what each field means and which side may send when (semantics), and how errors and timing are handled. Protocols are layered — each layer serves the one above it, which is why IP, TCP and HTTP can evolve independently.

## What a protocol actually fixes

Taking TCP as the canonical example (RFC 9293), a protocol specification defines:

1. **Packet/unit format** — fixed and variable parts: TCP header fields (source/destination port, sequence and acknowledgment numbers, flags SYN/ACK/FIN/RST, window, checksum).
2. **State machine** — legal transitions: LISTEN → SYN-RECEIVED → ESTABLISHED → FIN-WAIT/CLOSE, and what resets it.
3. **Procedures** — how to establish and close, how to retransmit, how to acknowledge, how to size the flow-control window.
4. **Encoding rules** — network byte order (big-endian), fixed 16/32-bit field widths, checksum algorithms.

```d2
direction: right
http: "HTTP\nrequest/response semantics" { width: 250; height: 80; style.fill: "#e8f5e9" }
tcp: "TCP\nreliable byte stream, ports" { width: 250; height: 80; style.fill: "#fff3e0" }
ip: "IP\naddressing and routing" { width: 220; height: 80; style.fill: "#e3f2fd" }
link: "Ethernet / Wi-Fi\nframes on a link" { width: 250; height: 80; style.fill: "#f3e5f5" }
http -> tcp: "segment payload"
tcp -> ip: "datagram payload"
ip -> link: "frame payload"
```

**Fig. 1.** Encapsulation chain: each layer treats the layer above as opaque payload and adds its own header, so protocols compose without knowing each other's internals.

## Families you should be able to name

- **Link/local:** Ethernet (frames, MAC addresses), ARP (IP → MAC resolution).
- **Network:** IPv4/IPv6, ICMP (control and diagnostics), routing protocols.
- **Transport:** TCP (ordered, reliable, connection-oriented), UDP (datagrams), QUIC (runs over UDP, provides streams and TLS 1.3 in one).
- **Application/service:** HTTP/1.1·2·3, TLS, DNS (name resolution), DHCP (host configuration), FTP, SMTP, WebSocket (upgrade over HTTP).

> [!warning] "Protocol" is not the program
> The protocol is the contract — the bytes and rules. Programs implement it, and implementations differ: two HTTP servers can both be RFC-compliant yet behave differently on malformed input. An interview answer that says "HTTP is when the browser sends a request" confuses the contract with one of its implementations.

Protocols are published as open specifications — RFCs for the Internet suite, ITU-T/ISO texts for OSI — so independent implementations can interoperate. See [[What is TCP]], [[What is UDP]], [[What is HTTP]], and [[What is DNS and how does DNS resolution work]] for concrete examples at each layer.

> [!tip] Interview answer
> A network protocol is the agreed format and behavior for machine-to-machine communication: message syntax, field semantics, state machine, error handling. I usually structure the answer by layers — Ethernet/ARP at the link layer, IP and ICMP at the network layer, TCP/UDP/QUIC at transport, HTTP/DNS/DHCP at application — and stress that each layer encapsulates the previous one and can be swapped independently.
