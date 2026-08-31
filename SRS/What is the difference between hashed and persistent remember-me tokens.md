<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is the difference between hashed and persistent remember-me tokens?

> [!abstract] Short answer
> Both are **browser cookies** consumed by **`RememberMeAuthenticationFilter.autoLogin`** when the session is gone. **Hashed** tokens (**`TokenBasedRememberMeServices`**) put a **signed payload** in the cookie (`username`, expiry, **password**, **key**) — **no table**. A stolen cookie works from **any client until expiry**; changing the **password** or **key** invalidates it. **Persistent** tokens (**`PersistentTokenBasedRememberMeServices`**) put only **series + token** in the cookie and store the rest in a **`PersistentTokenRepository`**. Each auto-login **rotates the token**; series match with a **wrong token** is **`CookieTheftException`**. Official docs prefer persistent when you need **revocation**.

## Signed cookie versus a pointer into a store

**`RememberMeServices.loginSuccess`** sets the cookie after form/Basic when the remember-me parameter is **`true`**. **`RememberMeAuthenticationFilter`** later calls **`autoLogin`**. Logout clears the cookie via **`LogoutHandler`**. Both strategies need a **`UserDetailsService`**. Default lifetime is **14 days** (`AbstractRememberMeServices.TWO_WEEKS_S`). Neither is a Bearer JWT ([[What is RememberMeServices]], [[What is RememberMeAuthenticationFilter]], [[How do you configure remember-me in Spring Security]]).

| | Hashed (`TokenBasedRememberMeServices`) | Persistent (`PersistentTokenBasedRememberMeServices`) |
| --- | --- | --- |
| Cookie | Base64 `username:expiry:algorithm:signature` | **series** + **token** (no username) |
| Signature | **SHA-256** of username + expiry + **password** + **key** (`encodingAlgorithm` **since 5.8**) | Random token; server compares the **row** |
| Extra store | None | **`PersistentTokenRepository`** (**since 2.0**): **`JdbcTokenRepositoryImpl`** or in-memory for tests |
| Theft | Valid until **expiry** / password / key change | Series OK + token mismatch → **`CookieTheftException`**; remaining tokens for that user should be **deleted** |
| Revoke one device | Change password (all devices) or wait | **`removeUserTokens(username)`** or delete the series row |
| DSL | **`rememberMe.key(...)`** | Also **`tokenRepository(...)`** — **`key` alone is not enough** |

Hash validation reloads **`UserDetails.getPassword()`** and recomputes the digest (Spring compares this to **HTTP Digest**). Persistent **`updateToken`** writes a **new token value** and **`last_used`** on every successful auto-login; **series** stays. Password/status changes should **delete rows** — they are **not** in the cookie signature. Expired persistent rows are **not** auto-purged; run a batch job.

Remember-me is **`IS_AUTHENTICATED_REMEMBERED`**, not fully authenticated ([[What is IS_AUTHENTICATED_ANONYMOUSLY]], [[How do you implement logout in Spring Security]]).

```java
http.rememberMe((remember) -> remember.key("a-long-unpredictable-key"));
```

**Listing 1.** Default **hash** cookie. Omit **`key`** and the configurer generates a **random** one — tokens **die on restart**.

```java
http.rememberMe((remember) -> remember
	.key("a-long-unpredictable-key")
	.tokenRepository(jdbcTokenRepository));
```

**Listing 2.** Switches to **persistent** series/token. You must create the **`persistent_logins`** table (**`JdbcTokenRepositoryImpl`**).

```d2
direction: down
hash: "hash cookie\nusername + expiry + HMAC" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
pers: "persistent cookie\nseries + token pointer" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
db: "PersistentTokenRepository\nrotate token / theft" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

pers -> db
```

**Fig. 1.** Hash is **self-contained**. Persistent is a **pointer** you can revoke and that **detects reuse**.

> [!warning] A guessable hash `key` forges cookies
> The key is a **shared secret** with **`RememberMeAuthenticationProvider`**. Anyone who has it (and can feed the signature the current **password hash**) can mint cookies. Persistent mode still needs that **key**, but **without a `tokenRepository` you stay on hash tokens**.

> [!warning] Stolen hash cookies have no theft signal
> Copying a hash cookie to another browser works until expiry. Persistent **reuse of an old token** after rotation is the theft signal — handle **`CookieTheftException`** (typically force re-login and wipe that user’s series). **`InMemoryTokenRepositoryImpl`** is **not** for production. Always **TLS** + **HttpOnly**.

> [!tip] Interview answer
> Hashed remember-me is a signed cookie over username, expiry, password, and a server key — no database, but a stolen cookie works until it expires or the password changes. Persistent remember-me stores series and token in a PersistentTokenRepository; the cookie is only a pointer, the token rotates, and a mismatch is CookieTheftException. I use hash for demos and persistent when I need to revoke a device.
