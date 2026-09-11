<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Message Router pattern?

> [!abstract] Short answer
> A **Message Router** consumes a message from one channel and **republishes it unchanged to a different channel** chosen by a set of conditions. It connects to multiple output channels, moves decision-making out of the components, and never modifies the message.

## Decision logic in one place, pipes stay dumb

The router is the first routing pattern because it changes the pipes-and-filters deal: instead of hard-wiring filter outputs, a filter publishes to a channel and a router decides what is next. Surrounding components stay unaware the router even exists — composition changes without touching them. The two hard properties: the router **does not modify message contents** (that would make it a transformer), and the **decision criteria live in a single location** — when rules change, only the router changes, not every producer or consumer. Centralization has a flip side: all messages pass through one component, so it is a natural maintenance hotspot and an ordering point, which is why specific routers (content-based, filter, dynamic) exist for the common condition types. Where the condition must reflect the payload, the router specializes into a [[What is the Content-Based Router pattern]]; where uninteresting messages must vanish, into the [[What is the Message Filter pattern]].

```d2
direction: down
in: "Input channel" {
  width: 190
  height: 55
  style.fill: "#e3f2fd"
}
r: "Message Router\nconditions, no edits" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
o1: "Channel A" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
o2: "Channel B" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
o3: "Channel C" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
in -> r
r -> o1
r -> o2
r -> o3```

**Fig. 1.** One input, many outputs, zero modification: the router is a valve, not a processor.

## Router versus transformer in code

```java
Message m = input.receive();
String out;                       // routing decides ONLY the destination
if (m.property("country").equals("DE")) {
    out = "orders.de";
} else {
    out = "orders.intl";
}
producer.send(session.createQueue(out), m);  // same message object
```

**Listing 1.** If this code needed to alter the payload to make it fit the destination, that logic belongs in a downstream [[What is the Message Translator pattern]], not in the router.

> [!warning] Routers quietly rot into rule engines
> Every new message type tempts another branch into the router; it becomes the single place everyone edits, with untestable nested conditions and no clear owner. Contain it: keep router conditions declarative and coarse, push data-dependent complexity into configurable rules or dedicated routers, and never hide transformation side effects in a "router".

> [!tip] Interview answer
> A Message Router consumes from one channel and republishes the untouched message to one of several output channels based on conditions. Its value is centralized decision-making — routing rules change in one place while producers and consumers stay oblivious — and its invariant is that it never modifies content. Content-based routing, filtering, and dynamic routing are specializations of this basic valve.
