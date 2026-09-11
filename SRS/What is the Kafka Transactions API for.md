<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka Transactions API for?

> [!abstract] Short answer
> Grouping many produces — across any number of partitions — plus the consumer offsets they correspond to into one atomic unit: either every output lands and every offset advances, or neither happens. The API is the transactional producer surface — `initTransactions`, `beginTransaction`, `commitTransaction`, `abortTransaction`, `sendOffsetsToTransaction` — keyed by a unique `transactional.id` that fences stale instances ([[What happens during a Kafka consume-transform-produce transaction]]).

## The method surface and its contract

Setting `transactional.id` is the entry fee: idempotence turns on automatically with it, and the id's job is recovery across producer sessions — a new process with the same id fences the zombie one ([[What is producer fencing in Kafka transactions]]). `initTransactions()` must be called before anything else: it registers the producer with the transaction coordinator and aborts any transaction a previous instance left open. Exactly one transaction may be open per producer at a time, and once `transactional.id` is set, every send must happen inside a transaction — records between `beginTransaction()` and `commitTransaction()` form one atomic batch.

```java
producer.initTransactions();
try {
    producer.beginTransaction();
    for (ConsumerRecord<String, String> r : batch) {
        producer.send(transform(r));
    }
    producer.sendOffsetsToTransaction(offsets(batch), consumer.groupMetadata());
    producer.commitTransaction();
} catch (ProducerFencedException | OutOfOrderSequenceException | AuthorizationException e) {
    producer.close();             // another instance owns this transactional.id
} catch (KafkaException e) {
    producer.abortTransaction();  // rollback, then retry the whole batch
}
```

**Listing 1.** The canonical transactional loop: recover first, begin, produce, attach the input offsets, commit — and the two-tier exception contract decides between closing and retrying.

The exception contract is the part interviews probe. Fatal errors — `ProducerFencedException`, `OutOfOrderSequenceException`, `AuthorizationException` — mean the producer cannot continue, and closing it is correct. Any other `KafkaException` leaves the producer usable: `abortTransaction()` rolls the batch back and the loop can retry. `sendOffsetsToTransaction` takes the consumer's `ConsumerGroupMetadata`, which is what lets the group coordinator validate the committing member — the offsets become part of the transaction exactly like the produced records. The timeout budget is `transaction.timeout.ms` (default 60 seconds); a value above the broker's `transaction.max.timeout.ms` fails the request with `InvalidTxnTimeoutException`.

## What commit actually publishes

```d2
direction: down
init: "initTransactions\nregister with coordinator,\nfence older instance" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
begin: "beginTransaction" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
work: "send() to any partitions\n+ sendOffsetsToTransaction\n(offsets join the txn)" {
  width: 340
  height: 110
  style.fill: "#fff3e0"
}
commit: "commitTransaction\ncontrol records: COMMIT" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
abort: "abortTransaction\ncontrol records: ABORT" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
init -> begin -> work
work -> commit: success
work -> abort: failure
```

**Fig. 1.** The transaction lifecycle: the coordinator records the participants, and on commit or abort every involved partition gets a control marker that `read_committed` consumers use to filter.

Commit does not "flush" anything to consumers by itself — it writes control records over every partition the transaction touched, and a consumer with `isolation.level=read_committed` reads only up to the last committed marker, skipping aborted material ([[What does isolation.level read_committed do in Kafka]]). Consumers of the default `read_uncommitted` see the raw records regardless — the atomicity is a property readers opt into. This API is also the substrate Kafka Streams builds on: `processing.guarantee=exactly_once_v2` packages the same begin-send-sendOffsets-commit cycle per committed batch ([[How do you achieve exactly-once processing in Kafka]]).

> [!warning] Idempotence alone is not transactions
> `enable.idempotence=true` only de-duplicates retries per partition — it says nothing about atomicity across partitions and does not cover consumed offsets. Only the transactional methods give the all-or-nothing unit; quoting idempotence as end-to-end exactly-once is the popular lie ([[What is an idempotent Kafka producer for]]).

> [!tip] Interview answer
> The Transactions API makes a set of produces plus the consumed input offsets atomic: init once with a transactional.id, then begin, send, sendOffsetsToTransaction, commit — or abort. The id fences zombie producers, fatal exceptions close the client while other KafkaExceptions just abort and retry, and read_committed consumers skip aborted work. It is the mechanism behind exactly-once consume-transform-produce loops and behind Streams' exactly_once_v2.

