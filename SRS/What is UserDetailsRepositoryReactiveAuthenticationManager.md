<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS

# What is `UserDetailsRepositoryReactiveAuthenticationManager`?

> [!abstract] Short answer
> It is Spring Security’s **username/password `ReactiveAuthenticationManager`** (since **5.0**): it loads **`UserDetails` via `ReactiveUserDetailsService.findByUsername`**, checks the password with a **`PasswordEncoder`**, and on success returns a **`UsernamePasswordAuthenticationToken`**. Same *job* as servlet **`DaoAuthenticationProvider`**, different types — not that class.

## `retrieveUser` + encoder

Javadoc: *A `ReactiveAuthenticationManager` that uses a `ReactiveUserDetailsService` to validate the provided username and password.*

It extends **`AbstractUserDetailsReactiveAuthenticationManager`** (since **5.2**): `authenticate` → `retrieveUser(username)` → validate password → **`UsernamePasswordAuthenticationToken`**. Principal is the **username string or the `UserDetails`**, depending on configuration.

Constructor: **`UserDetailsRepositoryReactiveAuthenticationManager(ReactiveUserDetailsService)`**. Samples pass **`MapReactiveUserDetailsService`** — [[What is MapReactiveUserDetailsService]], [[What is ReactiveAuthenticationManager]].

```java
@Bean
ReactiveAuthenticationManager authenticationManager(ReactiveUserDetailsService users) {
    UserDetailsRepositoryReactiveAuthenticationManager manager =
            new UserDetailsRepositoryReactiveAuthenticationManager(users);
    manager.setPasswordEncoder(PasswordEncoderFactories.createDelegatingPasswordEncoder());
    return manager;
}
```

**Listing 1.** Conceptual wiring. Default encoder on the abstract class is already **`PasswordEncoderFactories.createDelegatingPasswordEncoder()`** — set your own if you do not use `{id}`-prefixed hashes.

Parent **`setScheduler`**: default **`Schedulers.newParallel(...)`** because **modern password encoding is CPU-heavy**. Validation is **bounded by CPU count**. **`NoOpPasswordEncoder`** demos may use **`Schedulers.immediate()`**. That scheduler is **not** `boundedElastic` — dumps mix it up with JDBC offload.

`setUserDetailsPasswordService` upgrades hashes on success (`MapReactiveUserDetailsService` implements **`ReactiveUserDetailsPasswordService`**). `setPostAuthenticationChecks` / `setCompromisedPasswordChecker` (since **6.3**) run extra checks.

```d2
direction: down
auth: "UsernamePassword\nAuthenticationToken" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
mgr: "UserDetailsRepository\nReactiveAuthenticationManager" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
uds: "ReactiveUserDetailsService\nfindByUsername" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

auth -> mgr -> uds
```

**Fig. 1.** HTTP Basic / form login on WebFlux typically land here. Enable: [[What is EnableWebFluxSecurity]].

> [!warning] Not `DaoAuthenticationProvider`
> That provider talks **`UserDetailsService`** (blocking). This class talks **`ReactiveUserDetailsService`** and returns **`Mono<Authentication>`**.

> [!warning] Default scheduler is **parallel**, not `boundedElastic`
> Parallel is for **bcrypt/argon CPU**. **JDBC in `findByUsername`** still blocks whatever thread subscribed — use a **reactive** store or **`subscribeOn`** inside the service. Adapter for a servlet `AuthenticationManager`: **`ReactiveAuthenticationManagerAdapter`**.

> [!warning] Empty user vs bad password
> `retrieveUser`: authentication **failure is an error `Mono`**. Do not map “unknown user” to empty if you need a uniform `BadCredentialsException`.

> [!tip] Interview answer
> **`UserDetailsRepositoryReactiveAuthenticationManager` is reactive DaoAuthenticationProvider: `ReactiveUserDetailsService` + `PasswordEncoder` → `Mono<Authentication>`.** Default encoder is delegating; password checks run on a **parallel** scheduler. `MapReactiveUserDetailsService` is the in-memory demo store, not production JDBC on the event loop.
