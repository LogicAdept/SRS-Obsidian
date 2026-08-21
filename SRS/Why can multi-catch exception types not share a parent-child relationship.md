<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Java 7 multi-catch, catch (A | B e), requires alternatives that are not related by subclassing. If one listed type is a subclass of another, the compiler rejects the union as redundant: the parent would already catch the child.

The catch parameter is implicitly final and cannot be reassigned.
> [!warning] Unverified traps from the dump
> - Use multi-catch only when the handling logic is truly the same for each type.
> - Parent-before-child in separate catch blocks is an unreachable-catch error, not this multi-catch union error.
