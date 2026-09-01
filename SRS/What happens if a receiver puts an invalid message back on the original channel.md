<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If the receiver cannot process a message and puts it back on the same channel, the same receiver or another like it will consume it again. Ignored invalid messages then clutter the channel and hurt performance.

Silently consuming and throwing the message away hides problems that need to be detected. The pattern is to take improper messages off the working channel and park them where they are out of the way but still visible for diagnosis.
> [!warning] Unverified traps from the dump
> - Abandon or nack-with-requeue on a permanently bad payload creates a poison loop until a delivery-count cap finally dead-letters it.
