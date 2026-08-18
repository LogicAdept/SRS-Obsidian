<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use the generated static `valueOf(String)`. The string must match the constant identifier exactly or the call throws `IllegalArgumentException: No enum const class…`.

```java
LANG germanLang = LANG.valueOf("GERMAN_LANG");
```

Some dumps prefer a factory on the enum that can ignore case. `valueOf` is listed alongside `values()`, `name()`, and `ordinal()` as compiler-added API.

`name()` (and default `toString()`) is the other direction: constant → the identifier string.

> [!warning] Unverified traps from the dump
> - `valueOf` is case-sensitive in the dumps that show the IAE message.
> - If `toString()` is overridden, `valueOf` still keys off the constant name, not the custom `toString` text (shown in a dump where `valueOf` + overridden `toString` print a sentence).
