<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #SRS

# Why should you not catch Exception when validating a JWT?

> [!abstract] Short answer
> A blanket **`catch (Exception)`** that returns **`false`** (or a generic 401) **collapses every failure into one outcome** — expired token, bad signature, malformed token, and **misconfiguration** (wrong key, broken JWKS URL) all look the same. You lose the typed error Spring Security / JJWT already exposes, so monitoring, client hints, and incident response suffer.

## Different failures need different meaning

JWT validation is not a single boolean test. Typical failure modes include:

- **Expired** (`exp`) — normal client lifecycle; often handled with refresh
- **Malformed / unsupported** token — client bug or garbage input
- **Invalid signature** — wrong key, tampering, or algorithm mismatch
- **Claim validation** (`iss`, `nbf`, audience) — policy rejection

Treating all of these as **`false`** hides which case occurred and makes production debugging painful.

## Spring Security resource server path

In Spring Security, **`JwtAuthenticationProvider`** uses a **`JwtDecoder`** to decode, verify, and validate a JWT. Failures surface as **`JwtException`** — for example **`BadJwtException`** (“invalid in some way”) or **`JwtValidationException`**, which carries a collection of **`OAuth2Error`** objects with specific descriptions (timestamp / claim failures).

Default validation includes **`iss`**, **`exp`**, and **`nbf`** via **`JwtTimestampValidator`**. Let the decoder throw (or map **`JwtException`** types explicitly) instead of wrapping everything:

```java
try {
    Jwt jwt = jwtDecoder.decode(token);
    return jwt;
} catch (JwtValidationException ex) {
    // log ex.getErrors() — distinct OAuth2Error reasons
    throw ex;
} catch (BadJwtException ex) {
    // signature / parse failure — different ops signal than expiry
    throw ex;
}
```

**Listing 1.** Conceptual manual decode — handle **`JwtException`** subtypes, not **`Exception`**.

Prefer configuring **`oauth2ResourceServer().jwt()`** and a **`JwtDecoder` `@Bean`** so the filter chain performs this consistently. See [[How do you implement JWT authentication in Spring Security]].

## Manual parser libraries (JJWT)

Custom filters that call **`Jwts.parser()…parseClaimsJws(...)`** (JJWT) throw **typed `JwtException` subclasses** such as **`ExpiredJwtException`**, **`MalformedJwtException`**, and **`UnsupportedJwtException`** — not a generic failure bit. **`catch (Exception)`** also swallows unrelated bugs ( **`NullPointerException`**, wrong **`ClassLoader`**, I/O from key loading).

```d2
direction: right
bad: "catch (Exception)\nreturn false" {
  width: 220
  height: 70
  style.fill: "#fce4ec"
}
exp: "Expired\n(refresh path)" {
  width: 140
  height: 60
  style.fill: "#fff3e0"
}
sig: "Bad signature\n(tamper / key)" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
cfg: "Config / parse error\n(ops alert)" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}

bad -> exp: "same outcome"
bad -> sig: "same outcome"
bad -> cfg: "same outcome"
```

**Fig. 1.** Broad catch erases failure taxonomy operators rely on.

> [!warning] `false` hides configuration bugs too
> A wrong **`issuer-uri`**, unreachable JWKS endpoint, or mismatched signing key can fail validation the same way as a bad client token if you only return **`false`**. Logs and metrics need the **specific `JwtException` / `OAuth2Error`**, not a silent boolean. Expired tokens deserve different client handling than suspected tampering.

> [!tip] Interview answer
> JWT validation fails for many distinct reasons — expiry, malformed token, bad signature, claim mismatch, or bad server config. Catching Exception and returning false merges them all, so you cannot log, meter, or respond correctly. Catch JwtException subtypes (Spring Security or JJWT) or let the resource-server filter chain handle failures.
