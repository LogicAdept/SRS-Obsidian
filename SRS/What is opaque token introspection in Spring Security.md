<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #SRS

# What is opaque token introspection in Spring Security?

> [!abstract] Short answer
> The resource server **does not parse** the access token. It **POSTs** it to the authorization server’s **RFC 7662** introspection endpoint (form field **`token`**, typically with **client id/secret**). Success is JSON **`{ "active": true }`**. Spring’s SPI is **`OpaqueTokenIntrospector.introspect(String)`** → **`OAuth2AuthenticatedPrincipal`**. Boot: **`spring.security.oauth2.resourceserver.opaquetoken.introspection-uri`** plus credentials; DSL **`oauth2ResourceServer().opaqueToken()`**. Default implementation: **`SpringOpaqueTokenIntrospector`**. This is **not** **`JwtDecoder`**, and a missing JWT decoder does **not** fall through here.

## AS is the law, every Bearer request

RFC 7662: the **protected resource** asks whether a token is **active** (issued, not revoked, inside its time window). Inactive tokens get **`active: false`** and **no extra reason**. Spring maps **`active: true`** into authentication; scopes become **`SCOPE_…`** plus **`FACTOR_BEARER`**. Principal is **`OAuth2AuthenticatedPrincipal`** (`sub` → **`getName()`**). The **`Authentication`** type is **`BearerTokenAuthentication`**.

Need **`spring-security-oauth2-resource-server`** only (no jose jar). **`OpaqueTokenAuthenticationProvider`** calls the introspector. If you do not publish a custom introspector, Resource Server **falls back to `SpringOpaqueTokenIntrospector`** — that sentence is **opaque mode**, not “JWT failed so try introspection.”

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.oauth2ResourceServer((oauth2) -> oauth2.opaqueToken(Customizer.withDefaults()));
	return http.build();
}

@Bean
OpaqueTokenIntrospector introspector() {
	return SpringOpaqueTokenIntrospector.withIntrospectionUri(introspectionUri)
			.clientId(clientId)
			.clientSecret(clientSecret)
			.build();
}
```

**Listing 1.** Boot publishes that introspector from **`opaquetoken.introspection-uri`**, **`client-id`**, **`client-secret`**. DSL **`introspector(...)`** replaces it ([[What is JwtDecoder in Spring Security]], [[What is OAuth 2.0]]).

```d2
direction: down
api: "API Bearer token" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
rs: "OpaqueTokenAuthenticationProvider" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
as: "AS introspection\nactive: true|false" {
  width: 220
  height: 48
  style.fill: "#c8e6c9"
}

api -> rs
rs -> as: "POST token=…"
as -> rs: "JSON"
```

**Fig. 1.** One **network hop per request** unless you cache in a custom introspector (Javadoc allows a backing store). JWT resource servers validate **locally** with **`NimbusJwtDecoder`** ([[What is NimbusJwtDecoder]], [[How do you secure microservices with Spring Security]], [[How do you debug a silent 401 from an OAuth2 resource server]]).

Handy when **revocation** must take effect immediately. You can introspect a JWT too (docs: “Using Introspection with JWTs”) if you want the AS to remain source of truth.

> [!warning] Missing `JwtDecoder` is not introspection
> JWT mode needs **`issuer-uri` / `jwk-set-uri`** and jose. Opaque mode needs **`opaquetoken.introspection-uri`**. Mix them without an **`AuthenticationManagerResolver`** and you do not get a silent fallback. No introspection URL → Boot does **not** invent one; calls fail closed.

> [!warning] Introspection is a dependency on the AS
> Every API call (or cache miss) needs the authorization server **up**, plus **client credentials** that are allowed to introspect. `{ "active": false }` is a **200** from the AS and a **401** from your API. Do not log the raw token.

> [!tip] Interview answer
> Opaque introspection is RFC 7662: the resource server asks the authorization server if the Bearer token is active instead of verifying a JWT signature. Spring uses OpaqueTokenIntrospector / SpringOpaqueTokenIntrospector and oauth2ResourceServer().opaqueToken(). Prefer JWT plus JWK when you can; use introspection when you need central revocation.
