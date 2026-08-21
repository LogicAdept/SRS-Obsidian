<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps split.

One wording: checked types are everything that inherits Throwable except RuntimeException and Error — that includes Throwable itself and Exception, and excludes Error. Another wording: checked types are subclasses of Exception except RuntimeException — that leaves Throwable out.

The same dumps agree that Error and RuntimeException (and their children) are unchecked and that IOException is checked. throws Throwable is treated like a checked declaration: callers must catch or declare it.
> [!warning] Unverified traps from the dump
> - The popular line that checked exceptions directly inherit Throwable is already a dump lie: IOException sits under Exception.
> - catch (Throwable t) compiles even when the try throws no checked type, because Throwable also covers Error and RuntimeException.
