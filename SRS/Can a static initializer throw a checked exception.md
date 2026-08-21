<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: no. A static {} block is not a method and has no throws clause, so an explicit throw of a checked type (or a call that throws one) does not compile.

You may try/catch inside the static block and handle the checked exception there, without rethrowing it. Wrapping as an unchecked exception is the other dump workaround.
> [!warning] Unverified traps from the dump
> - There is no throws you can attach to a static initializer.
> - An uncaught RuntimeException from static initialization still surfaces as ExceptionInInitializerError.
