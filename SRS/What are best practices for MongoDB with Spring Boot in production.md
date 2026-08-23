<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS

# What are best practices for MongoDB with Spring Boot in production?

> [!abstract] Short answer
> Treat the driver’s **`MongoClient` as a shared pool** (Boot auto-configures one bean), keep **index creation under ops control**, shape reads with **projections/DTOs**, tune **URI timeouts / write concern / retries**, and watch health with **Actuator** plus cluster metrics — not ad-hoc clients or surprise startup index builds.

## One client, one pool

Spring Boot auto-configures a **`MongoClient`** (and `MongoDatabaseFactory` / templates) from `spring.data.mongodb.*` or a connection URI. Inject that bean; do **not** construct a new `MongoClient` per request. The driver owns the connection pool; creating clients repeatedly bypasses pooling and leaks resources.

Customize timeouts and pool sizing through the URI, `MongoClientSettings`, or `MongoClientSettingsBuilderCustomizer` beans — Boot applies `spring.data.mongodb` properties unless you supply a full `MongoClientSettings` yourself.

```properties
spring.data.mongodb.uri=mongodb+srv://user:pass@cluster/db?retryWrites=true&w=majority
spring.data.mongodb.auto-index-creation=false
management.health.mongo.enabled=true
```

**Listing 1.** Typical production-oriented Boot properties: shared URI with durability/retry options, auto-index off, Mongo health on.

## Indexes under control

Spring Data MongoDB can derive indexes from `@Indexed` / `@CompoundIndex` / …, but **auto-index creation is off by default since 3.0** precisely to avoid lifecycle and performance surprises. Docs recommend **explicit** creation (`IndexOperations` / migrations / ops scripts), not relying on startup auto-create in production. Turning `spring.data.mongodb.auto-index-creation=true` (or `autoIndexCreation()`) is a convenience for local/dev, not a deploy strategy for multi-instance prod.

## Shape what you fetch

Large documents and nested graphs amplify network and memory cost. Prefer **projections**, focused queries, or DTO mapping so callers do not pull entire documents when they need a few fields — same discipline as anywhere else in Spring Data MongoDB.

## Connection reliability and durability

Official MongoDB connection options that matter in prod:

- **`retryWrites`** / **`retryReads`** — drivers default these on for modern servers; keep them on unless you have a reason to disable.
- **`w=majority`** (or equivalent write concern) for writes that must survive primary failover; majority is the usual durability default on modern replica sets.
- **`connectTimeoutMS`** / **`socketTimeoutMS`** (and related driver settings) so hung networks fail fast instead of parking threads forever.

```d2
direction: right
app: "Spring Boot apps\n(shared MongoClient)" {
  style.fill: "#e3f2fd"
}
driver: "Driver pool +\nretries / timeouts" {
  style.fill: "#fff3e0"
}
rs: "Replica set / Atlas\nw=majority" {
  style.fill: "#e8f5e9"
}
ops: "Actuator health +\ncluster metrics" {
  style.fill: "#f3e5f5"
}

app -> driver -> rs
app -> ops
rs -> ops
```

**Fig. 1.** Shared client to the cluster; health and metrics observe both the app path and the database.

## Observe it

Boot auto-configures a **`MongoHealthIndicator`** (key `mongo`, toggle with `management.health.mongo.enabled`). Pair that with Atlas, Cloud Manager / Ops Manager, or your own Prometheus metrics for lag, connections, and slow ops — Actuator alone is not capacity planning.

> [!warning] Auto-index at startup races the fleet
> Several instances enabling auto-index creation can contend on index builds and surprise production with build locks or unexpected indexes. Prefer migrations and leave auto-index off.

> [!warning] New MongoClient per request
> That pattern destroys pooling: you pay handshake cost constantly and can exhaust file descriptors / connections. Always reuse the Spring-managed client.

> [!tip] Interview answer
> One Boot-managed `MongoClient` for the pool, indexes created explicitly (auto-index off in prod), projections so you do not over-fetch, URI/settings for majority writes and retryable reads/writes with sane timeouts, and Actuator Mongo health plus real cluster monitoring.

See [[How do you map a Java class to a MongoDB document in Spring Data]], [[What is MongoRepository]], [[What is MongoTemplate]], and [[How does Spring Data MongoDB differ from Spring Data JPA]].
