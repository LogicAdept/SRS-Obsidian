<!--
reps: 0
priority: 0
-->
#Networking/TCP #SRS
# How does TCP congestion control work

> [!abstract] Short answer
> Congestion control protects the *network*: the sender maintains a congestion window (cwnd) that grows cautiously while the path is healthy and shrinks when loss or delay signals overload. It starts with slow start (exponential growth per RTT until ssthresh), continues with congestion avoidance (additive increase, ~1 MSS per RTT), and reacts to loss with multiplicative decrease — halving cwnd on fast retransmit or collapsing to re-slow-start after RTO. Modern algorithms (CUBIC, BBR) refine the growth and loss-response curves.

## The state machine of one sender

1. **Slow start:** cwnd starts small (IW ~10 MSS); every ACK in an RTT doubles cwnd per RTT — probing for capacity exponentially.
2. **Congestion avoidance:** after cwnd ≥ ssthresh, growth turns linear (+1 MSS per RTT) — AIMD: increase additively, decrease multiplicatively.
3. **Fast retransmit / fast recovery:** three duplicate ACKs signal one lost segment; retransmit immediately (no RTO wait) and halve cwnd — the path is still delivering, so keep most of it.
4. **RTO timeout:** nothing arrived — severe congestion; cwnd collapses to the initial window and slow start begins again.
5. **CUBIC** (Linux default for years) scales the window as a cubic function of time since the last loss — fast recovery of big windows, gentler near the plateau; **BBR** instead models bottleneck bandwidth and RTT and paces accordingly, notably on lossy paths.

```d2
direction: down
ss: "Slow start\ncwnd doubles per RTT" { width: 260; height: 80; style.fill: "#e3f2fd" }
th: "cwnd >= ssthresh" { width: 220; height: 60; style.fill: "#fff3e0" }
ca: "Congestion avoidance\n+1 MSS per RTT (AIMD)" { width: 280; height: 80; style.fill: "#e8f5e9" }
loss: "3 dup-ACKs: fast retransmit\ncwnd = cwnd/2" { width: 300; height: 90; style.fill: "#ffebee" }
rto: "RTO timeout:\ncwnd reset, slow start again" { width: 300; height: 90; style.fill: "#ffebee" }
ss -> th -> ca
ca -> loss -> ca
ca -> rto -> ss
```

**Fig. 1.** Growth is cautious, response to loss is proportional: the sawtooth of classic TCP.

## Why the network needs senders to cooperate

Routers have finite queues. If every sender floods, queues overflow and *all* flows on the link degrade (and the Internet melts into congestion collapse — the reason this machinery exists). Because IP provides no feedback, TCP infers congestion from the only signals endpoints see: duplicate ACKs, RTO timeouts, RTT trends, or explicit ECN marks when available.

> [!warning] Flow control is not congestion control — and loss is not always congestion
> The receive window caps you because *the app is slow*; cwnd caps you because *the path is full* — the effective limit is the smaller of the two. And on Wi-Fi or long links, random (non-congestion) loss still makes classic loss-based algorithms back off, which BBR-style modeling fixes. Also "TCP cannot exceed the receiver's window" alone ignores cwnd — in-flight ≤ min(cwnd, rwnd) is the honest formula ([[How does TCP flow control work]]).

Context: [[What is TCP]], [[What is the TCP three-way handshake]] (initial window and options), and the UDP world where this must be reinvented: [[What is the difference between TCP and UDP]].

> [!tip] Interview answer
> The sender keeps a congestion window on top of the receive window: slow start doubles it per RTT until ssthresh, then AIMD grows linearly; three dup-ACKs trigger fast retransmit and a halving, an RTO collapses cwnd back to slow start. CUBIC shapes the curve, BBR models bandwidth and RTT instead of waiting for loss. Key line: cwnd protects routers, rwnd protects the receiver — in-flight is bounded by the minimum.
