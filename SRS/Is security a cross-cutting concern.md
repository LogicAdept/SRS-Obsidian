<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps say yes. Security applies across the app (with logging, transactions, caching). Spring Security uses filters at the web layer and Spring AOP for method security — both classic cross-cutting mechanisms.

It is not a business-module local check; that is why it is configured once in a filter chain and annotations rather than copied into every controller.
> [!warning] Unverified traps from the dump
> - Calling it ‘just a filter’ ignores method security AOP, which dumps also count as cross-cutting.
