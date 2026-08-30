<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Framework/WebFlux #SRS

# What is `ReactiveAuthenticationManager`?

> [!abstract] Short answer
> **`ReactiveAuthenticationManager`** is Spring Security’s **non-blocking `AuthenticationManager`**: a `@FunctionalInterface` with **`Mono<Authentication> authenticate(Authentication)`** (since **5.0**). Success → **`Mono` of authenticated `Authentication`**; unknown → **empty `Mono`**; failure → **error `Mono`** (typically `AuthenticationException`). Username/password from a **`ReactiveUserDetailsService`** uses **`UserDetailsRepositoryReactiveAuthenticationManager`**.

## One method, three outcomes

Javadoc: *Determines if the provided `Authentication` can be authenticated.*

| Result | Meaning |
| --- | --- |
| **`Mono` with `Authentication`** | Authenticated (token usually `isAuthenticated() == true`) |
| **Empty `Mono`** | This manager **cannot decide** (try the next, if delegated) |
| **Error `Mono`** | Authentication **failed** |

Known implementations include **`UserDetailsRepositoryReactiveAuthenticationManager`**, **`JwtReactiveAuthenticationManager`**, OAuth2/OIDC login managers, **`ReactivePreAuthenticatedAuthenticationManager`**, **`DelegatingReactiveAuthenticationManager`**, and **`ReactiveAuthenticationManagerAdapter`** (wraps servlet **`AuthenticationManager`**).

Username/password + map users: [[What is UserDetailsRepositoryReactiveAuthenticationManager]], [[What is MapReactiveUserDetailsService]]. HTTP wiring: [[How does Spring Security work with WebFlux]].

```java
ReactiveAuthenticationManager authenticationManager = authentication -> {
    authentication.setAuthenticated("Trusted Org Unit".equals(authentication.getName()));
    return Mono.just(authentication);
};
```

**Listing 1.** Conceptual Spring Security reactive X.509 sample — a **lambda** manager (no `UserDetails` lookup). Prefer a real class in production.

```d2
direction: down
token: "Authentication\n(credentials)" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
mgr: "authenticate() → Mono" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
ok: "authenticated token" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
empty: "empty (skip)" {
  width: 160
  height: 50
  style.fill: "#fff8e1"
}
err: "error (fail)" {
  width: 160
  height: 50
  style.fill: "#fce4ec"
}

token -> mgr
mgr -> ok
mgr -> empty
mgr -> err
```

**Fig. 1.** Do not `block()` inside `authenticate` to “get a `User`” — that pins the event loop.

## Blocking stores

**`ReactiveAuthenticationManagerAdapter`**: many credential stores (**JDBC, LDAP**) have **no reactive API**, and password hashes are **intentionally slow**. The adapter exists so that work can run **on another scheduler** (`setScheduler`). A custom `authenticate` that calls **`JdbcTemplate`** on the Netty thread is still an outage — [[How does the WebFlux event loop work]], [[How do you offload blocking work in WebFlux]].

> [!warning] Empty vs error
> Empty means **not this manager**. Error means **bad credentials / disabled user**. Returning empty on a password mismatch can skip to a manager that **succeeds by accident**.

> [!warning] `AuthenticationManager` is the servlet type
> Injecting `DaoAuthenticationProvider` into WebFlux does not implement this interface unless you wrap it with **`ReactiveAuthenticationManagerAdapter`** (and a scheduler).

> [!warning] Mutating the incoming token
> The X.509 sample calls `setAuthenticated` on the **provided** instance. Prefer returning a **new** authenticated token (`UsernamePasswordAuthenticationToken.authenticated(...)`) so you do not share a mutable unauthenticated object.

> [!tip] Interview answer
> **`ReactiveAuthenticationManager.authenticate` returns `Mono<Authentication>` — success, empty, or error.** Form/Basic typically use `UserDetailsRepositoryReactiveAuthenticationManager` + `ReactiveUserDetailsService`. Never block the event loop in `authenticate`; wrap blocking `AuthenticationManager` with the adapter and a scheduler.
