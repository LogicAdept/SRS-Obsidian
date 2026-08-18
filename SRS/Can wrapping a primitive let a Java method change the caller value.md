<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

One interview dump lists “change the value in method” as a reason for wrappers: Java is pass-by-value, so a primitive parameter cannot change the caller’s variable, “but if we convert the primitive value in an object, it will change the original value.”

That is the dump’s claim. The same dumps also say wrapper types are immutable, which conflicts with “the method mutates the caller’s number.”

> [!warning] Unverified traps from the dump
> - The dump claims boxing lets a method change the caller’s primitive — treat as a popular lie to verify.
> - Pass-by-value still copies the wrapper reference; reassigning the parameter does not reassign the caller’s variable.
> - Immutable `Integer` has no setter for the wrapped `int`.
