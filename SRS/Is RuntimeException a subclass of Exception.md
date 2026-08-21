<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps draw the tree as `Throwable` splitting into `Error` and `Exception`, with `RuntimeException` under `Exception` — not as a sibling of `Exception` under `Throwable`. Unchecked application exceptions live on that `RuntimeException` branch; other `Exception` subclasses are the checked branch.
> [!warning] Unverified traps from the dump
> - Popular diagram lie: placing RuntimeException as a direct child of Throwable next to Exception.
> - Because it extends Exception, catch (Exception e) also matches NullPointerException and other runtime exceptions.
