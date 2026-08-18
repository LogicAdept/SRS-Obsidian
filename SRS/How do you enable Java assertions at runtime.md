<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pass `-ea` (or the long form `-enableassertions`) to the `java` launcher. Dumps: assertions are **disabled by default**, so `java Test` does not run `assert` statements. `java -ea Test` does.

`-ea` with no class/package argument enables assertions in every **non-system** (user) class.

> [!warning] Unverified traps from the dump
> - Enabling is a **runtime** JVM flag, not a compile-time switch. `javac` still compiles `assert`.
> - `-enableassertions` is the same flag as `-ea`.
