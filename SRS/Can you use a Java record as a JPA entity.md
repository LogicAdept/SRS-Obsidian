<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Persistence/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: no. Hibernate/JPA is said to need:

1. A no-arg constructor.
2. Mutable fields (lazy loading, dirty checking).
3. A proxy mechanism (often a subclass).

```java
@Entity
public record User(Long id, String name) {}  // dumps: does not work

@Entity
public class User {
    @Id private Long id;
    private String name;
}
```

Records are positioned as DTOs / value objects next to ordinary entity classes. Spring Boot 3 DTO examples in the same dumps migrate Lombok `@Data` request bodies to records, not `@Entity` types.

> [!warning] Unverified traps from the dump
> - Record cannot extend a mapped superclass either — it already extends `java.lang.Record`.
> - A dump red flag: “You can use Record for a JPA entity hierarchy.”
