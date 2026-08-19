<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The servlet container does not know about Spring beans. `DelegatingFilterProxy` is registered with the container and looks up a Spring bean (default name `springSecurityFilterChain`) and delegates every request to it.

That bean is a `FilterChainProxy`: one Servlet `Filter` that holds your `SecurityFilterChain` instances. For each request it picks the first chain whose matcher matches and runs that chain’s ordered security filters.

```
Request → DelegatingFilterProxy → FilterChainProxy → matching SecurityFilterChain → app
```

`@EnableWebSecurity` wires this. Multiple `SecurityFilterChain` beans are ordered with `@Order`; `securityMatcher` scopes a chain (JWT API vs form-login UI).

> [!warning] Unverified traps from the dump
> - The bean name to remember for certification-style questions is `springSecurityFilterChain`.
> - `FilterChainProxy` is not the same as one `SecurityFilterChain` bean; it orchestrates them.
