<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring AOP advises **Spring-managed beans** only (objects from the IoC container that got a proxy).

`new Foo()` is not advised. For objects outside the container, dumps say use **AspectJ** compile-time or load-time weaving.

> [!warning] Unverified traps from the dump
> - Same limit as “Spring AOP vs AspectJ”: proxy AOP cannot reach arbitrary new instances.
