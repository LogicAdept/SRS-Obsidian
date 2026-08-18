<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. An enum extends `Object` / `Enum`, so `toString` can be overridden. If you do not, the base implementation returns the constant’s `name`.

```java
public String toString() {
    return name;  // from java.lang.Enum in dumps
}
```

> [!warning] Unverified traps from the dump
> - Overriding `toString` does not change `name()` or `valueOf` in the conversion dumps.
