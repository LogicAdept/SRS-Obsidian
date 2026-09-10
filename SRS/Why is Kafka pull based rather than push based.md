<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# Why is Kafka pull based rather than push based?

> [!abstract] Short answer
> Because a **pull** model lets each consumer read at its own pace: a slow consumer simply falls behind and catches up later, instead of a broker **pushing** data faster than it can process — which would overwhelm it. Pull also makes batching natural: the consumer fetches everything available from its position in one go. Producers still **push** to brokers; only the broker-to-consumer leg is pull.

## How the consumer pulls

A consumer issues **fetch requests** to the broker that leads each partition it wants, naming its **offset**; the broker answers with a chunk of the log from that position. The consumer controls the position, so it can rewind and re-consume — replay is just moving the offset back. Naive polling would busy-wait when there is no data, so fetch requests are long-polled: `fetch.min.bytes` (default 1) and `fetch.max.wait.ms` (default 500) make the broker hold the reply until some data arrives or the wait expires.

```java
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

public class PullDemo {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "pull-demo");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(List.of("orders"));
            int polls = 0;
            int seen = 0;
            while (polls < 10 && seen < 3) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(500));
                polls++;
                if (!records.isEmpty()) {
                    for (ConsumerRecord<String, String> r : records) {
                        System.out.printf("poll #%d: partition=%d offset=%d key=%s value=%s%n",
                                polls, r.partition(), r.offset(), r.key(), r.value());
                    }
                    consumer.commitSync();
                    seen += records.count();
                } else {
                    System.out.printf("poll #%d: no data, keep waiting%n", polls);
                }
            }
        }
    }
}
```

**Listing 1.** The poll loop is the pull model made visible: the application asks for records, the broker never initiates delivery. This exact loop, run against a local Kafka 4.3.1 broker, printed:

```console
poll #1: no data, keep waiting
poll #2: no data, keep waiting
poll #3: no data, keep waiting
poll #4: no data, keep waiting
poll #5: no data, keep waiting
poll #6: no data, keep waiting
poll #7: partition=0 offset=0 key=u1 value=order-created
poll #7: partition=0 offset=1 key=u2 value=payment-authorized
poll #7: partition=0 offset=2 key=u1 value=order-shipped
```

**Listing 2.** Six empty polls, then one poll returns the whole available chunk: batching falls out of the pull design for free.

## Why not push

In a push system the broker controls the transfer rate, and consumers differ in speed; when a consumer's processing rate drops below the production rate, the broker keeps pushing and the consumer drowns — effectively a self-inflicted denial of service. Push also has to guess whether to send now or accumulate: tuned for low latency it sends single messages that get buffered anyway. A pull-based consumer solves both: it takes everything available up to a configured maximum, and it degrades by growing lag, which is exactly what [[What is Kafka consumer lag and how do you debug it]] measures. The queue-style alternative where delivery is pushed per-record and acknowledged exists too — see [[What are Kafka subscribe and poll for]] for how the classic API splits this work.

> [!warning] “Pull” does not mean hammering the broker
> Consumers do not spin in tight read loops: fetches are long-polled with `fetch.min.bytes` and `fetch.max.wait.ms`, and a paused or idle group costs the broker nothing. If you see busy polling, check that a max wait is configured — not that you must switch to push.

> [!tip] Interview answer
> Kafka consumers pull: they send fetch requests with their offset to the partition leader and get back a chunk of the log. Push would put the broker in charge of the rate and overwhelm slow consumers, while pull lets a lagging consumer catch up at its own speed and gives optimal batching in one request. Long polling via fetch.min.bytes and fetch.max.wait.ms keeps pulls from busy-waiting when the log is empty.

