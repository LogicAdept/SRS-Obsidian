<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Compilations list reflection where types are not known at compile time:

- Frameworks (Spring, Hibernate): dependencies, injection, talking to classes dynamically.
- Testing (JUnit): instantiate test classes, invoke test methods.
- IDEs / tools: completion and class inspection.
- Serialization libraries: walk fields dynamically.
- Dynamic proxies and dynamic method invocation.

Dumps still warn: flexibility costs performance and can hurt security if overused.

> [!warning] Unverified traps from the dump
> - Prefer ordinary calls when the type is known at compile time.
