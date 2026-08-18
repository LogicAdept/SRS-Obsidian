<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Default `toString()` on `java.lang.Enum` returns `name` (the identifier). You may override `toString` for a display string.

`name()` is the generated/inherited method that returns the exact source identifier (`GERMAN_LANG`). Dumps: if `toString` is used for something else, convert enum → `String` with `name()`.

```java
String germanLang = LANG.GERMAN_LANG.name();  // GERMAN_LANG
System.out.println(LANG.GERMAN_LANG);         // may print a custom toString
```

> [!warning] Unverified traps from the dump
> - Do not feed a custom `toString()` result back into `valueOf` unless it equals the constant name.
