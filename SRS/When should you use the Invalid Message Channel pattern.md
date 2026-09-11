<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# When should you use the Invalid Message Channel pattern

> [!abstract] Short answer
> Use it whenever messages can arrive **delivered but unprocessable** and you need them inspected without disturbing the happy path — especially when many senders share one channel, or when parked traffic must be auditable. Skip it for application errors and for trivial systems where a separate channel costs more than it protects.

## The cases that justify the extra channel

The pattern pays for itself when the happy path must not be disrupted: receivers move contract-breaking traffic off the working channel and keep processing, while a dedicated error handler inspects the quarantine. The strongest case is a channel shared by **many senders**: the moment a new sender is added — one that omits a required header or sends the wrong type — its messages show up on the invalid channel immediately, turning silent contract drift into a visible alert. Integration suites lean on this for onboarding: an exception path parks the failing message on a queue such as `InvalidMessages`, and validators enrich the diagnosis — the mechanics are in [[How do you use XML or EDI validators with an Invalid Message Channel]]. Audit-driven domains (financial isolation, order review, IoT anomaly inspection) get a second benefit: parked messages are intact and reviewable, which is what makes [[How do you replay messages from an Invalid Message Channel]] possible after the fix.

The payoff grows with sender count, which is why the "ideal would be development-only" reading of some tooling notes is backwards: a development environment has one sender and one test payload, while a production channel with dozens of producers is where quarantine earns its keep — with the monitoring discipline from [[How does an error handler consume from the Invalid Message Channel]].

> [!warning] Invalid channel is not an application-error bin
> The pattern covers messages the receiver **cannot process** — the boundary against business failures (record missing, account overdrawn) is drawn in [[Why should you not treat an application error as an invalid message]]. Mixing them turns the quarantine into a generic error bucket and destroys its diagnostic meaning.

What it costs to maintain one — and when the trade-off fails — is the subject of [[When should you not use a separate Invalid Message Channel]]; the underlying pattern statement is [[What is the Invalid Message Channel pattern]].

> [!tip] Interview answer
> Use it when delivered-but-unprocessable traffic must be visible and the happy path must keep flowing — particularly with many senders on one channel, where a new or buggy sender appears on the invalid channel instantly, and in audit-heavy domains. Do not use it for domain errors on valid messages, and not for toy systems where the extra channel, storage, and workflow outweigh the benefit.
