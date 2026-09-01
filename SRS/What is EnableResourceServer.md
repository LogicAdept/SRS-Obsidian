<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/JWT #Java/Annotations #SRS

# What is `EnableResourceServer`?

> [!abstract] Short answer
> A **deprecated** **Spring Security OAuth** annotation (`org.springframework.security.oauth2.config.annotation.web.configuration`) that installed a filter to **authenticate `Authorization: Bearer` tokens**. You added **`@EnableWebSecurity`** plus a **`ResourceServerConfigurer`** (usually **`ResourceServerConfigurerAdapter`**) for paths and **resource id**. It created a **`WebSecurityConfigurerAdapter` with hard-coded `@Order(3)`**. Current replacement: **`http.oauth2ResourceServer(oauth2 -> oauth2.jwt())`** (or opaque) and **`spring.security.oauth2.resourceserver.jwt.issuer-uri`**.

## Token filter, not SSO

Javadoc: convenient annotation for **OAuth2 Resource Servers**; **`@Import(ResourceServerConfiguration.class)`**; **`@Deprecated`** → OAuth 2.0 Migration Guide. Boot’s OAuth2-autoconfigure wired **`OAuth2AuthenticationProcessingFilter`** after you also chose JWT (`jwk.key-set-uri` / `jwt.key-value`) or opaque (`token-info-uri`). Properties were **`security.oauth2.resource.*`**, not `spring.security.oauth2.resourceserver.*`.

`ResourceServerConfigurerAdapter.configure(HttpSecurity)`: by default **everything except `/oauth/**`** is protected. `configure(ResourceServerSecurityConfigurer)` set **resource id** (audience / realm in the old stack). Scope checks used SpEL **`#oauth2.hasScope('…')`**.

| Then (Security OAuth 2.x) | Now (Security 5.2+ / Boot 3) |
| --- | --- |
| **`@EnableResourceServer`** | **`oauth2ResourceServer()`** on a **`SecurityFilterChain`** |
| **`ResourceServerConfigurerAdapter`** | **`authorizeHttpRequests`** on the **same** chain |
| `#oauth2.hasScope('read')` | **`hasAuthority("SCOPE_read")`** |
| **`security.oauth2.resource.jwk.key-set-uri`** | **`spring.security.oauth2.resourceserver.jwt.issuer-uri`** (or `jwk-set-uri`) |

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()));
	return http.build();
}
```

**Listing 1.** Official JWT default. Boot also auto-configures this plus a **`JwtDecoder`** when the issuer property is set — **no** `@EnableResourceServer` ([[How do you debug a silent 401 from an OAuth2 resource server]], [[How do you secure microservices with Spring Security]]).

```d2
direction: down
ers: "@EnableResourceServer\nOrder 3 adapter" {
  width: 230
  height: 48
  style.fill: "#ffcdd2"
}
rs: "oauth2ResourceServer()\nBearer JWT / opaque" {
  width: 240
  height: 48
  style.fill: "#c8e6c9"
}
sso: "oauth2Login()\nbrowser session" {
  width: 200
  height: 48
  style.fill: "#e3f2fd"
}

ers -> rs: "same role" {
  style.stroke: "#2e7d32"
}
ers -> sso: "that was EnableOAuth2Sso" {
  style.stroke: "#1565c0"
}
```

**Fig. 1.** Resource server validates a **Bearer** token. **SSO login** was **`@EnableOAuth2Sso`** / **`oauth2Login()`** ([[What is EnableOAuth2Sso]], [[How do you implement OAuth2 login in Spring Security]], [[Why was WebSecurityConfigurerAdapter removed]]).

Hard-coded **order 3** meant a second adapter at order 3 **conflicts**. Boot also warned: default resource-server chain can **steal** all URLs unless you **narrow** `requestMatchers` / `antMatchers` on the resource adapter (or reorder). Migration: put **all** authorization rules on **one** Security DSL, not “bearer rules on `ResourceServerConfigurerAdapter` and cookie rules on `WebSecurityConfigurerAdapter`”.

> [!warning] Do not mix the annotation with `oauth2ResourceServer()`
> Two stacks, two filters (`OAuth2AuthenticationProcessingFilter` vs **`BearerTokenAuthenticationFilter`**), two property prefixes. Whichever **`SecurityFilterChain`** matches first wins. Drop **`spring-security-oauth2`** / **`spring-security-oauth2-autoconfigure`**.

> [!warning] `#oauth2.hasScope` does not exist on the new API
> Write **`hasAuthority("SCOPE_…")`**. **`resourceId`** was not ported; audience is an **`OAuth2TokenValidator`** on **`JwtDecoder`**. A JWT API still usually **`csrf.disable()`** + stateless — that is cookie CSRF, not this annotation ([[Why do you disable CSRF for a JWT REST API]]).

> [!tip] Interview answer
> EnableResourceServer was Spring Security OAuth’s deprecated switch to treat the app as a Bearer-token resource server, with ResourceServerConfigurerAdapter and a hard-coded order-3 chain. Spring Security 5.2+ uses oauth2ResourceServer().jwt() or opaque introspection. It is not EnableOAuth2Sso / oauth2Login.
