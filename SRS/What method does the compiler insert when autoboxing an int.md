<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: autoboxing is the compiler calling `Integer.valueOf(int)` when a primitive is used where an object is expected (`Integer x = 42`, `list.add(5)`). That is why the integer cache applies to autoboxing: `valueOf` may return a cached instance for `-128` to `127`. `new Integer(...)` is a different path and does not use that cache.

```java
Integer y = num; // compiler writes Integer.valueOf(num)
```

> [!warning] Unverified traps from the dump
> - Autoboxing uses `valueOf`, not `new Integer`.
> - `valueOf` is also why `==` can be true for two boxed `100`s and false for two boxed `200`s.
