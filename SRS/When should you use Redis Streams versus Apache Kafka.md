<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Messaging/Tools/Kafka #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Redis Streams: simpler setup, sub-millisecond latency, moderate throughput (tens of thousands of messages per second), data fits in memory, you already run Redis. Dump use: lightweight event sourcing.

Kafka: massive throughput (millions per second), disk persistence, log compaction, complex routing, cross-datacenter replication. Dump use: enterprise event-driven architectures.
> [!warning] Unverified traps from the dump
> - Redis Streams are not a drop-in Kafka replacement when the log must outgrow memory.
> - Having Redis already is a stated reason to pick Streams for smaller workloads.
