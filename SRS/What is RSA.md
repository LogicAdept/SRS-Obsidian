<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is RSA

> [!abstract] Short answer
> RSA (RFC 8017, PKCS #1 v2.2) is the public-key algorithm built on the hardness of factoring: the public key is `(n, e)`, the private key is the matching `d`. In practice RSA is used for **signatures and key transport**, never for bulk data - it is orders of magnitude slower than AES, so protocols use it to authenticate or wrap a symmetric session key. Modern usage demands OAEP for encryption and PSS for signatures, with keys of at least 2048 bits.

## The mechanics

Encryption is `c = m^e mod n` and signing is `s = m^d mod n`; security rests on deriving `d` from `(n, e)` requiring the factorization of `n`. The public exponent `e = 65537` is the conventional choice - large enough to avoid trivial attacks, small enough for fast verification.

```text
Keys:      n = p*q (2048+ bit), e = 65537, d = e^-1 mod lcm(p-1, q-1)
Encrypt:   c = m^e mod n                    (m raised to e)
Sign:      s = m^d mod n                    (verify: s^e == m)
```

**Listing 1.** Conceptual RSA. Real schemes never compute these on raw m - padding is mandatory.

## Padding is not optional

- **RSAES-OAEP** is the current encryption scheme; **RSAES-PKCS1-v1_5** is retained only for compatibility and is the padding Bleichenbacher's adaptive chosen-ciphertext attack tore apart (and its later variants).
- **RSASSA-PSS** is the recommended signature scheme; **RSASSA-PKCS1-v1_5** signatures remain widespread (certificates, JWT RS256) but PSS is the forward-looking choice.
- Textbook RSA - raw modular exponentiation with no padding - is deterministic and malleable; multiplying two ciphertexts multiplies their plaintexts. It is never acceptable.

```java
Cipher c = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
Signature s = Signature.getInstance("RSASSA-PSS"); // PSS params via ParameterSpec
```

**Listing 2.** JCE names for the padded schemes. "RSA/ECB/..." is misleading naming: ECB here only marks "no chaining", the security comes from OAEP.

## Where RSA shows up

- **TLS 1.2**: RSA key transport (dropped entirely in TLS 1.3) or RSA signatures in handshakes ([[What is the TLS handshake]]).
- **JWT RS256/PS256**: RSASSA-PKCS1-v1_5 / PSS signatures over the signing input ([[What is the difference between HS256 and RS256 in JWT]]).
- **Hybrid encryption**: RSA-OAEP wraps a random AES session key; AES does the bulk work ([[What is AES]], [[What is the difference between symmetric and asymmetric encryption]]).

Key sizes: 2048 bits is today's floor, 3072+ for long-lived secrets; 1024-bit keys are dead.

> [!warning] "Longer RSA keys mean stronger than AES"
> A 3072-bit RSA key and a 128-bit AES key are both roughly "128-bit security" - the numbers are not comparable directly. And RSA with broken padding is weak at any key size.

> [!tip] Interview answer
> RSA is factoring-based public-key crypto standardized in RFC 8017: public `(n, e)` with e usually 65537, private d. Because it is slow it signs or wraps - OAEP for encryption, PSS for signatures - while AES moves the data. 2048 bits is the minimum; raw or v1.5-padded encryption is legacy you should flag.
