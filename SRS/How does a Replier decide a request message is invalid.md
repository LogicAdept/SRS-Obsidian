<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The JMS Request-Reply dump uses three queues: jms/RequestQueue, jms/ReplyQueue, and jms/InvalidMessages. The Replier is an Event-Driven Consumer. onMessage accepts the request only if it is a TextMessage and JMSReplyTo is set. Otherwise it prints Invalid message detected and moves the message to jms/InvalidMessages.

A separate InvalidMessenger in the same dump sends an ObjectMessage on the request Datatype Channel while the Replier expects TextMessage. The Replier does not recognize the format and reroutes to the invalid queue. The request channel is still a Datatype Channel; the invalid channel is where the wrong type goes after delivery.
> [!warning] Unverified traps from the dump
> - Missing Return Address (JMSReplyTo) is enough to classify the request as invalid even if the body is text.
> - A malicious or mistaken sender can put a well-formed message of the wrong JMS type on the request channel; delivery still succeeds.
