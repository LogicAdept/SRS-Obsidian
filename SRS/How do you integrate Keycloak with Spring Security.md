<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/OIDC #Security/Keycloak #SRS

# How do you integrate Keycloak with Spring Security?

> [!abstract] Short answer
> Treat Keycloak as a generic **OpenID Provider**. Point Spring at the realm **issuer** (`/realms/{realm-name}`), then use **`oauth2Login()`** (browser session) and/or **`oauth2ResourceServer().jwt()`** (Bearer API). Do **not** add **`keycloak-spring-security-adapter`**: Keycloak **removed the Java adapters**. The app does not store user passwords.

## Keycloak is the issuer, Spring is the RP / RS

Keycloak’s OIDC discovery document is:

`/realms/{realm-name}/.well-known/openid-configuration`

Spring Boot’s **`issuer-uri`** is that realm base (host plus `/realms/myrealm`). Boot then GETs `{issuer-uri}/.well-known/openid-configuration` and fills authorization, token, JWK, and userinfo endpoints. Register a **confidential client** in the Keycloak admin console; put its **client id / secret** in Spring — not a Keycloak-specific starter.

**Browser app** — `spring-boot-starter-oauth2-client` (Boot 4: `spring-boot-starter-security-oauth2-client`) plus **`http.oauth2Login()`**:

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            client-id: my-app
            client-secret: "…"
            authorization-grant-type: authorization_code
            scope: openid,profile
        provider:
          keycloak:
            issuer-uri: "{issuer}/realms/myrealm"
```

**Listing 1.** Same `ClientRegistration` pattern as any OIDC provider. Redirect URI must match `{baseUrl}/login/oauth2/code/{registrationId}` unless you change the redirection endpoint.

**API** — `spring-boot-starter-oauth2-resource-server` plus **`http.oauth2ResourceServer((rs) -> rs.jwt(Customizer.withDefaults()))`**:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: "{issuer}/realms/myrealm"
```

**Listing 2.** Resource Server discovers the JWK set, then validates **`iss` / `exp` / `nbf`**. Supply **`jwk-set-uri`** as well if the app must start without pinging Keycloak (`/realms/{realm}/protocol/openid-connect/certs`).

```d2
direction: down
kc: "Keycloak realm\nOIDC issuer" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
login: "oauth2Login()\nsession" {
  width: 180
  height: 50
  style.fill: "#c8e6c9"
}
api: "oauth2ResourceServer().jwt()\nBearer" {
  width: 220
  height: 50
  style.fill: "#c8e6c9"
}

kc -> login
kc -> api
```

**Fig. 1.** Login is an **OAuth2 client**. An API that only checks JWTs is a **resource server**. Mixing both needs an explicit **`SecurityFilterChain`**. Keycloak is neither ([[How do you implement OAuth2 login in Spring Security]], [[What is the difference between an OAuth2 client and a resource server]], [[How do you configure Spring as an OAuth2 resource server]], [[How do you register a custom OAuth2 identity provider]]).

Default JWT authorities are **`scope` / `scp`** with a **`SCOPE_`** prefix. Keycloak also puts roles on **`AccessToken`** as **`realmAccess` / `resourceAccess`** (JSON `realm_access` / `resource_access`). **`hasRole("ADMIN")` from adapter-era dumps will not match `SCOPE_openid`**. Use **`JwtAuthenticationConverter` / `JwtGrantedAuthoritiesConverter`** (custom claim name or a converter that reads those objects).

The old dump — **`@KeycloakConfiguration`**, **`KeycloakWebSecurityConfigurerAdapter`**, **`keycloakAuthenticationProvider()`**, **`RegisterSessionAuthenticationStrategy`** — is the **deprecated Spring Security adapter**. Keycloak 25 docs: **Java adapters were removed**. Keycloak’s own guidance is Spring Security OAuth2/OIDC.

> [!warning] The adapter is not the interview answer
> **`KeycloakWebSecurityConfigurerAdapter`** is gone with the Java adapters. Boot 3 / Security 6 expect **`oauth2Login`** and/or **`oauth2ResourceServer`** plus **`issuer-uri`**. A `keycloak-spring-boot-starter` on the classpath is the same dead path.

> [!warning] Issuer must be the realm, and roles are not `SCOPE_`
> **`issuer-uri` must equal the token `iss`**, including `/realms/{name}` (older installs also had an `/auth` context path). Discovery fails if you point at the Keycloak host with no realm. **`hasRole`** does not see realm roles until you map them; the default converter only reads **`scope`/`scp`**.

> [!tip] Interview answer
> Integrate Keycloak as any OIDC provider: issuer-uri on the realm, then oauth2Login for a browser app or oauth2ResourceServer JWT for an API. Spring discovers /.well-known/openid-configuration; the app never stores passwords. The Keycloak Spring adapter and KeycloakWebSecurityConfigurerAdapter are removed — do not write that in Security 6. Map realm_access roles yourself if you need hasRole.
