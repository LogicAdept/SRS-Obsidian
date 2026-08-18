<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: autoboxing is fine for occasional conversions — adding items to a list, returning a value from a method. It becomes a problem in tight loops or high-frequency code where thousands of wrapper objects are created and discarded per second.

Using `ArrayList` for a list you iterate once is described as fine. Using `Long` as a loop counter in a calculation that runs millions of times is not. Profile first.

> [!warning] Unverified traps from the dump
> - The dump’s “always avoid autoboxing” is the wrong takeaway; the trap is hot loops and accumulators.
> - A wrapper loop accumulator (`Long total = 0L`) boxes on every `+=`.
