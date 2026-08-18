<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Patterns/GoF/Creational #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps show a record with a `static final INSTANCE`, sometimes plus `getInstance()`.

```java
public record Config(String databaseUrl, int maxConnections) {
    public static final Config INSTANCE =
        new Config("jdbc:postgresql://localhost:5432/mydb", 10);
}
```

They still say **enum singleton** is the stronger guarantee: the JVM prevents extra instances. A record does not — `new Config("other")` is still possible unless you try to hide the constructor.

```java
public record Config(String url) {
    private static final Config INSTANCE = new Config("default");
    private Config {}  // private compact constructor — dump still says reflection can bypass this
    public static Config getInstance() { return INSTANCE; }
}
```

Static field initialization is called thread-safe by JLS class-loading. Dumps also mention a nested Holder for lazy init.

The same write-up calls Singleton a controversial pattern and prefers DI.

> [!warning] Unverified traps from the dump
> - Do not say a record “guarantees a single instance”.
> - A private compact constructor is claimed not to fully stop reflection.
> - Serialization-as-singleton-safe is tied in one dump to Java 21 “JEP 445”; verify.
