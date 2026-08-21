<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the lambda may throw only what the target functional method declares.

Consumer / Function / Iterable.forEach declare no checked throws, so throwing IOException from the lambda body does not compile unless you catch it inside or wrap it in a RuntimeException. A custom @FunctionalInterface whose method declares throws Exception may throw checked types.

Unchecked exceptions (IllegalArgumentException) can be thrown from forEach without a throws clause.
> [!warning] Unverified traps from the dump
> - Callable.call() declares throws Exception, so a Callable lambda may throw checked types; Runnable.run() may not.
> - Wrapping in RuntimeException is a compiler bypass used with Stream APIs, not a language exception to catch-or-specify.
