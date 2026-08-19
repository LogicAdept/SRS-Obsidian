<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list three limits of XML autowiring:

1. Explicit `<property>` / constructor-arg **overrides** autowire.
2. You cannot autowire primitives, `String`, or `Class`.
3. It is less precise than explicit wiring — prefer explicit refs when the graph is unclear.

> [!warning] Unverified traps from the dump
> - Autowiring “just works” until a second bean of the same type appears.
> - Primitive/String limitation is XML autowire modes, not `@Value`.
