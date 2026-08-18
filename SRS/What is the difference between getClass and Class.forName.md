<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/JVM/ClassLoaders #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`getClass()` is an instance method: the `Class` of that object's runtime type.

`Class.forName(String)` is static: load (and, in the simple overload, initialise) a class by fully qualified name. You do not need an instance.

Dumps: use `getClass()` when you already have an object; use `forName` to load a class dynamically when you only have the name.

> [!warning] Unverified traps from the dump
> - `forName` uses the caller's ClassLoader in the one-arg form.
