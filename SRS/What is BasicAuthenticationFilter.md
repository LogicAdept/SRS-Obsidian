<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

BasicAuthenticationFilter reads the Authorization: Basic header (Base64 username:password), builds an Authentication, and calls AuthenticationManager. httpBasic() adds it to the chain.

Custom-filter dumps often addFilterAfter(custom, BasicAuthenticationFilter.class). It is the HTTP Basic landmark, not the form-login one.
> [!warning] Unverified traps from the dump
> - Base64 is encoding. Without TLS the password is visible. Do not confuse this filter with UsernamePasswordAuthenticationFilter.
