<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps show radix overloads:

```java
Integer seven = Integer.valueOf("111", 2); // binary 111 -> 7
int sevenPrimitive = Integer.parseInt("111", 2); // same, primitive int
int hundredPrimitive = Integer.parseInt("100"); // decimal 100
```

`parseXxx` returns a primitive; `valueOf` returns a wrapper.

> [!warning] Unverified traps from the dump
> - The second argument is radix, not a digit count.
> - Invalid digits for that radix throw `NumberFormatException`.
