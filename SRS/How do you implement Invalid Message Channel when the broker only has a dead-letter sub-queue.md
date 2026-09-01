<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Azure Service Bus (and AppFabric before it) expose a dead-letter sub-queue under each queue or subscription, not a separate invalid-message queue. The receiver still implements Invalid Message Channel: after peek-lock receive, if the payload is the wrong format or fails a business check, it calls Deadletter with a reason and description. Those values land on the message as DeadLetterReason and DeadLetterErrorDescription so a triage consumer can tell application-invalid from broker-dead (TTL, MaxDeliveryCount, filter evaluation).

Event Grid has no invalid-message channel either: HTTP 400 or 413 from the receiver causes an immediate dead-letter. At the time of that dump, Event Grid could only write those events to a blob, which is not a messaging channel, so an operator must pull them.
> [!warning] Unverified traps from the dump
> - DeliveryCount is not incremented when reading the dead-letter sub-queue, and Deadletter cannot be called again on a message already there.
> - If dead-lettered messages are never drained, queue size includes them and the entity can stop accepting new messages.
