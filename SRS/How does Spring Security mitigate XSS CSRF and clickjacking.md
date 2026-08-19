<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump list: CSRF (token filter), XSS (headers / Content Security Policy), clickjacking (X-Frame-Options), plus session-fixation protection. Some lists also name SQL injection — that is not a Spring Security filter; dumps still lump it under ‘security’.

Mitigation is the default filter chain and headers(), not a single annotation.
> [!warning] Unverified traps from the dump
> - Spring Security does not magically parameterize your JDBC. SQL injection is a data-access concern.
