<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS

# What happens when a message of the wrong type arrives on a Datatype Channel

> [!abstract] Short answer
> The broker still delivers it — a Datatype Channel is an application convention, not something the transport enforces. The receiver fails to recognize the type, treats the message as invalid, and moves it to the Invalid Message Channel instead of looping or dropping it.

## Delivery succeeds, interpretation fails

A Datatype Channel promises that every message on the channel has the same type, so the receiver already knows how to decode it. Nothing in the broker enforces that promise: a `BytesMessage` sent on a channel whose consumers expect `TextMessage` is transmitted happily, and so is XML that is not well-formed or does not validate against the agreed schema. When the receiver runs its check — in JMS, an `instanceof` test on the delivered `Message`; for XML, a schema validation pass — the contract breach surfaces **after delivery**, which is exactly the Invalid Message Channel trigger. Without a quarantine to park the evidence, the wrong-type message either sits back on the working channel (the requeue loop described in [[What happens if a receiver puts an invalid message back on the original channel]]) or is swallowed silently, and the violation stays invisible.

```java
public void onMessage(Message msg) {              // Conceptual
    if (msg instanceof TextMessage text) {
        process(text.getText());
    } else {
        msg.setJMSCorrelationID(msg.getJMSMessageID());
        invalidProducer.send(msg);                 // park, do not requeue
    }
}
```

**Listing 1.** Conceptual receiver shape from the book's JMS examples: the type check is the Datatype Channel contract; the `else` branch is the Invalid Message Channel move.

> [!warning] The quarantine is not the repair
> Parking proves the contract broke; it does not fix it. The repair is on the sender — send the right type — or in topology: the two contracts do not belong on one channel at all. How the preventive contract and the corrective quarantine relate is compared in [[What is the difference between Datatype Channel and Invalid Message Channel]].

> [!tip] Interview answer
> The messaging system delivers the message successfully because channel typing is an application agreement, not broker enforcement. The receiver's type check or schema validation fails, so the receiver treats the payload as an invalid message and parks it on the invalid channel. That makes the contract violation visible and diagnosable while the happy path stays clean.
