<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default chain: HeaderWriterFilter writes security response headers (X-Frame-Options, X-Content-Type-Options, HSTS, and the rest of the default header set). It runs early (dump position ~200), after SecurityContext is loaded.
> [!warning] Unverified traps from the dump
> - web.ignoring() skips this filter too — static paths get no security headers. permitAll() still runs HeaderWriterFilter.
