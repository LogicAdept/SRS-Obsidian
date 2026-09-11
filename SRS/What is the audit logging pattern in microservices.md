<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Observability #SRS

# What is the audit logging pattern in microservices

> [!abstract] Short answer
> The audit logging pattern records every user action that changes business state — who did what to which object, when, from where — in a persistent, tamper-resistant log used for compliance, forensics and dispute resolution. Richardson separates it from application logging: the audit log answers "what did users do", not "what did the code do"; its consumers are auditors and investigators, not developers.

## The mechanics: what belongs in an audit record

One record per state-changing user action, with a fixed shape: actor identity (the authenticated principal, not a username string — [[How do you secure microservices with Spring Security]] covers where identity comes from), the action in business terms (OrderCancelled, UserPromoted — the same events the domain publishes, [[What is the difference between a command and an event]]), the affected object, timestamp from a trusted clock, origin (IP, channel, correlation id linking the request's trace, [[What is the distributed tracing pattern in microservices]]), and before/after or the change payload. The log is append-only: corrections are new records, never edits — which makes the event stream a natural audit source (an event-sourced aggregate is its own audit log, [[How would you explain the event sourcing pattern]]). Records go to a store with its own retention and access policy, separate from application logs' lifecycle, and access to the audit trail is itself audited.

```d2
direction: right
req: "User request
PAID actor, intent" {style.fill: "#eceff1"}
svc: "Service
changes state" {style.fill: "#e8f5e9"}
al: "Audit log
who / what / when / whence" {shape: cylinder; style.fill: "#fff3e0"}
applog: "App logs
debugging detail" {shape: cylinder; style.fill: "#eceff1"}
req -> svc
svc -> al: one record per change
svc -> applog: operational detail
```

**Fig. 1.** Two different logs out of one service: the audit trail records user-driven state changes; app logs record machine behavior.

## The disciplines that make it audit-grade

Completeness by construction: hook the emission at the domain-event or command-handler boundary — then every state change is audited even if a new developer forgot the requirement ([[What is a command handler in CQRS]] is exactly such a chokepoint). Immutability and retention: append-only storage, retention matched to the compliance regime (years, not weeks), integrity protection (hash chains or WORM storage where regulation demands). Separation of duties: the services write it; only auditors and security tooling read it; operators do not quietly edit it. Performance honesty: writing the audit record synchronously inside the state-changing transaction is the only way to guarantee it exists if the change exists — which couples audit availability to transaction latency, the trade async pipelines avoid but then must prove delivery for (at-least-once plus idempotent audit ingestion, [[What is idempotency in HTTP and in messaging]]).

> [!warning] An audit log you cannot trust is worse than none
> If operators can edit it, clocks are unsynchronized, or gaps appear whenever a service crashes mid-transaction, the log fails exactly when it is needed most — in a dispute. Synchronized clocks (NTP), atomic write-with-commit, and monitored gaps are the minimum; and PII in audit records is a legal exposure — record who acted and on what, not their personal data in bulk.

> [!tip] Interview answer
> Audit logging records every user-driven state change — actor, action, object, trusted timestamp, origin, before/after — into an append-only store separate from application logs, with its own retention, access control and integrity guarantees. I emit it at the domain boundary so completeness doesn't depend on developer memory, write it atomically with the change (or prove delivery asynchronously), and treat the trail itself as sensitive: editing it must be impossible, reading it must be audited.
