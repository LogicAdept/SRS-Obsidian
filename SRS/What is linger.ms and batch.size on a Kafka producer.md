<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is linger.ms and batch.size on a Kafka producer?

> [!abstract] Short answer
> The two knobs of the producer's batching engine: `batch.size` (default 16384 bytes) caps how many bytes accumulate for one partition before the batch must ship, and `linger.ms` (default 5 ms) caps how long the batch waits for more records — whichever limit hits first sends it. Batching trades a few milliseconds of latency for far fewer requests, on both client and broker ([[How does a Kafka producer send a record internally]]).

## How the two interact

```d2
direction: right
arrive: "Records arrive\nfor one partition" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
batch: "Batch accumulates\nin the accumulator" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
size: "batch.size bytes?\nship immediately" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
time: "linger.ms elapsed?\nship whatever is there" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
arrive -> batch
batch -> size: full
batch -> time: timer wins
```

**Fig. 1.** Two exits from the accumulator: the size cap and the timer. Under load the size cap wins and linger costs nothing; idle traffic pays the full linger.

`batch.size` is per partition: a request to a broker carries multiple batches, one for each partition with data ready. No attempt is made to batch records larger than this size — a single record bigger than the cap gets its own batch. `linger.ms` adds a small artificial delay: rather than sending one record immediately, the producer waits up to that long hoping more records arrive for the same partition; the docs compare it to Nagle's algorithm in TCP. Since Kafka 4.0 the default linger is 5 ms rather than 0 — larger batches typically produce similar or lower end-to-end latency because the efficiency gain outweighs the wait. The timer is an upper bound, not a promise: broker backpressure can stretch the effective linger beyond the setting ([[What Kafka producer settings matter in practice]]).

```properties
batch.size=16384          # per-partition batch cap in bytes; 0 disables batching
linger.ms=5               # max wait for more records; 5 ms since Kafka 4.0
buffer.memory=33554432    # total memory for unsent batches
max.block.ms=60000        # how long send() blocks when buffer is exhausted
compression.type=none     # compression works per batch — batching feeds it
```

**Listing 1.** The batching quartet in context: the two caps, the memory that backs them, and the blocking bound ([[How is a Kafka producer structured]]).

## Choosing values

Raising `linger.ms` (say to 50) cuts request counts and raises throughput when load is moderate, at the cost of up to that much added latency for records that arrive with nothing else to batch with; raising `batch.size` lets each shipped request carry more useful bytes but wastes memory when traffic is sparse, because the producer allocates buffers of the batch size in anticipation. Compression interacts multiplicatively: a batch is the compression unit, so bigger batches compress better. The failure mode of over-tuning is memory: unsent batches live in `buffer.memory`, and when it is exhausted, `send()` blocks up to `max.block.ms` and then fails — a stall producers feel as a timeout spike rather than a slowdown ([[What is an idempotent Kafka producer for]]).

> [!warning] batch.size does not cap your record, and linger.ms does not cap your latency
> A record larger than `batch.size` still ships — as its own batch, subject to `max.request.size` and the broker's message cap. And the measured linger can exceed the setting under broker backpressure. Reading these as hard guarantees is the classic misconfiguration: the caps bound batching, not delivery, and `delivery.timeout.ms` is the bound that actually rules the end of a record's life.

> [!tip] Interview answer
> batch.size and linger.ms are the two exits of the producer accumulator: ship when a partition's batch reaches 16 KB by default, or when 5 ms have passed since the first record — whichever comes first. Since 4.0 linger defaults to 5 ms because batching usually lowers latency too. Bigger values raise throughput and compression efficiency but cost memory and tail latency, and when the record accumulator runs out, send blocks up to max.block.ms.

