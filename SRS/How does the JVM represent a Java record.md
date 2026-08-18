<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: a record is not only source sugar. The class file has `ACC_RECORD | ACC_FINAL`, superclass `java/lang/Record`, and a `Record` / `RecordComponents` attribute listing each component (name, type, annotations).

```java
public abstract class Record {
    protected Record() {}
    public abstract boolean equals(Object obj);
    public abstract int hashCode();
    public abstract String toString();
}
```

`java.lang.Record` is described as a special superclass you cannot `extends` directly. JVM rules cited: `ACC_FINAL` required, superclass must be `java.lang.Record`.

Why dumps say records cannot be subclassed: immutability, predictable `equals`/`hashCode`, JIT assumptions, pattern-matching deconstruction, and “value types / Valhalla” compatibility.

> [!warning] Unverified traps from the dump
> - A dump red flag: “Record inherits Object” — dumps say it inherits `java.lang.Record`.
> - Bytecode-level “cannot change through manipulation” is a dump claim, not something this card verifies.
