<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps put class-linking failures under `LinkageError`, a subclass of `Error`. Common children in those lists: `NoClassDefFoundError` and `ExceptionInInitializerError` (also `NoSuchMethodError` / incompatible class-change errors in other dumps).

The claimed meaning: a class depended on another type that was present at compile time but is missing or incompatibly changed at runtime.
> [!warning] Unverified traps from the dump
> - ClassNotFoundException is a checked Exception from reflective load-by-name, not a LinkageError.
> - A failed static initializer can surface first as ExceptionInInitializerError and later as NoClassDefFoundError — both under LinkageError.
