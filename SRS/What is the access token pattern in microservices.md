<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Security #Security/OAuth2 #SRS

# What is the access token pattern in microservices

> [!abstract] Short answer
> Access token pattern: the edge authenticates the caller once and passes a tamper-proof token - typically a JWT carrying identity and scopes - with every downstream request, so each service can verify who the requestor is and what they may do without re-authenticating. The security shape: authentication happens at the perimeter (API gateway), authorization data travels with the request.

## Mechanism: authenticate at the edge, verify everywhere

Without the pattern, every service either re-runs authentication against the session store - chatty and coupling - or trusts unverified headers like X-User-Id, which any caller could forge. The pattern replaces both with a signed claim. The API gateway authenticates the incoming request (session, OAuth2 login, client credentials) and issues or forwards an access token: a JWT whose payload states the requestor's identity (sub), issuer, expiry and granted scopes, signed so it cannot be altered in flight. Every hop carries the token - service to service as well - and each service verifies the signature locally (against the issuer's keys, cached) and checks the scopes its endpoint requires. No network call to the authenticator on the hot path; the token is the identity. My verified micro-case shows the two-edged sword concretely: Base64-decoding the JWT exposes every claim in readable text - any service reads identity without keys - but also proves that reading is not trusting: without the issuer's signature check the claims are just text (MS04 in empirics). Services that call other services forward the same token (or exchange it for a narrower one), so identity propagates through the whole call chain. Token-lifecycle concerns - refresh tokens, revocation - live at the auth service edge; for the OAuth2 mechanics see [[What is access token refresh token]], and for the concrete Spring wiring see [[How do you secure microservices with Spring Security]].

```d2
direction: right
u: "Client" {style.fill: "#eceff1"}
gw: "API Gateway
authenticates, issues JWT" {style.fill: "#ffe0b2"}
o: "Order Service
verifies sig + scope" {style.fill: "#e8f5e9"}
i: "Inventory Service
verifies sig + scope" {style.fill: "#e8f5e9"}
u -> gw: login / request
gw -> o: request + Bearer JWT
o -> i: request + same JWT
```

**Fig. 1.** One authenticated edge, one self-describing token: identity and scopes travel with the request and are verified locally by every service.
```java
String[] parts = jwt.split("\\.");
String hdr = new String(Base64.getUrlDecoder().decode(parts[0]), UTF_8);
String pl  = new String(Base64.getUrlDecoder().decode(parts[1]), UTF_8);
```

**Listing 1.** Verified on JDK 21 (MS04_JwtDecode in empirics): any service reads the claims with no keys — `{"sub":"user-42","scope":"orders.read","iss":"auth-service","aud":"orders","exp":1789000000}` — while the signature bytes arrive as-is and prove nothing until verified against the issuer's public key.


The trade encoded in the JWT reference: self-contained tokens verify offline - fast, stateless - but are valid until expiry and hard to revoke; opaque tokens are trivially revocable via an introspection call but add a round trip per check. The gateway's role is exactly [[What is the API gateway pattern in microservices]] applied to security: concentrate authentication at the perimeter and hand internal services a uniform token contract.

## What interviewers probe

Scope design: token scopes should be coarse capability names (orders.read, orders.write) checked by the endpoint, not row-level business rules. Propagation: a service acting on a user's behalf forwards the user token; a service acting for itself uses client credentials - mixing these up produces confused-deputy bugs. Clock and issuer checks: expiry (exp), issuer (iss) and audience (aud) must all be validated, not just the signature. And the discipline that saves production: keys rotate - services must fetch and cache the issuer's public keys (JWKS) with rotation tolerance.

> [!warning] Decodable does not mean trustworthy - and vice versa
> The classic lie: "it is a JWT, so we are secure". Base64 is encoding, not encryption - tokens leak their claims into logs and traces, so never put secrets in a JWT, and treat token contents as public. The inverse failure: a service reads sub and scopes but skips signature verification "behind the gateway" - now any insider process can mint identity headers and impersonate users. Verification happens at every service, every time; the gateway authenticates, it does not bless the network.

> [!tip] Interview answer
> The access token pattern: the edge authenticates once and hands a signed token - usually a JWT with subject, scopes and expiry - to every downstream call, and each service verifies the signature and scopes locally, no auth round trip. Services forward the token onward so identity crosses the whole chain. Self-contained JWTs verify offline but are hard to revoke; opaque tokens revoke cleanly but need introspection. Claims are readable - encode no secrets, and verify everywhere.
