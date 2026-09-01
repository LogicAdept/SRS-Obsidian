<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/JWT #SRS

# How do you configure Spring as an OAuth2 resource server?

> [!abstract] Short answer
> Add **`spring-boot-starter-oauth2-resource-server`**, set **`spring.security.oauth2.resourceserver.jwt.issuer-uri`**, and enable **`http.oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()))`**. Boot builds a **`JwtDecoder`** (`JwtDecoders.fromIssuerLocation`) that checks **signature**, **`iss`**, and **`exp`/`nbf`** (60s skew). That is **inbound Bearer** validation — **not** **`oauth2Login()`**. Opaque tokens use **`opaqueToken()`** + **`opaquetoken.introspection-uri`**. Do **not** use **`@EnableResourceServer`**.

## JWT resource server (Boot)

The resource server **hosts** the API and **accepts** access tokens. Two Bearer modes: **JWT** (`JwtDecoder`) or **opaque** (`OpaqueTokenIntrospector`). JWT is the usual interview path.

`issuer-uri` must match a discovery document: `{issuer}/.well-known/openid-configuration`, `/.well-known/openid-configuration/{issuer}`, or `/.well-known/oauth-authorization-server/{issuer}`. Boot then loads the JWK set. If the AS has **no** metadata, set **`jwk-set-uri`** (and still **`issuer-uri`** so **`iss`** is checked without pinging at startup). **`audiences`** is **optional** — **`aud` is not validated by default**.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: "{issuer}"
```

**Listing 1.** Keycloak: `{issuer}` is the **realm** base (`…/realms/{realm}`), not a homemade filter ([[How do you integrate Keycloak with Spring Security]], [[What is JwtDecoder in Spring Security]]).

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize
			.anyRequest().authenticated())
		.oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()));
	return http.build();
}
```

**Listing 2.** Equivalent to Boot’s default JWT chain. Scopes become **`SCOPE_{name}`** (`hasAuthority("SCOPE_read")`). Without Boot, also publish **`JwtDecoder`**: `JwtDecoders.fromIssuerLocation("{issuer}")` ([[What is NimbusJwtDecoder]], [[What is opaque token introspection in Spring Security]]).

```d2
direction: down
api: "API Authorization: Bearer" {
  width: 240
  height: 36
  style.fill: "#e3f2fd"
}
filter: "BearerTokenAuthenticationFilter" {
  width: 260
  height: 36
  style.fill: "#fff3e0"
}
dec: "JwtDecoder\nsig / iss / exp" {
  width: 200
  height: 48
  style.fill: "#c8e6c9"
}

api -> filter
filter -> dec
```

**Fig. 1.** Failures are usually **401** with an empty body. Unreachable JWKS is often **500** ([[How do you debug a silent 401 from an OAuth2 resource server]], [[How do you secure microservices with Spring Security]]).

A **user-facing client** obtains the token (`oauth2Login` / SPA). The resource server does **not** run the code grant. Two chains if the same process also has form login ([[What is the difference between an OAuth2 client and a resource server]], [[Why do you disable CSRF for a JWT REST API]]).

> [!warning] This is not `oauth2Login` and not `@EnableResourceServer`
> **`issuer-uri` under `resourceserver`** never creates a Google/GitHub button. **`@EnableResourceServer`** / **`ResourceServerConfigurerAdapter`** are the old OAuth library. Current properties are **`spring.security.oauth2.resourceserver.*`**, not **`security.oauth2.resource.*`**.

> [!warning] JWT happy path is not the only mode
> Missing a **`JwtDecoder`** does **not** fall through to introspection. **`aud`** needs **`jwt.audiences`** (or a custom validator). Do **not** invent an IdP-specific servlet filter for Keycloak — point **`issuer-uri`** at the realm.

> [!tip] Interview answer
> A Spring resource server is spring-boot-starter-oauth2-resource-server plus issuer-uri and oauth2ResourceServer().jwt(). JwtDecoder verifies the Bearer JWT. That is not oauth2Login. Opaque tokens use introspection instead. Replace EnableResourceServer with the SecurityFilterChain DSL.
