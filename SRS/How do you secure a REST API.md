<!--
reps: 0
priority: 0
-->
#API/REST #Security #SRS

# How do you secure a REST API

> [!abstract] Short answer
> Layer the standard controls: TLS everywhere for confidentiality and integrity; stateless authentication with short-lived bearer tokens (OAuth2 for delegation, client-credentials for machine-to-machine); authorization per endpoint and per object (the object-level check is the one everyone forgets); input validation and rate limiting at the edge; and an inventory discipline for what is exposed. The OWASP API Security Top 10 is the checklist — BOLA is its number one.

## The transport and identity layers

TLS is non-negotiable and terminates where you control it (edge or service mesh); it is the cheapest control and the one whose absence poisons everything else. Authentication for REST APIs is overwhelmingly bearer-token: OAuth2 access tokens (JWT or opaque with introspection) carried in Authorization, validated per request — which is what makes stateless design work ([[Why is REST stateless]]; the grant mechanics live in the security subtree — [[What is the OAuth2 authorization code grant in Spring Security]] among them). Machine-to-machine traffic uses the client-credentials grant; user-facing delegation uses authorization code with PKCE. Long-lived static API keys survive for legacy integrations but must be rotatable, scoped, and never travel in URLs — URLs land in logs, referrers, and browser history. Authorization is two distinct checks per request: function-level (may this role call this endpoint at all) and object-level (does this principal own THIS object) — the second is BOLA, OWASP API1, and the classic breach when developers check the first only ([[What is CORS in Spring Boot]] and CSRF notes cover browser-boundary concerns; [[What is the difference between CORS and CSRF in Spring Security]] untangles the pair).

```d2
req: incoming request
tls: TLS termination
authn: authenticate token
(signature, expiry, scopes)
fn: function-level authz
(role vs endpoint)
obj: object-level authz
(principal vs resource owner)
val: validate input + quotas
biz: business logic
req -> tls -> authn -> fn -> obj -> val -> biz
obj: the OWASP API-1 check
(BOLA lives here)
```

**Fig. 1.** The per-request gate order: transport, identity, function-level rights, object-level rights, then validation and business logic.

## The rest of the checklist

Rate limiting and quotas protect availability ([[How do you design rate limiting for a REST API]]); strict input validation and output shaping protect correctness and confidentiality — responses must be projection-shaped, not raw entities, or fields leak (mass assignment and over-exposure are their own OWASP entries). Error responses must not leak internals ([[How do you design error responses in a REST API]]); logs must not carry tokens. Inventory management — knowing every deployed endpoint, version, and shadow API — is OWASP API9 and the reason API gateways keep route inventories; undocumented test endpoints are a standing breach vector. Webhook-style callbacks need signature verification on the receiving side ([[What are webhooks and how do you implement them reliably]]). Finally, security headers and CORS policy matter only for browser clients; pure machine-to-machine APIs should not pretend otherwise ([[What is the difference between CORS and CSRF in Spring Security]] if the surface includes browsers).

```text
GET /api/orders/42
  Authorization: Bearer eyJ...          -> 401 if missing/expired (who are you?)
  scope check: orders:read              -> 403 if role lacks it (function-level)
  owner check: order.customerId == principal
                                        -> 404/403 if not (object-level; BOLA)
  body: projected fields only           -> never the raw entity
```

**Listing 1.** The per-request gate: authentication, function-level authorization, object-level authorization, then projection (conceptual).

## The concepts behind the gates

Each gate maps to a dedicated card: the three-property frame for classifying what each control protects is [[What is the CIA triad]]; the who-may-do-what split is [[What is the difference between authentication and authorization]]; the catalogue that ranks the failure classes is [[What is the OWASP Top 10]]. Token lifecycle details live in [[How do you revoke a JWT]] and [[Where should you store a JWT in a browser]]; the permissions philosophy behind both authz checks is [[What is the principle of least privilege]]; and the layered-controls logic - edge filtering, detection, response - is [[What is defense in depth]].

> [!warning] Function-level authorization is not object-level authorization
> GET /api/orders/42 guarded by "must be a logged-in user" still hands out order 42 to any user. Every object-bearing endpoint needs the ownership-or-scope check on the specific object, and penetration testers find the missing ones in minutes.

> [!tip] Interview answer
> TLS everywhere, then stateless bearer-token auth — OAuth2, client-credentials for machines, short-lived tokens validated per request. Authorization is two checks: role versus endpoint, and principal versus object — object-level is where BOLA, OWASP's API number one, bites. I add edge rate limiting, strict input validation, projected responses that never echo entities, error responses without internals, and an endpoint inventory. Static keys, if they exist, are scoped, rotatable, and never in URLs.
