<!--
reps: 0
priority: 0
-->
#Caching #DistributedSystems #SystemDesign/Architecture #SRS

# How would you explain distributed caching and cache hierarchies at a high level

> [!abstract] Short answer
> A cache hierarchy stacks several cache layers along the read path — client, CDN edge, web/proxy, application-local, distributed cache, database buffers — each closer to the user being faster but holding less coherent data. A distributed cache is the layer where many application nodes share one logical cache (Redis, Memcached), so one node's fill benefits all nodes; the price is a network hop and cluster-level invalidation.

## The layers and their tradeoff

From the user inward, each layer has more complete data but higher latency: a browser or CDN edge serves one user or one region, a reverse proxy serves one service, an in-process L1 serves one application instance, and a distributed L2 serves the fleet. An in-process cache is fastest (no network hop) but every node fills its own copy, so memory is wasted and coherence is per-node; a shared Redis or Memcached tier is one hop slower but a fill by node A is a hit for node B, and eviction/invalidation happens once. A two-level design (local L1 in front of shared L2) gets both — and inherits both invalidation problems, which is why [[How do you implement multi-level caching in Spring Boot]] and [[How do you invalidate Spring Cache in a cluster]] exist as concrete recipes.

## What makes a cache distributed

A distributed cache is itself a cluster: data is partitioned by key across shards (consistent hashing keeps remapping small when nodes join or leave) and often replicated for availability. The client library or a proxy routes each get/set to the shard owning the key. This scaling model is why the distributed tier can hold datasets far beyond one machine's RAM — but every operation is now a network round trip, so batching (mget) and hot-key mitigation matter. [[What is caching used for]] places the layer on the read path, [[What difficulties arise when working with caching]] lists the failure modes, and [[How do you use Redis as a Spring CacheManager]] shows the concrete Spring integration.

```d2
direction: down
App nodes: {
  shape: sql_table
  label: "app-1 | app-2 | app-3\nL1 in-process caches"
  width: 320
  height: 80
}
L2: {
  label: "distributed cache (Redis cluster)\nshard-1 | shard-2 | shard-3"
  width: 340
  height: 90
}
DB: {
  label: "origin database"
  width: 200
  height: 60
}
App nodes -> L2: "miss in L1 -> one network hop"
L2 -> DB: "miss in L2 -> fill + TTL"
```

**Fig. 1.** Two-level hierarchy: per-node L1 caches in front of a shared, sharded L2; only L2 misses reach the origin.

> [!warning] Every layer multiplies staleness
> With client, CDN, L1 and L2 caches, one write may leave four copies stale for four different TTLs. Deep hierarchies need explicit invalidation propagation or short TTLs at the outer layers — otherwise users see writes that "did not stick".

> [!tip] Interview answer
> A cache hierarchy is a stack of copy layers ordered by proximity: client and CDN, then local in-process, then a shared distributed cache like Redis, then database buffers. Distributed means many nodes share one logical cache, sharded by key, so fills benefit the fleet at the cost of a network hop and cluster-wide invalidation.
