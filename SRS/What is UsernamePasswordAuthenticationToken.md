<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# What is UsernamePasswordAuthenticationToken?

> [!abstract] Short answer
> **UsernamePasswordAuthenticationToken** is Spring Security’s **`Authentication`** type for username/password credentials. An **unauthenticated** token (principal + password) is submitted to **`AuthenticationManager`**; a successful provider returns an **authenticated** token with **`GrantedAuthority`** instances and usually a **`UserDetails`** principal.

## Unauthenticated vs authenticated tokens

The class has two construction paths:

| Form | `isAuthenticated()` | Typical use |
|---|---|---|
| Two-arg `(principal, credentials)` or `unauthenticated(...)` | **`false`** | Login request before validation |
| Three-arg `(principal, credentials, authorities)` or `authenticated(...)` | **`true`** | Trusted result from `AuthenticationManager` / `AuthenticationProvider` |

The two-arg constructor is safe for application code creating a login request. The three-arg constructor is intended for **`AuthenticationManager`** or **`AuthenticationProvider`** implementations that produce a **trusted** authenticated token.

Calling **`setAuthenticated(true)`** on a two-arg token throws **`IllegalArgumentException`** — you cannot promote an untrusted token to authenticated by flipping the flag.

## Where it appears in the servlet flow

On form login, **`UsernamePasswordAuthenticationFilter`** reads **`username`** and **`password`** from the request and builds an **unauthenticated** **`UsernamePasswordAuthenticationToken`**. That token is passed to **`ProviderManager`**, which delegates to providers such as **`DaoAuthenticationProvider`**.

On success, **`DaoAuthenticationProvider`** returns a new **authenticated** token: principal is typically **`UserDetails`**, credentials may remain until **`eraseCredentials()`** runs, and authorities come from the loaded user.

```d2
direction: right
req: "POST /login\nusername + password" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
filter: "UsernamePasswordAuthenticationFilter" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
unauth: "UsernamePasswordAuthenticationToken\nisAuthenticated = false" {
  width: 280
  height: 80
  style.fill: "#fce4ec"
}
mgr: "ProviderManager\n(DaoAuthenticationProvider)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
auth: "UsernamePasswordAuthenticationToken\nauthorities + UserDetails" {
  width: 280
  height: 80
  style.fill: "#c8e6c9"
}

req -> filter -> unauth -> mgr -> auth
```

**Fig. 1.** Form login: filter builds an unauthenticated token; the manager returns an authenticated one on success.

```java
Authentication request = UsernamePasswordAuthenticationToken
    .unauthenticated("alice", "secret");
Authentication response = authenticationManager.authenticate(request);
// response.isAuthenticated() == true; principal is usually UserDetails
```

**Listing 1.** REST login pattern from the Spring Security reference — unauthenticated request in, authenticated token out.

> [!warning] Returning a two-arg token is not a successful login
> A custom **`AuthenticationProvider`** that returns **`new UsernamePasswordAuthenticationToken(user, pass)`** (two-arg) leaves **`isAuthenticated()` false**. Callers treat that as an incomplete authentication. Return the three-arg form, or use **`UsernamePasswordAuthenticationToken.authenticated(principal, credentials, authorities)`**. See [[What is AuthenticationManager and AuthenticationProvider in Spring Security]] and [[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]].

> [!tip] Interview answer
> UsernamePasswordAuthenticationToken wraps username and password for Spring Security. The filter creates an unauthenticated two-arg token for ProviderManager; DaoAuthenticationProvider returns an authenticated three-arg token with authorities. Mixing those up — or calling setAuthenticated(true) on a two-arg token — is a common custom-auth bug.
