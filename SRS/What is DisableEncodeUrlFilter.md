<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default-order table (FIRST): DisableEncodeUrlFilter stops the container from rewriting URLs with a jsessionid query string, which would leak the session id in Referer headers and logs.
> [!warning] Unverified traps from the dump
> - It is not CSRF protection. It only blocks encodeURL session-id rewriting.
