<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A Java EIP dump's channel table lists Invalid Message Channel as the role that separates malformed or contract-breaking messages so bad data stays visible and recoverable. Implementations it names are a validation error topic or a quarantine queue.

It then says a Kafka topic, a JMS queue, or a RabbitMQ exchange is a mechanism. The EIP channel name describes the role that destination plays in the design, not the broker primitive itself.
> [!warning] Unverified traps from the dump
> - Naming a queue invalid-messages does not turn broker expiry and unroutable traffic into Invalid Message Channel behavior.
> - The same table's Dead Letter Channel row is recovery after failure, which dumps often collapse into the same quarantine topic.
