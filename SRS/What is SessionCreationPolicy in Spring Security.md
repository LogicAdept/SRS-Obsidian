<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS

# What is SessionCreationPolicy in Spring Security?

> [!abstract] Short answer
> **`SessionCreationPolicy`** tells Spring Security whether to **create** an `HttpSession` and whether to **read `SecurityContext` from one**. Four values: **`IF_REQUIRED`** (default — create only when Security needs one), **`ALWAYS`** (eagerly create), **`NEVER`** (never create, but **use** a session that already exists), **`STATELESS`** (never create **and never use** the session for `SecurityContext`). Set it with `http.sessionManagement(sm -> sm.sessionCreationPolicy(...))`.

## The four constants

`org.springframework.security.config.http.SessionCreationPolicy` (since 3.1). XML `create-session` uses the same four names (`ifRequired` is the namespace default).

| Policy | Create a session? | Use an existing session for `SecurityContext`? |
|---|---|---|
| **`IF_REQUIRED`** | Only if Spring Security needs one | Yes |
| **`ALWAYS`** | Yes — `ForceEagerSessionCreationFilter` creates one if missing | Yes |
| **`NEVER`** | No | **Yes** — will use one that already exists |
| **`STATELESS`** | No | **No** — `NullSecurityContextRepository`; also skips saving the request into the session |

```d2
direction: right
ifreq: "IF_REQUIRED\n(default)" {
  width: 160
  height: 55
  style.fill: "#e3f2fd"
}
always: "ALWAYS\nForceEagerSessionCreationFilter" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
never: "NEVER\nuse existing only" {
  width: 170
  height: 55
  style.fill: "#e8f5e9"
}
stateless: "STATELESS\nNullSecurityContextRepository" {
  width: 220
  height: 60
  style.fill: "#fce4ec"
}

ifreq -> always: "eager"
ifreq -> never: "no create"
never -> stateless: "also ignore session"
```

**Fig. 1.** `NEVER` vs `STATELESS` is the interview distinction: both refuse to **create**; only `STATELESS` also refuses to **load** `SecurityContext` from the session.

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .sessionManagement((session) -> session
            .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
        );
    return http.build();
}
```

**Listing 1.** `STATELESS` — typical token API. This is **not** JWT by itself; you still add a bearer filter or `oauth2ResourceServer`. See [[How do you configure session management in Spring Security]].

`ALWAYS` is the “force eager session creation” switch:

```java
http.sessionManagement((session) -> session
    .sessionCreationPolicy(SessionCreationPolicy.ALWAYS));
```

**Listing 2.** Installs `ForceEagerSessionCreationFilter`, which calls `getSession()` if none exists. That is **not** “create if needed” — `IF_REQUIRED` is.

## `NEVER` still creating a session

`NEVER` only binds **Spring Security**. Default `HttpSessionRequestCache` still **saves the original request** in the session so login can replay it. That is the usual reason a `NEVER` app still shows a `JSESSIONID`. `STATELESS` turns that save off. For `NEVER`, use `NullRequestCache` if you do not want the saved-request feature. Other filters in the app can still call `request.getSession()` — this enum is not a servlet-container lock.

You can also run a **stateless mechanism** (HTTP Basic, Bearer) **and** still persist `Authentication` by swapping in `HttpSessionSecurityContextRepository` on that filter. That is an override of the repository, not a fifth enum value.

Fixation and `maximumSessions` assume a real servlet session; they do nothing useful on a true `STATELESS` chain. See [[How do you handle session fixation in Spring Security]] and [[What is SessionAuthenticationStrategy]].

> [!warning] `ALWAYS` is not “if needed”, and `STATELESS` is not JWT
> Dump tables often define `ALWAYS` as “create if required” — that is **`IF_REQUIRED`**. `ALWAYS` **eagerly** creates. `STATELESS` only changes how Security treats `HttpSession`; you still need **`oauth2ResourceServer` / a Bearer filter** for JWT. Default CSRF storage is **`HttpSessionCsrfTokenRepository`** — CSRF stays **enabled** unless you disable it. A backend that **does not serve browser traffic** may `csrf.disable()`; cookie/session SPAs must not. Pairing: [[Why do you disable CSRF for a JWT REST API]].

> [!tip] Interview answer
> SessionCreationPolicy is how Spring Security decides whether to create an HttpSession and whether to read SecurityContext from it. IF_REQUIRED is the default; ALWAYS forces a session; NEVER will not create one but will use one that already exists; STATELESS neither creates nor uses the session and installs NullSecurityContextRepository. NEVER can still get a JSESSIONID from RequestCache; STATELESS is not JWT by itself.
