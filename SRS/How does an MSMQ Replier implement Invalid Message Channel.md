<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A .NET Request-Reply dump defines three queues: private$\RequestQueue, private$\ReplyQueue, and private$\InvalidQueue. The Replier is an Event-Driven Consumer (ReceiveCompleted). OnReceiveCompleted receives the request, reads Body as a string via XmlMessageFormatter, takes ResponseQueue as the Return Address, and sends a reply whose CorrelationId is the request's Id.

If processing throws, it prints Invalid message detected, copies requestMessage.Id onto CorrelationId, and Send the message to invalidQueue. An InvalidMessenger in the same dump sends BodyType 768 (binary) on the request Datatype Channel while the Replier expects text/XML. The Replier does not recognize the format and resends onto the invalid queue. Resend assigns a new Message ID; correlation keeps the original identity.
> [!warning] Unverified traps from the dump
> - Parking by Send is a new MSMQ message, not the same instance on the original queue.
> - Any Exception in OnReceiveCompleted, not only a wrong BodyType, follows the same invalid-queue path in that dump.
