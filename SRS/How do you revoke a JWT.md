<!--
reps: 0
priority: 0
-->
#Security/JWT #SRS

# How do you revoke a JWT

> [!abstract] Short answer
> You cannot *fully* revoke a stateless JWT before its `exp` - that is the price of local verification - so real designs do one of four things: keep tokens **short-lived** and rotate the refresh token; maintain a **denylist** of `jti` values checked at validation (which reintroduces state); **rotate the signing key** to invalidate everything at once; or switch that session to an **opaque token** introspected at the issuer. Choose by how fast a stolen token must die.

## The four levers

```d2
direction: right
j: "JWT issued\nexp: 15 min" { width: 190; height: 70; style.fill: "#e3f2fd" */
s: "Short exp + refresh rotation" { width: 280; height: 70; style.fill: "#e8f5e9"
d: "Denylist jti at the verifier" { width: 280; height: 70; style.fill: "#fff3e0" */
k: "Rotate signing key / kid" { width: 270; height: 70; style.fill: "#fff3e0" */
o: "Opaque token + introspection" { width: 290; height: 70; style.fill: "#ffebee"
j -> s
j -> d
j -> k
j -> o
```

**Fig. 1.** Four revocation levers with increasing statefulness. The more you demand immediate global death of a token, the more you rebuild the session store JWT was meant to remove.

- **Short `exp` + rotation**: the access token dies by itself; logout revokes the refresh token server-side (authorization servers expose token revocation for exactly this - [[What is the difference between an access token and a refresh token]]). Rotation with reuse detection kills refresh tokens that leak.
- **Denylist**: store the `jti` of revoked tokens (logout, admin ban) until `exp` passes; the verifier consults it on every request. This is honest state - a cache with TTL = remaining token life, sized to session counts.
- **Key rotation**: changing the signing key invalidates *all* tokens - a blunt instrument for key compromise or mass logout; validators pick up the new key from the JWKS via `kid`.
- **Opaque + introspection**: the token is a random handle; the resource server asks the issuer "is this live?" per request (or per short cache window) - full revocability, full round trip ([[What is opaque token introspection in Spring Security]]).

> [!warning] "JWTs cannot be logged out"
> And the mirror lie: "logout works because we delete the token from localStorage". Deleting the client copy changes nothing - the token is still valid. Logout that must be immediate means server-side state: denylist, session version, or introspection. A logout that only clears the browser is wishful thinking ([[Where should you store a JWT in a browser]]).

> [!tip] Interview answer
> A stateless JWT is valid until exp - real revocation is a trade. I keep access tokens short and rotate refresh tokens; for instant kill I either check a jti denylist with TTL = token lifetime, rotate the key, or move that session to opaque introspection. Every option buys immediacy with state, so the design question is how fast a stolen token must actually die.
