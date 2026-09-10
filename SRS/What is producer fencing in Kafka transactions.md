<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is producer fencing in Kafka transactions?

> [!abstract] Short answer
> Fencing is how Kafka stops a "zombie" producer — an instance the application believes is dead but that is still writing — from corrupting a transaction stream. Producers configured with the same `transactional.id` go through the transaction coordinator: `initTransactions` registers the id and **bumps its epoch**, and every request from a producer with an older epoch is rejected, while its open transaction is aborted.

The problem is session confusion, not just retries. An application can pause (GC, network partition, deployment overlap) and come back as two live copies believing both are current. With only idempotence, each copy is a distinct producer id, so the broker has no reason to reject either — [[What is an idempotent Kafka producer for]] covers what that mode does and does not promise. The `transactional.id` gives the cluster a stable name to reason across sessions: `initTransactions` runs `InitProducerId` with that id, the coordinator bumps the epoch, hands out the new producer id, and aborts any transaction the previous epoch left open. Writes or commits from the old epoch fail on the client.

## Two producers, one transactional.id

```java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.errors.ProducerFencedException;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

/** Two producers share one transactional.id; the second initTransactions fences the first. */
public class FencingDemo {
    public static void main(String[] args) {
        Properties p1cfg = new Properties();
        p1cfg.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        p1cfg.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        p1cfg.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        p1cfg.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "fence-demo");

        Properties p2cfg = new Properties();
        p2cfg.putAll(p1cfg);

        KafkaProducer<String, String> p1 = new KafkaProducer<>(p1cfg);
        try (KafkaProducer<String, String> p2 = new KafkaProducer<>(p2cfg)) {
            p1.initTransactions();
            System.out.println("p1 initTransactions ok");
            p2.initTransactions();
            System.out.println("p2 initTransactions ok, same transactional.id fences p1");
            try {
                p1.beginTransaction();
                p1.send(new ProducerRecord<>("fence-topic", "k", "zombie write"));
                p1.commitTransaction();
                System.out.println("p1 commit unexpectedly succeeded");
            } catch (ProducerFencedException | org.apache.kafka.common.errors.InvalidProducerEpochException e) {
                System.out.println("p1 write rejected: " + e.getClass().getSimpleName());
            }
        } finally {
            p1.close();
        }
    }
}
```

**Listing 1.** Run against a local Kafka 4.3.1 broker, kafka-clients 4.3.1:

```console
p1 initTransactions ok
p2 initTransactions ok, same transactional.id fences p1
p1 write rejected: InvalidProducerEpochException
```

**Listing 2.** The second `initTransactions` took the epoch; the zombie's commit attempt died with `InvalidProducerEpochException` — the 4.x surface of fencing, raised when a write or commit arrives with an old epoch (`ProducerFencedException` is its non-retriable sibling in the same hierarchy).

```d2
direction: right
p1: "p1 (epoch 0)\nzombie instance" {
  width: 210
  height: 80
  style.fill: "#ffebee"
}
p2: "p2 initTransactions\nepoch 0 → 1" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
coord: "Transaction coordinator\nstate in __transaction_state" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
rej: "p1 commit\nrejected: old epoch" {
  width: 230
  height: 70
  style.fill: "#ffebee"
}
p1 -> coord: requests with epoch 0
p2 -> coord: claim transactional.id
coord -> rej: fence epoch 0
```

**Fig. 1.** The coordinator stores the epoch with the transactional.id; after the bump, every old-epoch request is fenced and the previous instance's open transaction is rolled back.

> [!warning] No transactional.id, no fencing
> Fencing keys on the `transactional.id`; an idempotent producer without one cannot be fenced, because a restarted copy is simply a new producer id. Two practical traps: giving different application instances the same `transactional.id` on purpose (they will fence each other in a loop), and forgetting that `initTransactions` also aborts the previous session's pending transaction — a restart mid-transaction rolls back, it does not resume. Fencing is what makes the consume-transform-produce cycle in [[What happens during a Kafka consume-transform-produce transaction]] safe across restarts; the client-facing surface of these calls is [[What is the Kafka Transactions API for]].

> [!tip] Interview answer
> Producer fencing is the epoch mechanism over transactional.id: when a producer initializes, the transaction coordinator bumps the epoch and rejects anything arriving under an older one — a zombie's commits fail with ProducerFencedException or, in current clients, InvalidProducerEpochException, and its open transaction is aborted. It only works for producers that carry a transactional.id; plain idempotence cannot fence, since each session gets a fresh producer id.

