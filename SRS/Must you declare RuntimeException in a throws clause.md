<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: no. Unchecked exceptions (`RuntimeException` and subclasses) need not appear in `throws` and need not be caught. You may still write `throws RuntimeException` (or a subclass); the compiler does not require it. Checked types such as `IOException` must be caught or declared.
> [!warning] Unverified traps from the dump
> - Declaring throws NullPointerException does not stop an NPE from being thrown.
> - A throws clause listing only unchecked types does not satisfy a checked-exception obligation.
