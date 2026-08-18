<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: assertions can be stripped at compile time or turned off at runtime, so they must **not** change program behavior when removed. Do not call methods that mutate program state or the environment inside `assert`.

Because there is no guarantee the statement runs, it is inappropriate to put **required** logic in an assert (for example using assert to update a variable).

Coder-style dump: never use `assert` for anything with side effects; use `if (...) throw ...` when the check must always run.

> [!warning] Unverified traps from the dump
> - A dump example treats `assert` that assigns through the detail expression as inappropriate for the same reason: the assignment may not happen.
> - Side-effect-free still matters when assertions **are** enabled: the detail expression is only evaluated on failure.
