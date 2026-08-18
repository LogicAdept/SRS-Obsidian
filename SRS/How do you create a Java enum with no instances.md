<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes, as a utility-holder. A leading semicolon is required so the compiler sees “no constants”.

```java
public enum MessageUtil {
    ;  // no instances
    public static boolean isValid() {
        throw new UnsupportedOperationException("Not supported yet.");
    }
}
```

> [!warning] Unverified traps from the dump
> - This is a trick question: enums are usually a non-empty fixed set of instances.
