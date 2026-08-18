<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: it is **always inappropriate** to validate **public** method arguments with `assert`. A caller cannot know whether assertions are enabled on the JVM that runs the library.

Command-line arguments are the same case: they are arguments to public `main`, so do not assert on `args`.

For real input checks, dumps contrast `if (...) throw new IllegalArgumentException(...)` (always executes) with `assert` (off by default).

It **is** described as appropriate to assert on **private** method arguments (internal invariants).

> [!warning] Unverified traps from the dump
> - “Inappropriate” here means the check may never run in production, not that `javac` rejects it.
> - Public-API failures should stay visible as ordinary exceptions, not optional `AssertionError`.
