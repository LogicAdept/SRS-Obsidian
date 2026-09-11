<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/OLAP/Druid #Databases/OLAP/Pinot #SRS

# What is the difference between ClickHouse Druid and Pinot?

> [!abstract] Short answer
> All three are distributed columnar OLAP engines over immutable, append-oriented data — but they optimize different points. ClickHouse couples a full SQL engine with MergeTree storage for general analytics over wide data; Druid and Pinot are purpose-built for low-latency, high-concurrency event/druid-style serving: Druid organizes data as immutable segments in deep storage served by Historical processes, Pinot splits servers/brokers for user-facing real-time analytics managed through Helix/ZooKeeper.

## Architecture contrast

Druid's process model separates concerns explicitly: Master servers (Coordinator assigns segments to Historicals, Overlord manages ingestion tasks), query Brokers, and Data servers — Historicals serve queryable segments from deep storage while Middle Manager/Peon (or Indexer) handle ingestion; rollup can pre-aggregate events at ingest for cost savings. Pinot's serving posture targets real-time product analytics: Controller/Broker/Server roles, Apache Helix on top of ZooKeeper driving cluster state to match intended state, immutable segments (with streaming upsert support), and separate server/broker scaling for query volume versus data volume. ClickHouse concentrates power in the [[What is the MergeTree engine in ClickHouse]] storage model plus a vectorized SQL layer: fewer moving daemons, richer SQL (window functions, complex joins, dictionaries — [[What is a ClickHouse dictionary]]), and second-scale ad-hoc scans over petabytes rather than millisecond fixed-dashboard serving.

```d2
ch: "ClickHouse\nfull SQL + MergeTree\nad-hoc analytics" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
druid: "Druid\nsegments in deep storage\nHistorical/Broker serving" {
  width: 330
  height: 100
  style.fill: "#e8f5e9"
}
pinot: "Pinot\nservers + brokers, Helix/ZK\nreal-time user-facing" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
ch -> druid: both columnar + immutable units
druid -> pinot: both serving-oriented
pinot -> ch: both SQL-ish, MPP
```

**Fig. 1.** Three engines, one family: columnar append analytics differentiated by serving posture and SQL depth.

## Choosing by workload

Interactive dashboards and APIs with thousands of concurrent fixed-shape queries, strong pre-aggregation (rollup), and Kafka-first ingestion lean Druid/Pinot. Mixed analytical workloads — ad-hoc SQL, wide tables, text search over logs ([[How do you search logs in ClickHouse]]), joins and dictionaries, batch + streaming in one engine — lean ClickHouse. All three prefer denormalized event data and dislike frequent row updates ([[Why is denormalization recommended in ClickHouse]]); none is an OLTP store.

> [!warning] "X is always faster" comparisons are workload-shaped
> Each system posts eye-watering numbers on its home turf: Druid/Pinot on high-concurrency pre-aggregated serving, ClickHouse on complex ad-hoc SQL over raw data. Fixed query patterns with tight latency SLOs favor the serving engines; evolving analytical questions favor SQL depth. Benchmarks that hide the query mix and concurrency model answer nothing.

> [!tip] Interview answer
> They're all columnar OLAP over append-oriented data. ClickHouse is the generalist: full SQL, MergeTree storage, ad-hoc analytics at scale. Druid is a serving engine with deep-storage segments and process separation — coordinator, broker, historical — built for high-concurrency aggregations with ingest-time rollup. Pinot targets real-time user-facing analytics with server/broker scaling managed by Helix on ZooKeeper. Pick by query mix: serving versus ad-hoc SQL.
