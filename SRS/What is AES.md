<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is AES

> [!abstract] Short answer
> AES (FIPS 197) is the NIST-standardized symmetric block cipher: a 128-bit block size with key sizes of 128, 192, or 256 bits driving 10, 12, or 14 rounds respectively. Each round applies SubBytes, ShiftRows, MixColumns, and AddRoundKey. AES is secure as a primitive - real-world failures come from mode selection (ECB) and nonce reuse in GCM, not from the cipher itself.

## The rounds

AES is a substitution-permutation network operating on a 4x4 byte state. FIPS 197 defines the round transformation as four operations:

- **SubBytes** - byte-wise S-box substitution (the only non-linear step);
- **ShiftRows** - cyclic row shifts for diffusion across columns;
- **MixColumns** - GF(2^8) matrix multiply mixing each column (skipped in the final round);
- **AddRoundKey** - XOR with the round key derived from the key schedule.

The number of rounds depends on the key: 128-bit keys get 10 rounds, 192-bit 12, 256-bit 14. There are no known practical attacks better than brute force against full AES.

```java
KeyGenerator kg = KeyGenerator.getInstance("AES");
kg.init(256);
SecretKey key = kg.generateKey();
Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
c.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, nonce)); // 96-bit nonce
```

**Listing 1.** The modern Java incantation: AES with GCM, an authenticated mode. The nonce passed here must never repeat under the same key.

## Modes are where AES gets dangerous

- **ECB** encrypts equal blocks to equal ciphertext - the famous penguin image. It leaks structure and must not be used for real data.
- **GCM** (CTR + GHASH) provides confidentiality and integrity (AEAD). Its catastrophic failure mode is **nonce reuse**: reusing a 96-bit nonce with the same key leaks the authentication key and enables forgery. Nonces must come from a counter or be provably unique per key.
- **CBC** without authentication is malleable (padding oracles, bit-flipping) - pair it with a MAC or avoid it. When the use case is "encrypt to a public key holder", the symmetric cipher is the wrong tool on its own - that is the hybrid territory of [[What is RSA]] and [[What is the difference between symmetric and asymmetric encryption]].

```d2
direction: right
pt: "128-bit block" { width: 190; height: 70; style.fill: "#e3f2fd" }
r: "Round 1 .. N-1\nSubBytes, ShiftRows,\nMixColumns, AddRoundKey" { width: 300; height: 110; style.fill: "#fff3e0" }
fin: "Final round\n(no MixColumns)" { width: 220; height: 90; style.fill: "#fff3e0" }
ct: "128-bit ciphertext" { width: 210; height: 70; style.fill: "#e8f5e9" }
pt -> r -> fin -> ct
```

**Fig. 1.** AES processes each 128-bit block independently through N rounds (10/12/14 for 128/192/256-bit keys); block independence is a property of the *cipher*, and the mode decides whether that leaks.

> [!warning] "AES-256 is always safer than AES-128"
> For block-cipher strength yes (2^256 vs 2^128 keyspace), but AES-128 already has no practical attack, and a broken GCM nonce scheme or an ECB mode under AES-256 is worse than correct GCM under AES-128. Mode discipline beats key length.

> [!tip] Interview answer
> AES is the FIPS 197 symmetric block cipher - 128-bit blocks, 10/12/14 rounds for 128/192/256-bit keys, built from SubBytes, ShiftRows, MixColumns, AddRoundKey. The cipher itself is fine; everything that fails in practice is around it: ECB leaking structure, unauthenticated CBC, and GCM nonce reuse, which quietly destroys both integrity and confidentiality.
