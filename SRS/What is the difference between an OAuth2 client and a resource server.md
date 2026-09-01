<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/JWT #SRS

# What is the difference between an OAuth2 client and a resource server?

> [!abstract] Short answer
> RFC 6749: a **client** **obtains** an access token and **calls** APIs; a **resource server** **hosts** those APIs and **accepts** the token. In Spring Security the client is **`oauth2Login()`** and/or **`oauth2Client()`** (`spring-boot-starter-oauth2-client`). The resource server is **`oauth2ResourceServer()`** (`spring-boot-starter-oauth2-resource-server`). Login **delegates** the browser to the authorization server and often stores identity plus tokens. The API side typically uses **`jwt()`** (`JwtDecoder`) or **`opaqueToken()`**. Not **`@EnableOAuth2Sso`** / **`@EnableResourceServer`**.

## Two RFC roles, two Spring DSLs

| | Client | Resource server |
| --- | --- | --- |
| RFC 6749 §1.1 | App that requests protected resources **on the owner’s behalf** | Host that answers those requests **using access tokens** |
| Spring | **`HttpSecurity.oauth2Login()`** (browser login) and **`oauth2Client()`** (outbound Bearer) | **`HttpSecurity.oauth2ResourceServer()`** |
| Boot properties | `spring.security.oauth2.client.*` | `spring.security.oauth2.resourceserver.jwt.*` or `.opaquetoken.*` |
| Token direction | **Gets** tokens from the authorization server; **sends** `Authorization: Bearer` | **Validates** an **inbound** Bearer token on each request |

Spring’s OAuth2 overview: **OAuth2 Login is a client feature**, not a separate role. Typical layout: one user-facing client, several resource-server APIs, a third-party authorization server ([[What is OAuth 2.0]], [[How do you implement OAuth2 login in Spring Security]]).

```java
http.oauth2Login(Customizer.withDefaults());

http.oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()));
```

**Listing 1.** Left: client **login** (code grant, session). Right: resource server **JWT** path. Combine **`oauth2Login()`** with **`oauth2Client()`** when the same app also calls third-party APIs. JWT is **self-contained** (signature + claims, **`JwtDecoder`**). Opaque tokens use **`opaqueToken()`** and RFC 7662 introspection instead ([[What is JwtDecoder in Spring Security]], [[What is opaque token introspection in Spring Security]]).

```d2
direction: down
browser: "Browser / SPA" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
client: "OAuth2 client\noauth2Login / oauth2Client" {
  width: 260
  height: 50
  style.fill: "#c8e6c9"
}
as: "Authorization server" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
rs: "Resource server\noauth2ResourceServer" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

browser -> client: "login"
client -> as: "code / token grant"
as -> client: "access token (+ id_token)"
client -> rs: "Authorization: Bearer"
```

**Fig. 1.** The resource server does **not** run the redirect dance. One process may still be **both** roles (BFF / Gateway **TokenRelay**): login as client, then validate or forward Bearer downstream ([[How do you secure microservices with Spring Security]], [[How do you refresh an expired JWT in Spring Security]]).

> [!warning] Login is not the whole client role
> **`oauth2Login()`** is the dump’s “delegate login” story. **`oauth2Client()`** obtains tokens for **outbound** calls (`OAuth2AuthorizedClientManager`, including **client credentials**) **without** logging anyone in. Putting **`issuer-uri`** only under **`spring.security.oauth2.resourceserver`** never creates a Google/GitHub login.

> [!warning] `@EnableOAuth2Sso` / `@EnableResourceServer` are the old pairing
> Those annotations are **Spring Security OAuth / Boot OAuth2**, not Security 6. Current pair is **`oauth2Login()` + `oauth2ResourceServer()`**. JWT is the usual RS encoding in interviews; it is **not** the only one — missing a **`JwtDecoder`** does **not** fall through to introspection ([[What is EnableOAuth2Sso]], [[What is EnableResourceServer]]).

> [!tip] Interview answer
> Client gets tokens; resource server checks them. In Spring that is oauth2Login/oauth2Client versus oauth2ResourceServer. Login starts a session after the authorization server authenticates the user. The API validates Bearer JWT (or opaque introspection) per request. Do not answer with EnableOAuth2Sso and EnableResourceServer.
