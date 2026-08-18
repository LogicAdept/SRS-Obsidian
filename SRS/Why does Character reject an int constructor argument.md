<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A dump shows:

```java
Character c1 = new Character('C'); // only char constructor
// Character c2 = new Character(124); // COMPILER ERROR
```

`Character` is constructed from a `char`, not from an `int` literal in that example.

> [!warning] Unverified traps from the dump
> - An `int` literal is not a `char` argument; dumps require `'C'` or a `char` cast.
