<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is a segment at the Transport layer

> [!abstract] Short answer
> A segment is the TCP PDU at the Transport layer (Layer 4): a chunk of the application byte stream prefixed with a TCP header — source/destination ports, sequence and acknowledgment numbers, flags (SYN, ACK, FIN, RST, PSH, URG), window size and checksum. UDP's unit at the same layer is a datagram, not a segment. Segments travel inside IP packets and are what make end-to-end delivery to *processes* possible.

## Header fields and what they buy

| Field | Purpose |
|---|---|
| Source/destination port | deliver to the right process (with IP = the socket pair) |
| Sequence number | byte offset in the stream — enables ordering and duplicate filtering |
| Acknowledgment number | next byte expected — the ACK engine |
| Flags | SYN/ACK/FIN/RST manage the connection; PSH/URG are legacy hints |
| Window | receiver's advertised free buffer — flow control |
| Checksum | corruption detection over header+data |

```d2
direction: down
data: "Application byte stream\n(MSS-sized chunks)" { width: 320; height: 80; style.fill: "#e8f5e9" }
segs: "TCP segments\neach with seq number" { width: 320; height: 80; style.fill: "#fff3e0" }
pkts: "IP packets\n(host addressing)" { width: 300; height: 80; style.fill: "#e3f2fd" }
rec: "Receiver: reorder by seq,\ndrop duplicates, ACK" { width: 340; height: 100; style.fill: "#f3e5f5" }
data -> segs -> pkts -> rec
```

**Fig. 1.** Segmentation on send, reassembly on receive; sequence numbers are the bookkeeping that makes TCP a stream rather than a bag of packets.

## Why the transport layer exists

IP delivers to a host; ports deliver to a process — the 4-tuple (src IP, src port, dst IP, dst port) identifies the connection, and a server multiplexes thousands of clients on one port. Beyond multiplexing, TCP adds reliability (retransmission on missing ACKs), in-order delivery, flow control (the window) and congestion control. All of that is negotiated and tracked per connection, which is why the segment — not the raw byte stream — is the operational unit; the connection itself starts with the exchange in [[What is the TCP three-way handshake]].

> [!warning] "Segment" is TCP-only, and a segment is not a "message"
> Calling a UDP unit a segment is wrong — UDP is message-oriented datagrams with no stream, no ordering. And a segment is not what the application sent: one `send()` may be split into many segments (MSS, typically 1460 bytes on Ethernet), and many small sends may be coalesced into one (Nagle). The byte-stream abstraction deliberately erases message boundaries — see [[What is the difference between TCP and UDP]].

PDU neighbors: [[What is a packet at the Network layer]] and [[What is a frame at the Data Link layer]]; the full mapping lives in [[What PDU is associated with each OSI layer]].

> [!tip] Interview answer
> A segment is TCP's layer-4 PDU: ports plus sequence/acknowledgment numbers, flags, window and checksum around a stream chunk. Sequence numbers give ordering and duplicate filtering; the window gives flow control; retransmission gives reliability. I keep the vocabulary straight: segment (TCP), datagram (UDP), packet (IP), frame (Ethernet) — and note that TCP erases message boundaries by design.
