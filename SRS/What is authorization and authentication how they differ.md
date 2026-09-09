<!--
reps: 0
priority: 0
-->
#Java/Security #SRS

# What is authorization and authentication how they differ

> [!abstract] Short answer
> **Authentication answers "who are you?" — verifying an identity (password, token, certificate). Authorization answers "what may you do?" — checking rights for that identity against a resource.** AuthN comes first and establishes the principal; authZ runs on every request afterward against roles/permissions. They fail differently too: 401 versus 403.

## The two checks, in order

Authentication validates credentials and produces a principal (user, service, device) — in Java/Spring terms, an `Authentication` object on the security context. Authorization consults that identity for each protected operation: role checks (`hasRole`), permission checks, or policy engines. One authentication can be reused for many authorizations; a token check happens once, then every endpoint asks "may this principal act here?"

```d2
direction: right
cred: "Credentials\npassword, JWT, mTLS cert" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
a1: "Authentication\nverify identity -> principal" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
ctx: "Security context\nwho the caller is" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
a2: "Authorization\nrole / permission / policy check" {
  width: 310
  height: 90
  style.fill: "#e8f5e9"
}
ok: "Allow: perform operation" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
cred -> a1 -> ctx -> a2 -> ok
```

**Fig. 1.** Authentication produces the principal; authorization consumes it on every protected operation.

The HTTP error codes encode the distinction: **401 Unauthorized** means "who are you?" failed or was never answered — retry with valid credentials; **403 Forbidden** means the identity is known but lacks rights — retrying differently will not help. The two questions also have different lifecycles: authentication is usually paid once per session/token lifetime (login, JWT signature validation, mTLS handshake), authorization is evaluated per operation and can change without re-login (a role revoked applies on the next check).

> [!warning] "Authenticated" does not mean "allowed" — and the confusion has security consequences
> The interview trap: assuming a logged-in user is authorized for everything. Real consequences: IDOR vulnerabilities exist precisely where authentication succeeded but per-object authorization was never checked — user A reads user B's resource because the code only asked "is this a valid user?". Second trap: conflating the layers in configuration — mixing up 401/403 semantics leaks information (a 403 on an existing resource tells an unauthenticated caller it exists; that is why some APIs answer 401/404 defensively). Third, forgetting that authZ needs its own model: roles, scopes (OAuth2), ACLs, or ABAC policies — "who" without a rights model gives nothing to check. In Spring Security the split is explicit: authentication filters populate the context, `@PreAuthorize`/`hasRole` enforce — see [[How do you configure HTTP Basic authentication in Spring Security]] and [[How do you implement JWT authentication in Spring Security]] for the identity half and [[How do you handle session fixation in Spring Security]] for a login-time pitfall.

> [!tip] Interview answer
> **Authentication verifies who the caller is — password, JWT, certificate — and yields a principal. Authorization checks what that principal may do — roles, scopes, ACLs — and runs per operation. Status codes encode it: 401 is an identity problem, 403 is a rights problem. They differ in lifecycle too: authenticate once per session, authorize every request — and authenticated does not imply authorized, which is exactly how IDOR bugs happen.**

