<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/JVM/ClassLoaders #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Class.forName(String name)` loads **and initialises** the named class with the calling class's ClassLoader.

```java
Class<?> clazz = Class.forName("com.example.MyPlugin");

Class<?> lazy = Class.forName("com.example.MyPlugin",
                              false,           // do not initialise yet
                              customLoader);
```

Classic JDBC (pre-JDBC 4): `Class.forName("com.mysql.jdbc.Driver")` ran the driver's static block, which registered with `DriverManager`. JDBC 4+ uses `ServiceLoader` instead.

Rule of thumb from the dump: one-arg = load + initialise; three-arg with `initialize=false` = load only.

> [!warning] Unverified traps from the dump
> - `ClassNotFoundException` is the checked failure when the name is missing from the classpath.
