<!--
reps: 0
priority: 0
-->
#Security/JWT #Security/Cryptography #SRS

# What is the difference between HS256 and RS256 in JWT

> [!abstract] Short answer
> HS256 signs the JWT with **HMAC-SHA256 and one shared secret** - every issuer *and* every validator holds the same key. RS256 signs with **RSASSA-PKCS1-v1_5 and an RSA key pair** - the issuer holds the private key, validators verify with the public key fetched from a JWKS endpoint. The consequence drives the choice: HS256 is fast and simple for one service that both issues and verifies; RS256 is the default for multi-service systems because validators can verify without any ability to forge ([[What is HMAC]], [[What is RSA]]).

## The mechanics

```text
HS256:  signature = HMAC-SHA256(secret, base64url(header) + "." + base64url(payload))
RS256:  signature = RSA-PKCS1-v1_5-SHA256(private_key, same signing input)
```

**Listing 1.** Both sign the same signing input - the dot-joined encoded header and payload; only the key relationship differs.

```d2
direction: right
hs: "HS256\nsymmetric" { width: 170; height: 70; style.fill: "#e3f2fd" }
sh: "Shared secret\non issuer AND validators" { width: 280; height: 80; style.fill: "#ffebee"
rs: "RS256\nasymmetric" { width: 170; height: 70; style.fill: "#e8f5e9"
pv: "Private key\nissuer only" { width: 220; height: 80; style.fill: "#e8f5e9"
pb: "Public key via JWKS\nvalidators verify only" { width: 280; height: 80; style.fill: "#fff3e0" */
hs -> sh
rs -> pv
rs -> pb
```

**Fig. 1.** The security boundary difference: with HS256 a leaked validator secret mints tokens; with RS256 a validator compromise cannot sign anything.

## Practical selection

- **Single service, issuer == verifier**: HS256 is legitimate - one config value, no key distribution.
- **Microservices, third-party resource servers, public JWKS**: RS256 (or PS256/ES256) - the resource servers verify against the authorization server's published keys ([[What is opaque token introspection in Spring Security]] shows the no-crypto alternative).
- **Key rotation**: RS256 supports it gracefully via `kid` in the header; rotating an HS256 secret invalidates every deployed copy at once.

## The pitfall that forces explicit configuration

RFC 8725's attack class: a validator that picks the algorithm from the token's own header can be tricked - the classic variant downgrades to `alg: none`; the "key confusion" variant feeds the RS256 *public key* (which the attacker can download) as the HS256 secret, and the same validator library then happily HMACs with it. The defense is to pin the expected algorithm per verifier and never read `alg` as an instruction.

```java
NimbusJwtDecoder decoder = NimbusJwtDecoder.withPublicKey(rsaKey).build();   // RS256 pinned
NimbusJwtDecoder sym = NimbusJwtDecoder.withSecretKey(secret).build();       // HS256 pinned
```

**Listing 2.** Spring's `NimbusJwtDecoder` builders each fix exactly one algorithm - which is the right shape for the RFC 8725 rule ([[What is NimbusJwtDecoder]]).

> [!warning] "HS256 with a strong password is just as safe"
> The comparison misses the trust model, not the key length: with HS256 every verifier can *create* valid tokens, so the secret must live in every service and every deployment. The question is not entropy - it is how many components hold minting power ([[What is the principle of least privilege]]).

> [!tip] Interview answer
> HS256 is HMAC-SHA256 with a shared secret; RS256 is RSA signing with private-mint, public-verify. One service that verifies its own tokens can use HS256; anything multi-service wants RS256 plus JWKS so validators hold no minting power. Either way, pin the algorithm at the verifier - RFC 8725's key-confusion attack lives exactly in validators that trust the token's own alg header.
