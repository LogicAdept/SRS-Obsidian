<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/JWT #Security/OAuth2 #SRS

# How do you implement JWT authentication in Spring Security?

> [!abstract] Short answer
> **Do not write a parser.** Use **OAuth2 Resource Server**: **`spring-boot-starter-oauth2-resource-server`**, **`spring.security.oauth2.resourceserver.jwt.issuer-uri`**, **`http.oauth2ResourceServer((o) -> o.jwt(Customizer.withDefaults()))`**. **`BearerTokenAuthenticationFilter`** → **`JwtAuthenticationProvider`** → **`JwtDecoder`** → **`JwtAuthenticationToken`** (principal is the **`Jwt`**, plus **`FACTOR_BEARER`**). Minting is **Spring Authorization Server** or **`JwtEncoder.encode`** (`NimbusJwtEncoder`, since **5.6**) — not **`JwtAccessTokenConverter`**. A homemade **`OncePerRequestFilter`** that stuffs **`UsernamePasswordAuthenticationToken`** is a blog pattern, not the DSL.

## Validate Bearer JWT; mint only if you are the issuer

Most APIs are **resource servers**: they **verify** compact JWTs. Boot’s **`JwtDecoder`** is **`JwtDecoders.fromIssuerLocation`** (JWKS from discovery). Custom / unsigned-by-IdP JWTs still use **`NimbusJwtDecoder`** (JWK set, **RSA public key**, or HMAC) — still **`oauth2ResourceServer().jwt()`**, not a hand-rolled parser.

| Role | Spring API |
| --- | --- |
| Read `Authorization: Bearer` | **`BearerTokenAuthenticationFilter`** |
| Decode + verify | **`JwtDecoder`** / **`NimbusJwtDecoder`** |
| `Authentication` type | **`JwtAuthenticationToken`** |
| Issue compact JWT | **`JwtEncoder`** / **`NimbusJwtEncoder`**, or SAS token endpoint |
| Legacy both-ways | **`JwtAccessTokenConverter`** (deprecated OAuth library) |

```java
@Bean
SecurityFilterChain apis(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()));
	return http.build();
}
```

**Listing 1.** With YAML **`resourceserver.jwt.issuer-uri: "{issuer}"`** this is JWT authentication. Authorities include **`SCOPE_…`**. Dual UI/API: two **`SecurityFilterChain`** beans ([[How do you configure Spring as an OAuth2 resource server]], [[How do you configure JWT and form login as two SecurityFilterChain beans]]).

```java
Jwt jwt = jwtEncoder.encode(JwtEncoderParameters.from(claims));
```

**Listing 2.** Issuing (since **5.6**). Security **does not** mint on the resource-server path. Expired access JWTs are **rejected** here; a **new** JWT comes from **`grant_type=refresh_token`** at the **authorization server** ([[What is JwtDecoder in Spring Security]], [[How do you refresh an expired JWT in Spring Security]]).

```d2
direction: down
official: "oauth2ResourceServer().jwt()\nJwtAuthenticationToken" {
  width: 280
  height: 48
  style.fill: "#c8e6c9"
}
blog: "OncePerRequestFilter +\nUsernamePasswordAuthenticationToken" {
  width: 280
  height: 48
  style.fill: "#ffcdd2"
}
enc: "JwtEncoder / Authorization Server" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}

enc -> official: "compact JWT"
```

**Fig. 1.** A custom Bearer filter must still sit **before `AnonymousAuthenticationFilter`**. Official **`BearerTokenAuthenticationFilter`** already does ([[Why must a JWT filter run before AnonymousAuthenticationFilter]], [[What is NimbusJwtDecoder]]).

Bearer APIs usually **`csrf.disable()`** (no session cookie). Keep CSRF if the JWT lives in a **cookie** ([[Why do you disable CSRF for a JWT REST API]], [[How do you debug a silent 401 from an OAuth2 resource server]]).

> [!warning] Do not catch-all parse into `UsernamePasswordAuthenticationToken`
> The stock principal is **`JwtAuthenticationToken`**, not a form-login token. **`catch (Exception)`** around decode hides JWKS vs expiry ([[Why should you not catch Exception when validating a JWT]]). **`JwtAccessTokenConverter`** is **not** **`JwtDecoder`**.

> [!warning] A JWT is self-contained — the resource server cannot “log it out”
> There is **no** built-in blocklist on **`JwtDecoder`**. Invalidation is **short `exp` + refresh**, or **opaque introspection** / AS revocation. Clock skew is **60s**, not a logout switch ([[What is JWT clock skew in Spring Security]], [[What is the OAuth2 refresh token grant]]).

> [!tip] Interview answer
> JWT authentication in Spring Security is oauth2ResourceServer().jwt() plus a JwtDecoder from issuer-uri or JWKS. The filter produces JwtAuthenticationToken. Do not write a OncePerRequestFilter parser. If you issue tokens, use JwtEncoder or an authorization server. Resource servers reject expired JWTs; refresh happens at the token endpoint. Homemade UsernamePasswordAuthenticationToken JWT filters are not the documented path.
