<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

An Advent-of-EIP dump asks what happens when a message cannot be processed: malformed JSON, a schema version the consumer does not understand, or a queue that does not exist. It then names Invalid Message Channel as also known as a Dead Letter Queue and lists what ends up there: malformed messages (invalid JSON, missing required fields, wrong data types), poison messages that always crash the consumer, expired messages that exceeded TTL, and unroutable messages sent to non-existent queues or exchanges.

It also lists characteristics of that combined destination: no data loss (not silently dropped), operators can inspect failures, some DLQ systems can replay after a fix, and a spike is an alerting hook. RabbitMQ wiring in the same dump routes reject, expiry, and max-length overflow to a dead-letter exchange labeled as Invalid Message Channel.
> [!warning] Unverified traps from the dump
> - Unroutable destinations, TTL expiry, and queue-length overflow are broker Dead Letter Channel cases; dumps that equate IMC with a DLQ import them.
> - Malformed JSON after successful delivery is the Invalid Message Channel half of that list; the dump does not keep the split.
