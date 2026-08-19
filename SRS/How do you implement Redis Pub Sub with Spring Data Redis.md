<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Publisher: RedisTemplate.convertAndSend(channel, event).

Subscriber: implement MessageListener and handle onMessage. Wire a RedisMessageListenerContainer with the connection factory, then add the listener to a ChannelTopic or a PatternTopic (wildcard).

```java
redisTemplate.convertAndSend("order-events", event);
container.addMessageListener(orderSubscriber, new ChannelTopic("order-events"));
container.addMessageListener(inventorySubscriber, new PatternTopic("inventory.*"));
```

Messages are fire-and-forget; there is no persistence in this model.
> [!warning] Unverified traps from the dump
> - A down subscriber misses the message; this is not a work queue.
> - You must deserialize the message body yourself in onMessage in the dump's listener.
