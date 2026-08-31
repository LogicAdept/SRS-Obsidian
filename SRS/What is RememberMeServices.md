<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is RememberMeServices?

> [!abstract] Short answer
> **`RememberMeServices`** is the SPI for **cookie-based “remember me.”** Three methods: **`loginSuccess`** after interactive login (form/Basic), **`loginFail`** after a bad attempt, **`autoLogin`** when **`SecurityContextHolder` is empty**. Stock filters call it; **`RememberMeAuthenticationFilter`** is the one that **`autoLogin`s**. Implementations: **hash cookie** (**`TokenBasedRememberMeServices`**) or **persistent series/token** (**`PersistentTokenBasedRememberMeServices`**). If you never call **`http.rememberMe()`**, the filters use **`NullRememberMeServices`** — a **no-op**, not an error. This is **not** a Bearer JWT.

## Cookie on success, Authentication on a later request

Javadoc: **`AbstractAuthenticationProcessingFilter`** and **`RememberMeAuthenticationFilter`** invoke the interface. Spring does **not** inspect the cookie itself — the implementation decides validity and must **silently invalidate** a forged one. **`autoLogin`** should return an **`Authentication`** the **`AuthenticationManager`** accepts; recommended type **`RememberMeAuthenticationToken`** ([[What is RememberMeAuthenticationFilter]], [[What is UsernamePasswordAuthenticationFilter]], [[How do you configure HTTP Basic authentication in Spring Security]]).

**`loginSuccess`** should **not** always set a cookie. Look for an explicit POST parameter (default **`remember-me`**). The clock for hash tokens starts at that **interactive** login, not at the last auto-login. **`loginFail`** must cancel tokens on the request. Logout is a separate **`LogoutHandler`** on **`AbstractRememberMeServices`** ([[How do you implement logout in Spring Security]], [[What is AuthenticationSuccessHandler in Spring Security]], [[What is AuthenticationFailureHandler]]).

**Hash:** Base64 `username:expiry:algorithmName:hex(username:expiry:password:key)`. Default signature **SHA-256** (**`encodingAlgorithm` since 5.8**). Needs **`UserDetailsService`** so the **password** can be re-hashed. Password change or **key** change invalidates cookies. Default lifetime **14 days** (`tokenValiditySeconds`). Negative max-age → session cookie. **Persistent:** **`PersistentTokenRepository`** (typically JDBC) stores **series/token** so theft can be detected. Official docs prefer persistent for higher security ([[How do you configure remember-me in Spring Security]], [[What is UserDetails and UserDetailsService in Spring Security]]).

Remember-me is **`IS_AUTHENTICATED_REMEMBERED`**, not **fully authenticated** ([[What is IS_AUTHENTICATED_ANONYMOUSLY]]).

```java
public interface RememberMeServices {
	Authentication autoLogin(HttpServletRequest request, HttpServletResponse response);
	void loginFail(HttpServletRequest request, HttpServletResponse response);
	void loginSuccess(HttpServletRequest request, HttpServletResponse response,
			Authentication successfulAuthentication);
}
```

**Listing 1.** Contract (**7.1.1**). **`autoLogin` may return `null`**.

```java
@Bean
RememberMeServices rememberMeServices(UserDetailsService users) {
	return new TokenBasedRememberMeServices("change-this-key", users);
}
```

**Listing 2.** Hash implementation. Wire **`http.rememberMe((r) -> r.rememberMeServices(services))`** or use the DSL **`key` / `tokenRepository`**.

```d2
direction: down
ok: "loginSuccess\nset cookie if parameter present" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
later: "empty SecurityContext\nRememberMeAuthenticationFilter" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
al: "autoLogin → RememberMeAuthenticationToken" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}

ok -> later -> al
```

**Fig. 1.** Interactive login **writes** the cookie. A later request **without a session** **reads** it.

> [!warning] Unconfigured means no-op
> **`NullRememberMeServices`** is the default on form/Basic filters. Missing **`http.rememberMe()`** does **not** throw. A **weak `key`** forges **hash** cookies. **Username is in the hash cookie** (no DB). **JWT `STATELESS` APIs** should not use this cookie as an access token.

> [!warning] Auto-login is not fully authenticated
> **`fullyAuthenticated()`** **denies** remember-me. Stolen hash cookies work until **expiry / password / key** change; persistent tokens can **revoke** a series. Always use **TLS**; this is still a **browser credential**.

> [!tip] Interview answer
> RememberMeServices is how Spring Security sets and consumes a remember-me cookie: loginSuccess after a checkbox login, autoLogin when the session is gone, loginFail and logout to cancel it. TokenBasedRememberMeServices signs username and expiry with a key; PersistentTokenBasedRememberMeServices stores series/token in a database. If I never enable rememberMe, NullRememberMeServices is a silent no-op.
