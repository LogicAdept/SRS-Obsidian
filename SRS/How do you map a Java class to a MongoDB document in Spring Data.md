<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

@Document(collection = "...") marks a class as a MongoDB entity. @Id marks the primary key (mapped to _id). @Field("name") customizes the stored field name. @Indexed and @CompoundIndex declare indexes that Spring Data can auto-create on startup.

```java
@Document(collection = "users")
public class User {
    @Id
    private String id;

    @Indexed(unique = true)
    @Field("email_address")
    private String email;

    private int age;
}
```
> [!warning] Unverified traps from the dump
> - This is not JPA: dumps use @Document and @Field, not @Entity and @Column.
> - Index auto-creation on startup is listed as a mapping feature and later as something to avoid relying on in production.
