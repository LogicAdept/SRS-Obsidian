<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps contrast records with ordinary classes:

| Record | Regular class |
| --- | --- |
| All header fields `private final` | Any fields |
| Implicitly `final` — cannot be subclassed | Inheritance allowed |
| Extends `java.lang.Record` | Extends `Object` (unless you say otherwise) |
| Generated `equals` / `hashCode` / `toString` | Manual or IDE/Lombok |
| Accessors `x()` | Often JavaBean `getX()` |
| No extra instance fields | Extra instance fields allowed |

```java
public record Point(int x, int y) {}

// public class Bad extends Point {}           // compile error
// public record Bad extends Object {}         // compile error
public record User(String name) implements Serializable {}  // interfaces: ok
```

When dumps say to use a class instead: mutable state, inheritance, a mutable builder, or JPA entities (no-arg constructor, mutable fields, proxies).

> [!warning] Unverified traps from the dump
> - Records can implement interfaces even though they cannot extend a class.
> - A dump red flag: “Record is suitable for JPA” — dumps say JPA needs a no-arg constructor and mutable fields.
