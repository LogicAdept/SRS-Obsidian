<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What is the difference between HTTP 1.1 and HTTP 2

> [!abstract] Short answer
> The semantics are the same; the transport encoding changed. HTTP/1.1 is textual, one in-flight request per TCP connection (pipelining existed but was unusable), so browsers open 6+ connections and block on head-of-line. HTTP/2 (RFC 9113) is binary: one TCP connection carries many multiplexed streams with per-stream priorities, header compression (HPACK), and server push — the same stateless request/response, no queue behind a slow response. TLS is de-facto mandatory in browsers, and text headers become HPACK-compressed binary frames.

## The comparison

| Aspect | HTTP/1.1 (RFC 9112) | HTTP/2 (RFC 9113) |
|---|---|---|
| Encoding | plaintext text protocol | binary frames (DATA, HEADERS, SETTINGS...) |
| Multiplexing | none — one request per connection at a time (pipelining blocked on head-of-line) | many streams interleaved over one connection |
| Connection economy | 6+ parallel connections per origin (browser heuristic) | one connection (+ flow-control windows) |
| Headers | repeated full text | HPACK: static+dynamic tables, Huffman coding |
| Compression of bodies | Content-Encoding (gzip/br) — same both ways | same, but *header* compression separate (HPACK, CRIME-safe) |
| Server push | no | yes (rarely used; removed in HTTP/3 practice) |
| Transport requirements | any | order, no loss-tolerant issues — hence TCP; TLS in practice |

```d2
direction: right
h1: "HTTP/1.1\nconn1: req1...wait...\nconn2: req2..." { width: 280; height: 100; style.fill: "#e3f2fd" }
h2: "HTTP/2\none conn: [s1][s2][s1][s3]\nstreams interleaved" { width: 300; height: 100; style.fill: "#e8f5e9" }
h1 -> h2: "same semantics, new framing"
```

**Fig. 1.** Multiplexing removes the queue behind a slow response — the visible performance jump on resource-heavy pages.

## What it means in practice

- **Latency:** fewer handshakes (one connection), no head-of-line *at the HTTP layer*, faster page loads with many small assets — the motivation browsers had.
- **Backward compatibility:** methods, status codes, headers, cookies, caching — identical semantics ([[What are the HTTP request methods]]); content negotiation includes `Upgrade: h2c` (cleartext, rarely used) or ALPN over TLS (the real path).
- **Server ops:** a single connection changes load-balancing math — long-lived connections need L7 awareness to spread streams ([[What is the difference between L3 L4 and L7]]); header compression requires care with per-connection state.

> [!warning] HTTP/2 fixes HTTP head-of-line blocking, not TCP's
> A lost TCP packet stalls *all* streams on the connection — under lossy networks, six HTTP/1.1 connections can outperform one HTTP/2 connection. That is the exact motivation for HTTP/3 moving transport to QUIC, where streams are independent ([[What is HTTP 3 and why does it use QUIC]]). Second trap: "HTTP/2 pushes resources, so it is faster by default" — push was rarely beneficial and browsers de-prioritized/removed it; the wins are multiplexing and HPACK. And "text vs binary is cosmetic" ignores the operational shift: sniffing HTTP/2 on the wire needs tooling, and intermediaries that assumed line-based parsing broke.

> [!tip] Interview answer
> Same semantics, different framing: 1.1 is text with one request per connection — browsers cheat with parallel connections; 2 is binary frames with multiplexed streams, HPACK header compression and one TLS connection per origin. The sharp follow-up I volunteer: 2 removes HTTP-level head-of-line blocking but inherits TCP's — packet loss stalls all streams, which is precisely why HTTP/3 switched to QUIC with independent streams.
