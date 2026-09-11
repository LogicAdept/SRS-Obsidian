<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ alternate exchange

> [!abstract] Short answer
> An alternate exchange (AE) is an exchange-level fallback: when an exchange cannot route a message — no bindings match — the channel republishes the message to the configured AE instead of dropping it. It catches unroutable publishes during topology changes or mistakes.

## How it works

The AE is configured per exchange, either through an `alternate-exchange` policy or the exchange's x-arguments at declaration (arguments win over policies when both set it). If the target exchange has no matching binding, the message flows to the AE as if published there; the AE itself can have an AE, forming a chain until routing succeeds or the chain ends. For `mandatory` accounting, a message routed via an AE still counts as routed — no `basic.return` happens. The default exchange cannot have an AE because it is special-cased in code.

```d2
direction: down
pub: "publish\nkey 'orders.eu'" {
  width: 210
  height: 90
  style.fill: "#e3f2fd"
}
ex: "direct exchange\nno matching binding" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
ae: "alternate exchange\n(fanout)" {
  width: 230
  height: 80
  style.fill: "#ffebee"
}
q: "unroutable queue" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
ex -> ae: "cannot route → AE"
ae -> q
```

**Fig. 1.** An unroutable publish is diverted to the AE and lands in a parked queue instead of vanishing.

## AE versus DLX

An AE acts on the publishing side, before any queue sees the message; a dead letter exchange acts on the queue side, after reject, TTL, overflow, or delivery-limit — see [[What is a RabbitMQ dead letter exchange]] for the consumer-side counterpart. Typical AE uses: parking unroutable messages for inspection, "or-else" routing where unmatched keys fall to a generic handler, and migration safety nets while bindings move — the flow siblings are [[What does the RabbitMQ mandatory flag do]] (return to publisher) and drop (default).

```bash
rabbitmqctl set_policy AE "^orders$"   '{"alternate-exchange":"orders.unroutable"}' --apply-to exchanges
```

**Listing 1.** Policy-based AE declaration; policies are recommended over hardcoded x-arguments because they can change without redeploying publishers.

> [!warning] AE routing counts as routed
> Because a message that reached an AE counts as routed, publishers with confirms see a confirm and no return — the only trace is the message appearing in the AE topology. Teams that audit unroutable messages with `mandatory` alone will miss AE-routed ones; monitor the parked queue itself.

> [!tip] Interview answer
> An alternate exchange is the exchange's fallback for unroutable messages: no matching binding means the channel republishes to the AE, following its own type and possibly chaining further AEs. It is publish-side, unlike the DLX which fires queue-side, and it counts as routed so mandatory returns do not fire.
