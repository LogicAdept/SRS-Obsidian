<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The return in finally completes the method normally. The pending exception from try is discarded: no exception is thrown and no stack trace appears.

The same swallowing happens if finally returns after catch threw. Interview dumps treat return-in-finally as legal but almost always a bug.
> [!warning] Unverified traps from the dump
> - This is not a compile error; IDEs typically only warn.
> - throw in finally replaces the original exception instead of swallowing it; return swallows it completely.
