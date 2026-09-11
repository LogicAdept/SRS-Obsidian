<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging/Tools/RabbitMQ #SRS

# How does RabbitMQ dead-letter-exchange get used as an Invalid Message Channel

> [!abstract] Short answer
> A consumer that receives a malformed payload calls `basic.reject` (or `basic.nack`) with `requeue=false`, and RabbitMQ republishes the message to the queue's configured dead-letter exchange, whose binding parks it on a quarantine queue. The **receiver** made the decision — so the DLX machinery is serving the Invalid Message Channel role.

## Receiver-driven republishing over broker plumbing

RabbitMQ's dead-lettering documentation lists the events that republish a queue's message to its dead-letter exchange: negative acknowledgment via `basic.reject` or `basic.nack` with the `requeue` parameter set to `false`, per-message TTL expiry, the queue exceeding its length limit, and a quorum queue's delivery-limit exhaustion. The first of those is application-driven: the consumer parses, fails its own validation, and rejects without requeue — precisely the receiver decision that [[What happens if a receiver puts an invalid message back on the original channel]] demands. The wiring is a queue argument or a policy: attach `dead-letter-exchange` (optionally `dead-letter-routing-key`) to the working queue — for example `rabbitmqctl set_policy DLX ".*" '{"dead-letter-exchange":"my-dlx"}' --apply-to queues` — and declare a quarantine queue bound to that exchange. The broker then does the physical move, which is why the honest description is *IMC role on DLC machinery*: the split the pattern cares about is kept in [[What is the difference between Invalid Message Channel and Dead Letter Channel]], and the exchange itself is described in [[What is a RabbitMQ dead letter exchange]].

```text
# declare the quarantine queue bound to the DLX        (Conceptual wiring)
queue_declare("invalid-messages", durable=True)
queue_bind("invalid-messages", exchange="my-dlx", routing_key="orders")

# declare the working queue with the DLX attached
queue_declare("orders", arguments={"x-dead-letter-exchange": "my-dlx"})

# consumer side: validation failed -> park, never requeue
basic_reject(delivery_tag, requeue=False)
```

**Listing 1.** The three moves of the AMQP shape: quarantine binding, DLX argument on the working queue, and the consumer's no-requeue reject that triggers republishing.

> [!warning] The same DLX catches DLC traffic
> TTL expiry, max-length overflow, and delivery-limit exhaustion route to the same exchange, so a queue named `invalid-messages` fills with broker-dead messages that no receiver ever judged. Keep `reason` metadata (the first death's reason and queues are carried in dead-letter headers) and the discipline of [[What is a poison message in RabbitMQ]] so triage can separate receiver-invalid from broker-dead.

> [!tip] Interview answer
> You implement the pattern with a dead-letter exchange on the working queue and a quarantine queue bound to it. The consumer validates after delivery; on a structural failure it rejects with requeue=false, and RabbitMQ republishes the message to the DLX, parking it on the quarantine. The decision was the receiver's — but note the same DLX also catches expiry and overflow, which are broker dead-letter events.
