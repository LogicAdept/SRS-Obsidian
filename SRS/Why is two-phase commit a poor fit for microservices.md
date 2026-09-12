<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceCollaboration #Databases/Transactions #SRS

# Why is two-phase commit a poor fit for microservices

> [!abstract] Short answer
> Two-phase commit (2PC) synchronously locks every participant between prepare and commit/abort: the whole distributed transaction runs at the speed and availability of the slowest, flakiest service, locks span network hops and can outlive a crashed coordinator, and modern infrastructures (NoSQL stores, message brokers, REST services) simply do not implement the required participant protocol. Microservices therefore keep local ACID per service and settle cross-service workflows with sagas - trading atomicity for eventual consistency with compensations.

## What 2PC asks for, and why microservices cannot pay

Phase one: the coordinator asks every participant to prepare - apply changes to a staged state and vote yes or no. Phase two: if all voted yes, commit; if anyone voted no, abort everywhere. My verified micro-case reproduces the shape: flight-service votes yes and holds its locks, hotel-service vetoes, the coordinator broadcasts abort, both roll back (MS01 in empirics). The costs are structural, not incidental. Lock duration: a participant that votes yes must hold its locks until phase two arrives - across process boundaries, network round trips and other services' failures, so ordinary short transactions turn into long-distance lock windows that throttle throughput everywhere. Blocking: if the coordinator dies after phase one, participants that voted yes are stuck holding locks until recovery - classic blocking failure. Availability math: the whole operation is as available as its weakest participant, the same multiplication problem that motivates [[What is the self-contained service pattern]]. Participation barriers: each resource must implement the protocol; relational databases may (XA/JTA in the Java world), but [[How would you explain the database per service pattern]] deliberately puts data behind diverse technologies - MongoDB, Kafka, an external REST API - where 2PC simply has no hook to offer.

```d2
direction: right
co: "Coordinator" {style.fill: "#ffe0b2"}
a: "flight-service
voted YES, locks held" {style.fill: "#ffcdd2"}
b: "hotel-service
voted NO" {style.fill: "#ffcdd2"}
co -> a: prepare
co -> b: prepare
a -> co: YES
b -> co: NO
co -> a: ABORT
co -> b: ABORT
```

**Fig. 1.** Between the YES vote and the final decision, flight-service's locks are held hostage by the coordinator's fate - the window 2PC forces on every participant.
```java
boolean allYes = participants.stream().allMatch(Participant::prepare);
String decision = allYes ? "COMMIT" : "ABORT";
for (Participant p : participants)
    if (allYes) p.commit(); else p.rollback();
```

**Listing 1.** Verified on JDK 21 (MS01_TwoPhaseAbort in empirics): `hotel-service prepare -> NO (vote veto, releasing locks)` forces `Coordinator decision: ABORT` and both participants roll back; the all-yes scenario reaches `PHASE 2: commit` — with every YES voter holding locks across the whole window.


## What replaces it

The saga: a sequence of local transactions, each ACID inside one service, each publishing the step's outcome; when a step fails, previously executed steps are undone by compensating transactions ([[What is a saga and how would you explain one with a real-world example]] carries the full mechanics and the flight-hotel analogy; coordination styles are compared in [[How would you orchestrate communication between multiple services]]). The consistency posture changes from atomic to eventually consistent - intermediate states like order PENDING are visible and must be designed for, not hidden ([[What is eventual consistency]] frames the guarantee and its window). Reliability of the step-to-step messages is not optional plumbing: the transactional outbox is what makes "update my data and announce it" atomic without 2PC. So the honest summary: microservices do not abandon transactional integrity - they relocate it, from one global lock-protected transaction to locally ACID transactions plus designed, auditable compensation flows.

> [!warning] Sagas are not free 2PC
> Replacing 2PC with a saga is a semantic decision, not a drop-in: compensations are business logic someone must write and test (a charge is un-charged, not rolled back), intermediate states leak to consumers, and at-least-once event delivery forces idempotent consumers. Teams that discover this mid-project tend to sneak shared databases back in - which re-couples the services 2PC was supposed to span. Also do not confuse XA-style 2PC inside one service's database cluster with cross-service 2PC: the former can be fine, the latter is the one that does not fit.

> [!tip] Interview answer
> 2PC needs every participant to hold locks across a synchronous prepare-then-commit protocol, so throughput collapses, a crashed coordinator blocks prepared participants, and anything without an XA endpoint - NoSQL, brokers, REST APIs - cannot play. Microservices keep per-service ACID and use sagas with compensations instead, accepting eventual consistency and visible intermediate states. I pair that with the outbox for reliable step events and idempotent consumers for safe retries.
