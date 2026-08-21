<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If try (or catch) throws and finally also throws, the exception from finally is the one that leaves the try statement. The earlier pending exception is discarded.

This is why throwing from finally is treated as a bug in interviews: the original failure is lost, so debugging shows only the cleanup error.

The same finally-wins rule applies when catch throws one exception and finally throws another.
> [!warning] Unverified traps from the dump
> - A handwritten finally does not attach the original as a suppressed exception; that bookkeeping is try-with-resources.
> - A return in finally is another way to discard a pending exception: the method then completes normally.
