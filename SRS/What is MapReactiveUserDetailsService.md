<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS

# What is `MapReactiveUserDetailsService`?

> [!abstract] Short answer
> **`MapReactiveUserDetailsService`** is Spring Security’s **in-memory `ReactiveUserDetailsService`** (since **5.0**): users live in a **`Map`**, lookup is **`Mono<UserDetails> findByUsername`**. It is the WebFlux counterpart of servlet **`InMemoryUserDetailsManager`**, not a `UserDetailsService`. It also implements **`ReactiveUserDetailsPasswordService`** (`updatePassword`).

## In-memory reactive users

Javadoc: *A Map based implementation of `ReactiveUserDetailsService`*.

Constructors:

| Constructor | Note |
| --- | --- |
| **`UserDetails...` / `Collection<UserDetails>`** | Typical sample: `new MapReactiveUserDetailsService(user)` |
| **`Map<String, UserDetails>`** | The map **must be non-blocking** (no `Hashtable` / locking map that waits) |

`findByUsername(String)` returns a **`Mono<UserDetails>`** (the `Mono` itself is not null). Missing users complete empty; HTTP Basic / form login then fail authentication via **`UserDetailsRepositoryReactiveAuthenticationManager`** wrapping this service — [[What is UserDetailsRepositoryReactiveAuthenticationManager]], [[What is ReactiveAuthenticationManager]].

Spring Security *WebFlux Security* minimal config is **`@EnableWebFluxSecurity` + this bean** — [[What is EnableWebFluxSecurity]]:

```java
@Bean
public MapReactiveUserDetailsService userDetailsService() {
    UserDetails user = User.withDefaultPasswordEncoder()
            .username("user")
            .password("user")
            .roles("USER")
            .build();
    return new MapReactiveUserDetailsService(user);
}
```

**Listing 1.** Conceptual reference sample. `withDefaultPasswordEncoder()` is **`@Deprecated`**: demos only; password is still in the bytecode. Production: encode **ahead of time** with `PasswordEncoderFactories.createDelegatingPasswordEncoder()`, then `User.builder().password("{bcrypt}…")`.

```d2
direction: down
http: "httpBasic / formLogin" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
mgr: "UserDetailsRepository\nReactiveAuthenticationManager" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
map: "MapReactiveUserDetailsService\nfindByUsername → Mono" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

http -> mgr -> map
```

**Fig. 1.** Same `UserDetails` type as servlet; the **service** is reactive. Overview: [[How does Spring Security work with WebFlux]].

This is **not** a production user store. Use a **reactive** `ReactiveUserDetailsService` against your DB (or offload JDBC). A blocking `findByUsername` on the event loop is the usual outage — [[How does the WebFlux event loop work]].

> [!warning] `withDefaultPasswordEncoder()` is demo-only
> Spring: **not safe for production**; deprecated to mark that. Hash outside the source, or do not compile passwords into the JAR.

> [!warning] Not `InMemoryUserDetailsManager`
> That class is **`UserDetailsService`** (servlet). Wiring it into WebFlux does not give you `Mono` lookups.

> [!warning] The `Map` constructor must not block
> Javadoc: the map **must be non-blocking**. A map whose `get` waits (or a huge synchronized wrapper) stalls **`findByUsername`** on the loop.

> [!tip] Interview answer
> **`MapReactiveUserDetailsService` is in-memory reactive users — `Mono findByUsername`, WebFlux’s `InMemoryUserDetailsManager`.** Samples use `User.withDefaultPasswordEncoder()`; that is **not** production. Password upgrades go through `updatePassword`. Real apps replace the bean with a reactive (or offloaded) `ReactiveUserDetailsService`.
