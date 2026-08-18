<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps:

```java
if (!clazz.isRecord()) {
    throw new IllegalArgumentException("Not a record");
}
RecordComponent[] components = clazz.getRecordComponents();
for (RecordComponent rc : components) {
    rc.getName();
    rc.getType();
    Method accessor = rc.getAccessor();
    Object value = accessor.invoke(record);
}
```

`javap -p` on the class file is said to show `final class … extends java.lang.Record`, `private final` fields, the canonical constructor, and accessors.

> [!warning] Unverified traps from the dump
> - `Class.getRecordComponents()` is the dump’s record-specific API, not ordinary `getDeclaredFields()` alone.
