<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Channels #SRS

# What is the Channel Adapter pattern?

> [!abstract] Short answer
> A **Channel Adapter** connects an application that does **not speak messaging** to the messaging system: one side is a messaging client sending/receiving on channels, the other side calls the application's own API or reads its data. It is the glue that lets a legacy or non-messaging system join an integration solution.

## One adapter, two very different sides

The adapter acts as a messaging client to the messaging system and invokes application functions through an application-supplied interface. Any application can join the integration as long as it has a proper adapter, and the adapter can attach at different layers of the application — a file drop directory, a database table, a REST endpoint, a proprietary SDK — depending on where the needed data lives. Inbound adapters poll or subscribe to the application and publish messages; outbound adapters receive from channels and invoke application functions. Spring Integration's `inbound-channel-adapter` / `outbound-channel-adapter` pair, and its `@ServiceActivator`-style handlers, are direct implementations; the distinction from a [[What is the Messaging Gateway pattern]] is that a gateway hides messaging **inside** a domain-facing facade, while an adapter reaches out to an app that knows nothing about messaging at all. Both sit on top of the [[What is the Message Endpoint pattern]] idea.

```d2
direction: right
app: "Legacy app\n(no messaging API)" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}
api: "App interface:\nfiles / DB / SDK" {
  width: 210
  height: 65
  style.fill: "#fff3e0"
}
ad: "Channel Adapter\nmessaging client + glue" {
  width: 230
  height: 70
  style.fill: "#e3f2fd"
}
ch: "Message Channel" {
  width: 190
  height: 60
  style.fill: "#e8f5e9"
}
app -> api -> ad -> ch```

**Fig. 1.** The adapter is the only component that knows both worlds: the application's API and the messaging system's client API.

## Two directions, one contract

```java
// Outbound adapter: consume from channel, call the app
@RabbitListener(queues = "orders.print")
public void handle(OrderDto dto) {
    printerService.print(dto);   // app-supplied interface
}
// Inbound adapter: poll the app, publish to channel
@Scheduled(fixedDelay = 5000)
public void publishNewRows() {
    repository.findUnpublished()
        .forEach(row -> template.convertAndSend("crm.updates", row));
}
```

**Listing 1.** The same adapter concept in both directions: messaging on one side, the application's own API on the other, with the adapter translating between them.

> [!warning] An adapter is not a license to embed business logic
> The adapter should translate and dispatch, nothing more; once it starts making domain decisions it becomes a hidden service nobody tests or monitors. It also needs its own failure story — when the app API is down, the inbound adapter must retry or park, not silently skip data it failed to read.

> [!tip] Interview answer
> A Channel Adapter connects a non-messaging application to a messaging system: it is a messaging client on one side and a caller of the application's API or reader of its data on the other. Inbound adapters publish app data to channels, outbound adapters invoke app functions from messages. Spring Integration's channel adapters are the canonical example, and it is what lets legacy systems join an EIP-based integration unchanged.
