<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableAspectJAutoProxy` enables processing of `@Aspect` components, like XML `<aop:aspectj-autoproxy/>`.

It does **not** switch Spring to full AspectJ weaving; it still creates Spring AOP proxies that understand AspectJ *annotations*.

Dump example registers the aspect as an `@Bean` next to the annotation.

> [!warning] Unverified traps from the dump
> - proxyTargetClass=true forces CGLIB subclass proxies (from API/compilation lists).
> - Name is misleading: “AspectJ” here means the annotation style.
