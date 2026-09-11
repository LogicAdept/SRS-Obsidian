<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/WireTap #SRS

# What is the Wire Tap pattern?

> [!abstract] Short answer
> A **Wire Tap** is a fixed two-output recipient list inside a channel: it publishes the **unmodified message** both to the main channel and to a secondary one, so monitoring, auditing, or analysis tools can observe traffic **without touching the primary flow**.

## Observe everything, change nothing

Point-to-point channels ensure exactly one consumer per message — which is great for delivery and terrible for observers: nothing is left to inspect. The wire tap sits in the path and duplicates every message: main output continues the business flow, secondary output feeds whoever watches — a logger, an archiver, a live debugging console. It is formally a Recipient List with exactly two outputs, and its defining discipline: the tap publishes **unmodified** messages, and the analysis logic lives in a **separate component**, so inserting or removing the tap cannot alter primary behavior — reuse improves and instrumentation risk drops. The secondary channel is where the rest of the management tooling connects: a [[What is the Message Store pattern]] fed by a tap is the standard archive build, and when observation must become intervention, the in-path upgrade is the [[What is the Detour pattern]].

```d2
direction: right
in: "Input" {
  width: 130
  height: 50
  style.fill: "#e3f2fd"
}
wt: "Wire Tap\ncopy, unmodified" {
  width: 190
  height: 65
  style.fill: "#fff3e0"
}
main: "Main channel\nbusiness flow" {
  width: 190
  height: 65
  style.fill: "#e8f5e9"
}
sec: "Secondary channel\nmonitor / audit" {
  width: 200
  height: 65
  style.fill: "#fff3e0"
}
in -> wt
wt -> main
wt -> sec```

**Fig. 1.** One message in, two identical messages out; only the secondary side is optional to consume.

## Non-invasiveness is the contract

```java
from("orders.in")
    .wireTap("orders.audit")     // fire-and-forget copy
        .onPrepare(tapHeader("tappedAt", now()))
    .to("orders.process");       // main flow unchanged and unblocked
```

**Listing 1.** Camel's wireTap: the copy goes to a secondary endpoint, typically asynchronously; the main route proceeds with the same message.

> [!warning] A tap leaks data and can still hurt the flow
> Full-message copies — including PII and credentials — now land on the secondary channel with its own retention, access, and encryption story; an unguarded tap is a compliance incident. And if the tap implementation copies synchronously or the observer consumes slowly, the "passive" tap becomes backpressure in the main path — keep the tap fire-and-forget and bounded.

> [!tip] Interview answer
> A Wire Tap duplicates every message in a channel — unmodified — onto a secondary channel for monitoring, auditing, or debugging, while the primary flow continues untouched. It is a two-output recipient list whose whole contract is non-invasiveness: fire-and-forget copies, analysis in a separate component. Watch PII on the tap channel and keep the copy path asynchronous so observation never becomes backpressure.
