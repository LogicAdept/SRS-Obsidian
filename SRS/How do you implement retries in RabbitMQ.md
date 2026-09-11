<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How do you implement retries in RabbitMQ

> [!abstract] Short answer
> On the broker, combine a wait queue, TTL, and a DLX to bounce messages back to the work queue a bounded number of times, tracking attempts in headers, then park them in a final DLQ. Quorum queues offer a native `x-delivery-limit`; Spring AMQP offers RetryInterceptor with a RejectAndDontRequeueRecoverer. Never nack-and-requeue in a loop.

## Broker-side retry topology

The work queue's DLX points to a wait queue whose TTL returns the message to the work queue's exchange — each cycle is one retry with a backoff equal to the wait TTL. After N attempts (check the `x-death` header count or a custom header), route to a parking DLQ for humans. Quorum queues make the cap native: every reject (or crash) increments `x-delivery-count`, and once it exceeds `x-delivery-limit` (default 20 since 4.0) the message dead-letters or drops. The distinction from [[What is the difference between ack nack and reject in RabbitMQ]] matters here: nack does not count as failure since 4.3's counting change.

```d2
direction: down
work: "work queue\nx-delivery-limit=5" {
  width: 210
  height: 90
  style.fill: "#e3f2fd"
}
wait: "retry wait queue\nTTL = backoff" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
dlq: "parking DLQ\nafter limit exceeded" {
  width: 210
  height: 90
  style.fill: "#ffebee"
}
work -> wait: "reject requeue=false"
wait -> work: "TTL expiry → DLX"
work -> dlq: "delivery-limit exceeded"
```

**Fig. 1.** The retry loop is a TTL edge back into the work queue; the limit breaks the loop into the DLQ.

## Client-side retries and their trap

In-process retry libraries (Spring Retry, `RetryInterceptor`) retry the handler before returning a nack; exhausted retries should reject with requeue=false so the broker topology takes over — Spring's `RejectAndDontRequeueRecoverer` does exactly that. Retry-with-requeue inside the consumer is the poison loop generator: each redelivery restarts the handler, the queue never converges, and unacked pressure builds — the failure mode behind [[What is a poison message in RabbitMQ]].

```java
factory.setAdviceChain(RetryInterceptorBuilder.stateless()
        .maxAttempts(3)
        .backOffOptions(1000, 2.0, 10_000)
        .recoverer(new RejectAndDontRequeueRecoverer())
        .build());
```

**Listing 1.** Spring AMQP: three attempts with exponential backoff, then reject without requeue so the DLX path engages.

> [!warning] Requeue is not a retry strategy
> `basic.nack(requeue=true)` puts the message back at (or near) the head — with one consumer that is an immediate redelivery, i.e. a hot loop with zero backoff. Interviews treat "we just requeue until it works" as the classic outage recipe; bounded attempts plus a parking queue is the expected answer.

> [!tip] Interview answer
> Bound the attempts and add backoff: TTL wait queue bouncing through the DLX with an x-death counter, or quorum queues' native x-delivery-limit of 20, then a parking DLQ. Spring's RetryInterceptor with RejectAndDontRequeueRecoverer keeps in-process retries out of the requeue loop. Plain nack-requeue is the poison pattern.
