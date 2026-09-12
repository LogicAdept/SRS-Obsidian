<!--
reps: 0
priority: 0
-->
#Security/Keycloak #SRS

# What is Keycloak

> [!abstract] Short answer
> Keycloak is an open-source **identity and access management (IAM) server** from Red Hat/CNCF: it hosts login pages, user stores, and token issuance behind standard protocols - OpenID Connect, OAuth 2.0, and SAML 2.0 - so applications "add authentication with minimum effort" and stop storing or verifying credentials themselves. You federate or manage users in Keycloak, register clients, and your services consume issued tokens ([[What is OAuth 2.0]], [[How would you explain OAuth OpenID Connect]]).

## What it actually provides

- **Standards first**: OIDC for authentication on top of OAuth2, SAML 2.0 for legacy enterprise SSO; any conformant library can talk to it - no proprietary SDK required.
- **SSO across applications**: one realm, many clients; a login at one app carries to the others via the identity-provider session.
- **User federation and brokering**: users can live in LDAP/Active Directory or come from social/external IdPs; Keycloak proxies and maps identities instead of duplicating them.
- **Authn machinery**: password policy, OTP, WebAuthn, MFA policy per realm/client ([[What is multi-factor authentication]]), brute-force detection, required actions.
- **Authorization services** (optional): resource/permission management and central policy decision points beyond plain role checks.

```d2
direction: right
u: "User" { width: 120; height: 60; style.fill: "#e3f2fd" */
kc: "Keycloak\nrealm: users, clients, policies" { width: 300; height: 90; style.fill: "#e8f5e9"
apps: "Your apps\n(client registration)" { width: 230; height: 80; style.fill: "#fff3e0" */
tok: "OIDC tokens\n(JWT access/ID tokens)" { width: 230; height: 80; style.fill: "#fff3e0" */
u -> kc
apps -> kc
kc -> tok -> apps
```

**Fig. 1.** Keycloak sits beside the applications: they redirect users to it for authentication and accept the tokens it issues ([[What is the difference between HS256 and RS256 in JWT]] - the JWKS those tokens are verified against is Keycloak's).

## The realm model

A realm owns users, clients, roles, and policies - realm boundaries are hard (no cross-realm user sharing). Typical layout: one realm per environment or per security domain; a master realm administers the admin users of the others.

> [!warning] "Keycloak replaces my user database"
> It replaces the *authentication* part - credentials, sessions, tokens - not your domain data. Orders, profiles, and application-owned state stay in your services; you map Keycloak identities to your own records. Treating Keycloak as the app database, or stuffing authorization rules that belong to a domain service into realm policy, couples the identity plane to the business plane for no gain ([[What is the difference between authentication and authorization]]).

> [!tip] Interview answer
> Keycloak is a standard-protocol IAM server: OIDC/OAuth2/SAML, SSO per realm, LDAP or social federation, OTP/WebAuthn MFA, brute-force protection. Your apps become OAuth clients that verify its tokens against its JWKS instead of owning login pages and password storage - the integration with Spring Security is exactly that client setup ([[How do you integrate Keycloak with Spring Security]]).
