<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `RememberMeAuthenticationFilter`?

> [!abstract] Short answer
> A **`GenericFilterBean`** (not `OncePerRequestFilter`) that runs when **`SecurityContext` has no `Authentication`**. It calls **`RememberMeServices.autoLogin`**, then **`AuthenticationManager`**, and puts a **`RememberMeAuthenticationToken`** in the context so the request is logged in **without the form**. The **cookie is written on a previous successful login** (`loginSuccess` from [[What is UsernamePasswordAuthenticationFilter]] / [[What is BasicAuthenticationFilter]] when the `remember-me` parameter is present). It sits **before** [[What is AnonymousAuthenticationFilter]] in [[What is FilterOrderRegistration]].

## Auto-login only if the context is empty

```d2
direction: down
empty: "SecurityContext empty?" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
auto: "RememberMeServices.autoLogin\ncookie → Authentication" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
anon: "AnonymousAuthenticationFilter" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}

empty -> auto: "yes"
empty -> anon: "already authenticated"
auto -> anon: "null or after set"
```

**Fig. 1.** Chain **continues** if there is no cookie or `autoLogin` returns `null`. Optional `AuthenticationSuccessHandler` **stops** the chain and redirects. `LogoutFilter` uses the same services as **`LogoutHandler`** to clear the cookie.

Two **`RememberMeServices`**: **hash cookie** (`TokenBasedRememberMeServices`) vs **DB** (`PersistentTokenBasedRememberMeServices` + `persistent_logins`). Both need a **`UserDetailsService`**. Namespace cookie/parameter default **`remember-me`**, validity **14 days**. Set a unique **`key`**.

```java
http.formLogin(Customizer.withDefaults())
    .rememberMe(Customizer.withDefaults());
```

**Listing 1.** `HttpSecurity.rememberMe`: if the login request has parameter **`remember-me`**, the user stays authenticated after the **`HttpSession` expires**. Persistent store: `tokenRepository` / XML `data-source-ref`.

> [!warning] Cookie login, not JWT
> [[What is BearerTokenAuthenticationFilter]] / `STATELESS` APIs should **not** use this. A stolen **hash** token works from **any** browser until expiry (or a password/`key` change). Persistent tokens are the “more secure” option. LDAP-only setups need an extra `UserDetailsService`.

> [!tip] Interview answer
> RememberMeAuthenticationFilter auto-logs the user from a remember-me cookie only when SecurityContext is empty, then AuthenticationManager accepts a RememberMeAuthenticationToken. The cookie was set on an earlier form or Basic login with the remember-me checkbox. It is not for JWT resource servers. AnonymousAuthenticationFilter runs after it so a successful remember-me login is not overwritten.
