<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `java.lang.Class` is the entry point. It is the runtime metadata for a class or interface: name, methods, fields, constructors, super types. From it you create instances, invoke methods, and reach members that source-level access would hide.

Companion types in `java.lang.reflect`: `Field`, `Method`, `Constructor`, and `Array` (length / element access / create).

> [!warning] Unverified traps from the dump
> - Every reflective lookup starts with a `Class` object.
