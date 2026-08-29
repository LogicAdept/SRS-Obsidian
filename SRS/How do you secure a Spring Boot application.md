<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Boot/AutoConfiguration #SRS

# How do you secure a Spring Boot application?

> [!abstract] Short answer
> Add **`spring-boot-starter-security`**. Boot then **secures every request** (form login or HTTP Basic by content type) with an in-memory **`user`** and a **generated** password — **development only**. Replace that with a **`SecurityFilterChain`** `@Bean`: **`authorizeHttpRequests`**, then **`formLogin`**, **`httpBasic`**, **`oauth2Login`**, or **`oauth2ResourceServer`**. Add **TLS** (`server.ssl.*`), lock **Actuator**, and keep secrets out of git. Do **not** extend **`WebSecurityConfigurerAdapter`**.

## Starter first, then a chain you own

`SecurityAutoConfiguration` + `UserDetailsServiceAutoConfiguration` turn the starter into a default lock-down. A **`SecurityFilterChain`** bean **replaces** that web config, **including Actuator rules**. It does **not** remove the default user — that backs off only for a **`UserDetailsService`**, **`AuthenticationProvider`**, or **`AuthenticationManager`** ([[What is spring-boot-starter-security]], [[What is the default username and password in Spring Boot Security]]).

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

**Listing 1.** No `<version>` under `spring-boot-starter-parent`. WebFlux uses **`SecurityWebFilterChain`**. OAuth2/SAML are **other** starters (`spring-boot-starter-security-oauth2-client` / `…-resource-server` / `…-saml2`).

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize
			.requestMatchers("/", "/home").permitAll()
			.anyRequest().authenticated());
	http.formLogin(Customizer.withDefaults());
	return http.build();
}
```

**Listing 2.** Current DSL: **`authorizeHttpRequests`**, not `authorizeRequests()` / `antMatchers`. A **browser UI** keeps **CSRF** on and uses **form login** (or **OIDC** `oauth2Login()`). A **machine API** typically uses **`oauth2ResourceServer((rs) -> rs.jwt(Customizer.withDefaults()))`** and disables CSRF **only** for non-browser clients ([[How do you implement SSO in Spring Boot]], [[How do you configure Spring as an OAuth2 resource server]]).

```properties
spring.security.user.name=admin
spring.security.user.password=${ADMIN_PASSWORD}
server.port=8443
server.ssl.bundle=web
```

**Listing 3.** Externalize the password. TLS is **`server.ssl.*`** / SSL bundles on the embedded server — not a filter ([[How do you enable HTTPS in a Spring Boot application]]). `@EnableMethodSecurity` is a **second** layer (`@PreAuthorize`), not a substitute for the chain.

```d2
direction: down
starter: "spring-boot-starter-security" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
def: "Default: all authenticated\nuser + generated password" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
chain: "SecurityFilterChain\nauthorizeHttpRequests + login/JWT" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
extra: "TLS, Actuator EndpointRequest,\nno secrets in git" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

starter -> def -> chain -> extra
```

**Fig. 1.** The starter is **secure-by-default**, not “security finished.” Combine OAuth2 client **and** resource server in one app only with an explicit chain — Boot will not guess ([[Why was WebSecurityConfigurerAdapter removed]]).

Actuator: with the starter and **no** custom chain, everything except **`/health`** is authenticated. Your chain must use **`EndpointRequest`** or you just opened **`/actuator/**`** ([[How do you expose Spring Boot Actuator endpoints safely]]). Least privilege is matcher order: **permit** the few public paths, **`anyRequest().authenticated()`** (or **`hasRole`**) last.

> [!warning] `WebSecurityConfigurerAdapter` will not compile
> Boot 3/4 samples that `extends WebSecurityConfigurerAdapter`, call `antMatchers`, or set `password("password")` on `inMemoryAuthentication()` are dead. In-memory users need a **`PasswordEncoder`**. `WebMvcConfigurerAdapter` was never how you secure HTTP.

> [!warning] Your chain owns Actuator and CSRF
> One `permitAll()` on `/**` unlocks management endpoints. Default **CSRF** **403**s `POST` `/actuator/loggers` and form posts without a token. The generated **`user`** password in the log is **not** a production credential.

> [!tip] Interview answer
> I add spring-boot-starter-security so Boot authenticates every request, then I replace the default with a SecurityFilterChain: authorizeHttpRequests, form login or OIDC for browsers, JWT resource server for APIs. I put TLS on server.ssl, lock Actuator with EndpointRequest, and never commit passwords. WebSecurityConfigurerAdapter is gone.
