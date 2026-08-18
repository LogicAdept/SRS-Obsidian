<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: Sun introduced assertions in **Java 1.4**. From 1.4 onward `assert` is a **keyword**, not a legal identifier.

Until 1.3 you could write `int assert = 10;`. Compiling that as 1.4 fails with: as of release 1.4, `assert` is a keyword (dumps mention `javac -source 1.3` to keep the old identifier, with warnings).

> [!warning] Unverified traps from the dump
> - `-source 1.3` on a file that uses `assert` **as a statement** is a compile error in the dump’s pairing examples.
> - From 1.4 you cannot use `assert` as a variable name at the default source level.
