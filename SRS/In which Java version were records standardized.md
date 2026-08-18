<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps call a record a special class for immutable data carriers.

Preview: Java 14 (JEP 359). Second preview: Java 15 (JEP 384). Standardized: Java 16 (JEP 395).

```java
public record User(String name, int age, String email) {}

User user = new User("John", 25, "john@example.com");
user.name();  // John — not getName()
```

Other vault drafts still say “Java 14+” for the same idea. The interview split dumps want: preview in 14/15, stable in 16.

Record patterns in `switch` / `instanceof` are listed separately as Java 21 (JEP 440).

> [!warning] Unverified traps from the dump
> - Do not treat “Java 14+” and “Java 16” as the same claim without preview vs standard.
> - Dumps say records are not “just Lombok syntactic sugar” — they are a JVM data model (`ACC_RECORD`).
