<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

An Advent-of-EIP dump implements Invalid Message Channel as a RabbitMQ dead-letter exchange. The consumer parses JSON; on parse Error it nacks with requeue False so the broker routes the delivery to the queue's configured DLX instead of putting the payload back on the working queue.

Queue declaration can attach dead_letter_exchange and a DLQ name. The dump also says reject without requeue or message expiry automatically routes to that DLX, and it names the inspect-and-replay helpers invalid_message while still replaying from the DLQ.
> [!warning] Unverified traps from the dump
> - nack with requeue False plus a DLX is broker Dead Letter Channel machinery labeled Invalid Message Channel.
> - The same dump also dumps TTL expiry, max queue length, and unroutable traffic into that DLQ.
