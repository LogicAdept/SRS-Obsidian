<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump pattern: log line Security filter chain: [] means no SecurityFilterChain matched that URL. Check securityMatcher patterns. Repeated Did not match request to… means every chain rejected the request — effectively unsecured or falling through.
> [!warning] Unverified traps from the dump
> - Empty chain is not permitAll(). permitAll still prints a full filter list.
