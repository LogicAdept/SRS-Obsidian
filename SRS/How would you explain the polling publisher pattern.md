<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration #Messaging/Async #SRS

# How would you explain the polling publisher pattern?

> [!abstract] Short answer
> The **Polling Publisher** is the simple publisher half of a [[How would you explain the transactional outbox pattern|transactional outbox]]: a component **periodically queries the outbox table** for unsent rows and publishes each one to the message broker, then marks it sent.

## Query, publish, mark — with known trade-offs

The outbox row became durable in the same transaction as the business data; something must now carry it to the broker. The polling publisher does it with the dumbest reliable mechanism available: on a schedule, select the unsent rows, publish them, mark them. Its virtues are exactly that: it works with **any SQL database** — no log access, no special privileges, no extra infrastructure — and it is trivial to reason about and operate. Its costs are equally structural: **latency** is the polling interval (events leave on the next tick, not when they commit), the database absorbs a query load proportional to publish frequency and backlog, correct **ordering** is tricky once you parallelize (per-aggregate ordering needs care that naive `SELECT ... LIMIT n` does not give), and NoSQL stores without queryable secondary structures may not support the pattern at all. When interval-latency or query load is unacceptable, the upgrade path is the other outbox publisher: [[How would you explain transaction log tailing for integration]], which reacts to commits instead of polling.

```d2
direction: right
ob: "Outbox table\nsent = false" {
  width: 190
  height: 65
  style.fill: "#fff3e0"
}
pp: "Polling publisher\nevery N seconds" {
  width: 210
  height: 70
  style.fill: "#e3f2fd"
}
br: "Broker" {
  width: 140
  height: 55
  style.fill: "#e8f5e9"
}
mk: "mark sent" {
  width: 130
  height: 45
  style.fill: "#fff3e0"
}
ob -> pp: "select unsent"
pp -> br: "publish"
pp -> mk -> ob: "update" {
  style.stroke-dash: 4
}```

**Fig. 1.** Poll-publish-mark on a loop; the interval is the latency dial and the database-load dial at once.

## The loop in three statements

```sql
SELECT id, type, payload FROM outbox WHERE sent = false ORDER BY id LIMIT 100;
-- publish each payload to the broker
UPDATE outbox SET sent = true WHERE id IN (...);   -- crash here = redelivery
```

**Listing 1.** Ordering by the monotonic id preserves insertion order for a single-threaded publisher; parallelizing by aggregate needs a grouping step this loop does not show.

> [!warning] Marking is not atomic with sending
> A crash between publish and `sent = true` re-publishes the row — the pattern is at-least-once by construction, so consumers must dedup. Two subtler traps: parallel publishers breaking per-aggregate order, and interval tuning that looks fine in tests and doubles publish lag the first time the backlog grows.

> [!tip] Interview answer
> The Polling Publisher implements the outbox publication step by querying the outbox table on a schedule, publishing unsent rows to the broker, and marking them. It needs nothing but a queryable SQL table, at the price of interval-bounded latency, extra query load, and ordering pitfalls when parallelized. When poll latency is too high, replace it with transaction log tailing — and design consumers for at-least-once either way.
