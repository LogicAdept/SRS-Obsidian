<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: autoboxing is automatic conversion of a primitive to its wrapper. It occurs when:

- assigning a primitive to a wrapper variable (`Integer j = a`);
- passing a primitive to a method / collection that expects the wrapper (`list.add(25)`);
- other contexts that need an object (generics).

Unboxing is the reverse: assignment to a primitive, arithmetic, `list.get` into `int`.

Since Java 5 the compiler inserts `valueOf` / `xxxValue` so you do not write them.

> [!warning] Unverified traps from the dump
> - Enhorse-style dumps add extra rules: a `byte` *variable* does not autobox to `Short` without a primitive conversion.
> - Unboxing `null` in any of these contexts is NPE.
