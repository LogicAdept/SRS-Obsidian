<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How do you declare a durable quorum queue with a DLX

> [!abstract] Short answer
> One declare call: durable=true, x-queue-type=quorum, x-dead-letter-exchange (optionally x-dead-letter-routing-key), often x-delivery-limit and max-length. Publishers then send persistent messages with confirms; consumers use manual acks with bounded prefetch. Policies are the preferred configuration surface where possible.

## The declaration

Durable plus quorum type is the data-safety base; the DLX arguments wire the failure path. `x-delivery-limit` caps redelivery attempts (default 20) so poison messages dead-letter; `x-max-length` with `reject-publish` applies backpressure rather than dropping head. Quorum queues must be durable — a durable flag is implied — and the DLX itself must exist: an ordinary exchange plus a bound DLQ.

```java
ch.exchangeDeclare("orders", "direct", true);
ch.exchangeDeclare("orders.dlx", "direct", true);
ch.queueDeclare("orders.dlq", true, false, false, null);
ch.queueBind("orders.dlq", "orders.dlx", "orders");

Map<String, Object> args = Map.of(
    "x-queue-type", "quorum",
    "x-delivery-limit", 10,
    "x-max-length", 1_000_000,
    "x-dead-letter-exchange", "orders.dlx",
    "x-dead-letter-routing-key", "orders");
ch.queueDeclare("orders", true, false, false, args);
```

**Listing 1.** The full production shape: durable quorum queue, delivery limit, length bound, DLX target, and the DLQ behind it.

## The full path

Publishers close the loop: persistent delivery mode plus publisher confirms, so accepted messages are majority-persisted before the ack, per [[How do you make a RabbitMQ message survive a broker restart]]. Consumers run manual acks with prefetch tuned to handler speed, per [[What is RabbitMQ prefetch]]; rejected messages count toward the delivery limit and dead-letter into `orders.dlq` for triage, per [[What is a RabbitMQ dead letter exchange]]. Prefer policies over hardcoded x-arguments when operators, not deployments, should own the knobs — though queue type and delivery limits are declare-time values.

```bash
rabbitmqctl set_policy dlx "^orders$"   '{"dead-letter-exchange":"orders.dlx","dead-letter-routing-key":"orders"}'   --apply-to queues
```

**Listing 1.** The DLX leg via policy instead of x-arguments, so it can change without redeploying consumers.

> [!warning] The DLX must exist before traffic does
> Declaring a queue with a DLX that does not exist succeeds — the failure shows up at dead-letter time, when messages cannot be republished and are dropped. Topology order matters: exchanges and DLQ first, work queue second, traffic last.

> [!tip] Interview answer
> Durable quorum queue with x-dead-letter-exchange and x-dead-letter-routing-key, plus x-delivery-limit and max-length for poison and backpressure; DLX and DLQ declared beforehand; publishers persistent with confirms; consumers manual acks with bounded prefetch. Policies over hardcoded args where ops should own the values.
