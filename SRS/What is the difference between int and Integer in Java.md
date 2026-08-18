<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`int` is a primitive; `Integer` is the wrapper class for `int`.

Dumps contrast them as:

- `int`: 32-bit value, default field value `0`, cannot be `null`, not allowed as a generic type argument, generally faster.
- `Integer`: heap object with methods, default field value `null`, allowed in generics/collections, autoboxing/`valueOf`/constructors, extra object overhead.

```java
int primitiveInt = 10;
Integer objInt = Integer.valueOf(20);
Integer autoBoxed = primitiveInt; // autoboxing
int unboxed = objInt;             // unboxing
```

> [!warning] Unverified traps from the dump
> - You cannot write `List<int>`; you write `List<Integer>` and autobox.
> - A dump snippet that prints an uninitialized local `Integer` would not compile; locals have no default.
