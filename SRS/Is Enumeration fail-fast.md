<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump (table): **Enumeration is fail-safe**; **Iterator is fail-fast**. Same dump: Enumeration is **not safe** *because* it is fail-safe; Iterator is **safer**.

Another dump: Iterator **is** fail-fast; Enumeration **is not** fail-fast. Iterator is **slower** than Enumeration.

Another dump: Enumeration is **twice as fast** and uses **less memory**, but Iterator is **safer** because other threads cannot modify the collection being traversed, and Iterator can **remove**.

> [!warning] Unverified traps from the dump
> - “Fail-safe” vs “not fail-fast” is sloppy dump wording for the same row.
> - One compilation page calls Enumeration fail-fast; the interview tables usually say the opposite.
> - Legacy `Hashtable` / `Vector` **enumerations** vs **view iterators** are not the same cursor.
