<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Boot/AutoConfiguration #SRS

# What is spring-boot-starter-security?

> [!abstract] Short answer
> **`spring-boot-starter-security`** is the Boot starter that puts **Spring Security on the classpath**. A **web** app is then **secured by default**: every request (including `/error` and Actuator except **`/health`**) needs authentication; content negotiation chooses **form login** or **HTTP Basic**; an in-memory **`user`** gets a **random password** logged at **WARN**. Customize with a **`SecurityFilterChain`** `@Bean` — **not** `WebSecurityConfigurerAdapter`. It is **not** the OAuth2/SAML starters.

## Starter in, default `SecurityFilterChain` on

The build-systems table: starter **for using Spring Security**. Auto-config is **`SecurityAutoConfiguration`** + **`UserDetailsServiceAutoConfiguration`** (MVC) or **`ReactiveWebSecurityAutoConfiguration`** + **`ReactiveUserDetailsServiceAutoConfiguration`** (WebFlux / RSocket). WebFlux uses a **`SecurityWebFilterChain`**.

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

**Listing 1.** No `<version>` under `spring-boot-starter-parent` ([[Which common Spring Boot starters do you know]]; [[What is spring-boot-starter-parent]]).

Default in-memory user: name **`user`**, password **generated**, printed once:

```
Using generated security password: …
This generated password is for development use only.
```

**Listing 2.** Logger category **`org.springframework.boot.security.autoconfigure`** must stay at **WARN** or you never see it. Override with `spring.security.user.name` / `password` / `roles`. Adding your own **`UserDetailsService`**, **`AuthenticationProvider`**, or **`AuthenticationManager`** turns the default user **off**.

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
		.httpBasic(Customizer.withDefaults());
	return http.build();
}
```

**Listing 3.** A **`SecurityFilterChain`** bean **replaces** Boot’s default web security (including Actuator rules). Use **`EndpointRequest`** / **`PathRequest`** for actuators and static resources. `@EnableMethodSecurity` is separate (method annotations). **`@EnableWebSecurity`** is not what the starter “is” — Boot already enables web security when the library is present ([[Why was WebSecurityConfigurerAdapter removed]]).

OAuth2 / SAML need **`spring-boot-starter-security-oauth2-client`**, **`…-oauth2-resource-server`**, **`…-saml2`** (Boot 4 names; older `spring-boot-starter-oauth2-*` are deprecated). Those modules also **back off** the default **`UserDetailsService`** unless you define **`InMemoryUserDetailsManager`** yourself.

```d2
direction: right
dep: "spring-boot-starter-security" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
ac: "SecurityAutoConfiguration\nUserDetailsServiceAutoConfiguration" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
lock: "All requests authenticated\nformLogin or httpBasic" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

dep -> ac -> lock
```

**Fig. 1.** Default is a **lock-down**, not OAuth. Actuator: with this starter and **no** custom chain, endpoints other than **`/health`** are secured ([[How do you expose Spring Boot Actuator endpoints safely]]).

> [!warning] `WebSecurityConfigurerAdapter` will not compile on Boot 3/4
> Spring Security **6** removed the adapter. A custom **`SecurityFilterChain`** also **backs off** Boot’s Actuator security — you must restate those rules (or add a second chain). Combining OAuth2 Client + Resource Server is done with **your** chain, not by stacking adapters.

> [!warning] The generated password is not production config
> It is **development-only** (Boot says so in the log). Set **`spring.security.user.password`** or a real **`UserDetailsService`**. If you **quiet** the autoconfigure logger, you **lose** the printed password and cannot log in. This starter does **not** add OAuth2 client/resource-server support.

> [!tip] Interview answer
> spring-boot-starter-security puts Spring Security on the classpath so Boot auto-configures a lock-down: every web request authenticated, form login or HTTP Basic from the Accept header, and a generated user/password in the logs. I replace that with a SecurityFilterChain bean, not WebSecurityConfigurerAdapter. OAuth2 and SAML are separate security-* starters, and a custom chain also means I own Actuator access rules.
