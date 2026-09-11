<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging/Splitter #SRS

# What is the Splitter pattern?

> [!abstract] Short answer
> A **Splitter** breaks one composite message into **a series of individual messages**, each carrying one item — one order becomes one message per line item — so the items can be processed individually, possibly in parallel or on different channels.

## One composite in, a sequence out

The composite arrives with repeated elements — order line items, a batch of rows, a multi-part document. The splitter produces a message per element, each element processed by whatever consumes the output channel; the pieces may go in sequence, in parallel, or to different lanes. Two design points matter more than the split itself. First, **completeness bookkeeping**: consumers of the pieces usually need to know the whole exists — stamp each piece with sequence id, position, and total size (the [[What is the Message Sequence pattern]] fields) so a downstream [[What is the Aggregator pattern]] can decide when the set is complete. Second, **failure semantics**: if one item fails, what happens to the others — Camel's split EIP, for example, continues processing remaining splits by default and has explicit stop-on-exception and sharing-options modes, plus a choice of whether the aggregate result is returned or the original input message. The splitter is the structural inverse of the [[What is the Aggregator pattern]]; per-item payloads are the same shape the [[What is the Message Sequence pattern]] transports.

```d2
direction: down
ord: "Order O-9\n3 line items" {
  width: 190
  height: 65
  style.fill: "#e3f2fd"
}
sp: "Splitter\none message per item" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
i1: "Item 1\nseq=O-9 pos=1 of 3" {
  width: 230
  height: 60
  style.fill: "#e8f5e9"
}
i2: "Item 2" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
i3: "Item 3" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
ord -> sp
sp -> i1
sp -> i2
sp -> i3```

**Fig. 1.** The split stamps enough context on each piece that the pieces can be reassembled later.

## Split with a completion trail

```java
from("orders.incoming")
    .split(simple("${body.items}"), new OrderAggregationStrategy())
        .setHeader("seq-pos", simple("${exchangeProperty.CamelSplitIndex}"))
        .setHeader("seq-size", simple("${exchangeProperty.CamelSplitSize}"))
        .to("inventory.reserve")
    .end(); // result per Camel default: original input message
```

**Listing 1.** Camel's split EIP: the expression picks the elements, headers carry position and size, and the aggregation strategy decides what the route returns.

> [!warning] Splitting multiplies failure modes
> If item 7 of 100 fails, the route must say whether items 8-100 proceed, whether the order is failed as a whole, and who records the partial state — plus, under at-least-once delivery, consumers must tolerate a duplicate item message. Splitters that answer none of this leave half-processed composites that no one owns.

> [!tip] Interview answer
> A Splitter takes one composite message and emits one message per element — per line item, per row, per record — so elements process individually or in parallel. The production details are the interesting part: stamp position and total for later aggregation, decide continue-versus-stop on item failure, and remember the pieces arrive at-least-once. It is the structural inverse of the Aggregator.
