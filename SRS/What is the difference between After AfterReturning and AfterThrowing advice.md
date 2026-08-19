<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

From dumps:

- **`@After` (finally):** runs after the method, success or exception (not if the JVM dies).
- **`@AfterReturning`:** only if the method completes normally. Can bind the return value (`returning = "result"`).
- **`@AfterThrowing`:** only if the method throws. Can bind the throwable (`throwing = "ex"`).

`@After` does not give you the return value or the exception as cleanly as the specialized two.

> [!warning] Unverified traps from the dump
> - If the method catches the exception internally, AfterThrowing does not run.
