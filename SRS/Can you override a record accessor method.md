<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: you cannot change the accessor’s type or signature.

```java
public record Point(int x, int y) {
    public String x() {  // compile error — different return type
        return String.valueOf(x);
    }
}
```

Same dump set also says: starting with Java 16 (standard records) you *can* override an accessor with the same signature; that was forbidden in preview.

```java
public record User(String name) {
    public String name() { return name.toUpperCase(); }  // claimed OK in Java 16+
}
```

> [!warning] Unverified traps from the dump
> - Preview vs Java 16+ is the version split to verify for accessor overrides.
> - Dumps still warn against overriding accessors “without a reason”.
