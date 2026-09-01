<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

An Invalid Message Channel whose contents are ignored is about as useful as an error log that is ignored. Messages there mean integration is broken: a sender is publishing the wrong type or format, or a receiver's contract changed.

Those messages should be analyzed and the underlying coding or configuration problem fixed. Automation that consumes invalid messages and repairs the cause is ideal, but the cause is often a developer or analyst change. At minimum, applications that use the pattern need a process that watches the channel and alerts administrators whenever it contains messages. Senders of trade requests, for example, may watch the invalid channel to see whether their requests are being discarded.
> [!warning] Unverified traps from the dump
> - Parking invalid messages without alerting still lets the queue fill until the broker refuses new traffic.
