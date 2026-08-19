<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump filter alias X509_FILTER: X509AuthenticationFilter reads the client TLS certificate from the request and builds a pre-authenticated Authentication. Sibling of form-login / Basic, not a PasswordEncoder.
> [!warning] Unverified traps from the dump
> - The servlet container must request a client cert (needClientAuth). The filter cannot invent a certificate that Tomcat never negotiated.
