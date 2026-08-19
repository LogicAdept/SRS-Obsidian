<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

An aspect is a module that encapsulates a cross-cutting concern (logging, transactions, security). It holds pointcuts plus advice.

In Spring you declare it with `@Aspect` on a class (and usually `@Component` so it is a bean). One application can have many aspects.

> [!warning] Unverified traps from the dump
> - @Aspect alone does not register a bean; dumps pair it with @Component or an @Bean method.
> - Aspect = pointcut + advice is the interview slogan; Introduction is a third piece some lists add.
