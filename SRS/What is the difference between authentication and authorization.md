<!--
reps: 0
priority: 0
-->
#Security/Authentication #Security/Authorization #SRS

# What is the difference between authentication and authorization

> [!abstract] Short answer
> Authentication establishes **who** the caller is - verifying credentials or tokens against an identity; authorization decides **what that identity may do** - evaluating permissions against a policy. They are separate decisions with separate failure codes (401 vs 403), separate lifecycles (a session vs per-request policy), and they run in order: you cannot evaluate permissions meaningfully before the subject is established.

## The two decisions in one request

```d2
direction: right
req: "Request\n(Authorization header)" { width: 220; height: 70; style.fill: "#e3f2fd" }
authn: "Authentication\nverify identity/token" { width: 260; height: 80; style.fill: "#fff3e0" }
unauth: "401\nunknown or bad identity" { width: 200; height: 70; style.fill: "#ffebee" }
authz: "Authorization\npolicy on subject + resource" { width: 280; height: 80; style.fill: "#e8f5e9"
forbid: "403\nidentity OK, no permission" { width: 220; height: 70; style.fill: "#ffebee" }
res: "Resource" { width: 150; height: 60; style.fill: "#e8f5e9" }
req -> authn
authn -> unauth: "fails"
authn -> authz: "principal established"
authz -> forbid: "denied"
authz -> res: "granted"
```

**Fig. 1.** Two sequential gates. 401 answers "who are you, prove it"; 403 answers "I know you, and you still cannot".

What differs in practice:

- **Verification material**: authentication consumes credentials, sessions, or tokens ([[What is multi-factor authentication]]); authorization consumes rules - roles, scopes, attributes, or relationships ([[What is the difference between RBAC and ABAC]]).
- **State and lifetime**: authentication is often established once and cached in a session or token; authorization is evaluated per request and can change mid-session (role revoked -> next request denied).
- **Ownership of the decision**: authentication may be delegated to an identity provider (OIDC); authorization typically stays with the application because it owns the resources.
- **In Spring Security** the split maps to `AuthenticationManager`/`AuthenticationProvider` versus `AuthorizationManager` / method-security expressions like `@PreAuthorize` ([[What is hasPermission in Spring Security method expressions]]).

```java
Authentication auth = authenticationManager.authenticate(token); // who
if (!authz.check(() -> auth, request).isGranted()) throw new AccessDeniedException("no"); // what
```

**Listing 1.** The conceptual two-step: establish the principal, then evaluate the policy for this resource.

> [!warning] The 401 vs 403 trap
> HTTP 401 is named "Unauthorized" but semantically means **unauthenticated** - the server does not know or does not believe the identity; 403 means authenticated-but-forbidden. Swapping them leaks policy state (a 403 tells an anonymous prober the resource exists), and "401 when permissions are wrong" is the most common production inversion ([[How do you secure a REST API]]).

OAuth2 bundles both sides: the identity provider authenticates the user, and the access token carries the *authorization* - scopes - that the resource server enforces ([[What is OAuth 2.0]]).

> [!tip] Interview answer
> Authentication proves identity - credentials, tokens, MFA - and produces a principal; authorization evaluates that principal against policy for the specific resource and action. They fail with different codes (401 vs 403), have different lifecycles, and different owners - an IdP can authenticate, but authorization stays in the service that owns the data.
