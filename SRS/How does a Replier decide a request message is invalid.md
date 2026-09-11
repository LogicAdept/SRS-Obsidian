<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# How does a Replier decide a request message is invalid

> [!abstract] Short answer
> In the book's JMS Request-Reply example the Replier accepts a request only if it is a `TextMessage` **and** carries a `JMSReplyTo` destination. Anything else — wrong body type or a missing return address — is invalid: the Replier prints "Invalid message detected" and resends the message to the `jms/InvalidMessages` queue.

## The two checks in the official example

The Replier is an Event-Driven Consumer whose `onMessage` implements the request channel's Datatype Channel contract: requests are `TextMessage`s. The InvalidMessenger in the same example deliberately sends an `ObjectMessage` on that channel — delivery succeeds, the `instanceof TextMessage` check fails, and the message "does not recognize the format", so it moves to the invalid queue. The second check is the Return Address: a request that cannot say where the reply goes cannot fulfill Request-Reply even though its body parses, so a null `JMSReplyTo` alone classifies the request as invalid — the return-address half of the contract is in [[What is the Return Address pattern]].

The reply side runs the mirror image of the same code: the Requestor polls the reply queue with `receive` and applies the same `instanceof TextMessage` test, parking a wrong-typed reply on the same invalid queue. Both sides keep the original identity when parking, which is the mechanics of [[How do you preserve the original Message ID when parking an invalid JMS message]].

```java
public void onMessage(Message request) {            // Conceptual, book example shape
    if (request instanceof TextMessage && request.getJMSReplyTo() != null) {
        reply((TextMessage) request);
    } else {
        System.out.println("Invalid message detected");
        request.setJMSCorrelationID(request.getJMSMessageID());
        invalidProducer.send(request);               // jms/InvalidMessages
    }
}
```

**Listing 1.** Conceptual shape of the Replier's decision: type check plus return-address check, then a resend — not a requeue — to the invalid queue.

> [!warning] Well-formed does not mean processable
> A malicious or buggy sender can deliver a perfectly formed message of the wrong JMS type; the provider transmits it without complaint. The Replier's validity tests run after delivery — that is the whole reason the invalid queue exists in the example, and the general catalog behind it is [[What kinds of delivered messages does a receiver treat as invalid]].

> [!tip] Interview answer
> The Replier checks two things before processing a request: is it the expected datatype (`TextMessage`) and does it carry a return address (`JMSReplyTo`). If either fails, the request is invalid — the Replier copies the message id onto the correlation id and sends it to `jms/InvalidMessages`, where the error handler can inspect it. The Requestor applies the same test to replies.
