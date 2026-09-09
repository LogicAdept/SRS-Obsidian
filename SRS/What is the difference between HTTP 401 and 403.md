<!--
reps: 0
priority: 0
-->
#Java/Web #SRS

# What is the difference between HTTP 401 and 403

> [!abstract] Short answer
> **401 Unauthorized means the request was not authenticated — the server does not know who you are (missing, expired, or invalid credentials) and includes a `WWW-Authenticate` challenge. 403 Forbidden means authentication succeeded but the identified client lacks rights for this resource — the request should not be repeated with the same credentials.** Identity problem versus permission problem.

## What each code promises

The HTTP semantics (RFC 9110 §15.5.1/15.5.2) separate the two stages of access control. 401 is the "prove who you are" gate: the server, per spec, MUST generate a `WWW-Authenticate` header field describing the accepted scheme — that is what drives browser Basic-auth popups and token refresh flows. 403 is post-authentication: the identity is known, the server understands the request, and refuses to authorize it — and per spec, retrying with the same credentials will not help; the response may carry a body explaining why (or may deliberately hide the reason).

```d2
direction: right
req: "Request arrives" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
a: "Valid credentials?\n(token, session, cert)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
u401: "401 Unauthorized\nno / bad identity\n+ WWW-Authenticate header" {
  width: 330
  height: 100
  style.fill: "#ffebee"
}
z: "Rights for THIS resource?" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
f403: "403 Forbidden\nidentity known,\npermission missing" {
  width: 310
  height: 100
  style.fill: "#ffebee"
}
ok: "200 process the request" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
req -> a
a -> u401: "no"
a -> z: "yes"
z -> f403: "no"
z -> ok: "yes"
```

**Fig. 1.** Two gates in sequence: authentication (401 on failure), then authorization (403 on failure) — the mapping to the conceptual split is in [[What is authorization and authentication how they differ]].

Concrete cases: a request with no `Authorization` header against a JWT-secured API → 401 (with `WWW-Authenticate: Bearer`); an expired token → 401 (client should refresh/re-login); a valid token for a user who is not an admin calling `DELETE /users/42` → 403; a valid token deleting *someone else's* order → 403 (an IDOR-style check failing).

> [!warning] 401's name lies — and leaking 403 is an information disclosure
> Three classic mistakes. First, taking "Unauthorized" literally: 401 is about *unauthenticated* — the name is historical (an early draft wanted "Unauthorized" to mean "not authenticated"); quoting "401 means no permissions" in an interview fails the question. Second, returning 403 to unauthenticated callers on *sensitive* endpoints: a 403 reveals the resource exists and your identity was fine — security-conscious APIs return 404 instead to avoid enumerating protected resources; others deliberately return 403 to hide whether a login would help (per spec, 403 may also be returned to anonymous callers when revealing the auth requirement itself is unwanted). Third, sending 401 without `WWW-Authenticate` — the spec requires it; frameworks usually add it (Spring Security's entry point writes the challenge), hand-rolled filters forget it, and the client's refresh flow breaks. For the Java/Spring wiring of both codes — filters, entry points, `@PreAuthorize` — see [[How do you configure HTTP Basic authentication in Spring Security]] and [[How do you implement JWT authentication in Spring Security]]; session-level pitfall: [[How do you handle session fixation in Spring Security]].

> [!tip] Interview answer
> **401 is about identity: not authenticated — no token, expired or invalid credentials — and the response carries WWW-Authenticate describing how to authenticate. 403 is about permissions: we know who you are, you may not touch this resource, and repeating with the same credentials will not help. A quick mnemonic: 401 — who are you; 403 — I know you, but no. And 403 on existence-sensitive endpoints is often swapped for 404 to avoid leaking that the resource exists.**

