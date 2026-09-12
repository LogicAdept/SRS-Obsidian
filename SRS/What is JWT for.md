<!--
reps: 0
priority: 0
-->
#Security/JWT #Security/Authentication #SRS

# What is JWT for

> [!abstract] Short answer
> A JWT is a compact, URL-safe way to carry **signed claims between two parties** (RFC 7519): the claims travel as a JSON object inside a JWS (or JWE) structure and every holder can verify integrity without a database lookup. In backends that means stateless bearer authentication, self-contained authorization data such as roles or scopes, and service-to-service tokens in OAuth2 flows.

## The jobs JWTs are actually good at

- **Stateless authentication**: the resource server verifies the signature and reads `sub`, `exp`, `aud` locally - no session store, no per-request user lookup. That is the property Spring's `JwtDecoder` pipeline is built on ([[What is JwtDecoder in Spring Security]]).
- **Authorization data in transit**: scopes/roles/authorities ride in the payload, so the resource server enforces policy without calling the issuer for every request.
- **Delegated access in OAuth2**: the authorization server issues the access token - often a JWT - whose audience (`aud`) names the resource server it may be presented to ([[What is OAuth 2.0]], [[What is the difference between an access token and a refresh token]]).
- **Cross-domain / cross-service identity**: the same signed token proves identity to several internal services as long as they share the issuer's key or JWKS.

```d2
direction: right
as: "Authorization Server\nissues signed JWT" { width: 250; height: 80; style.fill: "#e3f2fd" }
c: "Client\nholds token" { width: 170; height: 70; style.fill: "#fff3e0" }
rs: "Resource Server\nverifies signature locally" { width: 280; height: 80; style.fill: "#e8f5e9" }
db: "No session store\nneeded per request" { width: 220; height: 70; style.fill: "#ffebee"
as -> c -> rs
rs -x db
```

**Fig. 1.** The value proposition: verification is local computation, not a shared session store. The same property is what makes revocation hard ([[How do you revoke a JWT]]).

## What a JWT is *not* for

- **Confidential data**: the payload is readable by design; JWE exists but is rare in web auth ([[How many parts does a JWT have]]).
- **Long-lived sessions**: a stateless token that lives for days is a standing credential; short `exp` plus refresh rotation is the workable shape.
- **Replacing the authentication protocol**: JWT is a *token format* - it does not define how the user proved anything. The user authentication may be form login, MFA, or OIDC; the JWT just carries the result.

> [!warning] "JWT == authentication"
> JWT is a claims container. An unsigned (`alg: none`) or wrong-audience token that happens to be well-formed proves nothing - validation (signature, issuer, audience, expiry) is the authentication, not the format. RFC 8725's best practices exist precisely because implementations skipped those checks ([[What is the difference between HS256 and RS256 in JWT]]).

> [!tip] Interview answer
> JWT is for carrying verified claims without a lookup: stateless resource-server auth, scopes inside the token, service-to-service bearer tokens. The trade is built in - self-contained means revocable only by rotation or denylist, and readable by anyone holding the string, so no secrets or PII in the payload unless you go JWE.
