<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pass `-da` (or `-disableassertions`) to disable assertions in every **non-system** class. Dumps also list `-dsa` / `-disablesystemassertions` for system classes.

Because the default is already off, `-da` is used to turn assertions **back off** after a broader `-ea` (for example enable a package, then disable one class).

> [!warning] Unverified traps from the dump
> - `-disableassertions` is the same flag as `-da`.
> - Flags can be mixed; dumps say they are applied **left to right**.
