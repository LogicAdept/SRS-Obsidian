<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: .formLogin(form -> form.disable()) (or httpBasic disable) so UsernamePasswordAuthenticationFilter is not added. Needed when addFilterAt a custom auth filter at that slot — addFilterAt does not remove the original.
> [!warning] Unverified traps from the dump
> - Disabling form login on the only chain removes /login. APIs want that; browser apps do not.
