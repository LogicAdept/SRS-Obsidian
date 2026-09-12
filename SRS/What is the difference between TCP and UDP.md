<!--
reps: 0
priority: 0
-->
#Networking/TCP #Networking/UDP #SRS
# What is the difference between TCP and UDP

> [!abstract] Short answer
> TCP is a connection-oriented, reliable, ordered byte stream with flow and congestion control; UDP is a connectionless, best-effort datagram service with only ports and a checksum. TCP costs a handshake, per-connection state and head-of-line blocking; UDP costs nothing and guarantees nothing. Choose TCP when every byte must arrive (web, APIs, file transfer) and UDP when loss is acceptable or when you build your own reliability (DNS, media, QUIC).

## The comparison table

| Aspect | TCP (RFC 9293) | UDP (RFC 768) |
|---|---|---|
| Connection | yes — 3-way handshake, FIN/RST teardown | none — fire and forget |
| Delivery | reliable: ACKs, retransmission | best-effort: silent loss |
| Ordering | strict byte-stream order | none |
| Duplicates | filtered by sequence numbers | possible, app must dedup |
| Flow control | receive window | none |
| Congestion control | required (slow start, AIMD) | none (app's job — see QUIC) |
| Data unit | segment, stream (no message borders) | datagram (message = unit) |
| Header | 20+ bytes with options | 8 bytes |
| Typical users | HTTP/1.1·2, SSH, SMTP, DB drivers | DNS, DHCP, QUIC/HTTP-3, VoIP, games |

```d2
direction: right
tcp: "TCP\nconnect -> stream -> ACK/retransmit\n-> close" { width: 320; height: 100; style.fill: "#e3f2fd" }
udp: "UDP\nsend datagram(s). done." { width: 260; height: 100; style.fill: "#fff3e0" }
q: "Does every byte matter?\nyes -> TCP | own-reliability or loss-OK -> UDP" { width: 380; height: 100; style.fill: "#e8f5e9" }
q -> tcp
q -> udp
```

**Fig. 1.** The decision hinge: guarantees are bought with state, latency and head-of-line blocking.

## How the tradeoff plays out

- **Web/API:** TCP (HTTP/1.1, HTTP/2) — correctness first; browsers tolerate latency better than corruption. With HTTP/3 the browser world shifted to QUIC over UDP to remove TCP head-of-line blocking and make TLS 1.3 part of the handshake ([[What is HTTP 3 and why does it use QUIC]]).
- **DNS:** UDP by default — one round trip; resolvers fall back to TCP for large answers (DNSSEC, zone transfers).
- **Streaming/voice:** UDP — a retransmitted video frame arrives too late to be shown; skip and encode the next one.
- **Dedup asymmetry:** TCP filters duplicates inside a connection; UDP leaves dedup to the app ([[How do you prevent duplicate message or packet delivery]]).

> [!warning] Three lies interviews tell about this pair
> (1) "UDP has no checksum" — it has one, mandatory in IPv6, optional (zero) in IPv4. (2) "UDP is always faster" — for bulk reliable transfer, TCP's congestion control beats a naive UDP sender that floods and loses. (3) "TCP guarantees the app processed the data" — it guarantees delivery to the receive buffer only; a crashed receiver loses ACKed-but-unprocessed bytes. [[What is TCP]] and [[What is UDP]] expand each side.

Transport-layer context: [[Which OSI layer provides end-to-end delivery flow control and error recovery]], [[What is a segment at the Transport layer]], [[What is the TCP IP protocol suite]].

> [!tip] Interview answer
> TCP: connection, ordered reliable stream, flow and congestion control — 20+ byte header, costs a handshake and head-of-line blocking. UDP: connectionless 8-byte-header datagrams, best-effort only. My selection rule: correctness-critical request/response goes TCP; one-shot queries, real-time media, or custom-built reliability go UDP — QUIC being the proof that "custom reliability over UDP" is now a mainstream choice.
