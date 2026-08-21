<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps treat `Error` as a separate `Throwable` branch so the idiom `catch (Exception e)` can catch application exceptions without also catching JVM-level failures such as `OutOfMemoryError` or `StackOverflowError`. Ordinary programs are not expected to recover from that `Error` branch.
> [!warning] Unverified traps from the dump
> - The sibling split is about catch (Exception e), not a language ban on catching Error.
> - Recoverability is a convention; Error remains a Throwable and can be caught.
