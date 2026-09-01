<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/JWT #Security/OAuth2 #SRS

# What is `NimbusJwtDecoder`?

> [!abstract] Short answer
> The stock **`JwtDecoder`** (since **5.2**) that uses **Nimbus JOSE** (`JWTProcessor`) to **verify and parse** a compact JWT. Boot builds it from **`issuer-uri`** / **`jwk-set-uri`**. Signature is checked against a **JWK set**, **RSA public key**, or **HMAC `SecretKey`**. Default algorithm is **RS256**. Claim checks (`iss`, **`exp`/`nbf`** + 60s skew) are **`OAuth2TokenValidator`s**, not Nimbus itself. **`decode`** throws **`JwtException`**. It is **not** **`JwtAccessTokenConverter`**.

## Nimbus `JWTProcessor` behind `JwtDecoder`

Javadoc: “a low-level Nimbus implementation of `JwtDecoder` which takes a raw Nimbus configuration.” Builders:

| Factory | Keys from |
| --- | --- |
| **`withJwkSetUri(uri)`** | Remote JWK set |
| **`withIssuerLocation(issuer)`** (6.1) | OIDC discovery → JWK Set URI at **`build()`** |
| **`withPublicKey(RSAPublicKey)`** | Static RSA |
| **`withSecretKey(SecretKey)`** | MAC |
| **`withJwkSource(...)`** (7.0) | Nimbus **`JWKSource`** |
| **`new NimbusJwtDecoder(jwtProcessor)`** | Your **`JWTProcessor`** (e.g. algorithm from JWKS) |

**`JwtDecoders.fromIssuerLocation`** does discovery **and** installs default validators. **`withIssuerLocation(...).build()`** only derives the JWK URI — docs then call **`setJwtValidator(JwtValidators.createDefaultWithIssuer(...))`**.

```java
NimbusJwtDecoder decoder = NimbusJwtDecoder.withJwkSetUri(jwkSetUri).build();
decoder.setJwtValidator(JwtValidators.createDefaultWithIssuer(issuerUri));
Jwt jwt = decoder.decode(compactToken);
```

**Listing 1.** Signature via Nimbus; **`iss`/`exp`/`nbf`** via **`setJwtValidator`**. A **`JwtDecoder` `@Bean`** **replaces** Boot’s auto-config ([[What is JwtDecoder in Spring Security]], [[What is JWT clock skew in Spring Security]]).

Audience is **not** on by default; add an **`OAuth2TokenValidator`** / Boot **`audiences`**. Default trust is **RS256** (`jws-algorithms` / **`jwsAlgorithm(...)`**). **`RestOperations`** and **`Cache`** customize JWKS fetch.

```d2
direction: down
boot: "issuer-uri / jwk-set-uri" {
  width: 210
  height: 36
  style.fill: "#e3f2fd"
}
n: "NimbusJwtDecoder\nJWTProcessor + JWK" {
  width: 230
  height: 48
  style.fill: "#c8e6c9"
}
v: "OAuth2TokenValidator\niss, exp, nbf" {
  width: 210
  height: 48
  style.fill: "#fff3e0"
}
out: "Jwt or JwtException" {
  width: 190
  height: 36
  style.fill: "#c8e6c9"
}

boot -> n
n -> v
v -> out
```

**Fig. 1.** Nimbus verifies JOSE; Spring validators check claims. TRACE on **`NimbusJwtDecoder`**: *Failed to parse token*, *Failed to retrieve JWK set*, *Failed to process JWT*. Unreachable JWKS is often **500**; a bad signature is **401** ([[How do you debug a silent 401 from an OAuth2 resource server]], [[Why should you not catch Exception when validating a JWT]]).

This class **decodes**. Minting was **`JwtAccessTokenConverter`** / **`JwtEncoder`** ([[What is JwtAccessTokenConverter]]). WebFlux uses **`NimbusReactiveJwtDecoder`**.

> [!warning] Your `@Bean` replaces Boot’s decoder
> A broken **`NimbusJwtDecoder`** (wrong JWKS, **`setJwtValidator`** that drops **`JwtIssuerValidator`**, only **RS256** vs **ES256** tokens) looks like “Security is not validating JWTs”. Prefer **`JwtDecoders.fromIssuerLocation`** unless you need a builder knob.

> [!warning] Audience and `typ` are extra
> Default claim set is **`iss` + timestamps**, not **`aud`**. Nimbus **`typ`** check is **off** unless **`validateType(true)`**. Do not `catch (Exception)` around **`decode`**.

> [!tip] Interview answer
> NimbusJwtDecoder is Spring Security’s Nimbus-backed JwtDecoder: JWK set or static key, RS256 by default, JwtException on failure. Boot creates it from issuer-uri. Claim validation is setJwtValidator. It is not the old JwtAccessTokenConverter.
