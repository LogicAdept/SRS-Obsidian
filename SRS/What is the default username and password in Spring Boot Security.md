<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Boot/AutoConfiguration #SRS

# What is the default username and password in Spring Boot Security?

> [!abstract] Short answer
> With **`spring-boot-starter-security`** and **no** `UserDetailsService` / `AuthenticationProvider` / `AuthenticationManager` of your own, Boot’s **`UserDetailsServiceAutoConfiguration`** creates an in-memory user named **`user`** and a **random password**. That password is **printed once at WARN** (`Using generated security password: …`) and is **development-only**. Set **`spring.security.user.password`** (and optionally **`name`** / **`roles`**) or replace the store.

## Generated once per process

The default **`UserDetailsService`** is a single in-memory account (`SecurityProperties.User`). Appendix defaults: **`spring.security.user.name=user`**; **`password`** is empty in the table because it is **generated** at startup (`isPasswordGenerated()`).

```
Using generated security password: 78fa095d-3f4c-48b1-ad50-e24c31d5cf35

This generated password is for development use only. Your security configuration must be updated before running your application in production.
```

**Listing 1.** Official log shape. Category **`org.springframework.boot.security.autoconfigure`** must remain **WARN** or the line never appears ([[What is spring-boot-starter-security]]).

```properties
spring.security.user.name=admin
spring.security.user.password=${ADMIN_PASSWORD}
spring.security.user.roles=USER
```

**Listing 2.** Fixed credentials. Externalize the password. A **`UserDetailsService`**, **`AuthenticationProvider`**, or **`AuthenticationManager`** bean **turns this default user off**. OAuth2 client / resource-server / SAML2 on the classpath also **backs off** this auto-config unless you define **`InMemoryUserDetailsManager`** yourself.

A custom **`SecurityFilterChain`** **does not** disable the default user — only the default **web** rules. You can still log in as **`user`** until you set a password or replace the `UserDetailsService` ([[Why was WebSecurityConfigurerAdapter removed]]).

```d2
direction: right
starter: "starter-security\nno UserDetailsService bean" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
uds: "InMemoryUserDetailsManager\nname=user" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
log: "WARN: generated password\nnew UUID each restart" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}

starter -> uds -> log
```

**Fig. 1.** Same properties work on WebFlux (`ReactiveUserDetailsService`). Env / CLI override the file ([[What is Spring Boot property source precedence]]). Admin samples often set **`spring.security.user`** for the **UI** login ([[How do you secure a Spring Boot Admin server]]).

> [!warning] New password every restart
> Unset `spring.security.user.password` ⇒ a **new random value** each process. Do **not** document yesterday’s UUID. Do **not** ship the generated user to production — Boot’s own log says to **update the security configuration** first. Silencing that logger “fixes” log noise and **locks you out**.

> [!warning] Default user ≠ default `SecurityFilterChain`
> Replacing the filter chain still leaves **`user` + generated password** unless you also replace authentication. Conversely, setting **`spring.security.user.password`** does **not** loosen **`anyRequest().authenticated()`**. There is **no** hardcoded password such as `password` / `admin` in current Boot.

> [!tip] Interview answer
> The default username is user and the password is random, printed at WARN when the app starts, and it changes every restart until I set spring.security.user.password. That InMemoryUserDetailsManager goes away if I define my own UserDetailsService. A custom SecurityFilterChain does not remove that default user, and the generated password is not for production.
