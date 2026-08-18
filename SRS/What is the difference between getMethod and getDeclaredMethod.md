<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Same split as fields:

- `getMethod(name, parameterTypes)` — public methods, walks superclasses.
- `getDeclaredMethod` — methods declared on this class, any visibility, not inherited.

```java
Method method = clazz.getMethod("methodName", parameterTypes);
Object returnValue = method.invoke(instance, arguments);
```

Private: `getDeclaredMethod` + `setAccessible(true)` + `invoke`. Static: pass `null` as the target instance.

> [!warning] Unverified traps from the dump
> - Overloads are distinguished by the `Class...` parameter-type array, not by name alone.
