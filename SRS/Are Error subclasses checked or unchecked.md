<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/Checked #Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps group `Error` with unchecked throwables: the compiler does not require `catch` or `throws` for `Error` or its subclasses (same compile-time rule as `RuntimeException`).

Checked exceptions are the other `Throwable` subclasses — everything except `RuntimeException` and `Error` (and their children). Examples listed next to Error: `OutOfMemoryError`, `VirtualMachineError`, `AssertionError`.
> [!warning] Unverified traps from the dump
> - Unchecked does not mean RuntimeException-only; Error is unchecked and is not a RuntimeException.
> - Some dumps still say Error cannot be caught; the language allows catch (Error) or catch (Throwable).
