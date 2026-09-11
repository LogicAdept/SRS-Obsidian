<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Transformation/PipesAndFilters #SRS

# What is the Pipes and Filters pattern?

> [!abstract] Short answer
> **Pipes and Filters** splits a large processing task into a **sequence of small, independent steps** (filters) connected by **channels** (pipes). Each filter consumes from its input pipe, transforms the message, and publishes to its output pipe — so steps compose, reorder, and reuse without knowing about each other.

## Decomposition with a uniform interface

One event triggers many requirements: decrypt, verify the certificate, deduplicate, then process. Doing all of that in one component welds together unrelated concerns with different change cadences. The architectural style splits them: each filter has a simple contract — messages in, messages out — and each pipe is just a channel. Because every component exposes the same interface, they **compose**: insert a filter, remove one, rearrange the order, reuse a step in another flow — without changing the filters themselves; the connection point between filter and pipe is a port, and the basic form is one input port plus one output port per filter. This style is the substrate the routing patterns grow from — a [[What is the Message Router pattern]] is the point where a pipe gets several exits — and when a step's format does not match the next pipe, the fix is a [[What is the Message Translator pattern]] between them. The cost of the style lives in the data model: all steps must agree on message shape, which is why a [[What is the Canonical Data Model pattern]] or an explicit [[What is the Format Indicator pattern]] keeps the pipes viable.

```d2
direction: right
src: "Encrypted,\nduplicated order" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
f1: "Filter:\ndecrypt" {
  width: 150
  height: 60
  style.fill: "#fff3e0"
}
f2: "Filter:\nverify cert" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
f3: "Filter:\ndedup" {
  width: 150
  height: 60
  style.fill: "#fff3e0"
}
out: "Filter:\nprocess order" {
  width: 170
  height: 60
  style.fill: "#e8f5e9"
}
src -> f1 -> f2 -> f3 -> out```

**Fig. 1.** Each pipe carries one clear transformation; the sequence is the only place that knows the whole recipe.

## Composition is the payoff

```text
New requirement: "audit every order before processing"
Before: edit every producer        After: insert one filter between f3 and out
Removed TLS?  delete f2            Reorder?  rewire pipes, filters unchanged
Reuse dedup elsewhere?  same filter, different pipe
```

**Listing 1.** The style's value is operational: changes localize to wiring or to one small filter, never to a monolith.

> [!warning] The shared data model is the hidden single point of failure
> Filters that pass rich, mutable context between steps couple through the back door: change one field and three filters downstream break. Keep inter-filter messages canonical and minimal, document each pipe's contract, and resist the temptation to smuggle step-to-step state in headers — that is a distributed monolith wearing a pipeline costume.

> [!tip] Interview answer
> Pipes and Filters divides processing into small independent steps connected by channels: each filter consumes, transforms, and republishes, with a uniform one-in-one-out interface. Because the interface is uniform, steps compose, reorder, and reuse freely. The style underlies most EIP routing patterns; its real cost is the shared message contract, which needs canonical modeling to stay maintainable.
