<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. The set of constants is fixed in the source. You cannot extend the enum in code to add elements later, and you cannot subclass an enum to add constants.

Binary-compatible evolution of enum types is mentioned in official material; these interview dumps only say you cannot add elements in the running program.

> [!warning] Unverified traps from the dump
> - Do not confuse with adding elements to an `EnumSet` of already-declared constants.
