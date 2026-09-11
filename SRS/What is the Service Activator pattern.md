<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Endpoints/ServiceActivator #SRS

# What is the Service Activator pattern?

> [!abstract] Short answer
> A **Service Activator** is the endpoint that **connects a service object to a channel**: when a message arrives, it invokes a method on the service — and if the service produces output, sends that back to an output channel. It is how a synchronous application service becomes callable asynchronously.

## Channel in, service call, channel out

The activator is the generic "call a method with this message" endpoint: inbound messages from a channel trigger invocations on an application-supplied service; a service that returns a value gets its result published to an output channel (or to the reply address carried by the request). Spring Integration's documentation frames it exactly this way — the endpoint type for connecting any Spring-managed object to an input channel so it may play the role of a service, with `@ServiceActivator` marking the method — and notes that essentially every outbound gateway and adapter is a specialization of this endpoint calling some object's method. The design decisions mirror the consumer styles: invocation can run on the sender's thread (synchronous semantics, exceptions propagate to the caller) or on a listener thread (async, exceptions go to error handling); with [[What is the Event-Driven Consumer pattern]] plumbing underneath it inherits all the threading caveats, and its output behavior interacts with [[What is the Return Address pattern]] for reply routing.

```d2
direction: right
ch: "Input channel\norders.process" {
  width: 200
  height: 65
  style.fill: "#e3f2fd"
}
sa: "Service Activator\ninvoke method(msg)" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
svc: "Service\nbusiness method" {
  width: 170
  height: 60
  style.fill: "#e8f5e9"
}
out: "Output channel\n(result)" {
  width: 190
  height: 60
  style.fill: "#fff3e0"
}
ch -> sa -> svc
svc -> out: "if it returns"```

**Fig. 1.** The activator is pure glue: channel-to-method on the way in, method result-to-channel on the way out.

## The annotation is the whole wiring

```java
@ServiceActivator(inputChannel = "orders.process",
                  outputChannel = "orders.done")
public OrderResult process(OrderRequest req) {
    return orderService.handle(req);   // plain domain method
}
```

**Listing 1.** The service stays framework-free; the annotation binds its method to the channel pair.

> [!warning] Sync activators run on the caller's thread
> On a direct (synchronous) channel, the activator's method executes in the sending thread — its exceptions become the caller's exceptions, and its latency becomes the caller's latency. Teams that assume "it went through a channel, so it is async" discover the opposite in production; the async variant needs an executor channel or a poller, and errors then land in error handling, not in the caller's stack.

> [!tip] Interview answer
> A Service Activator connects a channel to a service object: arriving messages invoke a method, and returned values go to an output channel or the reply address. Spring Integration's @ServiceActivator is the canonical form, and most outbound endpoints are specializations of it. Know the threading semantics — direct channels invoke synchronously on the caller's thread — and route errors explicitly once the call is async.
