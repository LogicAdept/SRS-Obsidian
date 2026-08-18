<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. From **1.4**, `assert` is a keyword, so `int assert = 10;` does not compile under a 1.4+ source level.

Dumps: `javac -source 1.3` can still compile `assert` as an identifier (with warnings). Pairing example in dumps:

- Class with `int assert = 0`: `-source 1.3` compiles with warnings; `-source 1.4` is a compile error.
- Class with `assert(false);`: `-source 1.3` is a compile error; `-source 1.4` compiles.

> [!warning] Unverified traps from the dump
> - “Identifier” here means a variable/method name, not the `assert` **statement**.
> - Modern compilers default to a source level far above 1.3; the `-source 1.3` story is historical SCJP material.
