<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **`Hashtable` is traversed by Enumerator and Iterator.** The **Enumerator is not fail-fast.** `HashMap` is traversed by **Iterator**, which **is fail-fast**.

`HashMap`’s Iterator, unlike `Hashtable`’s Enumeration, is fail-fast (throws on inconsistent data).

Enumeration vs Iterator dumps: Enumeration is used on legacy `Vector` / `Stack` / `Hashtable`, and they call Enumeration **fail-safe** while Iterator is fail-fast. Enumeration has `hasMoreElements` / `nextElement` and **no `remove`**.

> [!warning] Unverified traps from the dump
> - “Enumerator not fail-fast” vs “Enumeration is fail-safe” is the same idea with sloppy wording.
> - Enumeration cannot `remove`; Iterator can.
