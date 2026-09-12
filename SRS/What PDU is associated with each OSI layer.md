<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What PDU is associated with each OSI layer

> [!abstract] Short answer
> A PDU (protocol data unit) is the unit a layer exchanges: bits at Physical, frames at Data Link, packets at Network, segments (TCP) or datagrams (UDP) at Transport, and generic data/messages at Session, Presentation and Application. The classic mnemonic: "Some People Fear Birthdays" (Segment, Packet, Frame, Bit) for layers 4 → 1.

## The map

| OSI layer | PDU | Example |
|---|---|---|
| 7 Application | data / message | an HTTP request |
| 6 Presentation | data | encoded/encrypted payload |
| 5 Session | data | session checkpoint |
| 4 Transport | segment (TCP) / datagram (UDP) | TCP segment with ports and seq numbers |
| 3 Network | packet | IP packet with source/destination IP |
| 2 Data Link | frame | Ethernet frame with MAC header and FCS trailer |
| 1 Physical | bit / symbol | voltage or light pulses |

```d2
direction: down
seg: "TCP segment\n(header: ports, seq, ack)" { width: 300; height: 80; style.fill: "#fff3e0" }
pkt: "IP packet\n(header: src/dst IP, TTL)" { width: 300; height: 80; style.fill: "#fff3e0" }
frm: "Ethernet frame\n(header: src/dst MAC | trailer: FCS)" { width: 340; height: 90; style.fill: "#e3f2fd" }
bits: "bits on the wire" { width: 300; height: 60; style.fill: "#e3f2fd" }
seg -> pkt: "encapsulated as payload"
pkt -> frm: "encapsulated as payload"
frm -> bits: "serialized"
```

**Fig. 1.** Encapsulation for one hop: segment → packet → frame → bits; the receiver unwraps in the reverse order.

## Why the vocabulary matters

The PDU name tells you *where a device is allowed to read*: a switch forwards frames by reading the layer-2 header only; a router forwards packets by reading the layer-3 header (it rewrites the frame for the next hop, so MAC addresses change per hop while IP addresses stay end-to-end — except NAT, which rewrites them on purpose). Wireshark uses the same vocabulary in its dissection tree, so this is also how practitioners actually speak.

> [!warning] PDU names are per-protocol, not magical
> "Segment" is TCP; UDP's PDU is the datagram. "Packet" is IP; some books say "datagram" for IP too (RFC 791's own term) — both are accepted, but mixing them up ("UDP frame") signals memorization without understanding. Also, a single TCP segment may span several frames after fragmentation, or a frame may carry several small segments after aggregation, so the nesting is not always 1:1.

Applications: [[What is a frame at the Data Link layer]], [[What is a packet at the Network layer]], [[What is a segment at the Transport layer]] go one layer deeper each; [[How does encapsulation work in the OSI model]] shows how they nest.

> [!tip] Interview answer
> PDUs map top-down as data, then segment or datagram at transport, packet at network, frame at data link, bits at physical. I add the two facts that show understanding: MAC addresses change hop by hop while IP addresses stay end-to-end, and the names come from the concrete protocol — TCP gives segments, UDP datagrams.
