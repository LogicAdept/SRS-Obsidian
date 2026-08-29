<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Admin #Java/Spring/Security/FilterChain #SRS

# How do you secure a Spring Boot Admin server?

> [!abstract] Short answer
> Add **`spring-boot-starter-security`** next to **`spring-boot-admin-starter-server`**. Admin does **not** ship a default auth story — you own a **`SecurityFilterChain`**: **form login** for the UI, **HTTP Basic** for API clients, CSRF that **exempts** `POST /instances` and `DELETE /instances/*`. Minimal credentials: **`spring.security.user.name` / `password`** (externalize the password). That is **not** how you lock **client** Actuator endpoints.

## What you actually secure

Spring Boot Admin is a **UI and API** over registered apps’ Actuator data ([[What is the difference between Spring Boot Actuator and Spring Boot Admin]]). Securing the **server** means authenticating who may open that UI and register instances. Securing **clients** is a second layer (metadata `user.name` / `user.password` + `spring.boot.admin.instance-auth`).

```yaml
spring:
  security:
    user:
      name: admin
      password: ${ADMIN_PASSWORD}
```

**Listing 1.** Boot’s default user. Official quick start: form login at `/login` and HTTP Basic for API. Do not commit the password.

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http, AdminServerProperties adminServer)
		throws Exception {
	http.authorizeHttpRequests(auth -> auth
			.requestMatchers(adminServer.path("/assets/**"), adminServer.path("/login"))
			.permitAll()
			.requestMatchers(adminServer.path("/actuator/health"),
					adminServer.path("/actuator/info"))
			.permitAll()
			.anyRequest().authenticated())
		.formLogin(form -> form.loginPage(adminServer.path("/login")))
		.httpBasic(Customizer.withDefaults())
		.csrf(csrf -> csrf
			.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
			.ignoringRequestMatchers(
				PathPatternRequestMatcher.withDefaults()
					.matcher(POST, adminServer.path("/instances")),
				PathPatternRequestMatcher.withDefaults()
					.matcher(DELETE, adminServer.path("/instances/*"))));
	return http.build();
}
```

**Listing 2.** Conceptual `SecurityFilterChain` (Boot Admin **4.0**): UI form login, Basic for clients, permit **assets** and **login** or the login page never loads. Use `adminServer.path(…)` when the Admin app has a context path. The full sample also adds a JS CSRF cookie filter, ignores CSRF on the server’s `/actuator/**`, and optional remember-me.

OAuth2 / LDAP / a user database are valid **UserDetails** sources; the same filter chain still applies. Roles can split **ADMIN** (mutate `/instances/**`) vs **USER** (read).

```d2
direction: right
ui: "Browser\nform login" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
chain: "SecurityFilterChain\nanyRequest authenticated" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
reg: "Clients POST /instances\nCSRF ignored" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

ui -> chain
reg -> chain
```

**Fig. 1.** The Admin **server** is one `SecurityFilterChain`. Client Actuator passwords live in **registration metadata**, not in this chain ([[How do you expose Spring Boot Actuator endpoints safely]]).

> [!warning] `WebSecurityConfigurerAdapter` is not the current API
> Official Admin **4.x** samples use a **`SecurityFilterChain` `@Bean`**, not `WebSecurityConfigurerAdapter` ([[Why was WebSecurityConfigurerAdapter removed]]). Copy-pasting an old `httpBasic()` adapter that `permitAll`s **`/actuator/**`** on the Admin server opens the **server’s** Actuator, which is not the same as unlocking **client** `/actuator/**`. The documented authorize list permits only **`/actuator/health`** and **`/actuator/info`** on the server (plus assets and login).

> [!warning] CSRF will block instance registration
> Clients register with **`POST /instances`**. If CSRF is on (default with browser login), registration returns token errors unless you **ignore** that path (and `DELETE /instances/*`). Cookie CSRF for the UI needs **`CookieCsrfTokenRepository.withHttpOnlyFalse()`** plus the docs’ filter so JavaScript can read the token. Externalize **`ADMIN_PASSWORD`**; use HTTPS in real deployments.

> [!tip] Interview answer
> I secure the Admin server with spring-boot-starter-security and a SecurityFilterChain: form login for the UI, HTTP Basic for API, and spring.security.user or a UserDetailsService. I permit assets and /login, authenticate the rest, and CSRF-ignore POST /instances so clients can register. That is not permit-all on every Actuator path, and it is not WebSecurityConfigurerAdapter. Client actuator credentials are a separate metadata / instance-auth setup.
