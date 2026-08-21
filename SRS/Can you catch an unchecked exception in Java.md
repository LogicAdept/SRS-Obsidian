<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: yes. Unchecked means the compiler does not require a handler, not that `catch` is illegal. `catch (RuntimeException e)` or `catch (NullPointerException e)` is valid. Dumps still advise against catching programming bugs just to keep going — let them propagate unless you have a real recovery.
> [!warning] Unverified traps from the dump
> - catch (Exception e) also matches RuntimeException, so a handler meant for I/O can swallow an NPE.
> - Optional catch is not the same as forbidden catch.
