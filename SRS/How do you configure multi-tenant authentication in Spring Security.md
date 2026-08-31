<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Security/OAuth2 #Security/JWT #SRS

# How do you configure multi-tenant authentication in Spring Security?

> [!abstract] Short answer
> Spring Security’s documented multi-tenancy is a **resource server** with **several ways to verify a bearer token**, keyed by a **tenant id**. Resolve the tenant at request time with an **`AuthenticationManagerResolver<HttpServletRequest>`**, usually **`JwtIssuerAuthenticationManagerResolver`** on the JWT **`iss`** claim. Plug it into **`oauth2ResourceServer().authenticationManagerResolver(...)`**. Trusted issuers only — do not build a manager from an arbitrary `iss`. A custom tenant field on **`UsernamePasswordAuthenticationToken`** is **not** the official API.

## Tenant = which `AuthenticationManager` runs

A resource server is multi-tenant when **verification strategy** is keyed by tenant (two authorization servers, or one server with many issuers). Two jobs: **resolve** the tenant, then **propagate** it (same subdomain or claim downstream).

**`AuthenticationManagerResolver`** (since **5.2**) picks an **`AuthenticationManager`** from context. For JWTs, **`JwtIssuerAuthenticationManagerResolver`** (since **5.3**) reads **`iss`** from the Bearer token. **`fromTrustedIssuers(...)`** is since **6.2**. Each issuer gets a **`JwtAuthenticationProvider`**, created **lazily** on first use so startup does not require those authorization servers to be up ([[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is ProviderManager in Spring Security]]).

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	String issuerOne = "idp.example.org/issuerOne"; // trusted JWT iss
	String issuerTwo = "idp.example.org/issuerTwo";
	JwtIssuerAuthenticationManagerResolver resolver =
		JwtIssuerAuthenticationManagerResolver.fromTrustedIssuers(issuerOne, issuerTwo);
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.oauth2ResourceServer((oauth2) -> oauth2.authenticationManagerResolver(resolver));
	return http.build();
}
```

**Listing 1.** Static trusted issuers (`iss` is usually an absolute URI). XML: `authentication-manager-resolver-ref` on `<oauth2-resource-server>`.

```java
Map<String, AuthenticationManager> authenticationManagers = new ConcurrentHashMap<>();
authenticationManagers.put(issuer, new JwtAuthenticationProvider(JwtDecoders.fromIssuerLocation(issuer))::authenticate);

JwtIssuerAuthenticationManagerResolver resolver =
	new JwtIssuerAuthenticationManagerResolver(authenticationManagers::get);
```

**Listing 2.** Dynamic tenants: a **map of allowed issuers** you can edit at runtime. Keys **are** the allow-list. `resolve` throws **`OAuth2AuthenticationException`** if the Bearer token is malformed or no manager can be derived.

JWT vs opaque per tenant (or per path) is the same resolver idea: two **`ProviderManager`**s and `(request) -> useJwt(request) ? jwt : opaque`. **`useJwt`** typically uses **request** material (path). **`RequestMatcherDelegatingAuthenticationManagerResolver`** (since **5.7**) maps **`RequestMatcher`** → manager.

```d2
direction: down
req: "Bearer JWT\niss claim" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
resolver: "JwtIssuerAuthenticationManagerResolver" {
  width: 300
  height: 60
  style.fill: "#fff3e0"
}
one: "ProviderManager\nJwtAuthenticationProvider A" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
two: "ProviderManager\nJwtAuthenticationProvider B" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}

req -> resolver
resolver -> one
resolver -> two
```

**Fig. 1.** One filter chain; the resolver chooses the manager. Tenant by **subdomain** instead of `iss`: keep using the **same** hostname pattern when calling downstream resource servers.

To parse the JWT **once**, the reference composes a tenant-aware **`JWTClaimsSetAwareJWSKeySelector`** plus **`OAuth2TokenValidator`** that looks the issuer up in a **tenant repository** (allow-list), then a **`NimbusJwtDecoder`**. The authorization server must **sign the claim set**; otherwise `iss` can be swapped.

## What the dump’s custom token is not

Spring does **not** document a `CustomAuthenticationToken` with `getTenant()` for form login. Username/password multi-tenancy is **your** `UserDetailsService` / **`AuthenticationProvider`** plus a tenant taken from the **request** (host, header, path) — same **resolver** idea, not a subclass of **`UsernamePasswordAuthenticationToken`**. Register a **`ProviderManager`** per tenant or implement **`AuthenticationProvider`** as usual ([[How do you configure a custom AuthenticationProvider in Spring Security]]). A single **`loadUserByUsername`** with no tenant discriminator will return the **same** user for every tenant.

> [!warning] Never trust an arbitrary `iss`
> Anyone can stand up an authorization server. **`fromTrustedIssuers`** or a **map whose keys are known issuers** is required. Building a decoder from whatever `iss` appears in the token is unsafe.

> [!warning] Resolver then decoder parse the JWT twice
> `JwtIssuerAuthenticationManagerResolver` parses `iss`; **`JwtDecoder`** parses again. That is the simple path’s trade-off. Moving tenant selection into the JWS key selector needs the **claims in the signature**.

> [!tip] Interview answer
> Official multi-tenancy in Spring Security is an AuthenticationManagerResolver on the resource server, typically JwtIssuerAuthenticationManagerResolver keyed by the JWT iss claim, wired through oauth2ResourceServer.authenticationManagerResolver. I only accept issuers from a trusted list or a runtime map of those issuers. Form-login tenant tokens are not a Spring API — isolate users in the store or pick a ProviderManager from the request.
