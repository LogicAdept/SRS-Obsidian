<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Patterns/GoF/Creational #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Effective Java–style dumps: a one-constant enum is a singleton shortcut.

```java
public enum MySingleton { INSTANCE; }
```

Claimed benefits: controlled instance creation, serialization safety (deserialize back to the same constant), thread-safe init without double-checked locking or `volatile`. Constructor runs when the enum is first referenced.

Claimed downsides appear as “pros and cons” in Java67 without the cons listed on that page.

> [!warning] Unverified traps from the dump
> - Do not confuse this with “Singleton via a Java record” — records do not give the JVM single-instance guarantee dumps attribute to enum.
> - Java67 lists advantages/disadvantages but the cons live behind a “see here” link — not copied here.
