<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: autoboxing and unboxing are available from JDK 1.5 / Java 5 (also called J2SE 5.0) onwards. Before that, conversion was explicit (`Integer.valueOf`, `intValue`).

Since Java 5 you can write `Integer j = a;` and `int i = wrapper;` and the compiler inserts the factory / `xxxValue` calls.

> [!warning] Unverified traps from the dump
> - Java 5 is also when generics landed; dumps often mention both in the same breath.
