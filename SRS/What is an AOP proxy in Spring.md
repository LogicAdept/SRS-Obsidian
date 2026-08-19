<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

An AOP proxy is an object the framework creates to implement the aspect contracts at runtime. It intercepts method calls and runs advice.

Spring defaults to **JDK dynamic proxies** when the target implements an interface; otherwise **CGLIB** subclass proxies. The IoC container injects the proxy, not the raw instance.

> [!warning] Unverified traps from the dump
> - Nearby cards cover proxy kinds and limitations; this one is “what is the AOP proxy”.
> - Boot 3 dumps sometimes say CGLIB is the default even with interfaces — version-dependent claim.
