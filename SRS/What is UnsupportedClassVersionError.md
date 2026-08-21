<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview lists under "Exception in thread main": `java.lang.UnsupportedClassVersionError` when a class is compiled with one JDK and run with another (typically a newer class-file version on an older runtime).

It is an Error (linkage / class-format family), not a checked Exception you declare on `main`.
> [!warning] Unverified traps from the dump
> - This is not NoClassDefFoundError; the class file is present but its version is rejected.
> - Dumps say compiled from another JDK and run from another; the usual case is compile newer, run older.
