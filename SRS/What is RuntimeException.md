<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `RuntimeException` is the superclass of Java's application unchecked exceptions — types the compiler does not force you to catch or declare. Interview lists place it under `Exception` (not beside it under `Throwable`). Common subclasses named in dumps: `NullPointerException`, `IllegalArgumentException`, `ClassCastException`, `ArithmeticException`, `ArrayIndexOutOfBoundsException`, `NumberFormatException`.
> [!warning] Unverified traps from the dump
> - Dumps also call Error unchecked; that is the JLS Error branch, not a RuntimeException subclass.
> - Popular diagram lie: drawing RuntimeException as a sibling of Exception under Throwable.
