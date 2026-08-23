<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# Why does authorization matcher order matter in Spring Security?

> [!abstract] Short answer
> **`authorizeHttpRequests` rules are evaluated top to bottom; `AuthorizationFilter` applies only the first match.** Put **specific `requestMatchers` before catch-alls** like **`anyRequest()`** or broad **`/**`** patterns — otherwise a general rule **shadows** narrower ones and later rules **never run**.

## First-match semantics

Each **`requestMatchers(...).access(...)`** (or **`hasRole`**, **`permitAll`**, etc.) pair is an ordered authorization rule. At runtime **`AuthorizationFilter`** walks the list and stops at the **first pattern that matches the incoming request**.

The authorize-http-requests guide states explicitly that pairs are processed **in the order listed**, applying **only the first match**. Even though **`/**`** would also match **`/endpoint`**, listing **`/endpoint`** first is correct because the catch-all is never reached for that path.

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .requestMatchers("/api/public/**").permitAll()
    .anyRequest().authenticated()
);
```

**Listing 1.** Specific paths first; `anyRequest()` is the fallback for everything else.

## What goes wrong when order is reversed

If **`anyRequest().authenticated()`** (or **`/**`**) appears **before** a more specific matcher:

1. Every request matches the broad rule immediately.
2. **`/admin/**`**, **`permitAll()`**, or custom access rules **below** it are **dead code**.
3. Admins may be blocked, public endpoints may require login, or sensitive paths may stay open — depending on which broad rule you placed first.

```d2
direction: right
req: "Incoming HTTP request" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
rules: "Ordered matcher list\n(first match wins)" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
specific: "/admin/** → ADMIN" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
broad: "anyRequest() → authenticated" {
  width: 200
  height: 50
  style.fill: "#fce4ec"
}
skip: "Later rules\nnever evaluated" {
  width: 160
  height: 50
  style.fill: "#ffcdd2"
}

req -> rules
rules -> broad: "if broad is first"
broad -> skip
rules -> specific: "specific must be\nabove broad"
```

**Fig. 1.** Catch-all matchers placed too high shadow every rule below them.

Legacy **`authorizeRequests`** / XML **`<intercept-url>`** follow the same **first-match** idea; only the DSL spelling changed. See [[Does intercept-url order matter in Spring Security]].

> [!warning] `permitAll()` after `authenticated()` is unreachable
> **`anyRequest().authenticated()`** at the top makes a later **`requestMatchers("/health").permitAll()`** useless — health checks still require authentication. Public endpoints, actuator paths, and webhook URLs must appear **before** the default authenticated/deny rule. See [[What is AuthorizationFilter in Spring Security]] and [[What is the difference between securityMatcher and requestMatchers]].

> [!tip] Interview answer
> AuthorizationFilter evaluates authorizeHttpRequests rules in declaration order and stops at the first match. Put specific requestMatchers before anyRequest or /** catch-alls; reversing them shadows admin or permitAll rules so they never apply.
