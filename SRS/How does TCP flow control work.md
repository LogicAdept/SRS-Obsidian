<!--
reps: 0
priority: 0
-->
#Networking/TCP #SRS
# How does TCP flow control work

> [!abstract] Short answer
> Flow control protects the *receiver* from a faster sender. Every TCP segment carries the receiver's advertised window — how many bytes it can still accept beyond the last acknowledged byte; the sender may never have more in flight than that window. The window slides as the application reads data and ACKs arrive; a window-scaling option raises the 16-bit field's 64 KB ceiling, and a zero window pauses the sender until window probes report space again.

## The sliding window loop

1. The receiver tracks free buffer space: `window = receive buffer − unread bytes`, advertised in every ACK's Window field.
2. The sender keeps `effective window = advertised window − (bytes sent − bytes ACKed)` and stops transmitting when it hits zero.
3. As the app reads from the buffer and ACKs flow back, the window slides forward and the sender resumes.
4. **Window scaling** (negotiated at handshake, RFC 7323): the 16-bit Window field is multiplied by a scale factor, so windows of megabytes are possible on high-bandwidth paths.

```d2
direction: right
snd: "Sender\nin-flight <= advertised window" { width: 280; height: 90; style.fill: "#e3f2fd" }
rcv: "Receiver\nbuffer fills as app reads slowly" { width: 280; height: 90; style.fill: "#fff3e0" }
shr: "Window shrinks -> zero" { width: 230; height: 70; style.fill: "#ffebee" }
prs: "Zero-window probes\n.sender resumes when space frees" { width: 260; height: 90; style.fill: "#e8f5e9" }
snd -> rcv: "segments"
rcv -> snd: "ACK + Window"
rcv -> shr -> prs
```

**Fig. 1.** The window is feedback: a slow reader shrinks it to zero, probes carry the resumption signal.

## Flow control vs congestion control — the exam pairing

| | Flow control | Congestion control |
|---|---|---|
| Protects | the receiver's buffer | the network (routers' queues) |
| Signal | advertised receive window | loss, RTT growth, ECN |
| Who sets it | receiver | sender's policy (RFC 9293 leaves it to implementation: CUBIC, BBR...) |

Both limit the same "bytes in flight", which is why they are confused; the effective sending rate is the minimum of the two windows ([[How does TCP congestion control work]]).

> [!warning] The classic zero-window and silly-window traps
> A receiver stuck at `window = 0` must not be forgotten by a sender that just "waits" — TCP mandates zero-window **probe** timers, otherwise a lost window-update ACK deadlocks the connection forever. On the other side, if the app reads one byte at a time and the receiver advertises tiny windows, headers dominate payload ("silly window syndrome"); receivers use the MSS-based rules and senders use Nagle's algorithm to avoid it. And "the window field is 16 bits, so TCP maxes at 64 KB" ignores window scaling — a decade-old lie.

Mechanics around the window: [[What is a segment at the Transport layer]] (where the field lives), [[What is the TCP three-way handshake]] (where scaling is negotiated), and the sibling mechanism [[How does TCP congestion control work]].

> [!tip] Interview answer
> Flow control is receiver-driven: every ACK advertises the remaining buffer as the window, the sender keeps in-flight bytes under it, and window scaling extends the 16-bit field past 64 KB. Window zero pauses the sender, with mandatory probes so a lost update cannot deadlock. The one-liner that lands: flow control protects the receiver, congestion control protects the network — both cap the same in-flight counter.
