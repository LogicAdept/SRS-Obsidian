<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `int x = someIntegerObject` is unboxing. The compiler inserts `someIntegerObject.intValue()`. Bytecode uses `invokevirtual` calling `Integer.intValue()`.

If `someIntegerObject` is `null`, the JVM throws `NullPointerException` at that `intValue()` call, even though the source looks like a simple assignment. Java 14+ NPE messages are claimed to name the expression, e.g. “Cannot unbox a null value.”

The same hidden call shows up in arithmetic on a wrapper returned from a method or `Map.get`.

> [!warning] Unverified traps from the dump
> - Unboxing is a method call, not a magic load of bits.
> - NPE on `int x = obj;` is unboxing `null`, not a missing local initializer.
