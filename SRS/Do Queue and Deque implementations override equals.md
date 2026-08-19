<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: implementations of both `Deque` and `Queue` usually **do not override** `equals()` and `hashCode()`. They use the inherited `Object` methods based on **reference** comparison.

> [!warning] Unverified traps from the dump
> - Two queues with the same elements in the same order are **not** equal by content in this dump.
> - Contrast with `List`, which does define equality by sequence.
