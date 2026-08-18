<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Three dump recipes:

```java
Class<?> clazz = MyClass.class;                          // compile-time type
Class<?> clazz = myObject.getClass();                    // runtime class of an instance
Class<?> clazz = Class.forName("com.example.MyClass");   // name as String
```

`.class` when the type is known now. `getClass()` when you have an instance (may be a subclass / proxy). `Class.forName` when the name arrives at runtime (config, plugins).

> [!warning] Unverified traps from the dump
> - `forName` throws checked `ClassNotFoundException`.
