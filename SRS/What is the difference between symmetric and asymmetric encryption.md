<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is the difference between symmetric and asymmetric encryption

> [!abstract] Short answer
> Symmetric encryption uses one shared secret key for both encryption and decryption (AES) - very fast, but the key must reach every party over a trusted channel. Asymmetric encryption uses a key pair - public to encrypt (or verify), private to decrypt (or sign) (RSA, EC) - solving key distribution and adding digital signatures at the cost of being 100-1000x slower. Real systems are hybrid: asymmetric to authenticate and establish keys, symmetric for the data ([[What is the TLS handshake]]).

## The two models side by side

| Property | Symmetric | Asymmetric |
|---|---|---|
| Keys | one shared secret | public + private pair |
| Speed | fast (GB/s per core) | slow (orders of magnitude slower) |
| Key distribution | needs pre-shared channel | public key is publishable |
| Signatures | no (MACs instead) | yes, non-repudiable |
| Typical key sizes | 128-256 bits | 2048+ bits (RSA) / 256 bits (EC) |
| n parties need | pairwise keys n(n-1)/2 | n key pairs |

```java
KeyGenerator kg = KeyGenerator.getInstance("AES"); kg.init(256);   // symmetric
KeyPairGenerator kp = KeyPairGenerator.getInstance("RSA");          // asymmetric
kp.initialize(2048);
```

**Listing 1.** Generating both key types; the AES secret is a random 256-bit value, the RSA pair is built from primes.

```d2
direction: right
a: "Alice" { width: 130; height: 60; style.fill: "#e3f2fd" }
k: "Public key Kpub\npublished" { width: 210; height: 80; style.fill: "#fff3e0" }
b: "Bob\nKpriv secret" { width: 160; height: 70; style.fill: "#e8f5e9" }
c: "Ciphertext" { width: 150; height: 60; style.fill: "#fff3e0" }
a -> k: "fetch"
a -> c: "encrypt with Kpub"
c -> b: "decrypt with Kpriv"
```

**Fig. 1.** Asymmetric flow: anyone can encrypt to Bob's public key; only his private key decrypts. Symmetric would require the same key on both ends first.

## How hybrid encryption resolves the tradeoff

TLS, PGP, and envelope encryption all do the same dance: asymmetric crypto authenticates the peer and establishes (or wraps) a fresh symmetric session key, then the symmetric cipher encrypts the actual traffic. In TLS 1.3 the server's certificate key only *signs* the ephemeral Diffie-Hellman exchange - the session itself is AES/ChaCha ([[What is AES]], [[What is the Diffie-Hellman algorithm]]). Asymmetric key usage is also bounded: RSA keys sign or wrap megabytes, not gigabytes.

> [!warning] "Asymmetric is stronger because 2048 bits > 128 bits"
> The numbers count different things: 128-bit symmetric strength is a 2^128 brute-force space, while RSA factoring attacks scale far better than brute force - a 2048-bit RSA key is only around 112-bit security. Comparing raw bit lengths across the two families is meaningless ([[What is RSA]]).

> [!tip] Interview answer
> Symmetric = one shared key, AES-fast, but key distribution and no signatures. Asymmetric = key pair, solves distribution and non-repudiation, but too slow for data. Everything real is hybrid: TLS 1.3 signs an ephemeral DH exchange with the certificate key and then encrypts with AES-GCM, so each family does the job it is good at.
