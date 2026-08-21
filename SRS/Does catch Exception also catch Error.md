<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: no. `Error` is a sibling of `Exception` under `Throwable`, not a subclass of `Exception`. `catch (Exception e)` matches `IOException` and `NullPointerException` but not `OutOfMemoryError`. Catching the root `Throwable` would include `Error`.
> [!warning] Unverified traps from the dump
> - Exception is not a synonym for Throwable and does not catch everything throwable.
> - You can still catch Error via Throwable or Error itself; the sibling split does not make Error uncatchable.
