<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Endpoints/EventDrivenConsumer #SRS

# What is the Event-Driven Consumer pattern?

> [!abstract] Short answer
> An **Event-Driven Consumer** is invoked **by the messaging system when a message arrives**: the application registers a callback and sits dormant — no threads of its own — until delivery triggers it. The asynchronous counterpart of the [[What is the Polling Consumer pattern]].

## The push style of consumption

The consumer registers with the messaging system; when a message is delivered on the consumer's channel, the system invokes the consumer — typically on a delivery thread it owns — and the consumer hands the message to the application through the callback API. Whether the messaging system itself is internally event-driven is an implementation detail; what the application sees is: no polling loop, no parked threads, near-immediate reaction to arrival. JMS expresses it as a `MessageListener` with `onMessage(Message)`; message-driven beans and Spring's listener containers (`@JmsListener`, `@RabbitListener`) are industrialized versions managing the delivery threads, concurrency, and redelivery for you — and on a channel carrying commands they are the invocation engine of the [[What is the Service Activator pattern]]. The price is threading discipline: the callback runs on infrastructure threads, so long or blocking work inside it stalls deliveries and, on transacted sessions, holds the session hostage — the classic source of "my listener is mysteriously single-threaded" incidents. Consumption pacing and thread pooling belong in the container configuration, and heavy work should be handed off deliberately; the pacing-first alternative remains the [[What is the Polling Consumer pattern]].

```d2
direction: down
app: "Application\nonMessage(msg)" {
  width: 210
  height: 60
  style.fill: "#e8f5e9"
}
reg: "register listener\nthen sleep (no threads)" {
  width: 250
  height: 65
  style.fill: "#fff3e0"
}
ms: "Messaging system\nown delivery thread" {
  width: 230
  height: 65
  style.fill: "#e3f2fd"
}
cb: "delivery arrives\ninvoke callback" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
app -> reg -> ms
ms -> cb -> app: "push"```

**Fig. 1.** The application thread disappears between deliveries; the broker's delivery thread does the calling.

## The callback contract

```java
public class OrderListener implements MessageListener {
    public void onMessage(Message m) {
        // runs on the provider's delivery thread:
        // keep it short, or hand off to your executor
        handle(parse(m));
    }
}
consumer.setMessageListener(new OrderListener());
```

**Listing 1.** Registration replaces the loop; the method's runtime budget is the broker's thread, not the application's.

> [!warning] Blocking in onMessage blocks the delivery pipeline
> Slow database calls inside the callback stall the container's thread pool, delay redeliveries, and can trip session timeouts — the failure looks like a broker problem but lives in the callback. Size listener concurrency explicitly, monitor callback duration, and offload long work to a bounded executor with its own backpressure.

> [!tip] Interview answer
> An Event-Driven Consumer registers a callback and is invoked by the messaging system when a message arrives — the push model: dormant until delivery, no polling, minimal latency. JMS MessageListener and Spring listener containers are the standard forms. The catch is threading: callbacks run on infrastructure threads, so they must be short or deliberately offloaded, with container concurrency configured explicitly.
