<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring intercepts method calls with a **proxy** (JDK dynamic proxy if the bean implements an interface; CGLIB subclass otherwise).

1. Container creates the target bean, then wraps it in a proxy.
2. Advisors (pointcut + advice) are matched to methods.
3. A call through the proxy runs `@Before` / `@Around` / … then (unless around skips it) the target method.
4. Weaving is **runtime** — the target class bytecode is not rewritten.

Self-invocation on `this` never enters the proxy.

> [!warning] Unverified traps from the dump
> - XML <aop:aspectj-autoproxy/> and @EnableAspectJAutoProxy both turn this auto-proxy creator on.
