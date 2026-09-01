<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

An Advent-of-EIP dump says an Invalid Message Channel would catch events that fail validation after they are already queued, for example when producer and consumer schema versions diverge. Instead of crashing the consumer or dropping the event, it routes the payload to a dead-letter destination (chronicle.events.dead-letter) for investigation.
> [!warning] Unverified traps from the dump
> - Schema mismatch after delivery is a receiver-invalid case; the dump still names the destination like a broker DLQ.
> - A consumer crash on unknown fields is not the same as the broker failing to deliver.
