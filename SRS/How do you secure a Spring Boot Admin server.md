<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Admin #Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Admin is a web UI over Actuator. Secure it with Spring Security — HTTP basic or OAuth2.

Sample: `spring-boot-starter-security` plus `spring-boot-admin-starter-server`. A `WebSecurityConfigurerAdapter` that `httpBasic()`s and authenticates everything except maybe `/actuator/**`. Properties: `spring.security.user.name` / `password`.

> [!warning] Unverified traps from the dump
> - `WebSecurityConfigurerAdapter` is dump sample code; newer Security APIs differ.
> - Permit-all on `/actuator/**` on the Admin server is the opposite of locking Actuator on clients.
