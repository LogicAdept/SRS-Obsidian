<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: assertions are a **debugging** aid for development and test, not production control flow.

**Appropriate** examples:

- Validating **private** method arguments (internal assumptions).
- A branch that must be unreachable, for example `default: assert(false);` in a `switch` on a closed set of months.

**Inappropriate** examples:

- Mixing required program logic with `assert` (no guarantee it runs).
- Validating **public** method arguments.
- Validating command-line arguments (`main`).

> [!warning] Unverified traps from the dump
> - `assert(false)` in `default` only fires if assertions are enabled; it is not a substitute for throwing in production.
