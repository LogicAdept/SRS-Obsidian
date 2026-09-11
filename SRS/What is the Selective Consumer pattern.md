<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Endpoints/SelectiveConsumer #SRS

# What is the Selective Consumer pattern?

> [!abstract] Short answer
> A **Selective Consumer** filters **at the point of consumption**: it declares a message selector, and the messaging system delivers only messages matching it — the rest stay queued for consumers whose selectors do match.

## Broker-side filtering before delivery

The consumer is created with a selector expression; the provider evaluates it and restricts delivery to matching messages. This is a documented client capability — Jakarta Messaging's `MessageConsumer` can be created with a message selector that restricts delivered messages to those matching the selector — typically an SQL-92-style condition over message headers and properties, not the body: `JMSPriority >= 5` or `eventType = 'order.cancelled'`. The decisive property: unmatched messages are **not dropped and not discarded** — they remain on the channel, available to consumers with other (or no) selectors. That makes the pattern consumer-side routing: several consumers on one queue, each picking the subset it handles. Costs scale badly if abused: selector evaluation happens per message per consumer inside the broker, unmatched messages accumulate until someone consumes them, and body-based criteria are impossible — only headers and properties are visible to the selector. Contrast: a router-side [[What is the Message Filter pattern]] drops before the channel, a [[What is the Content-Based Router pattern]] redirects by content before delivery.

```d2
direction: down
q: "Queue\n10 messages, mixed types" {
  width: 230
  height: 65
  style.fill: "#e3f2fd"
}
c1: "Consumer 1\nselector: type = refund" {
  width: 240
  height: 65
  style.fill: "#fff3e0"
}
c2: "Consumer 2\nselector: type = order" {
  width: 240
  height: 65
  style.fill: "#fff3e0"
}
r: "Refund messages only" {
  width: 210
  height: 55
  style.fill: "#e8f5e9"
}
o: "Order messages only" {
  width: 210
  height: 55
  style.fill: "#e8f5e9"
}
q -> c1 -> r
q -> c2 -> o```

**Fig. 1.** One queue, two selectors: each consumer sees only its slice, and nothing is discarded.

## Selector in use

```java
// Only high-priority refunds reach this consumer; the rest stays queued
Consumer refundConsumer = session.createConsumer(
        refundsQueue, "type = 'refund' AND priority >= 5");
```

**Listing 1.** The condition reads headers and properties only; if the criterion lives in the body, the selector cannot see it.

> [!warning] Selectors are a broker tax and a queue-hoarding risk
> Every delivery is evaluated against every selector, so many consumers with complex selectors measurably load the broker; and if no consumer's selector matches, messages pile up indefinitely — capacity planning must count the "nobody wants it" case. RabbitMQ has no JMS-style selectors: the equivalent is binding-key routing (topic exchanges) decided before the queue, not after.

> [!tip] Interview answer
> A Selective Consumer declares a selector — an expression over message headers and properties — and the messaging system delivers only matching messages; everything else stays queued for others. It is consumer-side subset selection, standard in JMS via message selectors. Watch the costs: per-message broker evaluation, messages nobody selects accumulating forever, and no access to body content.
