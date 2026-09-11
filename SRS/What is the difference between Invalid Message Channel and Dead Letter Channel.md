<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #Messaging #SRS

# What is the difference between Invalid Message Channel and Dead Letter Channel

> [!abstract] Short answer
> An **Invalid Message Channel** receives messages that **were delivered** but the receiver cannot process — the receiver decides and moves them. A **Dead Letter Channel** receives messages the **messaging system could not deliver** — the broker decides and moves them. The split is who detected the failure and who owns the machinery.

## Two owners, two code paths

The dead-message side is broker plumbing: the messaging system evaluates its own delivery conditions — no route or destination, per-message TTL expiry, queue length limits, a delivery counter exhausted — and parks the message without any application involvement. On IBM MQ, messages reach the dead-letter queue from queue managers, message channel agents, and applications, and every one of them must carry the dead-letter header `MQDLH` whose reason field says why the message is there; RabbitMQ dead-letters a queue's messages on `basic.reject`/`basic.nack` with `requeue=false`, per-message TTL expiry, max-length overflow, and quorum-queue delivery-limit exhaustion. The invalid-message side is application code: the receiver parsed enough of the message to try, failed its own type/schema/header checks, and moves the intact payload itself — the receiver-relative validity behind that decision is [[How does validity of a message depend on the receiver]].

Because one side is product machinery and the other is your code, the design consequences differ: the developer is largely stuck with whatever Dead Letter Channel the product ships, while invalid-message handling — how many channels, what the consumer does, how triage is organized — is designed by the application team, as in [[What is the Invalid Message Channel pattern]].

```d2
direction: down
msg: "Message in flight" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
dl: "Messaging system cannot deliver\nTTL · no route · max length · delivery count" {
  width: 360
  height: 90
  style.fill: "#fff3e0"
}
dlq: "Dead Letter Channel\nbroker machinery, MQDLH-style reason" {
  width: 340
  height: 85
  style.fill: "#ffebee"
}
del: "Delivered to receiver" {
  width: 260
  height: 65
  style.fill: "#e8f5e9"
}
inv: "Receiver cannot process\ntype · schema · required headers" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
imc: "Invalid Message Channel\nreceiver moves the intact message" {
  width: 340
  height: 85
  style.fill: "#ffebee"
}
msg -> dl: "before delivery"
dl -> dlq
msg -> del: "delivery succeeds"
del -> imc: "receiver's own checks fail"
```

**Fig. 1.** The decision point is delivery: the same physical queue can even host both roles, but the contracts never merge.

> [!warning] The famous conflation
> Glossaries and dumps list "malformed payloads, poison messages, expired messages, unroutable messages" under one destination "also known as a DLQ". Only the first row is invalid-message traffic; expiry, unroutable, and overflow are dead-letter causes. Conflating them hides who must fix the problem — a sender bug or an operator — and queue names like `invalid-messages` on a broker DLX change nothing about it, as [[How does RabbitMQ dead-letter-exchange get used as an Invalid Message Channel]] shows.

> [!tip] Interview answer
> Dead Letter Channel is what the messaging system does with a message it could not deliver — TTL, no route, length limit, exhausted redelivery — using its own machinery and reason headers. Invalid Message Channel is what a receiver does with a message it did deliver but cannot process — wrong type, bad schema, missing headers — moving it by application code. One is broker-defined, the other receiver-designed; that is the whole difference.
