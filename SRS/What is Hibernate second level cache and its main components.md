<!--
reps: 0
priority: 0
-->
#Persistence/Caching #Java/Persistence/Hibernate/Cache #SRS

# What is Hibernate second level cache and its main components?

> [!abstract] Short answer
> The **second-level cache (L2)** is a **SessionFactory-scoped** store of **destructured entity/collection state** (attribute tuples), optional **natural-id → id** maps, and optional **query result lists**. It is **off** until you plug in a **`RegionFactory`** (`hibernate.cache.region.factory_class`) and mark types **`@Cacheable` / `@Cache`**. Main pieces: **`RegionFactory`** (provider SPI), named **`Region`s**, **`DomainDataRegion`** (entities, collections, natural ids) with a **`CacheConcurrencyStrategy`**, **`QueryResultsRegion` / `QueryResultsCache`**, and **`TimestampsCache`** (query-space invalidation). `SessionFactory.getCache()` is the eviction/contains API. L2 is **not** a bigger L1: different payload, shared across sessions, **bypasses the database’s concurrency control**.

## Provider, regions, domain data

`org.hibernate.cache.spi` is the **plug-in** for a cache backend. **`RegionFactory`** is the integration contract: it **builds `Region`s** for (1) **entity/collection (domain) data**, (2) **query result sets**, (3) **timestamps** used to decide whether a cached query list is stale. Implement the SPI, use `org.hibernate.cache.spi.support` (`StorageAccess` / `DomainDataStorageAccess`), or ship **JCache** via **`hibernate-jcache`**.

A **`Region`** is a **named** slice with its own expiry/replication, configured **outside** Hibernate. Default name = entity class or collection role; `@Cache(region=…)` overrides. Sharing one region among types also shares **eviction**: `evictEntityData(Class)` clears **everyone** on that region — usually give each hierarchy its own.

**`DomainDataRegion`** holds **destructured** entity and collection state plus **natural-id → PK** maps. Access goes through **`EntityDataAccess`**, **`CollectionDataAccess`**, **`NaturalIdDataAccess`**. Concurrent transactions pick a **`CacheConcurrencyStrategy`** on `@Cache(usage=…)`:

| Strategy | When |
| --- | --- |
| **`READ_ONLY`** | Immutable. **Update throws.** Simplest and fastest. |
| **Read/write, no lock** | Concurrent updates **extremely** rare. |
| **Read/write + soft lock** (`READ_WRITE`) | Updates possible but uncommon. |
| **Transactional** | Updates **frequent**. |

Only **read-heavy, write-rare** data belongs here. Unannotated entities are **always loaded from the database**.

```d2
direction: down
rf: "RegionFactory\n(Ehcache / JCache / …)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
dd: "DomainDataRegion\nentities, collections, natural ids" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
qr: "QueryResultsRegion\n+ QueryResultsCache" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
ts: "TimestampsRegion\n+ TimestampsCache" {
  width: 240
  height: 80
  style.fill: "#fce4ec"
}

rf -> dd
rf -> qr
rf -> ts
qr -> ts: stale if space invalidated
```

**Fig. 1.** `RegionFactory` builds three region kinds. Query-cache hits are validated against timestamps.

## Query cache and the `Cache` API

**Query result caching is separate** and **off** until `hibernate.cache.use_query_cache`. Mark a query **`setCacheable(true)`** (optional **`setCacheRegion`**). **`QueryResultsCache`** stores the **result list** under a **`QueryKey`** (HQL + bound parameters) in a **`QueryResultsRegion`**. A hit is **stale** if **any query space (table)** that query touches was invalidated since the put.

**`TimestampsCache`** lives in a special timestamps region. Hibernate **invalidates a space on DML** against that table. **`QueryResultsCache.get` always consults it.** Cached results are **ids**; if the **entity is not L2-cacheable** (or the instance is missing), Hibernate **hits the database for state** and the query cache buys little. Match query and entity cache policies.

L2 **enablement**: specifying a non-`NoCachingRegionFactory` **`RegionFactory`** turns L2 **on**; `hibernate.cache.use_second_level_cache` can force on/off. **`org.hibernate.Cache`**: `contains*` / `evictEntityData` / `evictCollectionData` / `evictNaturalIdData` / `evictQueryRegion`. Eviction is an immediate **hard** remove — **no** isolation. JDBC or another process **never** updates L2; you **evict** after external writes.

```java
factory.getCache().evictEntityData(Book.class, id); // one item
query.setCacheable(true).setCacheRegion("BookQueries");
```

**Listing 1.** Conceptual: programmatic eviction and a cacheable query. Entities in that result still need `@Cacheable`.

See [[What are Hibernate first and second level cache tiers]] for L1 vs L2. L1 is still the persistence context on one `Session`.

> [!warning] L2 is shared mutable state outside the database
> It **skips row locks / MVCC**. Stale reads after raw JDBC, ETL, or another JVM are **normal** until you evict. Query cache **without** cacheable entities (or with a busy `TimestampsCache`) can be **slower than no cache**. `READ_ONLY` plus an update is an **exception**, not a silent miss. `evictAll()` is **entities only**; use `evictAllRegions()` for collections, natural ids, and queries.

> [!tip] Interview answer
> Hibernate L2 is a SessionFactory-wide cache of destructured entity state, not the Session’s persistence context. A RegionFactory plugs in the backend and builds domain-data, query-result, and timestamp regions. I annotate read-mostly entities with @Cache and a concurrency strategy, and I only turn on the query cache when those entities are cacheable too, because results are ids checked against table timestamps. Anything updated outside Hibernate must be evicted; otherwise L2 will serve stale tuples.

See [[What are Hibernate first and second level cache tiers]], [[How does the Hibernate first-level cache work in Spring]], [[What is Hibernate performance tuning]], [[What is Hibernate SessionFactory]], [[What is Hibernate Query Language HQL]], and [[What is Hibernate as an ORM framework]].
