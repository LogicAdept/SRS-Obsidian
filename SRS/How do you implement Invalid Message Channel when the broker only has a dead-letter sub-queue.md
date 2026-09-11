<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# How do you implement Invalid Message Channel when the broker only has a dead-letter sub-queue

> [!abstract] Short answer
> Use the sub-queue deliberately, and let the **reason fields** carry the pattern split. On Azure Service Bus the receiver calls `Deadletter` (dead-lettering the message itself) after its validation fails, sets `DeadLetterReason`/`DeadLetterErrorDescription` to say *why*, and a triage consumer drains `<queue>/$deadletterqueue`, separating application-invalid messages from broker-dead ones.

## One physical sub-queue, two roles

Service Bus attaches a dead-letter sub-queue to every queue and subscription, addressable as `<queue path>/$deadletterqueue` (and a transfer variant `<queue path>/$Transfer/$DeadLetterQueue`). The receiver-side API makes it a valid parking place for the Invalid Message Channel role: after a peek-lock receive and a failed validation — the wrong region code, an unparsable payload — the application calls `DeadLetterMessageAsync` with its own reason, and the client documentation recommends putting the exception type into the reason and the stack trace into the description, minding the 256-character limit. Broker-dead traffic arrives in the same sub-queue with system reason codes: `MaxDeliveryCountExceeded` ("message couldn't be consumed after maximum delivery attempts", default delivery count 10), `TTLExpiredException` when expiry dead-lettering is enabled, `HeaderSizeExceeded` for quota violations. A triage consumer reads `DeadLetterReason`/`DeadLetterErrorDescription`, fixes or forwards, and completes the message — the official sample's flow — because parked messages count toward the entity's size and an undrained sub-queue eventually blocks new traffic. This is the pragmatic answer when no dedicated channel exists, the role-mechanism tension of [[What is the difference between an Invalid Message Channel and a broker queue or topic]].

Event Grid goes further in the same direction: for endpoint errors that cannot be fixed by retrying — HTTP 400 (bad request) or 413 (entity too large), plus 401/403 for webhooks — it does not retry at all; the event is dead-lettered into a blob container if dead-lettering is configured, and dropped otherwise, leaving only a storage artifact instead of a channel.

```text
Receiver:  receive (peek-lock) -> validate -> DeadletterMessageAsync(
             reason: "UnknownRegion", description: details)     // app-deadletter
Broker:    MaxDeliveryCountExceeded / TTLExpiredException        // broker-dead
Triage:    receiver on $deadletterqueue -> branch on DeadLetterReason
           -> fix/forward -> CompleteMessageAsync                 // drain
```

**Listing 1.** The three actors and the field that separates the roles: the reason string is where the pattern split lives.

> [!warning] A shared sub-queue hides the role boundary
> Without reason discipline, app-invalid and broker-dead messages merge into one undifferentiated pile, and the quarantine's diagnostic value evaporates — the conflation risk of [[What is the difference between Invalid Message Channel and Dead Letter Channel]] at its most literal. The receiver-side decision loop that feeds this sub-queue is in [[How does a receiving application move a poison message to an Invalid Message Channel]].

> [!tip] Interview answer
> On a broker like Service Bus you use the dead-letter sub-queue as the quarantine: the receiver dead-letters the message itself with explicit reason and description after validation fails, while broker dead messages arrive there with system reasons like MaxDeliveryCountExceeded or TTLExpiredException. Triage runs on the sub-queue, branches on the reason, and drains — undrained, it fills the entity's quota.
