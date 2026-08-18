<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/Versions/9 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Older dump:

```java
Class<?> clazz = Class.forName("com.example.MyClass");
Object instance = clazz.newInstance();  // deprecated in Java 9
```

Preferred dump:

```java
Constructor<?> constructor = clazz.getConstructor();
Object instance = constructor.newInstance();
```

Parameterized: `getConstructor(parameterTypes)` then `newInstance(arguments)`. Private constructors: `getDeclaredConstructor` + `setAccessible(true)`.

> [!warning] Unverified traps from the dump
> - `Class.newInstance()` is called out as deprecated in Java 9 — use `Constructor.newInstance`.
> - Abstract classes / interfaces cannot be instantiated (`InstantiationException` in related write-ups).
