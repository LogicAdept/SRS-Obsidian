<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: you can enable or disable assertions **class-wise or package-wise**.

- One class: `java -ea:pack1.B`
- Two classes: `java -ea:pack1.B -ea:pack1.pack2.C`
- Every class in a package: `java -ea:pack1`
- Package except one class: `java -ea:pack1 -da:pack1.B`
- Package and subpackages, except another subtree: `java -ea:pack1... -da:pack1.pack2...`

> [!warning] Unverified traps from the dump
> - The `...` suffix in dumps means the named package **and nested packages**.
> - Combine with `-da` when you enabled a wide prefix and need an exception.
