<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Boot/AutoConfiguration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: add spring-boot-starter-security and Boot auto-configures basic security (all endpoints authenticated, generated user/password, default login). Customize with @EnableWebSecurity and a SecurityFilterChain (dumps still show WebSecurityConfigurerAdapter).

It pulls in Spring Security web/config and the filter registration.
> [!warning] Unverified traps from the dump
> - The starter alone is a lock-down, not OAuth2. You still add oauth2-client / resource-server starters for those flows.
