<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A channel-chapter dump: a dead message is one the messaging system cannot deliver; an invalid message is delivered but the receiver cannot process it. Dead-message handling is the broker evaluating its delivery headers, and the developer is stuck with whatever Dead Letter Channel the product ships.

Invalid-message handling is the receiver moving the message because of the body or particular header fields it cares about, so the developer designs that path, including messages that look dead but the messaging system does not treat as dead.
> [!warning] Unverified traps from the dump
> - Using the broker DLQ as the only invalid-message destination mixes delivery failures with application-invalid payloads.
> - Receiver-side expiry after delivery is one dump's example of a seemingly dead message the application still parks as invalid.
