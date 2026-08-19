<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @Configuration + @EnableWebSecurity, @Bean SecurityFilterChain filterChain(HttpSecurity http). Lambda DSL (authorizeHttpRequests, requestMatchers, formLogin), return http.build(). This replaces WebSecurityConfigurerAdapter.

Multiple beans: securityMatcher + @Order; first match wins.
> [!warning] Unverified traps from the dump
> - authorizeHttpRequests replaced authorizeRequests. requestMatchers replaced antMatchers/mvcMatchers.
> - Always finish with anyRequest() so no path is left unsecured by accident (dump claim).
