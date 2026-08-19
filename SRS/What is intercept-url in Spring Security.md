<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

XML dump: <intercept-url pattern="..." access="..."> is how you restrict URLs. A few patterns cover most apps. access values like ROLE_ADMIN, ROLE_USER, or IS_AUTHENTICATED_ANONYMOUSLY.

Java config’s requestMatchers / hasRole is the same idea. Patterns are first-match; specific before /**.
> [!warning] Unverified traps from the dump
> - The dump’s index.jsp comment saying admin.jsp is anonymous is sloppy; read the actual patterns.
