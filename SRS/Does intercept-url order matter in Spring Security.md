<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

XML dumps: <intercept-url> patterns are processed in document order. Write more specific patterns before less specific ones so the right access attribute wins.

Same first-match idea as authorizeHttpRequests requestMatchers. Example: /admin/* ROLE_ADMIN before /** ROLE_USER.
> [!warning] Unverified traps from the dump
> - Java config has the same ordering bug; intercept-url is only the XML spelling.
