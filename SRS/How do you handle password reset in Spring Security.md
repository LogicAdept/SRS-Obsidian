<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Java/Spring/Security/Authentication #SRS

# How do you handle password reset in Spring Security?

> [!abstract] Short answer
> Spring Security **does not ship a forgotten-password filter or `/reset-password` controller**. You own request, mail, token, and verify. Persist the new secret with **`PasswordEncoder.encode`**, then **`UserDetailsPasswordService.updatePassword`** (already-encoded) or **`UserDetailsManager.updateUser`**. **`UserDetailsManager.changePassword(old, new)`** is for the **current** authenticated user who still knows the old password. **`passwordManagement()`** only redirects password managers from **`/.well-known/change-password`**.

## Forgotten reset is application code

Password Storage says most apps need a way to **update** a password, then shows **`http.passwordManagement()`** — a **Well-Known URL** that redirects to **your** change-password page (default **`/change-password`**). Compromised-password handling likewise redirects to **`/reset-password`** as **your** path. Neither endpoint implements mail or a token.

So a forgotten-password flow is a controller plus storage:

1. Accept an identifier (username / email). Do not require an existing **`Authentication`**.
2. Create a **one-time** token, store it with an **expiry**, mail a link.
3. On submit, **consume** the token (reject missing, expired, or reused).
4. Encode the new password and persist it.

**`InMemoryOneTimeTokenService`** (OTT **login**, since 6.4) is the framework’s own mailed-token pattern: **random UUID**, **expiry** (default **5 minutes**), **`consume`** returns **`null`** if invalid. That is **magic-link login**, not a password write. After OTT the user is authenticated; they still have not reset a forgotten password.

```java
String encoded = passwordEncoder.encode(rawNewPassword);
userDetailsPasswordService.updatePassword(user, encoded);
```

**Listing 1.** Conceptual persist step. **`PasswordEncoder.encode`** is a one-way adaptive hash. **`updatePassword`**’s Javadoc requires **`newPassword` already encoded** by the configured encoder.

```java
http
	.passwordManagement((management) -> management
		.changePasswordPage("/update-password")
	);
```

**Listing 2.** Password-manager discovery only. **`/.well-known/change-password`** redirects to **`/update-password`**. Wire that page yourself; it is not forgotten-password mail.

## `changePassword` is not forgotten-password

**`UserDetailsManager.changePassword(oldPassword, newPassword)`** “Modify the **current** user’s password.” **`JdbcUserDetailsManager`** reads **`SecurityContext`**, optionally re-authenticates **`oldPassword`** through **`AuthenticationManager`**, then **`UPDATE`s the password column with the string you passed** — it does **not** call **`encode`**. No **`Authentication`** → **`AccessDeniedException`**. A user who forgot the password cannot use this API.

| API | Who is logged in? | Old password | Encoding |
| --- | --- | --- | --- |
| **`changePassword(old, new)`** | **Current** user required | Re-checked if an **`AuthenticationManager`** is set | You pass what gets stored — **encode first** |
| **`UserDetailsPasswordService.updatePassword(user, new)`** | Any user you load | No | **`new` must already be encoded** |
| **`JdbcUserDetailsManager.updatePassword`** (7.0+) | Any user you load | No | Same, and **`setEnableUpdatePassword(true)`** or it is a no-op |

After a successful reset, expire other sessions so old logins die with the old password. Reactive Concurrent Sessions Control shows this with **`ReactiveSessionRegistry`** “when a user changes their password.”

```d2
direction: down
forgot: "Forgot password\n(no Authentication)" {
  width: 240
  height: 60
  style.fill: "#fce4ec"
}
logged: "Logged in, knows old password" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
app: "Your token + mail + consume" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
upd: "encode + updatePassword / updateUser" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
chg: "UserDetailsManager.changePassword" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ott: "oneTimeTokenLogin()\nlogs in, does not set password" {
  width: 280
  height: 60
  style.fill: "#f3e5f5"
}

forgot -> app
app -> upd
logged -> chg
forgot -> ott: "not the same feature"
```

**Fig. 1.** Reset is **unauthenticated persist**. **`changePassword`** is **authenticated rotate**. OTT is **login**.

Permit the public request and submit URLs (**`permitAll`**), keep **CSRF** on those POSTs, and use **`DelegatingPasswordEncoder`** / **`PasswordEncoderFactories.createDelegatingPasswordEncoder()`** for storage ([[What is PasswordEncoder in Spring Security]], [[What is the difference between encode and matches on PasswordEncoder]], [[What is UserDetailsManager versus UserDetailsService]]).

> [!warning] Do not call `changePassword` from a reset form
> Forgotten password means **no** current **`Authentication`** and **no** old password. **`JdbcUserDetailsManager.changePassword`** throws **`AccessDeniedException`** without a context user, and it **stores `newPassword` verbatim**. Passing the raw form field writes plaintext. Encode, then **`updatePassword`**. On JDBC in **Spring Security 7**, **`updatePassword` is off until `setEnableUpdatePassword(true)`**.

> [!warning] A raw UUID with no expiry is not Spring’s token model
> **`InMemoryOneTimeTokenService`** does use a **UUID**, but it **expires** and **`consume`** is one-shot. A reset row that keeps a forever UUID is the dump’s incomplete recipe. **`oneTimeTokenLogin()`** still **does not change the password**. **`passwordManagement()`** does not send mail.

> [!tip] Interview answer
> Spring Security has no built-in forgot-password endpoint. You mail a short-lived, single-use token, then PasswordEncoder.encode the new password and persist it with UserDetailsPasswordService.updatePassword or updateUser. changePassword is only for the currently authenticated user who still knows the old password, and JdbcUserDetailsManager stores whatever string you pass. passwordManagement() only advertises a change-password URL to password managers.
