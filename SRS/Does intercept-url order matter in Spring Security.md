<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# Does `intercept-url` order matter in Spring Security?

> [!abstract] Short answer
> **Yes.** `<intercept-url>` elements are matched **in document order**. The **first** pattern that matches the request wins; later lines are not consulted. Put **more specific** patterns above **more general** ones (`/admin/**` before `/**`). Java `authorizeHttpRequests` / `requestMatchers` is the same first-match rule, not a different model.

## First match, not “most specific wins by magic”

The namespace builds an ordered map of `RequestMatcher` → access attributes (historically `FilterInvocationSecurityMetadataSource` for `FilterSecurityInterceptor`; today `AuthorizationFilter` walks the same pattern/rule pairs). Matching stops at the first hit.

```xml
<http>
    <intercept-url pattern="/admin/**" access="hasRole('ADMIN')"/>
    <intercept-url pattern="/**" access="hasRole('USER')"/>
</http>
```

**Listing 1.** `/admin/users` matches the first line (`ROLE_ADMIN`). Swap the two lines and `/**` would grant `ROLE_USER` to `/admin/**` as well — the admin rule would never run.

```java
@Bean
SecurityFilterChain app(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((authorize) -> authorize
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .anyRequest().hasRole("USER"));
    return http.build();
}
```

**Listing 2.** Same first-match list as Listing 1. `intercept-url` is the XML spelling; `requestMatchers` / `anyRequest` is the Java spelling. See [[Why does authorization matcher order matter in Spring Security]] and [[What is intercept-url in Spring Security]].

```d2
direction: down
req: "GET /admin/users" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
u1: "intercept-url /admin/**\nhasRole(ADMIN)" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
u2: "intercept-url /**\nhasRole(USER)" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
win: "Use ADMIN rule\nstop" {
  width: 180
  height: 50
  style.fill: "#fce4ec"
}

req -> u1: "try first"
u1 -> win: "matches"
u1 -> u2: "only if no match"
```

**Fig. 1.** Declaration order is the evaluation order. A catch-all at the top makes every later `<intercept-url>` dead.

A `method` attribute (GET, POST, …) narrows a line to that HTTP method. If the **same** pattern appears both with a method and without, the **method-specific** line takes precedence. Otherwise keep relying on list order: specific paths first, `/**` last. `requires-channel` on `<intercept-url>` uses the same ordered matching for HTTP vs HTTPS.

This is **authorization-rule** order inside one `<http>` / one [[What is SecurityFilterChain]]. A different first-match list is which `SecurityFilterChain` (or which `<http pattern="…">`) `FilterChainProxy` selects — still specific-before-general, but that is chain selection, not `access=` on `intercept-url`.

> [!warning] A leading `/**` silently disables later rules
> `<intercept-url pattern="/**" …>` matches every request. Placing it first is not a merge and not a fallback — it is a **total** win. The rest of the list never runs. That is by design, not an XML-only bug; Java `anyRequest()` / `requestMatchers("/**")` declared first does the same.

> [!tip] Interview answer
> Yes — intercept-url order is first-match in document order, so specific patterns must sit above catch-alls like /**. The Java DSL uses the same rule with requestMatchers. Put /** or anyRequest first and every later admin or method-specific line is dead code.
