<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Correlation Identifier pattern?

> [!abstract] Short answer
> A **Correlation Identifier** is a unique value carried in the request and echoed in the reply that tells the requestor **which request this reply answers**. On a shared reply channel with many outstanding requests, it is the only dependable way to demultiplex.

## Six moving parts, one copied field

In the full request-reply setup — requestor, request channel, replier, reply channel, and the return address fields — the correlation id is the thread of continuity: the replier takes the request's id (typically `JMSMessageID`) and stores it as the correlation id in the reply; the requestor waits for replies whose correlation id matches one of its outstanding requests and dispatches to the right callback. Without it, a requestor with several in-flight requests on one reply queue cannot tell replies apart, and with [[What is the Aggregator pattern]]-style conversations the same idea groups partial results per original request; the gateway layer that usually hosts this demux is [[What is the Messaging Gateway pattern]]. The id is header data — set `JMSCorrelationID`, `correlation_id` in AMQP, or a custom header — never body content.

```d2
direction: down
rq1: "Request A id=111" {
  width: 190
  height: 55
  style.fill: "#e3f2fd"
}
rq2: "Request B id=222" {
  width: 190
  height: 55
  style.fill: "#e3f2fd"
}
rq: "Reply channel\n(shared)" {
  width: 210
  height: 60
  style.fill: "#fff3e0"
}
rp: "Requestor demux\ncorrId 111 -> callback A" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
rq1 -> rq
rq2 -> rq
rq -> rp: "reply corrId=111"```

**Fig. 1.** Many outstanding requests share one reply channel; the correlation id routes each reply to its waiting callback.

## Echo, do not invent

```java
// Replier: echo the id, never generate a new one for the reply
reply.setJMSCorrelationID(request.getJMSMessageID());
// Requestor: match replies to outstanding requests
Message r = consumer.receive(timeout);
Callback cb = pending.remove(r.getJMSCorrelationID());
if (cb == null) { /* late or foreign reply: log and drop */ }
```

**Listing 1.** If the replier fabricates its own id, the requestor's pending table can never be reconciled; unmatched replies are dropped loudly, not queued silently.

> [!warning] Correlation ids do not fix lost or duplicate replies
> The id tells you which request a reply belongs to — nothing about whether it is the **first** or a **duplicate** reply, or whether one will ever come. Timeouts plus idempotent handling of late duplicates are still required; on redelivery-heavy systems the same correlation id can legitimately arrive twice.

> [!tip] Interview answer
> A Correlation Identifier is a unique id stamped on the request and copied into the reply so the requestor can match replies to their requests — essential when many requests share one reply channel or the client is asynchronous. The replier must echo the request's id rather than mint a new one, and timeouts still handle the case where no matching reply ever arrives.
