<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `ElementType.TYPE` is a declaration target — class, interface, enum, annotation type.

`ElementType.TYPE_USE` (Java 8) is a type-use target — annotations on a type appearing in `new`, casts, type arguments, `implements`/`throws`, etc. Nested type annotations need `@Target(ElementType.TYPE_USE)`.

Declaration vs use can both apply to the same source position (a class declaration is also a type); dumps say the annotation’s `@Target` decides which of those contexts are legal.
> [!warning] Unverified traps from the dump
> - A dump used the name ElementType.USE; the JDK enum is TYPE_USE.
> - TYPE_PARAMETER is a different Java 8 target (type-parameter declarations), not TYPE_USE.
