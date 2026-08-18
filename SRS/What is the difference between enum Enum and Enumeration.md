<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

One dump’s three-way split:

- `enum` — the keyword that declares a group of constants.
- `Enum` — `java.lang.Enum`, the base class; every enum type is a direct subclass.
- `Enumeration` — `java.util.Enumeration`, a cursor interface for walking a collection (legacy vs `Iterator`).

The vault already has [[What is the difference between Enumeration and Iterator in Java]] for the cursor, not for `enum`.

> [!warning] Unverified traps from the dump
> - Do not mix `Enumeration` the iterator with Java 5 `enum` types.
