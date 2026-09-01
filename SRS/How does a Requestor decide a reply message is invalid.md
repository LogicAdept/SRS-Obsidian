<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The JMS Request-Reply dump's Requestor is a Polling Consumer on the reply queue. receiveSync accepts the reply only if it is a TextMessage. If the delivered reply is another JMS type, it prints Invalid message detected and resends the message to jms/InvalidMessages instead of discarding it.

Resend is a new send, so the broker assigns a new Message ID. Before send, the dump copies the original JMSMessageID onto JMSCorrelationID, the same parking step Replier.onMessage uses on the request Datatype Channel. Requestor.receiveSync is the reply-side copy of that invalid-message processing.
> [!warning] Unverified traps from the dump
> - A well-delivered reply of the wrong JMS type is still invalid for that Requestor.
> - Sharing jms/InvalidMessages with the Replier does not mean the parked payload was a failed request; it may be a failed reply.
