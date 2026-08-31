<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you configure HTTP Basic authentication in Spring Security?

> [!abstract] Short answer
> Declare a **`SecurityFilterChain`** that authorizes requests and calls **`http.httpBasic(Customizer.withDefaults())`**. Unauthenticated clients get **401** plus **`WWW-Authenticate: Basic`**. The next request must send **`Authorization: Basic`** plus Base64(`user-id:password`). **`BasicAuthenticationFilter`** builds a **`UsernamePasswordAuthenticationToken`** and the **`AuthenticationManager`** (usually **`DaoAuthenticationProvider`**) checks it **before** the controller. Base64 is **encoding**, not encryption — use **TLS**.

## Challenge, then `Authorization: Basic`

RFC **7617**: the client concatenates `user-id`, `:`, and password, then Base64-encodes that octet string. Spring’s filter matches **`Authorization`** with scheme **`Basic`**. Example from the filter Javadoc (user `Aladdin`, password `open sesame`):

```http
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
```

**Listing 1.** Wire format. The bytes are reversible Base64. Without TLS the password is **cleartext** on the network.

Default flow (servlet reference):

1. Unauthenticated call to a protected resource → **`AuthorizationFilter`** denies → **`ExceptionTranslationFilter`** → **`BasicAuthenticationEntryPoint`** sends **`WWW-Authenticate`**. **`RequestCache`** is typically **`NullRequestCache`** (the client can replay the original request).
2. Client retries with the header. **`BasicAuthenticationFilter`** extracts user/password, creates **`UsernamePasswordAuthenticationToken`**, calls **`AuthenticationManager`**.
3. Success: `Authentication` goes on **`SecurityContextHolder`**, then **`FilterChain.doFilter`**. Failure: context cleared, entry point sends **`WWW-Authenticate`** again.

Users still come from a **`UserDetailsService`** (or a custom **`AuthenticationProvider`**) — Basic only **presents** the password ([[What is BasicAuthenticationFilter]], [[What is AuthenticationEntryPoint]], [[What is DaoAuthenticationProvider]], [[What is UsernamePasswordAuthenticationToken]]).

```d2
direction: down
req: "GET /private\nno Authorization" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
entry: "BasicAuthenticationEntryPoint\n401 + WWW-Authenticate" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
retry: "Authorization: Basic …\nBasicAuthenticationFilter" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
mgr: "AuthenticationManager\nDaoAuthenticationProvider" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}

req -> entry -> retry -> mgr
```

**Fig. 1.** Browser or HTTP client: challenge first, credentials on the **next** request — not a login form.

## Explicit `SecurityFilterChain` (required once you configure servlet security)

Out of the box, servlet HTTP Basic is **on**. **Any** servlet `HttpSecurity` / `SecurityFilterChain` you add **turns that default off** — you must enable Basic again.

```java
@Configuration
@EnableWebSecurity
public class HttpBasicSecurityConfig {

	@Bean
	SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
		http
			.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
			.httpBasic(Customizer.withDefaults());
		return http.build();
	}

	@Bean
	UserDetailsService userDetailsService() {
		UserDetails user = User.builder()
			.username("user")
			.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
			.roles("USER")
			.build();
		return new InMemoryUserDetailsManager(user);
	}
}
```

**Listing 2.** Current Java DSL (**Spring Security 6 / 7**): **`authorizeHttpRequests`** + **`httpBasic(Customizer.withDefaults())`**. XML: `<http-basic />`. Default realm name is **`Realm`** (`HttpBasicConfigurer.realmName(...)`). Do **not** use **`WebSecurityConfigurerAdapter`**, **`authorizeRequests()`**, or **`.and()`** chaining ([[Why was WebSecurityConfigurerAdapter removed]], [[When should you use HTTP Basic versus form login]]).

By default the filter **does not save** the `SecurityContext` (stateless). Clients **resend** the header on each request. **`RememberMeServices`** (if set) can skip later Basic headers. To store Basic in the **`HttpSession`**, set **`HttpSessionSecurityContextRepository`** on the filter via **`ObjectPostProcessor`**.

> [!warning] Base64 is not confidentiality
> Filter Javadoc: Basic **transmits a password in clear text**. RFC 7617: use a secure channel such as **TLS**; otherwise the user-id and password travel as **cleartext**. `{bcrypt}` in the user store does **not** encrypt the `Authorization` header.

> [!warning] `X-Requested-With: XMLHttpRequest` hides the browser dialog
> The default Basic entry point **omits** both the **401 body** and **`WWW-Authenticate`** when that header is present, so SPAs can handle 401 themselves. Override with a custom **`BasicAuthenticationEntryPoint`** if you need the challenge on XHR.

> [!warning] Logout is “close the browser” (or send 401)
> After BASIC success, the **user agent caches** credentials. **`BasicAuthenticationEntryPoint.commence`** (401) is the simple way to force a new prompt. A server-side `logout` URL does not wipe the browser’s stored Basic header by itself.

> [!tip] Interview answer
> I expose a SecurityFilterChain with authorizeHttpRequests and httpBasic(Customizer.withDefaults()). Unauthenticated calls get 401 and WWW-Authenticate; the client retries with Authorization Basic plus Base64 of user:password. BasicAuthenticationFilter turns that into a UsernamePasswordAuthenticationToken for the AuthenticationManager. Base64 is not encryption, so this is for TLS and typically machine clients, not a substitute for form login.
