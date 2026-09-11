<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# Why would senders monitor the Invalid Message Channel

> [!abstract] Short answer
> Because it is their only feedback when a receiver discards their traffic. The book's example: an executing application invalidates trade requests of the wrong type, trades missing the security or share count, or trades missing the confirmation destination — and the applications sending those requests monitor the invalid channel to determine whether their requests are being discarded.

## The sender-side view of the same contract

The pattern's validity rule — it is the sender's job to publish messages every receiver of the channel will accept — implies that a contract violation surfaces as a parked message, not as an error returned to the sender. On a one-way channel the sender otherwise hears nothing: the receiver "ignores" it by rerouting to the Invalid Message Channel, per [[How does validity of a message depend on the receiver]]. The stock-trading example makes that concrete: a price quote sent on the trade channel (wrong type for the contract), a trade that does not specify the security or the share count (missing required content), and a trade that does not say where to send the confirmation (a missing Return Address, [[What is the Return Address pattern]]) all land on the invalid queue — so senders watch it to discover whether their requests are being discarded, which turns the quarantine into a shared contract-feedback loop alongside the operator-facing alerting of [[How does an error handler consume from the Invalid Message Channel]].

```text
Sender mistake                          What the executing app does
--------------------------------------  -------------------------------
price quote on the trade channel        invalid: wrong type
trade without security / share count    invalid: required values missing
trade without confirmation destination  invalid: return address missing
-> all three resends to Invalid Message Channel; senders monitor it
```

**Listing 1.** The book's trading examples: every invalidated request is visible to the sender that sent it — if that sender watches the quarantine.

> [!warning] Monitoring is not a business reply
> A parked request was **never processed** — the invalid channel says "discarded", not "rejected for business reasons", and it is not a NAK protocol. Business rejections flow back through Request-Reply ([[What is the Request-Reply pattern]]); sender-side monitoring merely shortens the time until someone notices the contract broke.

> [!tip] Interview answer
> Receivers ignore contract-breaking senders by moving their messages to the invalid channel, so the channel is where a sender learns its traffic is being discarded — the book's trading senders watch it for exactly that. It complements operator alerting, and it is not a business rejection: parked means never processed, and real replies travel the reply channel.
