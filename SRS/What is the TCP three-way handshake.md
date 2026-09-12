<!--
reps: 0
priority: 0
-->
#Networking/TCP #SRS
# What is the TCP three-way handshake

> [!abstract] Short answer
> The three-way handshake is how a TCP connection starts: the client sends SYN (with its initial sequence number ISN_c), the server answers SYN-ACK (its own ISN_s, acknowledging ISN_c+1), the client confirms with ACK. Three messages synchronize both sides' sequence numbers and prove both directions work — after which data flows and the connection is ESTABLISHED.

## The exchange, message by message

1. **SYN (client → server):** random ISN_c (randomized to prevent old-segment injection and simple spoofing), proposed options: MSS, window scaling, SACK-permitted.
2. **SYN-ACK (server → client):** server picks ISN_s, sets ACK = ISN_c + 1, echoes its accepted options. The server now holds half-open state (SYN-RECEIVED) — memory allocated *before* the client confirms.
3. **ACK (client → server):** ACK = ISN_s + 1. Both sides are ESTABLISHED; the client may already piggyback the first data byte on this very segment.

```d2
direction: right
c: "Client (CLOSED)" { width: 200; height: 70; style.fill: "#e3f2fd" }
s: "Server (LISTEN)" { width: 200; height: 70; style.fill: "#e8f5e9" }
m1: "1. SYN\nseq=ISN_c" { width: 180; height: 70; style.fill: "#fff3e0" }
m2: "2. SYN-ACK\nseq=ISN_s, ack=ISN_c+1" { width: 220; height: 80; style.fill: "#fff3e0" }
m3: "3. ACK\nack=ISN_s+1" { width: 180; height: 70; style.fill: "#fff3e0" }
c -> s: "SYN"
s -> c: "SYN-ACK"
c -> s: "ACK (+ first data)"
```

**Fig. 1.** SYN, SYN-ACK, ACK: each side announces its random starting sequence number and acknowledges the other's plus one.

## Why exactly three messages

- **Both ISNs must be confirmed.** Two messages (SYN, SYN-ACK) would leave the server unsure the client heard its ISN; the third ACK closes that loop — this is the RFC 9293 "three-way handshake" rationale: both parties learn the other received their starting sequence number.
- **Stale duplicates are rejected.** An old SYN retransmission from a dead connection is answered, but its old sequence numbers make the continuation invalid — fresh ISNs per connection prevent "old duplicate" injection (the original design goal).
- **Tearing down is symmetric:** FIN, FIN-ACK each way, with TIME-WAIT on the active closer so delayed segments die before the 4-tuple is reused.

> [!warning] The handshake is where denial-of-service and latency budgets meet
> A SYN flood exploits step 2's half-open state: fill the backlog table with SYNs and legit clients starve — mitigations are SYN cookies (stateless SYN-ACKs) and backlog tuning, not "more bandwidth". And that one RTT before any byte moves is why connection reuse (keep-alive), TLS 1.3's 1-RTT, and QUIC's merged crypto+transport handshake all focus on eliminating round trips ([[What is HTTP 3 and why does it use QUIC]]). Saying "the handshake negotiates the window size" is wrong — options like window *scaling* are negotiated, the window itself is per-segment (see [[How does TCP flow control work]]).

Mechanics around it: [[What is TCP]], [[What is a segment at the Transport layer]], and the dedup role of fresh ISNs in [[How do you prevent duplicate message or packet delivery]].

> [!tip] Interview answer
> Three-way handshake: SYN with a random ISN, SYN-ACK with the server's ISN and ack of ISN_c+1, then ACK — both sides ESTABLISHED. Its purpose is synchronizing sequence numbers and validating both directions, which also kills stale duplicates. I attach the two production angles: SYN floods abuse half-open state (SYN cookies), and this one RTT is what QUIC and TLS 1.3 work to erase.
