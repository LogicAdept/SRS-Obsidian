<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Java/Spring/AMQP #SRS

# How does Spring AMQP retry work?

> [!abstract] Short answer
> Listener **retry** is a **Spring Retry interceptor** on the container **advice chain** (`RetryInterceptorBuilder.stateless()` or `.stateful()`), not a broker feature. After **max attempts**, a **`MessageRecoverer`** runs. Spring AMQP’s **library default** recoverer **acks and logs WARN** (message **never** hits a DLX). Boot, when you **enable** listener retries, uses **`RejectAndDontRequeueRecoverer`**: reject, no requeue — DLX if the queue has one. Without any interceptor, a thrown listener exception **requeues indefinitely**.

## Client retry vs broker retry

Put a `RetryOperationsInterceptor` on `SimpleRabbitListenerContainerFactory` / `DirectRabbitListenerContainerFactory` (`setAdviceChain`). Builder: `maxRetries`, `backOffOptions(initial, multiplier, max)`. **Stateless** retry: no surrounding transaction, or the transaction starts **inside** the retry callback. **Stateful** retry: transaction started **above** the retry; needs a stable message key (`messageId` / `createMessageIds=true` / `MessageKeyGenerator`). Null `messageId` is **fatal** for the consumer by default (one retry then stop) unless `statefulRetryFatalWithNullMessageId=false` ([[How do you consume RabbitMQ messages in Spring Boot]], [[How do you implement retries in RabbitMQ]]).

Recoverers:

| Recoverer | After retries exhausted |
| --- | --- |
| Default AMQP `MessageRecoverer` | Consume (ack) + WARN — **no DLX** |
| `RejectAndDontRequeueRecoverer` | `AmqpRejectAndDontRequeueException` → drop or **broker DLX** |
| `RepublishMessageRecoverer` | Publish to an error exchange/rk (optional confirms subclass) |
| `ImmediateRequeueMessageRecoverer` | Requeue even if `defaultRequeueRejected` is false |

Boot: listener retries **disabled** by default; enable with `spring.rabbitmq.listener.simple.retry.enabled` (and the **direct** equivalent if `listener.type=direct`). Then Boot’s recoverer is **`RejectAndDontRequeueRecoverer`** unless you define a `MessageRecoverer` bean. Template retries are a **separate** switch: `spring.rabbitmq.template.retry.enabled` ([[What is a poison message in RabbitMQ]]).

```java
@Bean
RetryOperationsInterceptor retryInterceptor() {
	return RetryInterceptorBuilder.stateless()
			.maxRetries(5)
			.backOffOptions(1000, 2.0, 10000)
			.recoverer(new RejectAndDontRequeueRecoverer())
			.build();
}
```

**Listing 1.** Conceptual. Advice-chain interceptor; backoff is **on the consumer thread**.

**Broker-side** alternative: dead-letter + TTL back to the work queue (`x-death` / mapped `retry_count`). From AMQP 3.2, when **you** republish, increment **`retry_count`** yourself — RabbitMQ **4.0 ignores client `x-*` headers**. Manual loop: increment, `rabbitTemplate.send` to the queue, or `ImmediateAcknowledgeAmqpException` when done.

```d2
direction: down
listen: "@RabbitListener throws" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
retry: "Retry interceptor\nmaxAttempts + backoff" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
rec: "MessageRecoverer" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}
dlx: "reject → DLX\nor republish / ack" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
listen -> retry
retry -> rec: "exhausted"
rec -> dlx
```

**Fig. 1.** Exhausted recoverer decides DLX vs swallow vs republish.

> [!warning] Default recoverer swallows the poison
> If you copy AMQP samples and leave the **default** recoverer, retries end in an **ack**. The broker **never** dead-letters. Production Boot retry is the opposite: **reject and don’t requeue** — you still must **declare** the DLX/DLQ.

> [!warning] Blocking backoff holds the consumer
> Stateless/stateful interceptors **sleep on the listener thread**. Long `maxInterval` stalls that consumer (Simple: that worker; Direct: that AMQP thread). Long delays belong on the **broker** (TTL/DLX), not in the advice chain.

> [!tip] Interview answer
> Spring AMQP retry is an advice-chain interceptor plus a recoverer. Boot turns it on with listener retry properties and rejects after the last attempt so a DLX can take over. The library default recoverer logs and acks — that is not a DLX. Stateful retry is for transactions that must roll back between attempts. Broker TTL loops are a different retry.
