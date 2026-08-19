<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

HttpSecurity configures web-based security for HTTP requests: which endpoints need authentication, form login, HTTP Basic, CSRF, CORS, logout, and session policy.

Dumps configure it by overriding WebSecurityConfigurerAdapter.configure(HttpSecurity) or, in later samples, by exposing a SecurityFilterChain bean that calls http.authorizeRequests / authorizeHttpRequests and then http.build().
> [!warning] Unverified traps from the dump
> - Dumps still extend WebSecurityConfigurerAdapter; Spring Security 6 removed that class in favor of a SecurityFilterChain bean.
> - authorizeRequests and antMatchers are the old DSL; later dumps mix in authorizeHttpRequests and requestMatchers.
