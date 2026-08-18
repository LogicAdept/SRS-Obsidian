<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/JVM/ClassLoaders #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Tied to reflective / dynamic load in dumps:

| | `ClassNotFoundException` | `NoClassDefFoundError` |
| --- | --- | --- |
| Kind | Checked exception | Error |
| Typical trigger | `Class.forName()` / `ClassLoader.loadClass()` and the name is not on the classpath | Class was there at compile time, missing at runtime (JAR not deployed) |

```java
Class.forName("com.mysql.jdbc.Driver");  // CNFE if the JAR is absent
```

Rule of thumb: CNFE = you asked by name and it was missing; NCDFE = the JVM needed a class while resolving another and could not find it.

> [!warning] Unverified traps from the dump
> - This cue also belongs on `#Java/JVM/ClassLoaders`.
