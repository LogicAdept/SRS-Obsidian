<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When try executes return x, the value of x is saved first, then finally runs, then that saved value is returned. Assigning a new value to the local in finally does not change the already-saved return.

If x is a reference to a mutable object, finally can still mutate the object through that reference, so the caller observes the mutation even though the returned reference is the one saved before finally.
> [!warning] Unverified traps from the dump
> - This is a different rule from return in finally, which replaces the saved value entirely.
> - Interview output questions often mix the two: mutating the local versus returning from finally.
