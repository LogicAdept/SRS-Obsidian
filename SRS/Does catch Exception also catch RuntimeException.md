<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: yes. `RuntimeException` is a subclass of `Exception`, so `catch (Exception e)` matches both checked types such as `IOException` and unchecked types such as `NullPointerException`. That is why catching `Exception` is blunt — it folds the checked and runtime branches together.
> [!warning] Unverified traps from the dump
> - catch (Exception e) is not reserved for checked exceptions.
> - A handler meant for I/O can swallow an unexpected NullPointerException.
