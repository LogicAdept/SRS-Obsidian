<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A join point is a moment in program execution where an aspect can run (method call, exception, field access in the general AOP model).

In Spring AOP a join point is **always method execution** on a Spring bean. AspectJ can advise constructors, field get/set, and more.

> [!warning] Unverified traps from the dump
> - Interviewers mix “join point” (any possible place) with “pointcut” (the predicate that selects some of them).
