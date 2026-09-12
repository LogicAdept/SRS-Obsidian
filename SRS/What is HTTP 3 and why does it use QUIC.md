<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What is HTTP 3 and why does it use QUIC

> [!abstract] Short answer
> HTTP 3 (RFC 9114) is HTTP's semantics running over QUIC (RFC 9000) instead of TCP: a UDP-based transport that integrates TLS 1.3, establishes connections in fewer round trips, and makes streams independent — so one lost packet no longer stalls every response (TCP head-of-line blocking, HTTP/2's residual problem). It also survives network changes: connection IDs let a phone switch from Wi-Fi to LTE without dropping the session.

## What QUIC changes

1. **Fewer round trips to first byte.** TCP handshake + TLS handshake become one combined QUIC handshake: TLS 1.3's keys travel inside the QUIC initial packets — first request can go out after 1-RTT (0-RTT with resumption, with replay caveats).
2. **Independent streams.** QUIC multiplexes streams itself; a packet loss stalls only the streams whose data was lost, not the whole connection — HTTP/2 over TCP had exactly that stall ([[What is the difference between HTTP 1.1 and HTTP 2]]).
3. **Built-in TLS 1.3.** Encryption is not a layer above (as with TCP+TLS) but part of the protocol — headers are encrypted too, middleboxes cannot read or mutate connection metadata.
4. **Connection migration.** Connections are identified by connection IDs, not the 4-tuple; changing IP (Wi-Fi → cellular) keeps the session alive.
5. **User-space evolution.** QUIC runs in application space over UDP — transports improve with app updates, not OS kernels.

```d2
direction: down
sem: "HTTP semantics\n(methods, headers, status)" { width: 300; height: 70; style.fill: "#e8f5e9" }
h3: "HTTP/3 framing\n(QUIC streams)" { width: 280; height: 70; style.fill: "#fff3e0" }
q: "QUIC\nstreams, TLS 1.3, loss recovery" { width: 320; height: 80; style.fill: "#fff3e0" }
u: "UDP" { width: 160; height: 55; style.fill: "#e3f2fd" }
sem -> h3 -> q -> u
```

**Fig. 1.** The stack: the same HTTP you know, re-plumbed from the framing down to a new transport.

## Why the web moved

Browser telemetry on lossy mobile networks showed HTTP/2's TCP stall; connection setup (TCP+TLS) dominated short requests; and mobile IP churn killed sessions. QUIC answers all three — and the deployment is transparent: browsers and servers negotiate HTTP/3 via `Alt-Svc` headers or DNS HTTPS records, falling back to HTTP/2 ([[What is the difference between HTTP and HTTPS]] — TLS is inside QUIC now, so "HTTPS over HTTP/3" is automatic).

> [!warning] QUIC is not "TCP over UDP with a rename", and UDP-blocking networks hurt it
> It re-implements reliability, flow control per stream, congestion control (with the same duties as TCP's — [[How does TCP congestion control work]]), and loss detection in user space — done badly, it behaves worse than TCP. Practical friction: some firewalls/NATs throttle unknown UDP, and QUIC's encrypted headers disable the classic middlebox tricks (and the classic debugging tools — captures need QUIC-aware analysis, [[What is a packet at the Network layer]] still applies below UDP). And "0-RTT is free speed" ignores replay risk: 0-RTT data can be duplicated by attackers, so only idempotent requests belong there ([[What is idempotency in HTTP and in messaging]]).

> [!tip] Interview answer
> HTTP 3 is the RFC 9114 mapping of HTTP semantics onto QUIC — a UDP-based transport with integrated TLS 1.3, per-stream independence, connection migration by connection ID, and 1-RTT (0-RTT on resumption) setup. Why: kill TCP head-of-line blocking that HTTP/2 inherited, cut handshake round trips, and let the transport evolve in user space. I add the honest caveats: UDP-hostile networks and replay-sensitive 0-RTT.
