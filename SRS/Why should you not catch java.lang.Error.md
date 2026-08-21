<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: recovery from an Error is almost never possible, so the process should be allowed to terminate.

Worked dump claim: if `OutOfMemoryError` or `StackOverflowError` is caught, the JVM may not be able to free enough memory for the rest of the application to continue, so catching and continuing is worse than letting the process die.

Handling Error is not forbidden; it is discouraged except last-resort logging or cleanup at a boundary.
> [!warning] Unverified traps from the dump
> - Can you catch Error and should you catch Error are different questions; catch is legal.
> - catch (Exception e) does not catch Error; catch (Throwable t) does.
