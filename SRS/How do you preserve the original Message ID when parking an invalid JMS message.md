<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In the JMS Request-Reply dump, both Requestor and Replier keep a MessageProducer on a queue named jms/InvalidMessages. When the received message is not a TextMessage (or the request has no JMSReplyTo), they do not discard it. They resend it to that invalid-message queue.

Resending is a new send, so the messaging system assigns a new Message ID. Before send, the dump copies the original JMSMessageID onto JMSCorrelationID so triage still has the original identity: msg.setJMSCorrelationID(msg.getJMSMessageID()) then invalidProducer.send(msg).
> [!warning] Unverified traps from the dump
> - Parking by resend is not the same message instance on the original destination; correlation is the dump's way to keep the old ID.
> - The Replier also treats a TextMessage without JMSReplyTo as invalid, not only a wrong JMS type.
