<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is the difference between ROLE_USER and ROLE_ANONYMOUS?

> [!abstract] Short answer
> **`ROLE_ANONYMOUS`** is the **stock authority** **`AnonymousAuthenticationFilter`** puts on an **`AnonymousAuthenticationToken`** when the context is empty (principal **`anonymousUser`**, **on by default**). **`ROLE_USER`** has **no special meaning** in Spring Security — it is only present if **you** (or Boot’s generated user) put it on **`UserDetails`**, typically **`User.roles("USER")`**. Prefer **`anonymous()` / `isAnonymous()` / `AuthenticationTrustResolver`** over matching **`ROLE_ANONYMOUS` by name**. **`hasRole("USER")`** looks for **`ROLE_USER`** and **does not** match anonymous.

## Framework guest versus an application role

Both are **`GrantedAuthority` strings** with the **`ROLE_`** prefix. Authorization does not treat them as a pair of built-in levels ([[What is the difference between a role and an authority in Spring Security]], [[What is AnonymousAuthenticationToken]], [[What is AnonymousAuthenticationFilter]]).

| | **`ROLE_ANONYMOUS`** | **`ROLE_USER`** |
| --- | --- | --- |
| Who assigns it | **`AnonymousAuthenticationFilter`** (default) | Your **`UserDetails`** / **`User.roles("USER")`** |
| Principal | **`"anonymousUser"`** | A real username |
| Token type | **`AnonymousAuthenticationToken`** | Usually **`UsernamePasswordAuthenticationToken`** |
| **`isAuthenticated()`** | **`true`** (trap) | **`true`** after login |
| **`authenticated()`** | **Deny** | **Allow** |
| **`hasRole("USER")`** | **Deny** | **Allow** if you granted it |
| Official matcher | **`anonymous()`** / **`isAnonymous()`** | **`hasRole("USER")`** |

Official anonymous chapter: putting **`ROLE_ANONYMOUS`** on an interceptor matches **only that authority**. Logged-in users **typically do not keep it**, so they **fail** a “anonymous role” rule. Trust APIs (**`AuthenticatedAuthorizationManager.anonymous()`**, **`IS_AUTHENTICATED_ANONYMOUSLY`**) inspect **token type / trust resolver**, not that string ([[What is IS_AUTHENTICATED_ANONYMOUSLY]], [[What is hasRole versus hasAuthority in Spring Security]]).

**`permitAll()`** allows **everyone** (session is not consulted). **`authenticated()`** **rejects** anonymous. **`anonymous()`** requires the caller **still be** anonymous. Disabling anonymous (**`http.anonymous(AbstractHttpConfigurer::disable)`**) leaves **`getAuthentication()` null** instead of **`ROLE_ANONYMOUS`**. Anonymous **`AccessDeniedException`** is a **login challenge**, not **403** ([[What is the difference between HTTP 401 and 403 in Spring Security]], [[What is AuthenticationEntryPoint]]).

Boot’s generated user often has **`ROLE_USER`**. That is **Boot auto-config**, not a Security-wide default for every `UserDetails`.

```java
http.authorizeHttpRequests((authorize) -> authorize
	.requestMatchers("/login", "/css/**").permitAll()
	.requestMatchers("/me/**").hasRole("USER")
	.anyRequest().authenticated());
```

**Listing 1.** Public pages: **`permitAll`**, not **`hasRole("ANONYMOUS")`**. **`hasRole("USER")`** needs **`User.roles("USER")`** (or equivalent) after login.

```java
User.builder()
	.username("user")
	.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
	.roles("USER")
	.build();
```

**Listing 2.** Stores **`ROLE_USER`**. Anonymous traffic never gets this object.

```d2
direction: down
guest: "AnonymousAuthenticationToken\nanonymousUser + ROLE_ANONYMOUS" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
user: "logged-in Authentication\nROLE_USER only if you assigned it" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
auth: "authenticated() / hasRole(\"USER\")" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}

guest -> auth: "deny"
user -> auth: "allow if ROLE_USER present"
```

**Fig. 1.** **`ROLE_ANONYMOUS`** is the **guest placeholder**. **`ROLE_USER`** is **your** role name.

> [!warning] Anonymous is not `permitAll`
> **`authenticated()`** fails for **`ROLE_ANONYMOUS`**. **`hasRole("ANONYMOUS")`** fails for a logged-in **`ROLE_USER`**. Mixing **`hasRole("USER")`** on a page you meant to be public is the usual **login redirect**. **`isAuthenticated() == true`** on the anonymous token is **not** “logged in.”

> [!warning] Do not authorize on the `ROLE_ANONYMOUS` string
> Prefer **`anonymous()`** / **`isAnonymous()`**. If you **`anonymous(AbstractHttpConfigurer::disable)`**, there is **no** **`ROLE_ANONYMOUS`** and a null-check on **`Authentication`** starts to matter. XML **`access="ROLE_USER"`** only works if login **actually grants** that authority.

> [!tip] Interview answer
> ROLE_ANONYMOUS is what AnonymousAuthenticationFilter assigns to guests — principal anonymousUser, on by default. ROLE_USER is not built in; you grant it on UserDetails, usually User.roles("USER"). authenticated() and hasRole("USER") reject anonymous. I detect guests with anonymous() or AuthenticationTrustResolver, not by matching ROLE_ANONYMOUS, and I do not treat permitAll as the same as anonymous.
