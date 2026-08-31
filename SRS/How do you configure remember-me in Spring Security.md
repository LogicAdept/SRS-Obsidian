<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you configure remember-me in Spring Security?

> [!abstract] Short answer
> Call **`http.rememberMe(...)`** on a **`SecurityFilterChain`**. That sets a **cookie** so the browser can be logged in again after the **HTTP session** is gone. **Hash tokens** (`TokenBasedRememberMeServices`) sign username + expiry + password with a **key**. **Persistent tokens** (`PersistentTokenBasedRememberMeServices` + **`PersistentTokenRepository`**) store **series/token** so a stolen cookie can be detected and revoked. Both need a **`UserDetailsService`**. This is a **browser cookie**, not a Bearer JWT.

## Cookie after interactive login

Remember-me remembers the principal **between sessions**. **`UsernamePasswordAuthenticationFilter`** / **`BasicAuthenticationFilter`** call **`RememberMeServices.loginSuccess` / `loginFail`**. **`RememberMeAuthenticationFilter`** calls **`autoLogin`** when **`SecurityContextHolder`** is empty. Logout uses **`LogoutHandler`** to clear the cookie ([[What is RememberMeServices]], [[How do you use form login authentication in Spring Boot]]).

The login form must send the remember-me **parameter** as **`true`** (or set **`alwaysRemember(true)`**). Cookie name defaults to **`remember-me`**, **HttpOnly**. Prefer **`useSecureCookie(true)`** (HTTPS only). Validity: **`tokenValiditySeconds`** — **`TWO_WEEKS_S`** is the constant on **`AbstractRememberMeServices`**.

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.formLogin(Customizer.withDefaults())
		.rememberMe((remember) -> remember.key("a-long-unpredictable-key"));
	return http.build();
}
```

**Listing 1.** Hash-based remember-me (default **`TokenBasedRememberMeServices`**). DSL since **3.2**. XML: `<remember-me key="…"/>`. If you omit **`key`**, the configurer uses a **secure random** key — tokens **die on restart**. Do **not** use a guessable string. Old `.formLogin().and().rememberMe()` chaining is gone with **`WebSecurityConfigurerAdapter`**.

LDAP (and any provider **without** `UserDetailsService`) does **not** issue remember-me unless a **`UserDetailsService` bean** is also present.

## Hash token vs persistent series/token

**Hash cookie** (Base64): `username:expirationTime:algorithmName:hex(username:expirationTime:password:key)`. Default signature algorithm **SHA-256**. A **stolen cookie works from any client until expiry**. Changing the **password** or **key** invalidates all such tokens. Spring compares this to digest authentication.

**Persistent** (Jaspan-style): cookie holds **series + token**, **not** the username. Store:

```sql
create table persistent_logins (
	username varchar(64) not null,
	series varchar(64) primary key,
	token varchar(64) not null,
	last_used timestamp not null
);
```

**Listing 2.** Schema for **`JdbcTokenRepositoryImpl`**. **`InMemoryTokenRepositoryImpl`** is tests only.

```java
http.rememberMe((remember) -> remember
	.key("a-long-unpredictable-key")
	.tokenRepository(jdbcTokenRepository));
```

**Listing 3.** Switching to **`PersistentTokenBasedRememberMeServices`**. On each auto-login the **token** is rotated, **series** stays. Series match + **wrong token** → **`CookieTheftException`**. Password/user-status changes should **delete** that user’s rows. Expired rows are **not** auto-deleted — run a batch job. XML: `<remember-me data-source-ref="…"/>`.

```d2
direction: down
login: "formLogin / httpBasic\nremember-me=true" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
svc: "RememberMeServices\nset cookie" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
later: "No SecurityContext\nRememberMeAuthenticationFilter" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
token: "RememberMeAuthenticationToken\nRememberMeAuthenticationProvider" {
  width: 300
  height: 70
  style.fill: "#f3e5f5"
}

login -> svc -> later -> token
```

**Fig. 1.** Interactive login plants the cookie; a later visit without a session is authenticated from it. Same key must be on **`RememberMeAuthenticationProvider`**. Details: [[What is the difference between hashed and persistent remember-me tokens]].

> [!warning] A weak `key` forges hash tokens
> The key is a **HMAC secret** shared with **`RememberMeAuthenticationProvider`**. Anyone who knows it can mint cookies for any user whose **password hash** they can also feed the signature (the cookie embeds data checked against **`UserDetails.getPassword()`**). Use a long random key and keep it out of source control. A captured **hash** cookie is valid **until expiry** on **any** user agent.

> [!warning] Not a JWT / `STATELESS` API substitute
> Remember-me is a **browser cookie** for **interactive** logins (form, and Basic if hooked). It still needs **`UserDetailsService`**. It does **not** replace Bearer tokens on a JSON API. Persistent tokens without a **unique series** constraint can assign the same series to two users.

> [!tip] Interview answer
> I enable rememberMe on the SecurityFilterChain and set a strong key. The default is a hashed cookie signed with that key and the user’s password — stolen cookies work until they expire or the password changes. For revocation I switch to PersistentTokenBasedRememberMeServices with a JDBC series/token table so theft can throw CookieTheftException. Both require a UserDetailsService; this is not how I authenticate a stateless JWT API.
