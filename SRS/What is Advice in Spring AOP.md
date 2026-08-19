<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Advice is the action an aspect takes at a matched join point — the actual extra code.

Dump types: `before`, `after` (finally), `after-returning`, `after-throwing`, `around`.

Dumps also warn that `after`/`around` only see the method boundary. If a method swallows an exception inside try/catch, after-throwing / transaction rollback may not see it unless the error leaves the method.

> [!warning] Unverified traps from the dump
> - There is already a card listing advice types; this one is the definition of Advice.
