<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Serialization #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: a record may implement `Serializable`. Serialization is based on the record components, not the usual field-based mechanism.

Claims:

- No `serialVersionUID` is required (you may still add one).
- Deserialization always goes through the canonical constructor, so compact-constructor validation runs — unlike ordinary classes, where deserialization is said to bypass constructors.

```java
record Point(int x, int y) implements Serializable {}
```

One dump also labels this “JEP 445, Java 21” / “enhanced serialization”. Treat the JEP number as unverified; the constructor-on-deserialize claim appears in both dumps without that number.

> [!warning] Unverified traps from the dump
> - Regular class deserialization bypassing constructors is the contrast the dumps want.
> - Verify whether `serialVersionUID` is truly optional and whether “JEP 445” is the right document.
