<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Request-Reply pattern?

> [!abstract] Short answer
> **Request-Reply** implements two-way conversation over messaging: the requestor sends a request message and expects a reply message **on a separate reply channel**, addressed via a return address and matched by a correlation identifier. It is messaging's equivalent of a synchronous call — without holding a socket open.

## Two channels, two roles

Request-Reply has two participants: a **Requestor**, which sends the request and later processes the reply, and a **Replier**, which consumes the request and publishes a reply. The request channel may be point-to-point (one processor) or publish-subscribe (broadcast to interested parties), but the reply channel is almost always point-to-point — broadcasting replies rarely makes sense. The requestor has two consumption styles: a **synchronous block**, where one thread sends then blocks in a receive (simple, but one outstanding request per thread and painful to recover after a crash), or an **asynchronous callback**, where a dedicated reply thread dispatches replies into callbacks, allowing many outstanding requests over a shared reply channel. The plumbing details live in [[What is the Return Address pattern]] and [[What is the Correlation Identifier pattern]].

```d2
direction: right
req: "Requestor" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
q1: "Request channel\n(point-to-point or pub-sub)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
rep: "Replier" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
q2: "Reply channel\n(point-to-point)" {
  width: 220
  height: 65
  style.fill: "#fff3e0"
}
req -> q1 -> rep -> q2 -> req: "correlate\nreply" {
  style.stroke-dash: 4
}```

**Fig. 1.** Two one-way channels form the conversation; replies come back on their own channel, matched to their request.

## JMS reply plumbing

```java
// Requestor: reply goes where I say, replies carry the request's id
request.setJMSReplyTo(replyQueue);
request.setJMSCorrelationID(requestId);
producer.send(requestQueue, request);

// Replier: copy the request id, publish to the requested address
reply.setJMSCorrelationID(request.getJMSMessageID());
producer.send((Queue) request.getJMSReplyTo(), reply);
```

**Listing 1.** The full protocol is three header fields: where to reply, which request this is, and a reply payload.

> [!warning] Request-reply on messaging can quietly become slow RPC
> Blocking a thread per request and waiting on a reply channel spends the asynchrony you paid for; if every request must complete before the next step, messaging only added two broker hops. If the call is truly request-scoped and latency-critical, use an RPC stack; use request-reply when buffering and durability across outages matter, and make the timeout explicit either way.

> [!tip] Interview answer
> Request-Reply is two one-way messages: a request on a request channel and a reply on a reply channel, usually point-to-point. The request carries the reply address, and replies carry a correlation id so the requestor can match them. There are two styles — one blocked thread per request, or an async reply thread with callbacks for many outstanding requests. It is the messaging equivalent of a call, and it needs timeouts like any call.
