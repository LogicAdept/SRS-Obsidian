<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is the Diffie-Hellman algorithm

> [!abstract] Short answer
> Diffie-Hellman is a key-agreement protocol: two parties publish `g^a mod p` and `g^b mod p` over an untrusted channel and both compute the same shared secret `g^(ab) mod p`, which an eavesdropper cannot derive without solving the discrete logarithm problem. It establishes **shared secrets, not authenticated ones** - anonymous DH is trivially man-in-the-middleable, so real protocols authenticate the exchange (signed DH in TLS 1.3).

## The core exchange

With public prime `p` and generator `g`, and private secrets `a` and `b`:

```text
A = g^a mod p          (Alice publishes)
B = g^b mod p          (Bob publishes)
Alice computes: B^a mod p = g^(ab) mod p
Bob computes:   A^b mod p = g^(ab) mod p
```

**Listing 1.** Conceptual core of DH. The eavesdropper sees p, g, A, B but needs a or b - the discrete-log problem - to get the shared secret.

An attacker in the middle can run two separate DH exchanges and relay both secrets - DH provides secrecy of the result, **not** the identity of the peer.

```d2
direction: right
alice: "Alice\nsecret a" { width: 180; height: 80; style.fill: "#e3f2fd" }
bob: "Bob\nsecret b" { width: 180; height: 80; style.fill: "#e8f5e9" }
m1: "g^a mod p" { width: 160; height: 60; style.fill: "#fff3e0" }
m2: "g^b mod p" { width: 160; height: 60; style.fill: "#fff3e0" }
k: "shared g^(ab) mod p\n-> session key material" { width: 260; height: 80; style.fill: "#ffebee" }
alice -> bob: m1
bob -> alice: m2
alice -> k
bob -> k
```

**Fig. 1.** Both sides derive the same value from what they sent and received; the published values alone do not reveal it.

## Groups and TLS usage

- **FFDHE (RFC 7919)** standardizes safe finite-field groups (ffdhe2048 and up) so servers stop offering hand-picked weak primes - the flaw Logjam exploited when clients accepted 512-bit export groups.
- **ECDHE** replaces finite-field exponentiation with elliptic-curve scalar multiplication at far smaller key sizes; TLS 1.3 removed static RSA and finite-field non-ephemeral modes, keeping only (EC)DHE with signatures - which is what gives forward secrecy ([[What is the TLS handshake]]).
- **Static DH keys** stored long-term are rarely used; "DHE/ECDHE" ephemeral keys are fresh per session, so a later private-key leak does not decrypt past sessions.

> [!warning] "DH is encryption"
> DH is not encryption - it is key agreement. It produces the secret that a symmetric cipher then uses ([[What is AES]]). Saying "we encrypt with Diffie-Hellman" is a red flag in an interview; pair it with authentication to get an authenticated key exchange ([[What is the difference between symmetric and asymmetric encryption]]).

> [!tip] Interview answer
> Diffie-Hellman lets two parties derive a shared secret over a public channel using modular exponentiation - each publishes g raised to its secret power, and only the combination g^(ab) is hard to reverse. On its own it is anonymous and MITM-able, so TLS 1.3 signs ephemeral DH parameters; RFC 7919 fixed the weak-custom-primes era with standard ffdhe groups.
