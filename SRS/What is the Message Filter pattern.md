<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages #SRS

# What is the Message Filter pattern?

> [!abstract] Short answer
> A **Message Filter** is a router with **a single output channel** that **discards** messages not matching its criteria. It is how a component in the middle of a flow stops uninteresting messages from going further — the message is dropped, not transformed and not bounced.

## Drop the unwanted, forward the rest

The customer-news flow publishes every price change; a customer only trades gadgets and does not care that widgets are discounted. A filter inserted between the broadcast and that customer's processing eliminates non-matching messages: if content matches, route to the output channel; if not, discard. The discard is the defining behavior — no dead-letter, no reply, no modification — which is why the filter is formally "a special kind of Message Router". Choosing **where** to filter is the design decision: filtering early saves downstream work but cannot adapt per consumer, while per-consumer filters multiply; brokers offer declarative variants (RabbitMQ binding keys, JMS selectors at the consumer — the [[What is the Selective Consumer pattern]]), and when the goal is to strip data **inside** a message rather than drop whole messages, that is a different pattern entirely: [[What is the Content Filter pattern]]. Distinction from the generic router: [[What is the Message Router pattern]] has many outputs; the filter has one.

```d2
direction: right
in: "Price updates\n(all items)" {
  width: 200
  height: 65
  style.fill: "#e3f2fd"
}
f: "Message Filter\nitem == gadgets" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
out: "Output channel\nmatching only" {
  width: 210
  height: 65
  style.fill: "#e8f5e9"
}
x: "Non-matching\ndiscarded" {
  width: 160
  height: 60
  style.fill: "#ffebee"
}
in -> f
f -> out: "match"
f -> x: "no match: drop"```

**Fig. 1.** One output, and the discard path ends at nothing: filtered messages simply cease to flow.

## Filter semantics against its neighbors

```text
Pattern           Input messages        Effect on non-matching
----------------  --------------------  ------------------------------
Message Filter    whole messages        dropped entirely
Selective Consumer consumer-side view   left queued for other consumers
Content Filter    one message's fields  message forwarded, fields removed
```

**Listing 1.** The three "filter" meanings diverge on one axis: what happens to the rejected part. Only the Message Filter makes whole messages disappear.

> [!warning] Silent drops need observability
> A filter is the only component in the flow whose normal job is to make messages vanish, so "my consumer got nothing" is indistinguishable from "filter ate everything" without counters. Log or expose discard metrics per rule — otherwise the first debug session turns into archaeology across every filter in the path.

> [!tip] Interview answer
> A Message Filter is a single-output router that discards non-matching messages so downstream components never see them. It differs from a broker selector, which leaves messages queued for others, and from a Content Filter, which strips fields inside a message but forwards it. Because its job is silent deletion, wire discard metrics into monitoring from day one.
