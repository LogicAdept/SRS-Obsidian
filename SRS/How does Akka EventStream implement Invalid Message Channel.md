<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# How does Akka EventStream implement Invalid Message Channel

> [!abstract] Short answer
> As an **in-process** quarantine: a processing actor that cannot handle a message publishes an `InvalidMessage` on the actor system's event stream, and a subscribed handler actor picks it up off the main processing path. The EventStream is Akka's built-in pub-sub event bus — a teaching-scale implementation of the pattern with no broker involved.

## Publish, subscribe, handle off-path

Akka documents the event stream as a facility of the actor system for publishing and subscribing to events, with actors registering interest through `Subscribe` (the typed API wraps this via message adapters; the classic API exposes `system.eventStream.subscribe(ref, Topic.class)`). The glossary implementation uses exactly those two primitives: the processing actor matches on its incoming domain message and, for any message type it cannot process, publishes `InvalidMessage(body)` on `context.system.eventStream` instead of throwing or dropping; an `InvalidMessageHandlerActor` subscribed to that topic receives the payload and handles it — log, inspect, alert — without touching the processing actor's state machine. The sequence mirrors the pattern's flow: receiver decides, quarantine holds, error-handler consumes ([[How does an error handler consume from the Invalid Message Channel]]), with the channel itself reduced to an in-JVM topic.

```text
ProcessingActor   --publish-->  system.eventStream  --Subscribe-->  InvalidMessageHandlerActor
 (main path)                    InvalidMessage(body)                (diagnosis, off-path)
```

**Listing 1.** The three participants: publisher on the main path, the event-stream topic as quarantine, and the subscribed handler.

> [!warning] No durability, no redelivery, no restarts
> An in-process bus vanishes with the JVM: there is no persistence, no acknowledgment, and no cross-node delivery, so this shape is for diagnostics and teaching, not for a quarantine that must survive an outage. If you need those properties, the quarantine belongs in a broker destination — the role-versus-mechanism split in [[What is the difference between an Invalid Message Channel and a broker queue or topic]] — and glossaries that list "Dead Letter Channel" as an alias of this pattern are repeating the conflation sorted out in [[What is the difference between Invalid Message Channel and Dead Letter Channel]].

> [!tip] Interview answer
> Akka's EventStream is an in-JVM pub-sub bus, and the pattern collapses to two primitives: the failing actor publishes an InvalidMessage event, a subscribed handler actor consumes it off the main path. It demonstrates the receiver-decides flow nicely — but it is in-process only, so it has no persistence or redelivery and is not a production quarantine across nodes.
