<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

**Static weaving:** aspects are baked into target bytecode at compile time (AspectJ). Needs a special compiler. Dumps call it more performant.

**Dynamic weaving:** aspects are applied at runtime. Spring AOP creates JDK or CGLIB proxies as the app runs. No special compiler; proxy overhead.

> [!warning] Unverified traps from the dump
> - Load-time weaving sits between the two: bytecode change, but at class-load, not compile.
