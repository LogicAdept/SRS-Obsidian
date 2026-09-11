<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging/Tools/Kafka #SRS

# How does schema evolution send a queued event to an Invalid Message Channel

> [!abstract] Short answer
> Producer and consumer schema versions diverge; the event is queued and **delivered** normally, but the consumer's deserialization or validation against its expected schema fails. The consumer parks the event on the invalid channel for investigation instead of crashing or dropping it — the message did arrive; the contract around it moved.

## A delivered event that no longer fits the consumer's schema

Schema evolution is one of the most common real-world sources of delivered-but-unprocessable traffic. The event was produced against version N of the schema; by the time it is consumed, the consumer expects version N+1 — a field was removed it still requires, a type was widened it cannot read, or the payload carries unknown fields its mapping rejects. The broker did nothing wrong: the message is in the queue and delivered, which is exactly why the fix belongs to the receiver-side pattern and not to broker dead-lettering ([[What is the difference between Invalid Message Channel and Dead Letter Channel]]). The dump that popularized this example routes such events to a dedicated dead-letter destination for investigation — the Invalid Message Channel role with an unhelpfully DLC-flavored name — instead of crashing the consumer or losing the event.

Registry tooling narrows the window but does not close it. Confluent's Schema Registry checks compatibility at registration and defaults to `BACKWARD` — new schema versions must be readable by code written against the previous one — with `FORWARD`, `FULL`, and transitive variants for stricter guarantees. Even under a registry, a consumer can still meet an event it cannot process: an unregistered subject, a version gap, corrupt bytes, or a consumer whose own mapping lags behind a compatibly-evolved schema. Those failures are the receiver's to classify — the general catalog is in [[What kinds of delivered messages does a receiver treat as invalid]] — and in event-streaming systems the parked message is the evidence that a deployment lagged, the sibling discipline of [[How do you handle a poison pill message in Kafka]].

```text
v1 producer  -> topic  -> v2 consumer (expects added field)
                          deserialize OK, validate against v2 schema FAILS
                          -> park on invalid channel: event, schema id, reason
```

**Listing 1.** The failure is a contract mismatch discovered after delivery, so the artifact you preserve includes the schema identity, not just the bytes.

> [!warning] Registration-time checks cannot save a running consumer
> Compatibility modes gate what enters the registry; they do not roll back a consumer that was built against an older schema, nor heal a payload produced before a breaking change was caught. Teams that treat "registry enforces BACKWARD" as immunity end up without any quarantine when the edge cases arrive — and replaying a schema-orphaned event without fixing versions is the pointless redelivery of [[Why should you not retry a structurally invalid message]].

> [!tip] Interview answer
> When producer and consumer schemas diverge, the event still delivers — and the consumer's deserialization or validation fails, which makes it an invalid message, not an undeliverable one. The consumer parks it with the schema id and reason for investigation; a schema registry with compatibility modes like BACKWARD shrinks the risk but leaves the quarantine as the last line of defense.
