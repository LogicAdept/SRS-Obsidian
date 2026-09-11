<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Channels/PublishSubscribe #SRS

# What is the Publish-Subscribe Channel pattern?

> [!abstract] Short answer
> A **Publish-Subscribe Channel** delivers **a copy of each message to every subscriber**: one input fan-outs to one output per subscriber, and each subscriber consumes its own copy exactly once. Use it when an event must reach all interested parties, not just one worker.

## One input, one output channel per subscriber

The channel splits its single input into multiple output channels, one per subscriber. When a message is published, the channel delivers a copy to each output; each output has exactly one subscriber, which consumes the copy once. This is the opposite trade-off of a point-to-point channel: no load balancing, but every subscriber is guaranteed its own copy. In JMS this is a `Topic` with `TopicSubscriber`s; in RabbitMQ it is a fanout (or topic) exchange with **one queue per subscriber** bound to it; in Kafka it is a consumer group per subscriber all reading the same topic. The same mechanism doubles as a debugging tool — an extra subscriber can eavesdrop on traffic without disturbing the flow, which is the passive cousin of the [[What is the Wire Tap pattern]] and feeds [[What is the Message Store pattern]]-style archives.

```d2
direction: right
pub: "Publisher\n(PriceChanged)" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
ps: "Publish-Subscribe Channel" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
s1: "Subscriber A\nown copy" {
  width: 170
  height: 65
  style.fill: "#e8f5e9"
}
s2: "Subscriber B\nown copy" {
  width: 170
  height: 65
  style.fill: "#e8f5e9"
}
s3: "Subscriber C\nown copy" {
  width: 170
  height: 65
  style.fill: "#e8f5e9"
}
pub -> ps
ps -> s1
ps -> s2
ps -> s3```

**Fig. 1.** Each subscriber receives its own copy; a slow subscriber never steals another's message.

## RabbitMQ mechanics

```text
exchange: prices.fanout  (type=fanout)
  queue: billing.prices   bound to prices.fanout  -> billing service
  queue: audit.prices     bound to prices.fanout  -> audit service
Publishing once to prices.fanout enqueues one copy in each bound queue.
```

**Listing 1.** One queue per subscriber is what makes it pub/sub: sharing a single queue between two services would instead create competing consumers on one queue.

> [!warning] One queue per subscriber, not one consumer per queue
> Several consumers on the **same** queue split messages between themselves — that is the [[What is the Competing Consumers pattern]], not publish-subscribe. Mixing the two up in an interview or in code review means some services silently stop receiving copies of events they depend on.

> [!tip] Interview answer
> A Publish-Subscribe Channel broadcasts each message as a copy to every subscriber: one input channel fans out into one output per subscriber, each consumed once. In RabbitMQ that means a fanout exchange plus one queue per subscriber; in Kafka, one consumer group per subscriber on the same topic. It maximizes fan-out, not throughput per worker.
