<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# When should you use RabbitMQ instead of HTTP

> [!abstract] Short answer
> When the caller must not wait, when work should survive the receiver being down, when several independent consumers need the same event, or when spikes must be buffered instead of crashing the backend. Keep HTTP for synchronous request-response the user actively waits on.

## The decision axis

Synchronous HTTP couples availability: both ends must be up, the caller waits, and spikes become load spikes. A broker decouples in time (buffering), in availability (messages wait), and in fan-out (one event, many subscribers via [[What is a RabbitMQ fanout exchange]]). It also adds delivery semantics — acks, retries, dead-lettering — that HTTP services have to re-implement ad hoc. The cost side: eventual completion instead of immediate answers, a new operational component, message schema discipline, and reordering or redelivery to handle.

```d2
direction: down
http: "HTTP\ncaller waits\nboth must be up" {
  width: 210
  height: 100
  style.fill: "#fff3e0"
}
mq: "broker\nbuffer, fan-out, retry" {
  width: 210
  height: 100
  style.fill: "#e8f5e9"
}
use1: "report generation\nemail, media jobs" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
use2: "order events\naudit, analytics, CRM" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
mq -> use1
mq -> use2
```

**Fig. 1.** Typical broker workloads: async jobs and one-event-many-consumers integrations.

## The honest boundary

Long-running operations over HTTP need webhooks or polling glue that a broker gives you natively — [[What is the Request-Reply pattern]] explains what reply-over-broker looks like when an answer *is* needed. Do not push every CRUD read through a queue: latency and feedback loops matter there, which is why the answer is workload-shaped, not religious. The architectural framing is the [[What is the Message Broker pattern|message broker]] versus direct API choice.

> [!warning] Queues do not make failures disappear
> Moving a call onto a broker shifts the failure to message handling time — the work still needs a working consumer, idempotency, and DLQ hygiene. Teams that treat "we use RabbitMQ" as reliability itself end up with unmonitored DLQs and silent backlogs instead of 5xx.

> [!tip] Interview answer
> Choose the broker when the caller should not block, when buffering spikes or surviving receiver downtime matters, or when multiple consumers need the same event. Choose HTTP for synchronous reads and user-facing writes. Async jobs, event fan-out, and integration glue fit RabbitMQ; CRUD over queues is ceremony, not design.
