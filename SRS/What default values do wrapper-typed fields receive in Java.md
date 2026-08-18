<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

One compilation dump answers “default values of the wrapper classes” as:

- `null` for `Integer`, `Double`, `Boolean`, etc.
- `0` for numeric wrappers like `Byte`, `Short`, `Integer`, `Long`, `Float`, and `Double`.

Those two bullets contradict each other. Other dumps say a wrapper field that is not assigned is `null` (it is a reference), while numeric *primitives* default to `0`.

> [!warning] Unverified traps from the dump
> - The dump lists both `null` and `0` for the same numeric wrappers — treat as unverified and conflicting.
> - Do not confuse wrapper field defaults with primitive field defaults (`0` / `false` / `\u0000`).
