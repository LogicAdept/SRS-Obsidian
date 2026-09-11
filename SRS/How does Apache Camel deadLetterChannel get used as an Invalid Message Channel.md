<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# How does Apache Camel deadLetterChannel get used as an Invalid Message Channel

> [!abstract] Short answer
> You install `errorHandler(deadLetterChannel("jms:queue:invalid-messages"))` and throw from validation — when the body is null or the `MessageType` header is wrong, the exchange moves to the configured endpoint. The dead-letter endpoint is thus used as the Invalid Message Channel, while the moving machinery is Camel's Dead Letter Channel error handler.

## Validation throws, the error handler parks

Camel's documentation describes the Dead Letter Channel as an error handler implementing the EIP: messages that fail processing are moved to a dead letter queue, which is a Camel **endpoint** — any component, from `log:` to `jms:` to a database. The IMC-shaped usage makes the validation explicit: an `otherwise` clause (or an `onException`) throws an `IllegalArgumentException` when the payload fails the channel's contract, and the error handler moves the exchange to the quarantine endpoint with the failure recorded. Two documented defaults matter for the interview: the dead letter channel's redelivery policy uses `maximumRedeliveries` of 0 and a `redeliveryDelay` of 1000 ms, and only when all redelivery attempts have failed does the message move to the dead letter queue — so with default settings the park happens on the first failure, while a raised maximum turns the flow into retry-then-park, the distinction dissected in [[What is the difference between the Retry Pattern and Invalid Message Channel]]. The handler also supports using the **original input message** when moving the exchange — the quarantine receives the payload as delivered, which is the pattern's requirement.

```java
errorHandler(deadLetterChannel("jms:queue:invalid-messages")   // Conceptual
    .maximumRedeliveries(0)
    .useOriginalMessage());

from("jms:queue:orders")
    .choice()
      .when(header("MessageType").isNotEqualTo("Valid"))
        .throwException(new IllegalArgumentException("contract violation"))
      .otherwise().to("bean:orderService");
```

**Listing 1.** Conceptual shape: the contract check throws, the error handler parks on the invalid-messages endpoint with the original message.

> [!warning] The endpoint name is convention, not the pattern split
> `deadLetterChannel(...)` is Dead Letter Channel machinery end to end — redelivery counters, error-handler semantics, broker delivery. Labeling the endpoint `invalid-messages` serves the IMC role only if the traffic routed there is genuinely receiver-invalid; everything else is DLC and the difference is [[What is the difference between Invalid Message Channel and Dead Letter Channel]].

> [!tip] Interview answer
> In Camel you express the pattern as an error handler plus validation: `errorHandler(deadLetterChannel("jms:queue:invalid-messages"))`, with route logic throwing on contract violations. The failed exchange goes to that endpoint with its original message. Remember the machinery is a dead-letter error handler — maximumRedeliveries defaults to 0, and any redelivery you add is DLC behavior around an IMC-shaped destination.
