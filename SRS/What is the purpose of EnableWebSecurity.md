<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

@EnableWebSecurity turns on Spring Security’s web support and Spring MVC integration. Dumps put it on a @Configuration class that customizes HttpSecurity (historically by extending WebSecurityConfigurerAdapter).

It is the switch that lets you register security beans such as SecurityFilterChain, PasswordEncoder, and UserDetailsService instead of relying only on Boot’s default lock-down.
> [!warning] Unverified traps from the dump
> - On Spring Boot, adding spring-boot-starter-security already secures the app; @EnableWebSecurity is for customizing that auto-config, not for ‘turning security on’ from zero.
> - Spring Security 6 still uses @EnableWebSecurity, but not WebSecurityConfigurerAdapter.
