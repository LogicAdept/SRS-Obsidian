<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# How does encapsulation work in the OSI model

> [!abstract] Short answer
> Encapsulation is the downward walk of data through the sending stack: every layer takes what the layer above produced and wraps it with its own header (and, at Data Link, a trailer), turning messages into segments, segments into packets, packets into frames, and frames into bits. Each added header is meaningful only to the peer layer on the receiving side, which removes it in the same order.

## The downward steps

1. **Application (7)–Presentation (6)–Session (5):** the program produces data; encodings/encryption and dialog bookkeeping apply (on TCP/IP stacks these duties sit inside the app and TLS).
2. **Transport (4):** the data is cut into TCP segments (ports, sequence numbers) or UDP datagrams (ports only).
3. **Network (3):** each segment becomes the payload of an IP packet (source/destination IP, TTL, protocol number).
4. **Data Link (2):** the packet becomes the payload of a frame for *this* link (MAC addresses, EtherType, FCS trailer).
5. **Physical (1):** the frame's bits are encoded into signals on the medium.

```d2
direction: down
app: "Data" { width: 160; height: 60; style.fill: "#e8f5e9" }
t: "[TCP header | data]\nsegment" { width: 260; height: 70; style.fill: "#fff3e0" }
n: "[IP header | segment]\npacket" { width: 280; height: 70; style.fill: "#e3f2fd" }
d: "[Eth header | packet | FCS]\nframe" { width: 320; height: 70; style.fill: "#f3e5f5" }
b: "10110100...\nbits on the wire" { width: 220; height: 60; style.fill: "#ffebee" }
app -> t -> n -> d -> b
```

**Fig. 1.** Nesting on the sender: each arrow adds exactly one layer's header; the receiver peels them in reverse (see [[How does de-encapsulation work in the OSI model]]).

## The facts interviews probe

- **Peer logic:** a header added at layer N is *read and consumed* by layer N on the receiving peer — a switch reads the MAC header, a router reads the IP header, the TCP stack reads the TCP header. Nobody else does.
- **Per-hop lifetime:** the frame and its MACs die at every hop; the packet survives end to end; the segment survives host to host.
- **MTU interactions:** a segment too big for the link's MTU forces fragmentation (IPv4) or an ICMP "packet too big" + path MTU discovery (IPv6).
- **Terminology anchors:** segment/datagram (L4), packet (L3), frame (L2), bits (L1) — [[What PDU is associated with each OSI layer]].

> [!warning] Encapsulation adds overhead per layer — that is not decoration
> Every header costs bytes: Ethernet 14 (+4 VLAN) + IPv4 20 (IPv6 40) + TCP 20 → an MSS of 1460 on classic 1500-byte Ethernet. Saying "the OSI model adds headers" is wrong in another direction — the *protocols* add headers; OSI is just the model describing who owns them.

Cross-checks: [[What is a segment at the Transport layer]], [[What is a packet at the Network layer]], [[What is a frame at the Data Link layer]] for each wrapping step, and [[What is the purpose of each OSI layer]] for why each layer exists.

> [!tip] Interview answer
> Encapsulation is the sender's walk down the stack: data → TCP/UDP header (segment) → IP header (packet) → Ethernet header and FCS (frame) → bits. Each header is addressed to the peer layer at the other end, so the receiver de-encapsulates in reverse order; frames are rebuilt on every hop while the packet survives end to end. I close with the overhead math: 14 + 20 + 20 bytes of headers per 1460-byte segment on classic Ethernet.
