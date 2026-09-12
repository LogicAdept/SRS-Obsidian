<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# Which OSI layer provides end-to-end delivery flow control and error recovery

> [!abstract] Short answer
> The Transport layer (Layer 4) — specifically TCP: it gives end-to-end, host-to-host delivery between processes, flow control (the receiver's advertised window), and error recovery (checksums, acknowledgments, retransmission, reordering). UDP sits on the same layer but provides none of those; then recovery belongs to the application.

## Why these duties are Layer 4's

1. **End-to-end, not per-link.** Layers 1–2 protect one hop; a frame checked at a switch says nothing about the middle of the path. Only the two endpoints share state, so only they can ACK, retransmit, and reorder — that is what makes the guarantees "end-to-end".
2. **Per-process addressing.** Ports deliver data to sockets, not just to machines — the multiplexing layer above IP.
3. **Feedback loop.** TCP's ACK stream plus the receive window close the control loop: window = flow control (protect the *receiver*), loss/RTT signals = congestion control (protect the *network*).

```d2
direction: down
send: "Sender TCP\nseq: bytes 1-1460, 1461-2920..." { width: 300; height: 90; style.fill: "#e3f2fd" }
ack: "Receiver TCP\nwindow = 65535, ACK next byte" { width: 300; height: 90; style.fill: "#fff3e0" }
loop: "lost segment -> retransmit\nslow ACK -> shrink in-flight" { width: 320; height: 90; style.fill: "#ffebee" }
send -> ack: "segments"
ack -> loop: "ACKs / window updates"
loop -> send
```

**Fig. 1.** The transport layer's engine: sequence numbers, ACKs and the window form a closed loop between the two endpoints only.

## What each guarantee actually is

- **Flow control** — a receiver-paced limit: the `Window` field says how much more the sender may have in flight; a slow reader shrinks it.
- **Error detection** — the TCP checksum covers header + data (mandatory in TCP; optional in IPv4's own header terms, removed in IPv6 header).
- **Error recovery** — detection plus repair: missing ACK range → retransmit (fast retransmit after 3 dup-ACKs, or RTO timer), out-of-order arrivals → reordering by sequence number. Recovery *implies* possible duplicates (an ACK may be lost after the data arrived), which is why [[How do you prevent duplicate message or packet delivery]] pairs with this card.

> [!warning] "Transport layer = TCP" overclaims, and L2 checks are not recovery
> UDP is a transport-layer protocol with checksum-only protection — no delivery, ordering, or flow control; QUIC adds reliability back over UDP. Conversely, Ethernet's FCS or IPv4's header checksum are *per-hop* integrity checks, not end-to-end recovery — frames get dropped, not fixed. The interview-safe sentence: "reliable end-to-end delivery is what TCP, at the transport layer, adds on top of IP".

Contrast: [[What is a segment at the Transport layer]] for the PDU mechanics, [[What is the difference between TCP and UDP]] for the reliability tradeoff, [[What is the job of the Network layer under the OSI model]] for why L3 stops short.

> [!tip] Interview answer
> Layer 4 — and concretely TCP: ports for process-to-process delivery, receiver window for flow control, checksums plus ACK-driven retransmission and reordering for error recovery. I flag the two follow-ups proactively: UDP is transport too but guarantees nothing, and per-hop CRCs at layer 2 are detection, not recovery — only the endpoints share enough state to recover anything.
