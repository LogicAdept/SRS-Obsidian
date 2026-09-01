<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/JWT #Security/OAuth2 #SRS

# What is `JwtDecoder` in Spring Security?

> [!abstract] Short answer
> A **`@FunctionalInterface`** (`decode(String) → Jwt`) that turns a compact **JWS/JWE** into a validated **`Jwt`**. **`JwtAuthenticationProvider`** calls it on an OAuth2 resource server. Failures throw **`JwtException`** → typically **401** with an empty body. Boot auto-configures **`NimbusJwtDecoder`** from **`spring.security.oauth2.resourceserver.jwt.issuer-uri`** via **`JwtDecoders.fromIssuerLocation`**. It is **not** opaque introspection and **not** **`JwtAccessTokenConverter`**.

## Decode + verify, then `JwtAuthenticationToken`

Javadoc (since **5.0**): implementations **verify a JWS** and/or **decrypt a JWE**. Stock types: **`NimbusJwtDecoder`**, **`SupplierJwtDecoder`** (lazy JWKS / first JWT). Reactive apps use **`ReactiveJwtDecoder`**.

Need **`spring-security-oauth2-resource-server`** **and** **`spring-security-oauth2-jose`** (Boot starter pulls both). Default algorithm trust is **RS256**.

Boot, with `issuer-uri` set and **no** `JwtDecoder` `@Bean`, publishes:

```java
@Bean
JwtDecoder jwtDecoder() {
	return JwtDecoders.fromIssuerLocation(issuerUri);
}
```

**Listing 1.** Factory hits Provider Configuration / Authorization Server Metadata, derives the **JWK Set URI**, and wires validators (`iss`, **`JwtTimestampValidator`** 60s skew). A **`JwtDecoder` `@Bean`** or DSL **`decoder(...)`** **replaces** that auto-config ([[What is JWT clock skew in Spring Security]], [[How do you debug a silent 401 from an OAuth2 resource server]]).

```java
Jwt jwt = jwtDecoder.decode(compactToken);
```

**Listing 2.** Contract. Success: **`JwtAuthenticationConverter`** maps claims → authorities (`SCOPE_…`, plus **`FACTOR_BEARER`**). Principal is the **`Jwt`**.

```d2
direction: down
f: "BearerTokenAuthenticationFilter" {
  width: 250
  height: 36
  style.fill: "#e3f2fd"
}
p: "JwtAuthenticationProvider" {
  width: 220
  height: 36
  style.fill: "#fff3e0"
}
d: "JwtDecoder.decode" {
  width: 180
  height: 36
  style.fill: "#c8e6c9"
}
ctx: "JwtAuthenticationToken\non SecurityContextHolder" {
  width: 250
  height: 48
  style.fill: "#c8e6c9"
}

f -> p
p -> d
d -> ctx
```

**Fig. 1.** The decoder does **not** mint tokens. That was **`JwtAccessTokenConverter`** / an authorization server ([[What is JwtAccessTokenConverter]], [[What is EnableResourceServer]], [[How do you secure microservices with Spring Security]]).

Opaque tokens are a **different** bean: **`OpaqueTokenIntrospector`** + **`opaquetoken.introspection-uri`**. “Fallback to `SpringOpaqueTokenIntrospector`” means **opaque mode without a custom introspector**, not “no `JwtDecoder`”. Unreachable JWKS is usually **500**, not a silent 401.

> [!warning] Missing `JwtDecoder` is not introspection
> No `issuer-uri` / `jwk-set-uri` and no jose jar → JWT resource server does **not** start correctly. Boot does **not** then call an introspection endpoint unless you configured **opaque** properties. A broken custom **`JwtDecoder` `@Bean`** also **replaces** Boot’s decoder — it looks like “Security is not validating JWTs”.

> [!warning] `JwtException` stays out of the HTTP body
> The filter maps it to **401** / **`invalid_token`**. Do not `catch (Exception)` around **`decode`**. Read **DEBUG/TRACE** and **`WWW-Authenticate`** ([[Why should you not catch Exception when validating a JWT]]).

> [!tip] Interview answer
> JwtDecoder is the resource-server SPI that verifies and parses a Bearer JWT into a Jwt. Boot builds NimbusJwtDecoder from issuer-uri. JwtAuthenticationProvider calls decode; JwtException becomes 401. Opaque tokens use OpaqueTokenIntrospector instead.
