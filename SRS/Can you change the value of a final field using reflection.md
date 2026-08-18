<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

One compilation says **yes**: `setAccessible(true)`, then strip `FINAL` via the `modifiers` field on `Field`, then `set`.

```java
Field field = clazz.getDeclaredField("finalFieldName");
field.setAccessible(true);
Field modifiersField = Field.class.getDeclaredField("modifiers");
modifiersField.setAccessible(true);
modifiersField.setInt(field, field.getModifiers() & ~Modifier.FINAL);
field.set(instance, newValue);
```

Another dump: you can **read** finals; changing them needs extra tricks; you can **invoke** final methods but cannot **override** them via reflection.

Treat the `Field.modifiers` hack as a popular interview recipe that may fail on current JDKs.

> [!warning] Unverified traps from the dump
> - `Field.class.getDeclaredField("modifiers")` is a known fragile trick — modules / JDK internals may block it.
> - Compile-time constant finals are a further case these dumps do not spell out.
