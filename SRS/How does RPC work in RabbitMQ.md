<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How does RPC work in RabbitMQ

> [!abstract] Short answer
> The client publishes a request with `reply_to` and `correlation_id`, the server consumes, processes, and publishes the response back to `reply_to` carrying the same correlation id; the client matches answers to outstanding requests. Direct reply-to is the built-in optimisation that removes the reply queue entirely.

## The message contract

`reply_to` addresses where the answer goes — traditionally an exclusive, server-named callback queue the client created — and `correlation_id` tags the request so replies can be matched even out of order. The server is just a competing consumer on the request queue that publishes a response instead of acking-work-only. Timeouts and unresolved requests are the client's problem: the broker guarantees nothing about the server's answer, which is the classic distinction from [[What is the Request-Reply pattern]]'s EIP view.

```d2
direction: right
cli: "RPC client\ncorrelation_id = abc" {
  width: 210
  height: 90
  style.fill: "#e3f2fd"
}
req: "request queue\nreply_to, corr_id" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
srv: "RPC server\nprocesses" {
  width: 170
  height: 70
  style.fill: "#fff3e0"
}
rep: "reply queue (or direct)\nsame corr_id" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
cli -> req
req -> srv
srv -> rep
rep -> cli
```

**Fig. 1.** Request and response ride the correlation id; the reply address travels with the request.

## Direct reply-to

Declaring a queue per request is expensive, and one long-lived reply queue serialises answers; direct reply-to replaces both: the client consumes from the pseudo-queue `amq.rabbitmq.reply-to` (never declared, invisible in management), and publishes requests with `reply_to` set to it. The broker routes the response straight back through the server's channel without storing it. Constraints are strict: auto-ack consumption on the client, same connection and channel for consume and publish, at-most-once semantics for replies — a lost reply means the client retries after its timeout. Scale-oriented docs push it for tens of thousands of short-lived RPC clients; the ack mode it depends on is described in [[What is RabbitMQ consumer acknowledgement]], and the queue it avoids in [[What is an exclusive queue and an auto-delete queue in RabbitMQ]].

```java
props.replyTo = "amq.rabbitmq.reply-to";   // direct reply-to
props.correlationId = reqId;
// consume replies on the same channel with autoAck=true
```

**Listing 1.** The direct reply-to shape: no queue declaration, auto-ack consumer, one channel for both directions.

> [!warning] Direct reply-to is at-most-once
> Because no queue buffers replies, a disconnected or slow client simply loses them — the docs are explicit. Presenting it as the general RPC upgrade ignores its semantics; workloads needing at-least-once replies keep a real (exclusive or durable) reply queue, with the trade-offs in [[What delivery guarantees does RabbitMQ provide]].

> [!tip] Interview answer
> RPC rides two properties: reply_to addressing the answer and correlation_id matching it, with the server publishing into reply_to. Classic layout uses an exclusive callback queue; direct reply-to swaps it for the amq.rabbitmq.reply-to pseudo-queue — cheaper at scale, auto-ack, same channel, and at-most-once for replies.
