<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `AnonymousAuthenticationFilter`?

> [!abstract] Short answer
> A late authentication filter (`GenericFilterBean`) that, if `SecurityContextHolder` still has **no** `Authentication`, puts an **`AnonymousAuthenticationToken`** there (default principal **`anonymousUser`**, authority **`ROLE_ANONYMOUS`**). On by default with `@EnableWebSecurity`. There is **no** conceptual difference from “not logged in” — it is a **placeholder** so the rest of the chain is not dealing with `null`. `Authentication.isAuthenticated()` is **true**. Use **`AuthenticationTrustResolver.isAnonymous()`**, not a role-name check.

## After real login filters

```d2
direction: down
real: "form / Basic / Bearer …" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
anon: "AnonymousAuthenticationFilter\nif context empty" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
etf: "ExceptionTranslationFilter" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
authz: "AuthorizationFilter" {
  width: 220
  height: 40
  style.fill: "#fce4ec"
}

real -> anon
anon -> etf
etf -> authz
```

**Fig. 1.** Architecture lists it as the **last authentication filter**. Put tenant/authorization filters **`addFilterAfter(..., AnonymousAuthenticationFilter.class)`**. See [[What is addFilterAfter in Spring Security]].

Three types: **`AnonymousAuthenticationToken`**, **`AnonymousAuthenticationProvider`** (same **`key`** as the filter), **`AnonymousAuthenticationFilter`**. The filter does **not** overwrite an existing `Authentication`. `http.servletRequest.getUserPrincipal()` / MVC `Authentication` method args stay **`null`** for anonymous — use **`@CurrentSecurityContext`**.

`ExceptionTranslationFilter` uses `isAnonymous`: anonymous + access denied → **`AuthenticationEntryPoint`** (login / 401), not 403. That is why `anyRequest().authenticated()` sends guests to login. **`permitAll()`** does not require an `Authentication`. Forgetting `permitAll` on `/login` or `/css/**` is the usual “public page 401/redirect loop.” See [[How do you configure authorizeHttpRequests in Spring Security 6]] and [[What is ExceptionTranslationFilter in Spring Security]].

```java
http.anonymous((anonymous) -> anonymous.disable()); // Authentication stays null — NPEs in assuming code

http.anonymous((anonymous) -> anonymous.authorities("ROLE_ANON")); // default is ROLE_ANONYMOUS
```

**Listing 1.** `HttpSecurity.anonymous` (on by default). Disable only if you want **`null`**. Custom authorities make `hasRole("ANONYMOUS")` lie — hence **`isAnonymous()`**, not the role string.

> [!warning] Anonymous is still “authenticated” on the token
> TRACE shows `Authenticated=true` and `ROLE_ANONYMOUS`. `authenticated()` in the DSL **rejects** that token. Do not write `if (authentication.isAuthenticated())` to mean “logged in.”

> [!tip] Interview answer
> AnonymousAuthenticationFilter fills an empty SecurityContext with AnonymousAuthenticationToken so filters are not staring at null. It runs after real authentication filters, default ROLE_ANONYMOUS. ExceptionTranslationFilter treats that as not logged in and starts the entry point. Disable it and you get null; prefer isAnonymous over checking the role name.
