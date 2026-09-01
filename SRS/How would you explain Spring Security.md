<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# How would you explain Spring Security?

> [!abstract] Short answer
> Official one-liner: a framework for **authentication**, **authorization**, and **protection against common attacks**, for **Servlet and reactive** Spring apps. On Servlet it is a **`FilterChainProxy`** that runs a **`SecurityFilterChain` before `DispatcherServlet`**: **who** (`Authentication` in **`SecurityContextHolder`**) then **what** (`AuthorizationManager` / **`AuthorizationFilter`**), plus **CSRF**, **headers**, **session-fixation**. Boot 3 / Security **6**: a **`SecurityFilterChain` `@Bean`**, not **`WebSecurityConfigurerAdapter`**. **`formLogin()`** vs **`oauth2ResourceServer().jwt()`** are different mechanisms. **`@EnableMethodSecurity`** is extra (method interceptors), not the HTTP chain.

## Filters in front of MVC, then decisions

The client hits the container **FilterChain**. Spring Security sits there as **`DelegatingFilterProxy` → `FilterChainProxy`**. Only the **first matching** `SecurityFilterChain` runs. Authentication filters populate **`SecurityContext`**. Authorization then allows or denies. The MVC controller runs **only if** those filters call `chain.doFilter`.

| Pillar | What to say |
| --- | --- |
| Authentication | Who is this? **`AuthenticationManager` / `AuthenticationProvider`** → **`Authentication`** |
| Authorization | What may they do? HTTP **`authorizeHttpRequests`**; methods **`@PreAuthorize`** |
| Exploits | **On by default** for a session app: **CSRF**, **X-Frame-Options**, **changeSessionId()** |
| Security 6 | **`http.build()`** bean; **`AuthorizationManager`**, not voters / adapter |

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.formLogin(Customizer.withDefaults());
	return http.build();
}
```

**Listing 1.** Security **6** / Boot **3**. The dump’s **`WebSecurityConfigurerAdapter`** was **removed in 6**. Swap **`formLogin()`** for **`oauth2ResourceServer((o) -> o.jwt())`** when the API takes **Bearer JWTs** — that is **not** a login page ([[What is SecurityFilterChain]], [[Why was WebSecurityConfigurerAdapter removed]], [[What changed between Spring Security 5 and 6]]).

```d2
direction: down
req: "HTTP request" {
  width: 140
  height: 32
  style.fill: "#e3f2fd"
}
fcp: "FilterChainProxy\nSecurityFilterChain" {
  width: 240
  height: 48
  style.fill: "#fff3e0"
}
authn: "Authentication\nSecurityContextHolder" {
  width: 220
  height: 48
  style.fill: "#c8e6c9"
}
authz: "AuthorizationFilter" {
  width: 180
  height: 36
  style.fill: "#c8e6c9"
}
mvc: "DispatcherServlet" {
  width: 160
  height: 32
  style.fill: "#f3e5f5"
}

req -> fcp
fcp -> authn
authn -> authz
authz -> mvc
```

**Fig. 1.** Method security runs on **beans** (`@EnableMethodSecurity`), not as this servlet picture ([[What are the core components of Spring Security]], [[What is EnableMethodSecurity]]).

Browser apps that **own passwords** use **form login**. Delegated identity uses **`oauth2Login()`**. JSON APIs that **validate tokens** use a **resource server**. CSRF/clickjacking/XSS **headers** are the third pillar, not optional trivia ([[What are the essential features of Spring Security]], [[When should you use OAuth2 login versus form login]], [[How do you configure Spring as an OAuth2 resource server]], [[How does Spring Security mitigate XSS CSRF and clickjacking]]).

> [!warning] “Authn + authz” is incomplete
> Interviews that stop at who/what miss **CSRF**, **session fixation**, and **security headers**, which are **default** on a session-backed Servlet app. Disabling CSRF because “we have JWT” is only safe for **Bearer** APIs, not cookie sessions.

> [!warning] One chain is not every feature
> **`oauth2Login`** starts a **session**; **`oauth2ResourceServer`** checks **Bearer**. Method security is **another** interceptor stack. **`AccessDecisionManager` / `WebSecurityConfigurerAdapter`** are history, not the Security 6 answer.

> [!tip] Interview answer
> Spring Security is authentication, authorization, and exploit protection in front of the app. Servlet-wise that is FilterChainProxy and a SecurityFilterChain bean before DispatcherServlet. Security 6 dropped WebSecurityConfigurerAdapter. Form login, oauth2Login, and jwt resource server are different DSLs. Method security is extra. Defaults already cover CSRF and clickjacking for session apps.
