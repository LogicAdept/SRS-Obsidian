<!--
reps: 0
priority: 0
-->
#Networking/UDP #SRS
# What is UDP

> [!abstract] Short answer
> UDP (User Datagram Protocol, RFC 768) is a connectionless transport protocol: it adds only ports and an optional checksum on top of IP, delivering independent datagrams with no handshake, no ordering, no retransmission and no flow control. What you lose in guarantees you gain in latency, simplicity and control — which is why DNS, DHCP, QUIC, VoIP and games are built on it.

## The entire protocol

The UDP header is 8 bytes: source port, destination port, length, checksum. That is the whole spec. A datagram is one IP datagram's worth of data: no fragmentation of application messages, no stream — each `send()` is one unit, delivered (maybe) once, in whatever order the network delivers.

- **Connectionless:** no SYN/ACK dance — a UDP "session" is just both sides agreeing on ports; state lives in the application.
- **Unreliable:** dropped datagrams are gone; the sender is not told.
- **Unordered and unregulated:** datagrams can arrive out of order or duplicated; there is no window, so a fast sender can overflow a slow receiver (the app must pace itself or handle loss).
- **Checksum:** IPv4 allows zero (unused); IPv6 requires it — it is the only protection against corruption and misdelivery.

```d2
direction: down
app: "App sends datagrams 1, 2, 3" { width: 280; height: 70; style.fill: "#e8f5e9" }
net: "IP best-effort\ndrops, reorders, duplicates possible" { width: 300; height: 90; style.fill: "#e3f2fd" }
rcv: "Receiver gets 1, 3, 2(dupe?)\napp decides what to do" { width: 300; height: 90; style.fill: "#fff3e0" }
app -> net -> rcv
```

**Fig. 1.** UDP passes the network's chaos straight to the application — every guarantee beyond ports and checksums is DIY.

## Who uses it and why

- **DNS** — one small query, one small answer; a TCP handshake would triple the latency of a lookup (retry logic is built into resolvers).
- **DHCP** — the client has no address yet, so a connection cannot even exist.
- **QUIC / HTTP 3** — rebuilds reliability, ordering and TLS inside userspace over UDP, gaining streams without head-of-line blocking and connection migration ([[What is HTTP 3 and why does it use QUIC]]).
- **Real-time media and games** — a late retransmitted frame is worthless; better to drop forward.

> [!warning] "UDP is faster because it does less" is only half true
> UDP skips handshake and retransmission overhead, yes — but it also inherits IP's problems without relief: no congestion control means an app can congest-kill a network (that is why QUIC implements congestion control in userspace), and large datagrams risk IP fragmentation, which retransmits badly. "Always use UDP for speed" is the wrong takeaway; the right one is: use UDP when losing data is acceptable or when you implement exactly the reliability you need ([[What is the difference between TCP and UDP]]).

Suite context: [[What is the TCP IP protocol suite]]; handshake contrast: [[What is the TCP three-way handshake]]; the PDU name at this layer: [[What is a segment at the Transport layer]] (and why datagram ≠ segment).

> [!tip] Interview answer
> UDP is RFC 768 minimalism: ports, length, checksum — no connection, ordering, retransmission or flow control. I use it when one message is the unit (DNS, DHCP), when timeliness beats completeness (voice, games), or when I want to build custom reliability — QUIC is the flagship example. The honest caveat: "faster" holds only if the app handles loss, ordering and congestion itself.
