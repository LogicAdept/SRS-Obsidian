<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: both branches are unchecked (no required `throws` / `catch`).

`RuntimeException` (NPE, `ArithmeticException`, bounds errors) is treated as a programming defect the application can often prevent or handle. `Error` (`OutOfMemoryError`, `StackOverflowError`, `VirtualMachineError`) is treated as an environment / JVM failure that ordinary code should not try to recover from.

`Error` is a sibling of `Exception` under `Throwable`; `RuntimeException` sits under `Exception`.
> [!warning] Unverified traps from the dump
> - Some dumps call Error a runtime exception; it is not a subclass of RuntimeException.
> - Both are unchecked, but catch (RuntimeException e) still misses Error.
