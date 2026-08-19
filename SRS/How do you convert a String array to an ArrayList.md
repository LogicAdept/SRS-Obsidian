<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Arrays #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: beginner check of the two utility classes **`Collections`** and **`Arrays`**. Use `Arrays.asList`:

```java
String[] words = {"ace", "boom", "crew", "dog", "eon"};
List wordList = Arrays.asList(words);

Integer[] nums = {1, 2, 3, 4};
List numsList = Arrays.asList(nums);
```

Dump: not `String`-specific; any element type’s array can be passed.

> [!warning] Unverified traps from the dump
> - The dump stops at `Arrays.asList`; it does not say whether the result is a `java.util.ArrayList` or whether `add`/`remove` are allowed.
