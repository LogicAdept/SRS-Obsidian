<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Java/Spring/Cloud/Gateway #Security/OAuth2 #Security/JWT #SRS

# How do you secure microservices with Spring Security?

> [!abstract] Short answer
> Treat each API as an **OAuth2 resource server**: **`oauth2ResourceServer().jwt()`** (or opaque introspection) plus **`authorizeHttpRequests`**. A **user-facing client** (or **Spring Cloud Gateway** with **`oauth2Login()`** + **`TokenRelay`**) obtains the access token; **every** downstream service still **validates** the Bearer JWT with **`JwtDecoder`**. Do **not** use **`@EnableResourceServer`**.

## One client, many resource servers, one issuer

Spring Security’s OAuth2 overview describes a typical microservices layout: **one user-facing client**, **several backend resource servers**, and an **authorization server** (often a third party). Spring Security implements the **client** and **resource server** roles; it does not make the APIs share a session cookie.

Each service:

```java
@Bean
SecurityFilterChain apis(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests(auth -> auth
			.requestMatchers("/public/**").permitAll()
			.anyRequest().authenticated())
		.oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
	return http.build();
}
```

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: "{issuer}"
```

**Listing 1.** Security 5.2+ / Boot 3: **`SecurityFilterChain`** + **`JwtDecoder`** from **`issuer-uri`** (JWK discovery). Scopes become **`SCOPE_`** authorities, not `#oauth2.hasScope`. **`authorizeRequests()` / `antMatchers()`** are the old dump.

The edge can be **`oauth2Login()`** (browser) or a SPA that already holds a Bearer token. **Spring Cloud Gateway** forwards that access token with **`TokenRelay`**:

```yaml
spring:
  cloud:
    gateway:
      server:
        webflux:
          routes:
            - id: orders
              uri: "{orders-service}"
              predicates:
                - Path=/orders/**
              filters:
                - TokenRelay=
```

**Listing 2.** Omitting **`clientRegistrationId`** relays the logged-in user’s token. Needs **`spring.security.oauth2.client.*`**. Default authorized-client store is **in-memory** — not production. Downstream still runs Listing 1; the gateway is **not** a substitute for **`JwtDecoder`**.

```d2
direction: down
user: "Browser / SPA" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
edge: "Client or Gateway\noauth2Login + TokenRelay" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
rs: "Each microservice\noauth2ResourceServer JWT" {
  width: 250
  height: 50
  style.fill: "#c8e6c9"
}
as: "Authorization server" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}

user -> edge
edge -> rs
as -> edge: "access token"
rs -> as: "JWK / iss"
```

**Fig. 1.** Tokens are minted at the AS, **relayed** at the edge, **verified** on every resource server ([[What is the difference between an OAuth2 client and a resource server]], [[How do you configure Spring as an OAuth2 resource server]], [[How do you debug a silent 401 from an OAuth2 resource server]], [[What is Spring Cloud Gateway]]).

Service-to-service calls use **OAuth2 Client** (`OAuth2AuthorizedClientManager` + Bearer on **`RestClient`/`WebClient`**), not a copied `SecurityContext` across processes. JWT REST APIs typically drop CSRF ([[Why do you disable CSRF for a JWT REST API]]).

**`@EnableResourceServer`** / **`ResourceServerConfigurerAdapter`** belong to **Spring Security OAuth** (`spring-security-oauth`). That stack is **deprecated**; the migration guide maps them to **`oauth2ResourceServer`**. **`WebSecurityConfigurerAdapter`** is gone too — use a **`SecurityFilterChain` `@Bean`**. The architecture-level pattern behind the JwtDecoder wiring is [[What is the access token pattern in microservices]].

> [!tip] Interview answer
> Secure microservices as OAuth2 resource servers: each API validates the JWT (issuer-uri / JWK), while a client or Spring Cloud Gateway TokenRelay obtains and forwards the access token. That is oauth2ResourceServer().jwt() on SecurityFilterChain, not @EnableResourceServer. The authorization server is separate; Spring Security does not share HttpSession across services.
