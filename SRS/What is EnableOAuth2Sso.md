<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Java/Annotations #SRS

# What is `EnableOAuth2Sso`?

> [!abstract] Short answer
> A **deprecated** Boot / **Spring Security OAuth** annotation that turned an app into an **OAuth2 SSO client**: redirect to the authorization server, then a **local session**. Put it on a **`WebSecurityConfigurerAdapter`** (enhances that adapter with a filter and entry point) or alone (Boot adds an adapter that **secures every path**). Current replacement is **`http.oauth2Login()`** plus a **`ClientRegistration`**. It is **not** on the Spring Security 6 classpath.

## Old SSO annotation, current Login DSL

The class lived in `org.springframework.boot.autoconfigure.security.oauth2.client` (`spring-security-oauth2-boot`). Javadoc: **`@Deprecated`** — see the **OAuth 2.0 Migration Guide**. Meta-annotations include **`@EnableOAuth2Client`**. It is **not** `org.springframework.security.config.annotation…`.

Boot’s OAuth2 Boot guide: fetch user details (`user-info-uri`) and turn them into an **`Authentication`**. Properties were **`security.oauth2.client.*`**, **`security.oauth2.resource.user-info-uri`**, **`security.oauth2.sso.login-path`** (default **`/login`**).

| Dump pairing | Then | Now |
| --- | --- | --- |
| Browser SSO | **`@EnableOAuth2Sso`** | **`oauth2Login()`** + `spring.security.oauth2.client.registration.*` |
| API tokens | **`@EnableResourceServer`** | **`oauth2ResourceServer()`** (JWT / opaque) |

The migration wiki is explicit: Spring Security OAuth called this **SSO**; Spring Security calls it **OAuth 2.0 Login**.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

	@Bean
	SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
		http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
			.oauth2Login(Customizer.withDefaults());
		return http.build();
	}
}
```

**Listing 1.** Replacement: a **`SecurityFilterChain`** bean, not the annotation and not **`WebSecurityConfigurerAdapter`** ([[How do you implement OAuth2 login in Spring Security]], [[How do you register a custom OAuth2 identity provider]], [[Why was WebSecurityConfigurerAdapter removed]]).

```d2
direction: down
old: "@EnableOAuth2Sso\n+ adapter / all paths" {
  width: 230
  height: 48
  style.fill: "#ffcdd2"
}
login: "oauth2Login()\nbrowser session" {
  width: 200
  height: 48
  style.fill: "#c8e6c9"
}
rs: "oauth2ResourceServer()\nBearer API" {
  width: 220
  height: 48
  style.fill: "#e3f2fd"
}

old -> login: "same role, new name" {
  style.stroke: "#2e7d32"
}
old -> rs: "not this annotation" {
  style.stroke: "#1565c0"
}
```

**Fig. 1.** SSO client ≠ resource server. Mixing **`@EnableOAuth2Sso`** with **`oauth2ResourceServer()`** is two generations in one process ([[How do you debug a silent 401 from an OAuth2 resource server]]).

Default with the annotation **and no adapter**: every path authenticated, including **`/error`**. Official warning: SSO failure that redirects to **`/error`** can **loop** with the IdP unless `/error` is `permitAll` (or you fix the real error).

> [!warning] Not Spring Security 6
> **`@EnableOAuth2Sso`** is **`spring-security-oauth2-boot`** / old **`security.oauth2.*`** properties. Boot 2 already moved first-class OAuth to Security 5 **`oauth2Login()`**. Security 6 / Boot 3 do not ship this annotation. If it “still compiles”, you still have the dead library on the classpath.

> [!warning] All paths locked, including `/error`
> Annotation-only = Boot adds a **`WebSecurityConfigurerAdapter`** that secures **everything**. On an adapter, it only **adds** the SSO filter and entry point — you still write `authorizeRequests`. That adapter type is **gone in Security 6**.

> [!tip] Interview answer
> EnableOAuth2Sso was Boot’s deprecated OAuth2 SSO client annotation: redirect to the auth server, then a session. It decorated WebSecurityConfigurerAdapter or secured all URLs by default. Spring Security renamed it OAuth 2.0 Login: oauth2Login() and a ClientRegistration. APIs use oauth2ResourceServer(), not this annotation.
