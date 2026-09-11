<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# What is the difference between the Retry Pattern and Invalid Message Channel

> [!abstract] Short answer
> Retry assumes the **same attempt can succeed later** — the failure is transient. The Invalid Message Channel assumes **every future attempt fails the same check** — the message itself is the problem. The engineering decision is which kind of failure you are looking at.

## Transient versus deterministic failure

Retry applies to failures whose outcome depends on the world: a downstream timeout, a connection blip, a lock contention spike. Those benefit from another attempt after a delay — frameworks give the policy real knobs; in Apache Camel's redelivery policy the `maximumRedeliveries` defaults to 0 and `redeliveryDelay` to 1000 ms, and only when all redelivery attempts have failed does the message move to the dead letter channel. A structurally invalid message has no such world-dependence: a missing required header, a wrong datatype, a schema mismatch — the validation is a pure function of the payload, so attempt number five fails exactly like attempt number one, as argued in [[Why should you not retry a structurally invalid message]]. That is the Invalid Message Channel case: park once, alert, fix the sender.

```text
Failure kind          Example                     Correct move
--------------------  --------------------------  ----------------------------
Transient             downstream timeout          retry with backoff + cap
Transient             connection blip             retry, then dead-letter
Deterministic         missing JMSReplyTo header   park on invalid channel now
Deterministic         payload fails schema        park on invalid channel now
```

**Listing 1.** Classify first, then choose: the table is the interview answer in one glance.

> [!warning] Retry-then-park is DLC machinery, not IMC
> Glossaries that put the Retry Pattern inside the Invalid Message Channel — "retry failed messages before they are designated invalid" — describe Dead Letter Channel behavior with its redelivery counters. An error handler like Camel's `deadLetterChannel` retries and then dead-letters; that is a different contract from a receiver that validates and parks on first detection, the distinction kept in [[What is the difference between Invalid Message Channel and Dead Letter Channel]].

In practice the two combine: a receiver retries a bounded number of times for plausibly transient errors and, once the failure is clearly deterministic, moves the message to the invalid channel instead of burning the cap.

> [!tip] Interview answer
> Retry is for transient failures — timeouts and blips that can succeed on a later attempt — with backoff and a cap. The Invalid Message Channel is for deterministic failures — structural or contract violations that fail identically on every redelivery — so retrying is waste and the message is parked once for diagnosis. If a framework retries before dead-lettering, that is dead-letter machinery, not invalid-message handling.
