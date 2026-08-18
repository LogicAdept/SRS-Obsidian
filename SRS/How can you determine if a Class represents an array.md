<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

```java
boolean isArray = clazz.isArray();
```

The Reflection API dump also lists `java.lang.reflect.Array` for creating and indexing arrays when the component type is only known at runtime.

> [!warning] Unverified traps from the dump
> - A `Class` for `String[]` is not the same as `String.class`; check `isArray()` / `getComponentType()`.
