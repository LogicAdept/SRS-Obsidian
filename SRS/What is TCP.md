<!--
reps: 0
priority: 0
-->
#Networking/TCP #SRS
# What is TCP

> [!abstract] Short answer
> TCP (Transmission Control Protocol, currently RFC 9293) is a connection-oriented transport protocol that turns IP's unreliable packet delivery into a reliable, ordered, duplex byte stream between two sockets — using sequence numbers, acknowledgments, retransmission, flow control (receive window) and congestion control. It is the transport under HTTP/1.1, HTTP/2, SSH, SMTP and most request/response traffic.

## The mechanisms, in order of importance

1. **Connection.** A TCP connection is identified by the 4-tuple (src IP, src port, dst IP, dst port) and starts with the three-way handshake ([[What is the TCP three-way handshake]]); state lives only in the endpoints.
2. **Byte stream + sequence numbers.** Every byte is numbered; the receiver reorders arrivals and discards duplicates — the app sees one clean stream, message boundaries erased.
3. **Acknowledgments and retransmission.** Cumulative ACKs confirm the next expected byte; missing ACK ranges trigger fast retransmit (after 3 duplicate ACKs) or the RTO timer. Lost ACKs are absorbed because ACKs are cumulative.
4. **Flow control.** The receiver advertises a window; the sender may not exceed it — a slow consumer throttles the sender instead of dropping.
5. **Congestion control.** The sender maintains cwnd: slow start at the beginning, AIMD afterwards — this protects the *network*, not the receiver.
6. **Checksum, MSS, options.** Corruption detection; MSS (~1460 on Ethernet), window scaling and SACK negotiated at handshake.

```d2
direction: down
app: "Application writes bytes" { width: 260; height: 70; style.fill: "#e8f5e9" }
seg: "TCP: split into segments\nseq numbers, checksum" { width: 300; height: 80; style.fill: "#fff3e0" }
ip: "IP forwards best-effort\n(drops, reorders happen)" { width: 300; height: 80; style.fill: "#e3f2fd" }
rcv: "Receiver TCP:\nreorder, dedup, ACK, deliver in order" { width: 340; height: 90; style.fill: "#fff3e0" }
app2: "Application reads the same byte stream" { width: 320; height: 70; style.fill: "#e8f5e9" }
app -> seg -> ip -> rcv -> app2
```

**Fig. 1.** TCP's contract: the stream that enters the sender is the stream the receiver reads, regardless of what IP does in between.

> [!warning] TCP's reliability is not a delivery guarantee
> A connection can be reset mid-transfer (RST), a peer can die (kept alive only by timeouts/keepalives), and "ACKed" data can be lost if the machine crashes before the app processes it — application-level confirmation is a separate contract. Also TCP adds head-of-line blocking: one lost segment stalls delivery of everything after it, which is exactly what QUIC's per-stream independence was designed to fix ([[What is HTTP 3 and why does it use QUIC]]).

Where TCP fits in the suite: [[What is the TCP IP protocol suite]]; the comparison: [[What is the difference between TCP and UDP]]; the mechanics: [[How does TCP flow control work]] and [[How does TCP congestion control work]].

> [!tip] Interview answer
> TCP is a connection-oriented, reliable byte-stream transport over IP: sequence numbers give ordering and dedup, cumulative ACKs with fast retransmit and RTO give recovery, the receive window gives flow control, cwnd with slow start and AIMD gives congestion control. All state is in the endpoints — the network stays best-effort. Costs I name: connection setup latency and head-of-line blocking, which QUIC attacks.
