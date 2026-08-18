<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Obtain a `Method`, then `invoke`:

```java
Method method = clazz.getMethod("methodName", parameterTypes);
Object returnValue = method.invoke(instance, arguments);
```

`invoke` takes the receiver (or `null` if static) and the argument list. Dumps: you can call methods whose names were not known at compile time.

> [!warning] Unverified traps from the dump
> - Target exceptions are often wrapped (not detailed in these compilations — verify `InvocationTargetException`).
