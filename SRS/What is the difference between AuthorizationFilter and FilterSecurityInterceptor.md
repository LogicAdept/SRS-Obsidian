<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is the difference between `AuthorizationFilter` and `FilterSecurityInterceptor`?

> [!abstract] Short answer
> Both are the **last URL enforcer** in a servlet chain. **`FilterSecurityInterceptor`** is the **legacy** `AbstractSecurityInterceptor`: `FilterInvocation` metadata + **`AccessDecisionManager`** + **voters**. **`AuthorizationFilter`** (since **5.5**, Spring Security **6** DSL) asks an **`AuthorizationManager`** with a **lazy** `Supplier<Authentication>` — the same API as method security. `http.authorizeHttpRequests(...)` installs the new filter; `authorizeRequests` installed the old one. Spring Security **7** removed `authorizeRequests`. [[What is ExceptionTranslationFilter in Spring Security]] still **wraps** whichever enforcer you keep.

## Same slot, different decision API

```d2
direction: down
etf: "ExceptionTranslationFilter" {
  width: 260
  height: 40
}
old: "FilterSecurityInterceptor\nAccessDecisionManager + voters" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
new: "AuthorizationFilter\nAuthorizationManager" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

etf -> old: "authorizeRequests"
etf -> new: "authorizeHttpRequests"
```

**Fig. 1.** `AuthorizationManager` **supersedes** `AccessDecisionManager` / `AccessDecisionVoter`. The new filter skips metadata sources and `ConfigAttribute` lists. Official migration notes: delayed `Authentication` lookup (only when a rule needs it) and reuse of the same manager types as method interceptors. See [[What is AuthorizationFilter in Spring Security]], [[What is FilterSecurityInterceptor]], and [[How do you configure authorizeHttpRequests in Spring Security 6]].

`FilterSecurityInterceptor` defaulted to **once-per-request** (`observeOncePerRequest`). `AuthorizationFilter` runs on **every dispatch** (`REQUEST`, `FORWARD`, `ERROR`, `INCLUDE`). A 5.x app that never authorized an error forward can start denying it after the switch. [[What is FilterOrderRegistration]] lists **both** classes near the end of the table; `SwitchUserFilter` is still last.

```java
http.authorizeHttpRequests((authorize) -> authorize
        .anyRequest().authenticated());
```

**Listing 1.** Spring Security 6/7 wiring. This bean path creates `AuthorizationFilter`, not `FilterSecurityInterceptor`. Keep `authorizeRequests` (or old XML without `use-authorization-manager`) only while you still compile against a stack that has it.

> [!warning] Two enforcers in TRACE is leftover DSL
> If DEBUG shows **both** filters, you still have `authorizeRequests` **and** `authorizeHttpRequests` (or mixed XML). Drop the old DSL. They do **not** replace each other: `addFilterAt` with a second enforcer **does not** remove the first.

> [!tip] Interview answer
> FilterSecurityInterceptor was the old last filter: metadata source, AccessDecisionManager, voters. AuthorizationFilter is the Spring Security 6 replacement: it calls AuthorizationManager with a Supplier of Authentication, the same pattern as method security. authorizeHttpRequests installs the new one; ExceptionTranslationFilter still sits above it and turns AccessDeniedException into 401 or 403.
