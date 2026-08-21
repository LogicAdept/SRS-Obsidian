<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: only `Throwable` and its subclasses can be thrown by the JVM or a `throw` statement, and only those types can be the argument type of a `catch` clause. Custom application types should extend `Exception` or `RuntimeException`, not `Throwable` itself.
> [!warning] Unverified traps from the dump
> - Older dumps sometimes call Throwable an interface; it is a class.
> - Extending Throwable directly creates a type that is neither Exception nor Error, so catch (Exception e) will miss it.
