<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`antMatchers` matched the raw URL with Ant patterns. `mvcMatchers` used Spring MVC path matching, so trailing slashes and suffix variants (`/orders` vs `/orders/`) were treated as the same resource — safer, because `antMatchers("/orders")` could be bypassed with `/orders/`.

In Spring Security 6 both are gone in favor of `requestMatchers`, which uses MVC-aware matching when Spring MVC is on the classpath. `authorizeHttpRequests` replaced `authorizeRequests`.

Rules are first-match-wins: specific patterns before `anyRequest()`.

> [!warning] Unverified traps from the dump
> - Trailing-slash bypass of `antMatchers` is the interview reason `mvcMatchers` existed.
> - Leaving off `anyRequest()` can leave paths unsecured.
