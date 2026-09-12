<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #Networking/Web/Protocols/TLS #SRS
# What is the difference between HTTP and HTTPS

> [!abstract] Short answer
> HTTPS is not a different application protocol — it is ordinary HTTP running inside a TLS tunnel: same methods, headers, status codes and bodies, but every byte is encrypted and the server (and optionally the client) is authenticated by certificates. Concretely: HTTPS = HTTP over TLS over TCP; the URL scheme and default port (443 vs 80) differ, and an unauthenticated network observer sees connection metadata, not your data.

## What TLS adds to plain HTTP

1. **Confidentiality.** Symmetric encryption (AES-GCM, ChaCha20) with per-record nonces — passwords, cookies, tokens and payloads are unreadable on the wire.
2. **Integrity.** AEAD ciphers authenticate every record; an active attacker cannot flip bytes undetected (plain HTTP has *no* payload integrity beyond TCP checksums).
3. **Authentication.** The server presents an X.509 certificate chain rooted in a trusted CA, bound to the hostname you are contacting; client certificates can do mutual TLS.
4. **Session establishment.** A TLS handshake (1-RTT in TLS 1.3, RFC 8446) negotiates ciphers and keys before the first HTTP byte; session resumption shortens repeat visits.

```d2
direction: down
http: "HTTP request/response\n(same semantics both ways)" { width: 300; height: 70; style.fill: "#e8f5e9" }
tls: "TLS record layer\nencrypt + authenticate bytes" { width: 300; height: 80; style.fill: "#fff3e0" }
tcp: "TCP connection :443 (vs :80)" { width: 280; height: 70; style.fill: "#e3f2fd" }
http -> tls -> tcp
```

**Fig. 1.** HTTPS = the same HTTP wrapped by TLS; the application protocol and the tunnel are independent layers.

## What stays the same — and what it costs

Semantics are identical: caching, cookies (with Secure flag), methods, status codes behave the same ([[What are the HTTP request methods]]). Costs: handshake round trips (mitigated by TLS 1.3, session tickets, keep-alive), CPU for crypto (negligible at modern scale), and operational duty — certificate issuance/renewal (ACME automated this), cipher policy, and the fact that TLS terminates *somewhere*: at your reverse proxy, CDNs, or a load balancer, which then re-encrypts to upstreams ([[What is a web server]] for termination points). Byte overhead is a few KB per connection, not per request.

> [!warning] "HTTPS means the site is safe" conflates transport security with application security
> TLS guarantees you talk privately with *whoever owns that certificate* — a phishing site with a valid cert is fully HTTPS. It does not stop XSS, SQL injection, or a malicious server logging everything — those are application-security concerns above the transport. Also note where HTTPS does NOT help: traffic analysis (SNI leaks the hostname unless Encrypted Client Hello is on; DNS leaks unless DoH/DoT), and intra-datacenter hops after termination — an HTTP hop to a "secure" service reintroduces plaintext ([[How do containers find each other by name on a Docker network]] networks are exactly where plaintext east-west traffic hides).

Protocol context: [[What is HTTP]], [[What happens when you type a URL into a browser and press Enter]] for where the handshake sits; the encryption-layer mythology: [[Why do many dumps place HTTPS encryption at the Presentation layer]].

> [!tip] Interview answer
> HTTPS is HTTP unchanged, tunneled through TLS: encryption for confidentiality, AEAD for integrity, certificate-based server authentication — plus the 1-RTT TLS 1.3 handshake and port 443. Everything above (methods, caching, cookies) is identical, with Secure/HSTS hardening cookies and redirects. The boundary I draw: TLS secures the transport between endpoints — it says nothing about the trustworthiness of the site or what happens after termination.
