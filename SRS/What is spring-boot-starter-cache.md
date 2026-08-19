<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Boot/AutoConfiguration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Boot starter you add so caching auto-config and annotations work. After the dependency, annotate a config class with `@EnableCaching`. Pair with Caffeine or Redis for a real store.

> [!warning] Unverified traps from the dump
> - The starter is not a distributed cache. Default remains an in-memory map until another provider is on the classpath.

