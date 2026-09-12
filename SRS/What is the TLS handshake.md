<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/TLS #Security/Cryptography #SRS

# What is the TLS handshake

> [!abstract] Short answer
> The TLS 1.3 handshake (RFC 8446) establishes a session in **one round trip**: the client sends a ClientHello with its key-share, the server answers ServerHello plus its key-share, then both derive the same traffic keys - and everything after the Key Exchange phase is encrypted. Authentication (server certificate plus a `Finished` message proving possession of the derived key) is folded into the same flight; TLS 1.2 needed two round trips and a separate key-negotiation step.

## The three phases of TLS 1.3

RFC 8446 describes the handshake as three phases:

1. **Key Exchange** - ClientHello carries supported cipher suites and a `key_share` (an ephemeral (EC)DHE public value); the server answers with its share, and both sides compute the shared secret - "everything after this phase is encrypted."
2. **Server Parameters** - extension-level settings: whether the client must authenticate, ALPN protocol choice, session ticket parameters.
3. **Authentication** - the server presents its certificate chain and signs the handshake transcript; the `Finished` messages provide key confirmation and handshake integrity for both directions.

```d2
direction: right
c: "Client" { width: 130; height: 60; style.fill: "#e3f2fd" */
ch: "1. ClientHello\nkey_share = g^a" { width: 230; height: 80; style.fill: "#fff3e0" */
sh: "2. ServerHello + cert\nkey_share = g^b, signed" { width: 300; height: 80; style.fill: "#fff3e0" */
fin: "3. Finished x2\nkeys derived on both sides" { width: 270; height: 80; style.fill: "#e8f5e9" */
app: "Application data\nencrypted from here" { width: 240; height: 70; style.fill: "#e8f5e9" */
c -> ch -> sh -> fin -> app
```

**Fig. 1.** TLS 1.3's 1-RTT flight: key shares travel in the Hellos, the certificate and its signature ride the encrypted leg, and application data begins after the Finished exchange.

## What the handshake actually establishes

- **Authenticated key agreement, not trust by transport**: the ephemeral (EC)DHE exchange ([[What is the Diffie-Hellman algorithm]]) provides forward secrecy - a later private-key leak does not decrypt past sessions because session keys were derived from ephemeral shares; the certificate's RSA/ECDSA signature ties the server identity to that exchange ([[What is RSA]]).
- **Cipher-suite selection is minimal in 1.3**: suites name only the AEAD cipher and hash (TLS_AES_128_GCM_SHA256...) - key exchange is always (EC)DHE, signature algorithms are negotiated separately.
- **Session resumption**: PSK-based resumption allows 0-RTT early data - at the cost of replayability, so 0-RTT must never carry non-idempotent requests.

> [!warning] "TLS encrypts, so the site is safe"
> The handshake authenticates the *certificate's identity*, not the trustworthiness of the site - a phisher with a valid certificate for lookalike.domain passes the same handshake. And TLS 1.2 leftovers matter: static RSA key exchange (no forward secrecy) and CBC suites are the legacy the 1.3 redesign removed - a "TLS handshake" conversation should say which version ([[What is the difference between HTTP and HTTPS]] is the outer context; [[What is HMAC]] and AEAD protect the records after the handshake).

> [!tip] Interview answer
> TLS 1.3's handshake is one round trip in three phases - key exchange with ephemeral (EC)DHE key shares, server parameters, and authentication where the certificate signs the transcript and Finished messages confirm the keys. It gives forward secrecy by construction, resumes with PSK (0-RTT replayable, so idempotent requests only), and everything after the first flight is encrypted application data.
