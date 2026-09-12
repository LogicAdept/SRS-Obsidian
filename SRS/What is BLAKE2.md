<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is BLAKE2

> [!abstract] Short answer
> BLAKE2 (RFC 7693) is a modern cryptographic hash based on the SHA-3 finalist BLAKE, designed to be **faster than MD5 while offering SHA-3-level security**. It comes in BLAKE2b (up to 64-byte digests, 64-bit words) and BLAKE2s (up to 32-byte digests, 32-bit words), and has a **built-in keyed mode** that provides a MAC without needing HMAC.

## Design highlights

BLAKE2b compresses with the round function of the ChaCha stream cipher - ARX operations (add, rotate, XOR) on a wide internal state, 12 rounds for BLAKE2b and 10 for BLAKE2s. The parameter block lets the caller choose digest length, key, salt, and personalization, so one algorithm covers plain hashing, MACs, and KDF roles.

- **Digest size is a parameter**: BLAKE2b outputs 1-64 bytes, BLAKE2s 1-32 bytes, not a fixed size per name.
- **Keyed hashing is first-class**: supplying a key switches BLAKE2 into prefix-MAC mode - the key is fed as part of the parameter block, and the RFC describes this as replacing HMAC where a fast keyed hash is needed.
- **Performance**: the RFC's own benchmarks show BLAKE2b around 3-5 bytes per cycle on 64-bit platforms - roughly 10x SHA-3-512 and faster than MD5.

```java
// Not in the standard JCE - needs BouncyCastle or similar provider
Blake2bDigest digest = new Blake2bDigest(256);        // plain, 256-bit output
Blake2bDigest mac = new Blake2bDigest(key, 32, null, null); // keyed: a MAC
```

**Listing 1.** The JDK does not ship BLAKE2; adding a provider is the price for it, which is why SHA-256 stays the default choice in pure-Java stacks.

## Where it fits

| Need | Fit |
|---|---|
| General-purpose digest, speed-critical | BLAKE2b/2s strong candidate |
| MAC without extra HMAC step | keyed BLAKE2 |
| Password storage | **No** - still a fast hash, not a KDF ([[How should you store and handle passwords securely]]) |
| Compatibility with FIPS-only environments | SHA-2/SHA-3 instead |

Adoption examples: BLAKE2 is available in OpenSSL, libsodium, and wire protocols (WireGuard uses BLAKE2s as its hash), while the standard Java JCE ships only MD5/SHA families - hence the provider dependency above. BLAKE3 extends the design with a Merkle tree for parallel and incremental hashing but is a separate specification, not part of RFC 7693.

Against [[What is SHA-2]] the trade is simple: equal-ish security margin, noticeably higher throughput, less universality. Against [[What is MD5]] there is no trade - BLAKE2 is faster *and* unbroken, which is why "we kept MD5 for speed" has not been a valid argument for a decade.

> [!warning] Keyed BLAKE2 vs HMAC
> Keyed BLAKE2 is not HMAC - it is a different construction with its own analysis. The RFC positions it as a fast replacement where HMAC's two-pass cost matters, but security proofs differ; when a spec literally requires "HMAC-SHA-256", swapping in keyed BLAKE2 changes the algorithm, not just the speed ([[What is HMAC]]).

> [!tip] Interview answer
> BLAKE2 is a ChaCha-core hash from RFC 7693: BLAKE2b and BLAKE2s with parameterized digest sizes, faster than MD5 while having no known collisions, and with built-in keyed mode that acts as a MAC. It is not in the standard JDK and, like every fast hash, is wrong for password storage.
