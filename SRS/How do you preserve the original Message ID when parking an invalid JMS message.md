<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# How do you preserve the original Message ID when parking an invalid JMS message

> [!abstract] Short answer
> Parking is a **new send**, so the provider mints a new `JMSMessageID`. Before sending, copy the original id onto the correlation id: `msg.setJMSCorrelationID(msg.getJMSMessageID())`. The parked message then still points at the identity it had on the working channel, and triage can trace it.

## Why the copy is needed and why it is legal

The book's JMS example does exactly this in both parking sites — the Replier on the request side and the Requestor on the reply side — right before `invalidProducer.send(msg)`. Resending is not the same message instance traveling again; it is a fresh provider message, so the provider assigns a fresh `JMSMessageID` on send and the old id would be lost without the copy. The trick is legal because of the JMS header ownership rules: `JMSMessageID` is **provider-set** — a client cannot choose it — while `JMSCorrelationID` is **client-set**, free-form, and meant precisely for linking related messages. Linking a parked copy to its original is the Correlation Identifier idea applied to quarantine traffic ([[What is the Correlation Identifier pattern]]).

The .NET twin of the example does the same thing with MSMQ: `requestMessage.CorrelationId = requestMessage.Id` before `invalidQueue.Send`, and the MSMQ `Message.CorrelationId` documentation defines the property as the identifier used by acknowledgment, report, and response messages to reference the original message.

```text
On the working channel            On the invalid channel
--------------------------------  ----------------------------------------
JMSMessageID  = ID:abc123         JMSMessageID      = ID:xyz789  (new, provider)
JMSCorrelationID = <reply link>   JMSCorrelationID  = ID:abc123  (copied)
                                  -> original identity survives the resend
```

**Listing 1.** The id swap in the official example: the parked copy's correlation id is the working-channel message id.

> [!warning] Parking is not forwarding the same instance
> Teams that assume the parked message "is" the original get burned by two details: the new `JMSMessageID` breaks naive log correlation, and properties set by the provider on the original send are re-derived on the resend. Store what you need in the correlation id or message properties before sending — as in [[How does a Replier decide a request message is invalid]].

> [!tip] Interview answer
> Since parking means sending a new message, the provider overwrites the message id — so before the send you copy the original `JMSMessageID` into `JMSCorrelationID`, which is client-settable by design. That keeps the original identity queryable on the invalid queue; the MSMQ version of the example does the identical thing with `CorrelationId = Id`.
