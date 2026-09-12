<!--
reps: 0
priority: 0
-->
#Security/JWT #SRS

# How many parts does a JWT have

> [!abstract] Short answer
> A signed JWT (a JWS-secured JWT, the kind used for authentication) has **three** dot-separated Base64url segments: the JOSE header, the payload (the JWT Claims Set), and the signature. An encrypted JWT (JWE) instead has **five** segments - the extra two cover the encrypted-key and authentication-tag machinery.

## The three segments of a JWS JWT

```d2
direction: right
h: "Header (JOSE)\nalg, typ, kid" { width: 220; height: 80; style.fill: "#e3f2fd" }
p: "Payload\nJWT Claims Set\niss, sub, aud, exp..." { width: 250; height: 90; style.fill: "#fff3e0" }
s: "Signature\nover base64url(header) + \".\" + base64url(payload)" { width: 320; height: 90; style.fill: "#e8f5e9" }
h -> p -> s
```

**Fig. 1.** The three parts are concatenated with dots into one compact, URL-safe string; the first two are readable by anyone, the third is verifiable only with the key.

- **Header** - a JSON object naming the algorithm (`alg`: HS256, RS256...), typically `typ: JWT`, and optionally `kid` to select the verification key.
- **Payload** - the JWT Claims Set: registered claims `iss` (issuer), `sub` (subject), `aud` (audience), `exp` (expiration), `nbf` (not before), `iat` (issued at), `jti` (JWT ID) plus private and public claims. Registered names are reserved by the JWT RFC and interpreted uniformly.
- **Signature** - computed over the base64url form of the first two parts; HS256 signs with a shared secret ([[What is HMAC]]), RS256 with a private key ([[What is RSA]]).

```java
String[] parts = jwt.split("\\.");
String claimsJson = new String(Base64.getUrlDecoder().decode(parts[1]), UTF_8);
```

**Listing 1.** Decoding the payload takes one line and no key - the claims are **encoded, not encrypted**.

## The five-part JWE case

When confidentiality is required, the JWT becomes a JWE: header, encrypted key, initialization vector, ciphertext, authentication tag - five segments. Resource servers almost always receive the three-part signed form; five-part tokens show up when the claims themselves must be secret.

One more count that surprises people: the **signature covers the encoded header and payload**, not the JSON itself - change one Base64url character and the signature check fails. That is why tokens are transmitted and stored byte-exact, and why a server that "re-serializes" a token before verifying it is doing something suspicious.

> [!warning] "The payload is secure because it is signed"
> A signature gives integrity, not confidentiality. Base64url decodes with no key, so tokens in URLs, logs, or browser storage expose every claim - including anything PII you put there. Encryption requires JWE ([[What is JWT for]], [[Where should you store a JWT in a browser]]).

> [!tip] Interview answer
> Three parts for the everyday signed JWT - header, claims, signature - Base64url-joined with dots, with registered claims like iss, sub, aud, and exp carrying the semantics. Five parts means JWE encryption. And I always flag that the first two parts decode without any key: encoding is not encryption.
