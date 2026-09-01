<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Datatype Channel says every message on a channel has the same type so the receiver already knows how to process it. When that contract is broken — a byte message on a text channel, XML that is not well formed or does not match the agreed DTD or schema — the broker may still deliver the message. The receiver cannot process it, so it is invalid and should be moved to the Invalid Message Channel.

The messaging system guaranteed delivery, not that the receiver would understand the body. Without an invalid channel, the wrong-type message either loops on the datatype channel or is dropped and the contract violation is hidden.
> [!warning] Unverified traps from the dump
> - Fixing the sender or splitting channels is the real repair; the Invalid Message Channel only isolates the evidence.
