<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `Optional` was designed as a **return type** for “no result”, not a general maybe. Fields add a wrapper per instance and break Java serialization; parameters force callers to box and make call sites ambiguous.

```java
class User { private Optional<String> nickname; }  // avoid
void greet(Optional<String> name) { }              // avoid

class User { private String nickname; }
void greet() { } void greet(String name) { }
```

Official-designer guidance in the dump: return type only; not fields, parameters, or constructor arguments.

> [!warning] Unverified traps from the dump
> - The mixed dump How would you explain java.util.Optional already lists this anti-pattern.
