<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/JWT #Security/OAuth2 #SRS

# How do you debug a silent 401 from an OAuth2 resource server?

> [!abstract] Short answer
> The **body is empty on purpose**. Read **`WWW-Authenticate`** (RFC 6750 `error` / `error_description`) and turn **Spring Security TRACE/DEBUG** on — that is where expiry, issuer, signature, and missing-token cases show up. A missing Bearer token is **`WWW-Authenticate: Bearer`** with **no** `error`. A bad JWT is typically **`invalid_token`** plus a description. An unreachable JWK set is usually a **500**, not a 401.

## Why the HTTP body looks empty

Spring Security **does not put the rejection reason in the response body**. On an OAuth2 resource server, **`BearerTokenAuthenticationEntryPoint`** sets the status and a **`WWW-Authenticate`** header and **writes no body**. RFC 6750 puts developer detail in that header (`error`, optional `error_description`) and says a request **with no credentials** should **not** include an error code.

So a client that only prints JSON sees a “silent” 401. The header is the on-the-wire clue:

| What you sent | Typical status | Typical `WWW-Authenticate` |
| --- | --- | --- |
| No `Authorization: Bearer` | **401** | `Bearer` (no `error=`) |
| JWT failed decode/validation (`BadJwtException`) | **401** | `Bearer error="invalid_token", error_description="…"` |
| Missing CSRF on a session POST | **403** | none of the above — **`AccessDeniedHandler`** |
| JWK set unreachable / malformed JWK (`JwtException`, not `BadJwtException`) | **500** | entry point is **not** used |

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer error="invalid_token", error_description="An error occurred while attempting to decode the Jwt: Jwt expired at …"
```

**Listing 1.** Conceptual 401. **`BearerTokenAuthenticationEntryPoint`** copies **`OAuth2Error`** into the header. The example description is what **`JwtTimestampValidator`** produces after **`NimbusJwtDecoder`** wraps it.

## Path from header to 401

**`BearerTokenAuthenticationFilter`** resolves the Bearer token. If none is present it traces *Did not process request since did not find bearer token* and continues; later authorization fails and the entry point challenges. If a token is present, **`JwtAuthenticationProvider`** calls **`JwtDecoder.decode`**.

- **`BadJwtException`** (malformed token, unsigned `alg=none`, **`JwtValidationException`** for `exp` / `nbf` / `iss`) → **`InvalidBearerTokenException`** → **401**
- other **`JwtException`** (JWK fetch / malformed JWK set) → **`AuthenticationServiceException`**. The default **`AuthenticationEntryPointFailureHandler`** **rethrows** that, so you get a **500**, not a bearer challenge

Default JWT checks (Boot `issuer-uri` / `jwk-set-uri`): signature against the JWK set, **`iss`**, **`exp`**, **`nbf`**. Boot also has **`audiences`** for **`aud`**. Clock leeway is **60 seconds** on **`JwtTimestampValidator`**.

```d2
direction: down
filter: "BearerTokenAuthenticationFilter" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
provider: "JwtAuthenticationProvider\nJwtDecoder.decode" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
bad: "BadJwtException\nInvalidBearerTokenException" {
  width: 260
  height: 60
  style.fill: "#fce4ec"
}
svc: "JwtException\nAuthenticationServiceException" {
  width: 260
  height: 60
  style.fill: "#f3e5f5"
}
ep: "BearerTokenAuthenticationEntryPoint\n401 + WWW-Authenticate, empty body" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
err500: "Rethrow → 500" {
  width: 180
  height: 50
  style.fill: "#ffe0b2"
}

filter -> provider
provider -> bad
provider -> svc
bad -> ep
svc -> err500
```

**Fig. 1.** Invalid token is a **401 challenge**. A **broken JWK URI** is a **service failure**.

## Logs that actually name the cause

Official recipe: **`logging.level.org.springframework.security=TRACE`**. That covers the filter chain **and** `org.springframework.security.oauth2.*`. Restricting TRACE to `oauth2` alone misses **`FilterChainProxy`** / **`CsrfFilter`** lines.

| Logger | Level | What you see |
| --- | --- | --- |
| **`NimbusJwtDecoder`** | **TRACE** | *Failed to parse token*, *Failed to retrieve JWK set*, *Failed to process JWT*, *Failed to decode unsigned token* |
| **`JwtAuthenticationProvider`** | **DEBUG** | *Failed to authenticate since the JWT was invalid* |
| **`JwtTimestampValidator`** | **DEBUG** | *Jwt expired at …* / *Jwt used before …* |
| **`BearerTokenAuthenticationFilter`** | **TRACE** | *Failed to process authentication request* (includes the exception) |
| **`CsrfFilter`** | **DEBUG** | *Invalid CSRF token found …* then **403**, not 401 |

```properties
logging.level.org.springframework.security=TRACE
```

**Listing 2.** Boot property from the Architecture **Logging** section. Use it while reproducing the 401; turn it down afterward.

You can also listen for **`AuthenticationFailureBadCredentialsEvent`** when the failed **`Authentication`** is a **`BearerTokenAuthenticationToken`** — Resource Server publishes that for an **`InvalidBearerTokenException`**.

Confirm Boot actually built a JWT resource server: **`spring.security.oauth2.resourceserver.jwt.issuer-uri`** or **`jwk-set-uri`** (or your own **`JwtDecoder` `@Bean`**). No URI and no decoder means JWT resource-server auto-config never started. Need **`spring-security-oauth2-resource-server`** plus **`spring-security-oauth2-jose`** for JWT.

> [!warning] Empty body is not the same as no reason
> Look at **`WWW-Authenticate`** before the logs. **`error_description`** is for developers (RFC 6750), not an end-user JSON problem. A header with **no** `error` usually means **no Bearer token** was sent, not a bad signature. **CSRF** on POST is **403**. An **unreachable JWK set** is typically **500**. Browser calls can hide even a correct 401 if CORS is not processed before security — configure **`CorsConfigurationSource`** so preflight is not treated as anonymous ([[How do you configure CORS on HttpSecurity]], [[Why do you disable CSRF for a JWT REST API]]).

> [!warning] TRACE is a debug switch
> TRACE/DEBUG exist **because** the body is empty. The XML **`<debug/>`** infrastructure **must stay off outside development** — it can log headers and parameters. Leave package TRACE on only while you reproduce the 401. Widening **`JwtTimestampValidator`** clock skew past **60s** can hide a real **`exp`** bug; sync clocks first ([[What is JWT clock skew in Spring Security]], [[How do you configure Spring as an OAuth2 resource server]]).

Related: [[What is the difference between HTTP 401 and 403 in Spring Security]], [[Why should you not catch Exception when validating a JWT]], [[What is AuthenticationEntryPoint]].

> [!tip] Interview answer
> A resource-server 401 is silent in the body by design: BearerTokenAuthenticationEntryPoint only sets WWW-Authenticate. Read that header, then enable TRACE on org.springframework.security. You will see Jwt expired at, issuer failures, parse or JWK errors, or no bearer token at all. CSRF is a 403; a dead JWK URI is usually a 500 AuthenticationServiceException, not a 401.
