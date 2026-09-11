<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How do you delay a message in RabbitMQ

> [!abstract] Short answer
> The community plugin `x-delayed-message` is no longer maintained, so the supported answer is TTL plus dead-lettering: publish to a wait queue whose message TTL expires and whose DLX forwards to the real queue. Per-message delays work, but TTL only fires at the queue head, so mixed delays can stall.

## TTL plus DLX: the supported pattern

Create a wait queue with `x-message-ttl` (or per-message `expiration`) and `x-dead-letter-exchange` pointing at the real routing exchange; no consumers on the wait queue. Expired messages dead-letter into the real queue after the delay. The head-of-line constraint matters: classic and quorum queues expire messages as they reach the head, so a queue mixing 10-second and 10-minute messages delays the short ones behind the long one — per-delay wait queues or one-delay-per-queue topologies avoid it.

```d2
direction: down
pub: "publish\nexpiration: 30000" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
wait: "wait queue\nx-message-ttl=30000\nno consumers" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
dlx: "DLX → real exchange" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
work: "real queue\nconsumer" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
pub -> wait
wait -> dlx: "expiry at head"
dlx -> work
```

**Fig. 1.** The delay queue holds without consumers; expiry is the timer, the DLX is the forwarding leg. This topology is also the backbone of [[How do you implement retries in RabbitMQ]] — retries are delays with a counter and a parking lot.

## The plugin's fate

The delayed-message exchange plugin accepted an `x-delay` header per message and routed after the delay; its README now states the project is unmaintained — its design rests on Mnesia, which RabbitMQ removed in the 4.3 cycle, and delayed messaging as a supported feature moved to the commercial Tanzu RabbitMQ. Answers that present the plugin as the standard tool are out of date; retries built on top of TTL+DLX remain fully supported, per [[How do you implement retries in RabbitMQ]].

```bash
rabbitmqctl set_policy wait "^orders.wait$"   '{"message-ttl":30000,"dead-letter-exchange":"orders.real"}'   --apply-to queues
```

**Listing 1.** One policy turns `orders.wait` into a 30-second delay leg toward the real exchange.

> [!warning] Dead-letter expiry needs a DLX or the message is dropped
> An expired message with no DLX simply disappears — the "delay" topology silently loses work. And because expiry happens at the head, one long-delay message parks every shorter one behind it; per-delay queues or an external scheduler are the honest fix.

> [!tip] Interview answer
> Supported path: a wait queue with TTL and no consumers, dead-lettering into the real queue — delay equals TTL, and per-delay queues dodge head-of-line blocking, the limit semantics of [[What is message TTL and queue max-length in RabbitMQ]]. The x-delayed-message plugin is unmaintained since the Mnesia removal, and native delayed queues exist only in the commercial Tanzu edition.
