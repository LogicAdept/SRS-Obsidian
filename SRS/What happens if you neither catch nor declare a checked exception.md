<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the compiler rejects the class. Typical message: unreported exception java.io.FileNotFoundException; must be caught or declared to be thrown.

FileReader / FileInputStream used in main with no try/catch and no throws on main is the usual illustration. After adding throws IOException (or a catch), the same code compiles.
> [!warning] Unverified traps from the dump
> - RuntimeException and Error do not produce this compile error even when they can be thrown.
> - throws on main satisfies the compiler; if the exception still escapes, the JVM prints the stack and exits.
