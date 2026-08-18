<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Serialization #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. `Optional` does not implement `Serializable`, deliberately, to discourage using it as a field. A class with an `Optional` field cannot be Java-serialized; dumps also say JPA entities and some DTO mappers choke on it.

```java
class Account implements Serializable {
    private Optional<String> email;  // breaks serialization
}

private String email;
public Optional<String> getEmail() { return Optional.ofNullable(email); }
```

> [!warning] Unverified traps from the dump
> - Persist/serialize a nullable field; expose `Optional` from the getter.
