<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: an **Advisor** is the pair **Pointcut + Advice** in Spring’s interceptor API (the older programmatic / XML style).

Internally Spring AOP still talks in advisors: the proxy’s interceptor chain is advisors matching the method.

> [!warning] Unverified traps from the dump
> - @Aspect style hides Advisor; you still meet the word in Spring AOP internals questions.
