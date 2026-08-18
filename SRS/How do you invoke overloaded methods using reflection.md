<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Overloads share a name and differ by parameter types. Reflection requires the signature:

```java
getDeclaredMethod(String name, Class<?>... parameterTypes)
```

Pass a `Class[]` that matches the overload you want, then `invoke`.

> [!warning] Unverified traps from the dump
> - Wrong parameter-type array → `NoSuchMethodException`, not a silent pick of another overload.
