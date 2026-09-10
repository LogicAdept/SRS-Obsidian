<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How do Kafka consumers fetch messages from a broker?

> [!abstract] Short answer
> The consumer sends fetch requests to the broker leading each assigned partition, stating its offset, and receives back chunks of the log as record batches. The request long-polls: the broker holds it up to `fetch.max.wait.ms` (500 ms default) until at least `fetch.min.bytes` (1 byte default) is available, so an empty partition does not spin the network. Several fetches run in parallel and their results are buffered for `poll()`.

## The fetch loop

Kafka's consumer works by issuing fetch requests to the brokers leading the partitions it wants to consume; it specifies its offset in the log with each request and receives back a chunk of log beginning from that position. That position is the consumer's own — it can rewind it to re-consume data, which is the basis of replay — see [[What is Kafka Consumer position for]].

Four client configs shape every fetch:

* `fetch.min.bytes` (1) — the server waits until at least this much data accumulates; raising it improves throughput at the cost of latency;
* `fetch.max.wait.ms` (500) — the maximum time the broker blocks when `fetch.min.bytes` is not yet reachable, the long-poll ceiling;
* `max.partition.fetch.bytes` (1 MiB) — the per-partition cap of one fetch response;
* `fetch.max.bytes` (50 MiB) — the total cap for one fetch; the consumer performs multiple fetches in parallel.

The caps are soft by design: if the first record batch of the first non-empty partition is larger than the limit, the batch is still returned so the consumer can make progress — a single oversized record can never wedge a fetch.

```d2
direction: right
cons: "consumer\nfetch(offset) per partition" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
lead: "partition leader broker\nlong-poll: wait until\nmin bytes or max wait" {
  width: 300
  height: 110
  style.fill: "#fff3e0"
}
log: "log read from offset\nrecord batches" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
buf: "client-side buffer\nfetches run in parallel" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
poll: "poll() drains up to\nmax.poll.records (500)" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
cons -> lead
lead -> log
log -> buf
buf -> poll
```

**Fig. 1.** Fetching and polling are decoupled: background fetches fill a buffer sized by the byte limits, and each `poll()` hands out at most `max.poll.records` from it — the records-per-poll setting does not change how much is actually fetched.

## Incremental fetch sessions

Re-sending the full partition list on every fetch scales badly for topics with thousands of partitions. Since KIP-227 the leader caches fetch sessions: the first request establishes a session (id plus epoch) and later requests only carry changed partitions, while the leader responds incrementally with whatever is new. Sessions are bounded on the broker — `max.incremental.fetch.session.cache.slots` defaults to 1000 — and a client whose session was evicted gets `FetchSessionIdNotFound` and simply re-establishes one; followers get priority in the cache over consumer sessions. The leader keeps serving from its log, and the same offset contract described in [[How does Kafka store data on disk as a log]] governs what comes back.

> [!warning] The "raise max.partition.fetch.bytes or big messages hang the consumer" myth
> The progress rule is explicit in the config contract: the first batch of the first non-empty partition is returned even when it exceeds `fetch.max.bytes` or `max.partition.fetch.bytes`. A consumer never hangs because one batch is too big — it receives it whole. What those limits really tune is batching efficiency: too small a per-partition cap just means many round trips for a backlogged partition.

> [!tip] Interview answer
> Fetching is a pull long-poll: the consumer asks each partition leader for a chunk of log from its own offset, the broker waits up to 500 ms for at least fetch.min.bytes of data to avoid busy-waiting, and returns record batches capped per partition at 1 MiB and per request at 50 MiB — oversized first batches are still returned to guarantee progress. Fetches run in parallel into a buffer that poll drains, and incremental fetch sessions since KIP-227 keep the requests cheap for high-partition topics.

