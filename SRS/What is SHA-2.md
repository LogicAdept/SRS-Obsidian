<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is SHA-2

> [!abstract] Short answer
> SHA-2 is the FIPS 180-4 family of Merkle-Damgard hash functions - SHA-224, SHA-256, SHA-384, SHA-512 (plus the truncated 512/224 and 512/256 variants) - with digest sizes of 224 to 512 bits and a 64- or 80-round compression function. It remains collision-resistant with no practical attack, and is the default general-purpose hash today ("SHA-256" is the 256-bit member of the SHA-2 family).

## The family and its mechanics

All members pad the message, append its 64-bit length, and compress 512-bit (or 1024-bit for the 512 variants) blocks through rounds of shifts, rotations, AND/OR/XOR, and additions of round constants. The variant names encode digest size and word width:

| Variant | Digest | Word size | Rounds | Max message |
|---|---|---|---|---|
| SHA-224 | 224 bit | 32 bit | 64 | 2^64 - 1 bits |
| SHA-256 | 256 bit | 32 bit | 64 | 2^64 - 1 bits |
| SHA-384 | 384 bit | 64 bit | 80 | 2^128 - 1 bits |
| SHA-512 | 512 bit | 64 bit | 80 | 2^128 - 1 bits |

```java
MessageDigest md = MessageDigest.getInstance("SHA-256");
byte[] digest = md.digest(data);
```

**Listing 1.** In Java the family member is selected by name; there is no bare "SHA-2" algorithm id.

SHA-2 output distribution does not make it a password hasher - it is fast, which is exactly wrong against offline guessing (see [[How should you store and handle passwords securely]]).

## Security status

- **No practical collisions or preimages** for any SHA-2 member; NIST's confidence comes from 20+ years of analysis after MD5 and SHA-1 fell.
- **Length extension applies.** SHA-256 and SHA-512 are Merkle-Damgard hashes, so `SHA256(key || message)` is not a secure MAC - [[What is HMAC]] wraps the hash with inner and outer pads precisely to kill that attack.
- **Not SHA-3.** SHA-3 (Keccak, FIPS 202) is a different sponge construction chosen by competition; it exists as a hedge, not because SHA-2 is weak.
- **Performance note**: the 64-bit-word members (SHA-384/512) are typically *faster* than SHA-256 on 64-bit CPUs because they process twice the bits per round - relevant when hashing large payloads at line rate.

## Where each member is used

SHA-256 dominates: TLS certificates, Git object IDs, Bitcoin proof-of-work, JWT HS256/RS256 components, file integrity. SHA-384/512 appear where 32-bit-word length-extension or collision margins matter, and SHA-224/512-224 survive mostly for compatibility when a shorter digest fits a protocol field. For keyed uses the family pairs with HMAC ([[What is HMAC]]); for signatures with RSA or ECDSA the digest is computed first and then signed ([[What is RSA]]).

> [!warning] Naming traps
> "SHA" alone usually means SHA-1 in old configs - broken since 2017 (practical collision, SHAttered). "SHA-2" is the family; "SHA-256" is one member. A config that says `sha` may negotiate SHA-1 silently - check the actual algorithm identifier.

> [!tip] Interview answer
> SHA-2 is the current NIST-standardized hash family defined in FIPS 180-4: SHA-224/256 with 32-bit words and 64 rounds, SHA-384/512 with 64-bit words and 80 rounds. It has no practical attacks, but being fast and Merkle-Damgard it is used with HMAC for authentication and never raw for passwords or as a keyed MAC.
