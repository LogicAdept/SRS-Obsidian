<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`getConstructors()` — public constructors. `getDeclaredConstructors()` — all constructors on the class (private included).

```java
Constructor<?> constructor = clazz.getConstructor(parameterTypes);
Object instance = constructor.newInstance(arguments);
```

`getParameterTypes()` on `Constructor` returns the parameter `Class` array for matching arguments.

> [!warning] Unverified traps from the dump
> - `getConstructor` does not see a private constructor — use `getDeclaredConstructor`.
