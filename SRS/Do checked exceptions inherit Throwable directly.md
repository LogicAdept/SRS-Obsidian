<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Some dumps define checked exceptions as classes that directly inherit `Throwable` except `RuntimeException` and `Error` (`IOException`, `SQLException`). That wording is a popular lie: neither `IOException` nor `RuntimeException` inherits `Throwable` directly — they sit under `Exception`. The tree rule the same dumps also state: checked means `Exception` minus `RuntimeException`; `Error` and `RuntimeException` are unchecked.
> [!warning] Unverified traps from the dump
> - Direct subclasses of Throwable are Exception and Error, not IOException.
> - Checked versus unchecked is which branch you sit on, not how many hops from Throwable.
