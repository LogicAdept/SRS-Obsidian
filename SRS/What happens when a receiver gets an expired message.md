<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# What happens when a receiver gets an expired message

> [!abstract] Short answer
> It depends on who notices the expiry first. If the **messaging system** sees the message is expired before delivery, it discards it or moves it to a Dead Letter Channel. If the message **was delivered** and the receiver then judges it expired for its purposes, the receiver treats it as an invalid message and moves it to the Invalid Message Channel.

## The same timestamp, two owners

Message Expiration attaches a deadline to a message, and the pattern page splits the enforcement cleanly: broker-side expiry is messaging-system machinery — the comparison happens against the broker's clock before delivery, so it looks like Dead Letter Channel behavior and needs no application code. But a receiver can also receive a message and only then determine that the deadline has passed for its processing — for example a trade request that must execute within seconds, where clock skew or provider delivery delays make the receiver the first one able to judge. That receiver-side judgment is a validity decision about the message's content and headers, so the message goes to the Invalid Message Channel — the reasoning tracks [[What is the difference between Invalid Message Channel and Dead Letter Channel]].

On a Publish-Subscribe Channel the split matters twice over: each subscriber gets its **own copy**, so one subscriber declaring its copy expired does not force that verdict on the others. The deadline judgment is per-receiver, which is another consequence of validity being receiver-relative ([[How does validity of a message depend on the receiver]]).

```text
Expiry noticed by    When                        Destination
-------------------- --------------------------- --------------------------
Messaging system     before delivery             Dead Letter Channel /
                                                 discard (broker machinery)
Receiver             after delivery              Invalid Message Channel
                                                 (application decision)
```

**Listing 1.** The book's Message Expiration notes route the two cases to two different patterns; the decision point is delivery, not the timestamp itself.

> [!warning] Time normalization is the broker's job
> The producer's clock and the broker's clock may disagree by hours. The messaging system is expected to normalize time when comparing the expiration against its own clock, and receivers should not re-derive deadlines from raw local timestamps without agreeing on a clock — otherwise a merely skewed message gets parked as "expired".

> [!tip] Interview answer
> Expiry found before delivery is broker business: the messaging system drops or dead-letters the message. Expiry discovered after delivery — the receiver decides the message is too late to be useful — is a receiver decision, so the message moves to the Invalid Message Channel like any other message the receiver cannot process. On pub-sub each subscriber judges its own copy independently.
