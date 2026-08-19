<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Gang of Four Singleton: **one instance per ClassLoader**.

Spring `singleton` scope: **one instance per bean definition per IoC container**. Two contexts (or two bean definitions of the same class) can each hold their own instance. The default scope is still singleton.

> [!warning] Unverified traps from the dump
> - “Spring beans are singletons so they are the GOF pattern” is the popular lie interviewers wait for.
> - A singleton bean is still not automatically thread-safe; shared mutable fields are a race.
