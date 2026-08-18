<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: automatic boxing/unboxing exists to bridge primitives (fast, no object header) and the collection/generics world that requires objects. Before Java 5 you had to call `Integer.valueOf(i)` and `integer.intValue()` by hand.

Trade-offs claimed: primitives are faster and smaller (`int` 4 bytes vs `Integer` about 16–20 bytes with object header) and cannot be `null`. Wrappers are needed for `List`, generics, and nullable columns. Cost is heap allocation and GC pressure in loops. Project Valhalla is mentioned as a future attempt to put primitives into generics so this split shrinks.

> [!warning] Unverified traps from the dump
> - Autoboxing is a compiler convenience, not a new JVM primitive type.
> - Dumps treat Project Valhalla as future; do not treat it as already shipping behavior.
