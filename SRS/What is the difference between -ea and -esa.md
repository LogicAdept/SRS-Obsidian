<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps split two enable flags:

- `-ea` / `-enableassertions` — enable assertions in every **non-system** class (user / application classes).
- `-esa` / `-enablesystemassertions` — enable assertions in every **system** class (predefined / platform classes).

Matching disable flags: `-da` for non-system, `-dsa` / `-disablesystemassertions` for system classes.

> [!warning] Unverified traps from the dump
> - `-ea` does **not** turn on assertions inside the JDK/system classes; that is `-esa`.
> - The four flags can appear together; dumps apply them left to right.
