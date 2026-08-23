<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# How do you implement Redis Pub/Sub with Spring Data Redis?

> [!abstract] Short answer
> Publish with `RedisTemplate.convertAndSend(channel, payload)` (or `RedisMessageSendingTemplate` for Spring Messaging conversion). Subscribe through a `RedisMessageListenerContainer` that registers `MessageListener` instances on `ChannelTopic` (exact name) or `PatternTopic` (wildcard). Redis Pub/Sub is fire-and-forget — offline subscribers miss messages.

## Publish

`RedisOperations.convertAndSend` publishes to a channel name and serializes the body with the template’s **value serializer**. The return value is the number of clients that received the message.

```java
@Service
class OrderEventPublisher {

  private final RedisTemplate<String, Object> redisTemplate;

  OrderEventPublisher(RedisTemplate<String, Object> redisTemplate) {
    this.redisTemplate = redisTemplate;
  }

  void publish(OrderCreatedEvent event) {
    redisTemplate.convertAndSend("order-events", event);
  }
}
```

**Listing 1.** High-level publish through `RedisTemplate` (Spring Data Redis “Publishing” reference).

## Subscribe

Low-level `RedisConnection.subscribe` blocks the calling thread. Production code uses **`RedisMessageListenerContainer`**: it manages subscription connections, threading, and dispatch to listeners.

```java
@Configuration
class RedisPubSubConfig {

  @Bean
  RedisMessageListenerContainer redisMessageListenerContainer(
      RedisConnectionFactory connectionFactory,
      MessageListener orderEventsListener,
      MessageListener inventoryEventsListener) {

    RedisMessageListenerContainer container = new RedisMessageListenerContainer();
    container.setConnectionFactory(connectionFactory);
    container.addMessageListener(orderEventsListener,
        ChannelTopic.of("order-events"));
    container.addMessageListener(inventoryEventsListener,
        PatternTopic.of("inventory.*"));
    return container;
  }

  @Bean
  MessageListener orderEventsListener(RedisTemplate<String, Object> template) {
    return (message, pattern) -> {
      OrderCreatedEvent event = (OrderCreatedEvent) template.getValueSerializer()
          .deserialize(message.getBody());
      // handle event
    };
  }
}
```

**Listing 2.** Container + exact channel and pattern subscriptions. Prefer `MessageListenerAdapter` to delegate deserialization to the configured serializer automatically.

```d2
direction: right
pub: "convertAndSend\n(channel, payload)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
redis: "Redis PUBLISH\nfire-and-forget" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
container: "RedisMessageListenerContainer" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
listener: "MessageListener.onMessage\n(or @RedisListener)" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}

pub -> redis -> container -> listener
```

**Fig. 1.** Publisher does not know subscribers; the listener container drives async delivery.

`ChannelTopic` matches one channel; `PatternTopic` uses Redis pattern subscribe (`inventory.*`). Alternative: `@RedisListener` on a Spring bean method — infrastructure registers it with the same container.

> [!warning] Not durable and not a queue
> Pub/Sub does not persist messages. A subscriber that is down when `convertAndSend` runs never sees that message. There is no ack/retry semantics — use [[What is the difference between Redis Pub Sub and Redis Streams]] or a broker when you need consumer groups or replay. Match serializer on publish and subscribe sides.

See [[What is RedisTemplate]] and [[What serialization strategy should you use with RedisTemplate]].

> [!tip] Interview answer
> I publish with `redisTemplate.convertAndSend("order-events", event)` and subscribe with a `RedisMessageListenerContainer` wired to my `RedisConnectionFactory`. I register listeners on `ChannelTopic` for exact channels or `PatternTopic` for wildcards. It is broadcast messaging, not a work queue — offline consumers miss messages.
