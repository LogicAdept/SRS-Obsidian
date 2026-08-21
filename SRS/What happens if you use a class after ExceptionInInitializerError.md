<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump scenario: class `A` has a static block that throws `ArithmeticException` (`1/0`). The first `new A()` raises `ExceptionInInitializerError` caused by that `ArithmeticException`.

If that Error is caught and the code tries `new A()` again, dumps show `NoClassDefFoundError: Could not initialize class ...A` — the JVM does not retry static initialization after the first failure.

Dump advice: prevent `ExceptionInInitializerError` because it is likely followed by `NoClassDefFoundError`.
> [!warning] Unverified traps from the dump
> - The second failure is NoClassDefFoundError, not a second ExceptionInInitializerError.
> - This is a different NCDFE path than a missing .class file on the classpath.
