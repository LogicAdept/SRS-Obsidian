<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus secure applications?

> [!abstract] Short answer
> Through layered extensions: **`quarkus-oidc`** for OpenID Connect — bearer-token (JWT/access token) protection of services and authorization-code flow for web apps, typically against Keycloak; **`quarkus-smallrye-jwt`** for verifying signed JWTs directly; **`quarkus-http` security policies** (`quarkus.http.auth.*`) for path-based rules; plus Basic auth and custom `IdentityProvider` implementations. Authorization is the standard annotation set — **`@RolesAllowed`**, `@Authenticated`, `@PermitAll`, `@DenyAll` — enforced through a `SecurityIdentity` injected into beans.

## Authentication mechanisms and the identity model

An incoming request is matched to an authentication mechanism (bearer token, code flow cookie, Basic) by configuration or the new per-endpoint mechanism annotations; the mechanism validates credentials against an identity provider — for OIDC, token signature, expiry and issuer/audience are checked against the provider's metadata, cached via local JWKS verification. The result is a `SecurityIdentity` with principals, roles (mapped from token claims such as `groups`/`realm_access.roles` via `quarkus.oidc.roles.role-claim-path`) and permissions. Authorization then happens at Jakarta REST level (`@RolesAllowed("admin")` on classes/methods), path level (`quarkus.http.auth.permission.*.paths=/api/*` + `policy=authenticated`), or programmatically (`SecurityIdentity.hasRole(...)`). A custom `IdentityProvider<T>` bean lets non-token credentials (API keys from headers, mTLS DNs) join the same model.

```java
// The verified app exposes /q/health with permit-all style management endpoints and this
// authorization shape (JDK 21, Quarkus 3.39.2). Shape of the service side:
//
// package org.acme;
//
// import jakarta.annotation.security.RolesAllowed;
// import jakarta.inject.Inject;
// import jakarta.ws.rs.GET;
// import jakarta.ws.rs.Path;
// import io.quarkus.security.identity.SecurityIdentity;
//
// @Path("/api")
// public class ApiResource {
//     @Inject SecurityIdentity identity;          // principals, roles, attributes
//
//     @GET @Path("/me")
//     public String me() { return identity.getPrincipal().getName(); }
//
//     @GET @Path("/admin")
//     @RolesAllowed("admin")                       // enforced from token roles
//     public String admin() { return "granted"; }
// }
// application.properties (bearer-token service):
//   quarkus.oidc.auth-server-url=https://idp.example.com/realms/demo
//   quarkus.oidc.client-id=backend-service
//   quarkus.http.auth.permission.public.paths=/q/health/*
//   quarkus.http.auth.permission.public.policy=permit
//   quarkus.http.auth.permission.api.paths=/api/*
//   quarkus.http.auth.permission.api.policy=authenticated
// (Conceptual listing: the OIDC provider side was not part of the no-Docker verified run;
//  the health/permission split below WAS exercised - /q/health/ready returned 200 UP.)
```

**Listing 1.** Marked `Conceptual` for the IdP stanza; the mechanism to narrate: bearer token validated by quarkus-oidc, roles surfaced on `SecurityIdentity`, `@RolesAllowed` and path policies enforcing.

```d2
direction: down
tok: "Request + token / credentials" {
  width: 260
  height: 50
}
mech: "Mechanism\nOIDC bearer | code flow | Basic | custom" {
  width: 340
  height: 60
  style.fill: "#e3f2fd"
}
idp: "IdentityProvider / OIDC provider\nsignature, expiry, issuer, claims" {
  width: 330
  height: 65
  style.fill: "#fff3e0"
}
sid: "SecurityIdentity\nprincipal, roles, permissions" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
authz: "Authorization\n@RolesAllowed | quarkus.http.auth.* | programmatic" {
  width: 380
  height: 60
}
tok -> mech -> idp -> sid -> authz
```

**Fig. 1.** One pipeline from credentials to enforcement: mechanisms produce identities, identities carry roles, annotations and path policies consume them ([[What fault tolerance annotations does Quarkus provide]] uses the same interceptor foundation).

## Dev-loop and operational notes

Dev Services provisions a Keycloak container in dev/test mode automatically when quarkus-oidc is present (Docker available), and dev mode prints the admin console link — the test story for secured endpoints uses test tokens or `OidcWiremock` test support. Token introspection vs local JWT verification is a documented trade-off (revocation freshness vs latency); the TLS registry secures both HTTP and OIDC client connections.

> [!warning] "It's secure because there's a token" — say who checks what
> Three frequent gaps: a path policy that never matches (typo'd prefix or wrong policy name) leaves endpoints with the default `permit` posture — verify with an unauthenticated curl; role claims that do not map (wrong `role-claim-path`) produce 403s that look like bugs but are claim-mapping bugs; and storing the IdP client secret in `application.properties` instead of a Secret/config source is a review blocker ([[How do you configure a Quarkus application]] — env vars and config sources exist exactly for this). Security annotations require the security extension to be active — adding `@RolesAllowed` with no security extension present does not fail the build, and that silence is the trap.

> [!tip] Interview answer
> Quarkus security is layered: quarkus-oidc handles OpenID Connect — bearer tokens for services, code flow for web apps, with Keycloak the typical provider and Dev Services provisioning it locally; smallrye-jwt verifies raw JWTs, and custom IdentityProviders bring any credential into the model. Everything resolves to a SecurityIdentity with roles mapped from claims, and enforcement is @RolesAllowed on endpoints or quarkus.http.auth path policies. My checklist: path policy actually matches, role claim path correct, secrets come from config sources.
