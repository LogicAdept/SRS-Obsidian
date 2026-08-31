<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# How do you implement logout in Spring Security?

> [!abstract] Short answer
> **`EnableWebSecurity` already installs logout.** **`POST /logout`** (CSRF token required) runs a list of **`LogoutHandler`s**: invalidate the **`HttpSession`**, clear **`SecurityContextHolder`** and **`SecurityContextRepository`**, drop remember-me and CSRF state, then fire **`LogoutSuccessEvent`**. Default **`LogoutSuccessHandler`** redirects to **`/login?logout`**. **`GET /logout`** does **not** log the user out when CSRF is on — it serves the generated **confirmation page** (CSRF field included). Customize with **`http.logout(Customizer)`**. A JWT API still clears the request context; the **token stays valid** until expiry unless you revoke it.

## LogoutFilter runs before authorization

**`LogoutFilter`** sits **ahead of `AuthorizationFilter`**, so the default **`/logout`** URL does **not** need **`permitAll`**. It polls **`LogoutHandler`s** in order, then **`LogoutSuccessHandler`**. Handlers are for **cleanup** and **must not throw**; the success handler may ([[What is LogoutFilter]], [[What is SecurityContextLogoutHandler]]).

Default POST `/logout` stack (servlet logout reference):

1. **`SecurityContextLogoutHandler`** — invalidate session (**default `true`**), clear authentication, clear the repository (drops **`JSESSIONID`**; you do **not** also **`deleteCookies("JSESSIONID")`**).
2. Remember-me (**`TokenBasedRememberMeServices` / `PersistentTokenBasedRememberMeServices`**) if configured ([[How do you configure remember-me in Spring Security]]).
3. **`CsrfLogoutHandler`** — remove the saved CSRF token ([[What is CsrfFilter in Spring Security]]).
4. **`LogoutSuccessEventPublishingLogoutHandler`**.
5. Redirect **`/login?logout`** (**`SimpleUrlLogoutSuccessHandler`**). That matches the generated login form’s **`?logout`** banner ([[How do you create a custom login form in Spring Security]]).

**`GET /logout`** (CSRF **enabled**): **`DefaultLogoutPageGeneratingFilter`** renders a confirm page whose POST carries the CSRF token. CSRF **disabled**: no confirm page; **`logoutUrl`** accepts **any HTTP method** — **`LogoutConfigurer`** still calls GET-as-logout a bad practice. Use **`logoutRequestMatcher`** only if you insist.

**`logoutUrl("/my/logout")`** only changes **`LogoutFilter`**. A **custom success MVC URL** is processed **after** Security, so **`logoutSuccessUrl(...).permitAll()`** (or **`authorizeHttpRequests`**) is required. **`logoutSuccessHandler`** **replaces** **`logoutSuccessUrl`**. APIs often use **`HttpStatusReturningLogoutSuccessHandler`**. **`addLogoutHandler`** / **`deleteCookies`** / **`HeaderWriterLogoutHandler(ClearSiteDataHeaderWriter)`** run **before** the default session/context handlers.

A home-grown **`@PostMapping` logout** must call **`SecurityContextLogoutHandler.logout(...)`** or the context can survive the next request. Prefer the DSL.

Stateless / JWT: **`STATELESS`** means there is **no session cookie** to kill; logout still **clears this request’s context**. The bearer token remains usable until it expires unless the issuer **revokes** it or you keep a denylist ([[How do you implement custom token-based authentication in Spring Security]]). OIDC apps use a separate RP-initiated logout success handler, not this cookie flow.

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.formLogin(Customizer.withDefaults())
		.logout((logout) -> logout
			.logoutUrl("/logout")
			.logoutSuccessUrl("/login?logout")
			.deleteCookies("remember-me")
			.permitAll()
		);
	return http.build();
}
```

**Listing 1.** **`logout(Customizer)`** (7.x). Default URLs are already **`/logout`** and **`/login?logout`** — shown here explicitly. **`permitAll()`** on the DSL opens the **success** page for anonymous users after the session is gone; the filter itself already matches **`/logout`**.

```java
http.logout((logout) -> logout
	.logoutSuccessHandler(new HttpStatusReturningLogoutSuccessHandler())
);
```

**Listing 2.** JSON API: **200** (or a chosen status) instead of a login redirect.

```d2
direction: down
get: "GET /logout\nconfirm page + CSRF" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
post: "POST /logout + CSRF" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
handlers: "LogoutHandlers\nsession, context, remember-me, CSRF" {
  width: 300
  height: 70
  style.fill: "#fce4ec"
}
ok: "LogoutSuccessHandler\n/login?logout or 200" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

get -> post -> handlers -> ok
```

**Fig. 1.** Confirm with GET; **mutate** with POST. Skipping CSRF on a cookie session makes **GET logout** a one-click CSRF.

> [!warning] GET does not log you out (CSRF on)
> The dump that “GET `/logout` is gone” is wrong for **7.x**: GET shows the **confirm** page. The dump that “POST + CSRF is the action” is right. **`http.logout().logoutUrl(...)`** chaining is gone — use a **`Customizer`**. Logging out with **GET** while CSRF is **off** is how a forged image tag ends a session.

> [!warning] Custom MVC logout without SecurityContextLogoutHandler
> Redirecting to `/home` from your own controller **without** **`SecurityContextLogoutHandler`** leaves the user **authenticated** on the next request. **`logoutSuccessHandler`** ignores **`logoutSuccessUrl`**. Deleting **`JSESSIONID`** yourself is redundant with session invalidation.

> [!tip] Interview answer
> I use the default LogoutFilter: POST /logout with a CSRF token runs SecurityContextLogoutHandler, remember-me cleanup, and CsrfLogoutHandler, then redirects to /login?logout. GET /logout only shows the generated confirm page while CSRF is enabled. For an API I swap in HttpStatusReturningLogoutSuccessHandler; a JWT is not invalidated by clearing the SecurityContext unless I revoke it.
