<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/JWT #Security/OAuth2 #SRS

# What is `JwtAccessTokenConverter`?

> [!abstract] Short answer
> A **deprecated** **Spring Security OAuth** helper (`org.springframework.security.oauth2.provider.token.store`) that **translates both ways** between a **JWT string** and **`OAuth2Authentication` / `OAuth2AccessToken`**. It is also a **`TokenEnhancer`** when the old authorization server **grants** tokens. You sign with **`setSigningKey`** (MAC or OpenSSH RSA) or **`setKeyPair`**. It is **not** **`JwtDecoder` / `NimbusJwtDecoder`**. Resource servers today use **`oauth2ResourceServer().jwt()`**. Spring Security **does not mint** access tokens; that is **Spring Authorization Server** (or **`JwtEncoder`** if you issue JWTs yourself).

## Bidirectional converter, not `JwtDecoder`

Javadoc (2.5.2, `@Deprecated` → OAuth 2.0 Migration Guide): implements **`AccessTokenConverter`**, **`TokenEnhancer`**, **`InitializingBean`**. Package is **`spring-security-oauth`**, crypto via **`spring-security-jwt`** (`Signer` / `SignatureVerifier`).

| Method | What it actually does |
| --- | --- |
| **`convertAccessToken(token, authentication)`** | Claim **`Map`** for JSON — **not** the compact JWT |
| **`encode(...)`** (protected) | Compact **JWT string** |
| **`decode(jwt)`** (protected) | Claim **`Map`** from the JWT |
| **`extractAuthentication(map)`** | **`OAuth2Authentication`** (client + user) |
| **`extractAccessToken(value, map)`** | **`OAuth2AccessToken`** |
| **`enhance(...)`** | **`TokenEnhancer`**: extra info while **granting** |

Dumps that say “`convertAccessToken` encodes” are flattening **map vs compact JWT**.

Boot wired it on the **authorization server** with a matching **`JwtTokenStore`** — “not really a store”; **share the same converter** (or the same verifier) as the minter:

```java
@Bean
JwtAccessTokenConverter accessTokenConverter() {
	JwtAccessTokenConverter converter = new JwtAccessTokenConverter();
	converter.setKeyPair(keyPair);
	return converter;
}

@Bean
TokenStore tokenStore() {
	return new JwtTokenStore(accessTokenConverter());
}
```

**Listing 1.** Legacy OAuth2 Boot JWT format. **`setSigningKey(String)`**: MAC **or** RSA in **OpenSSH (`ssh-keygen`)** form. HMAC: verifier = signing key. RSA: **`setVerifierKey`** is the **public** key exposed so resource servers can fetch it ([[What is EnableResourceServer]], [[How do you secure microservices with Spring Security]]).

```d2
direction: down
as: "Old AS\nenhance / encode" {
  width: 200
  height: 48
  style.fill: "#ffcdd2"
}
c: "JwtAccessTokenConverter" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
rs: "Old RS\ndecode / extractAuthentication" {
  width: 260
  height: 48
  style.fill: "#ffcdd2"
}
now: "JwtEncoder vs JwtDecoder\noauth2ResourceServer().jwt()" {
  width: 280
  height: 48
  style.fill: "#c8e6c9"
}

as -> c
c -> rs
c -> now: "replaced by split APIs" {
  style.stroke: "#2e7d32"
}
```

**Fig. 1.** One class used to **mint and parse**. Current Security splits **encode** (`NimbusJwtEncoder`) and **decode** (`NimbusJwtDecoder` + **`JwtTimestampValidator`**) ([[How do you debug a silent 401 from an OAuth2 resource server]], [[What is JWT clock skew in Spring Security]], [[Why should you not catch Exception when validating a JWT]]).

Spring Security’s OAuth2 chapter: **no token-minting endpoint**; **`JwtEncoder`** exists if you sign JWTs. Migrating an old **`@EnableAuthorizationServer`** is **out of scope** of that wiki — use **Spring Authorization Server**.

> [!warning] Not on the Security 6 resource-server path
> **`oauth2ResourceServer().jwt()`** never instantiates this class. If it still compiles, **`spring-security-oauth`** is on the classpath. **`JwtClaimsSetVerifier`** is the old claims hook; today that is **`OAuth2TokenValidator<Jwt>`**.

> [!warning] `convertAccessToken` is a `Map`
> Compact JWT is **`encode` / `decode`**. Custom dumps that only override `convertAccessToken` do not change the signature. **`JwtTokenStore.getAccessToken(authentication)` always returns null** — there is no lookup table.

> [!tip] Interview answer
> JwtAccessTokenConverter is the deprecated Spring Security OAuth JWT bridge: TokenEnhancer on issue, AccessTokenConverter on parse, signing key on the bean. JwtTokenStore shares that instance. Today the API validates with JwtDecoder; an authorization server mints tokens. It is not NimbusJwtDecoder.
