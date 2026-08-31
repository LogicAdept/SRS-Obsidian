<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken?

> [!abstract] Short answer
> **Unauthenticated:** **`UsernamePasswordAuthenticationToken.unauthenticated(principal, credentials)`** (**since 5.7**) — two-arg constructor, **`isAuthenticated() == false`**, typically a username **`String`** plus password. That is what **`UsernamePasswordAuthenticationFilter`** sends to **`AuthenticationManager`**. **Authenticated:** **`authenticated(principal, credentials, authorities)`** — three-arg constructor, **`isAuthenticated() == true`**, principal usually **`UserDetails`**, plus authorities (and **`FACTOR_PASSWORD`** in **7.x**). **`setAuthenticated(true)` on an existing instance throws.** A trusted token is always a **new** object from a provider, not the request token flipped in place.

## Two constructors, one trust bit

Javadoc: the **two-arg** constructor is **safe for any code** (`isAuthenticated()` **false**). The **three-arg** constructor is **only** for an **`AuthenticationManager` / `AuthenticationProvider`** that is satisfied the token is trusted ([[What is UsernamePasswordAuthenticationToken]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]]).

**`setAuthenticated(boolean)`** is overridden: **`true`** → **`IllegalArgumentException`** (*Cannot set this token to trusted - use constructor which takes a GrantedAuthority list instead*). **`false`** is allowed (un-trust). You cannot promote the filter’s token; **`DaoAuthenticationProvider.createSuccessAuthentication`** builds a **new** **`authenticated(...)`** with the **original** credentials object, mapped authorities, and **`FactorGrantedAuthority.PASSWORD_AUTHORITY`** ([[What is DaoAuthenticationProvider]], [[What is a principal in Spring Security]], [[How does form login work internally in Spring Security]]).

**`AbstractSecurityInterceptor`** uses **`isAuthenticated()`** to decide whether to call **`AuthenticationManager` again**. A forged three-arg token in **`SecurityContextHolder`** **skips** **`PasswordEncoder.matches`**. **`ProviderManager`** then **`eraseCredentials()`** (default **on**), which nulls **`credentials`** on the success token; **`User`** as principal can also be erased if reused from a cache.

Request token: principal **`String`**, credentials password, **empty authorities**. Success token: principal **`UserDetails`** unless **`forcePrincipalAsString`**. Same class, **different instances**.

```java
UsernamePasswordAuthenticationToken request =
		UsernamePasswordAuthenticationToken.unauthenticated("alice", "secret");
// request.isAuthenticated() == false
```

**Listing 1.** Filter / REST login input. **`unauthenticated`** is the two-arg constructor.

```java
Authentication result = authenticationManager.authenticate(request);
// result instanceof UsernamePasswordAuthenticationToken
// result.isAuthenticated() == true
// result != request
```

**Listing 2.** Provider output is a **new** **`authenticated(...)`** token. **`request.setAuthenticated(true)`** throws.

```d2
direction: down
req: "unauthenticated(username, password)\nisAuthenticated false" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
mgr: "AuthenticationManager.authenticate" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
ok: "authenticated(UserDetails, creds, authorities)\nisAuthenticated true" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

req -> mgr -> ok
```

**Fig. 1.** Trust is a **constructor choice**, not a setter. The interceptor trusts **`true`** without hashing again.

> [!warning] Do not use the three-arg constructor in application code
> **`authenticated(user, password, List.of(new SimpleGrantedAuthority("ROLE_ADMIN")))`** in a filter **is** a logged-in admin with **no** password check. The dump that “reuses the unauthenticated token” is slightly wrong: you **cannot** flip the flag; the real hole is **minting** the trusted constructor yourself.

> [!warning] `isAuthenticated()` is not “has a session”
> Anonymous tokens are authenticated **`true`** with a different type. This class’s **`false`** means **“present me to the manager.”** After success, **`eraseCredentials`** leaves **`getCredentials() == null`**; do not stash the same **`User`** instance in a cache if the provider will erase its password.

> [!tip] Interview answer
> Unauthenticated UsernamePasswordAuthenticationToken.unauthenticated holds the raw username and password and isAuthenticated is false so AuthenticationManager must run. On success DaoAuthenticationProvider returns a different authenticated(...) token with UserDetails and authorities; setAuthenticated(true) on the old instance throws. I never call the three-arg constructor myself because that skips PasswordEncoder.
