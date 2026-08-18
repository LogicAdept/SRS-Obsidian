<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps contrast `assert` with leftover `System.out` debug prints: prints stay in the binary and hurt performance/logging unless you delete them. Assertions can be left in the source and **switched off**; the default is **disabled**, so you do not have to delete `assert` lines before a release.

Usual story in dumps: enable in development and test; do not rely on them in production. They are for catching developer bugs / invariants, not production input validation.

> [!warning] Unverified traps from the dump
> - “Disabled by default” is a **runtime** JVM default: you still compile `assert`; you enable it with `-ea` when you want the checks.
> - Dumps say you do not have to delete assert statements before a release the way you must delete leftover `System.out` debug lines.
