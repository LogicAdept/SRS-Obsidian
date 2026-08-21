<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: no. Parent throws RuntimeException (or ArithmeticException). Override throws Exception or IOException — compile error.

An unchecked throws clause does not create a checked contract. The parent's checked set is empty, so the child cannot introduce IOException or Exception.
> [!warning] Unverified traps from the dump
> - RuntimeException in throws is optional documentation; it does not license a checked exception on the override.
