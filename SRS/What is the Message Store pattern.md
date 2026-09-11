<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages #SRS

# What is the Message Store pattern?

> [!abstract] Short answer
> A **Message Store** captures information about each message **in a central location** — typically a copy fed by a Wire Tap onto a special channel — so you can report, audit, and debug message flows without disturbing the transient, loosely coupled main path.

## A durable shadow of a transient stream

The main path is asynchronous and deliberately forgetful; answering "what did we actually send?" needs a record. The store receives message information via a dedicated channel — components can send the copy themselves, or a [[What is the Wire Tap pattern]] inserted in the channel duplicates the flow — and persists it for later analysis. Two properties keep it healthy. The copy is sent **fire-and-forget**, so the store never slows the main flow — though it does add network traffic, which is exactly why many deployments store **selected fields** (message id, channel, timestamp, status) instead of whole bodies. The store's channel is effectively part of the [[What is the Control Bus pattern]]: it is management infrastructure, not a business consumer. What you get at the end: a queryable timeline for reporting ("how many orders per hour?"), correlation ("where did this conversation go?"), and forensics — the persistent twin of the in-message trail kept by [[What is the Message History pattern]], and the natural home for payloads parked by a [[What is the Claim Check pattern]].

```d2
direction: right
flow: "Main flow\nmessage in transit" {
  width: 200
  height: 65
  style.fill: "#e3f2fd"
}
wt: "Wire Tap\ncopy, fire-and-forget" {
  width: 210
  height: 65
  style.fill: "#fff3e0"
}
st: "Message Store\nids, fields, bodies?" {
  width: 200
  height: 65
  style.fill: "#fff3e0"
}
an: "Reporting / forensics" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
flow -> wt -> st -> an```

**Fig. 1.** The store sits beside the flow, fed asynchronously; the business path neither waits for it nor knows its queries.

## What to store, and what it costs

```text
Stored content        Value                    Cost
--------------------  -----------------------  ---------------------------
id + channel + time   correlation, counts      minimal traffic
+ headers             routing forensics        moderate; mind PII
+ full body           replay, deep debug       heavy; retention explodes
```

**Listing 1.** Decide per use case: the traffic and retention bill grows with every field you keep.

> [!warning] The store becomes a production database with a compliance burden
> It accumulates every message you send — including sensitive fields nobody audited — at production rates, with retention obligations from the moment of capture. Size it like a real system (write throughput, retention, indexes), inventory what it stores for privacy, and give replayed data a version story: a three-month-old body may not parse with current schemas.

> [!tip] Interview answer
> A Message Store persists message information centrally — usually copies fed by a wire tap over a fire-and-forget channel — so reporting, auditing, and debugging never disturb the main flow. You choose the depth: ids and timestamps for correlation, full bodies for replay, each step multiplying storage and PII obligations. It is management infrastructure with the SLAs of a production database.
