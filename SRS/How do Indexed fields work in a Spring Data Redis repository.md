<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Java/Annotations #SRS

# How do Indexed fields work in a Spring Data Redis repository?

> [!abstract] Short answer
> `@Indexed` tells Spring Data Redis to maintain a Redis `SET` per property value that holds entity ids, so derived finders like `findByFirstname` can resolve ids without scanning every hash. Redis itself has no field query API; the repository layer owns these secondary structures.

## What Redis stores on save

A `@RedisHash` entity is a hash at `keyspace:id`. Each `@Indexed` property also gets a set whose key embeds the property path and value; members are entity ids. A helper set at `keyspace:id:idx` lists the index keys that belong to that entity so updates and deletes can clean them.

```java
@RedisHash("people")
public class Person {

  @Id String id;
  @Indexed String firstname;
  String lastname;
}

public interface PersonRepository extends CrudRepository<Person, String> {
  List<Person> findByFirstname(String firstname);
}
```

**Listing 1.** Domain type with a secondary index and a derived finder (Spring Data Redis repositories).

```text
HMSET people:<id> _class … firstname rand …
SADD  people <id>
SADD  people:firstname:rand <id>
SADD  people:<id>:idx people:firstname:rand
```

**Listing 2.** Conceptual commands from the Redis Repositories anatomy guide on insert (hash + keyspace set + secondary index + per-entity index tracking).

```d2
direction: down
hash: "Hash people:id\nfields of the entity" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
idx: "SET people:firstname:rand\nmembers = entity ids" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
track: "SET people:id:idx\nindex keys to clean" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
find: "findByFirstname\nSINTER / SMEMBERS → HGETALL" {
  width: 300
  height: 80
  style.fill: "#f3e5f5"
}

hash -> idx: "on save"
hash -> track: "on save"
idx -> find
```

**Fig. 1.** Hash holds the document; `@Indexed` sets enable id lookup; the `:idx` helper drives cleanup on update/delete.

Nested properties work the same way (`people:address.city:tear`). Indexes cannot be resolved on `@Reference` associations. You can also register indexes programmatically via `IndexConfiguration` / `@EnableRedisRepositories(indexConfiguration = …)` without annotating the field. Geospatial fields use `@GeoIndexed` and Redis `GEO*` commands instead of plain sets.

## Cost and expiry cleanup

Every save writes (and may rewrite) index sets — write amplification versus a plain hash. Deletes remove members from those sets using the `:idx` helper. Expiration cleanup is **not** automatic inside Redis alone: Spring Data Redis relies on keyspace notifications and a key-expiry listener (enable via `@EnableRedisRepositories` / `RedisKeyValueAdapter.EnableKeyspaceEvents`). Official docs warn that Pub/Sub is not durable — if a key expires while the application is down, secondary indexes can keep stale id references. Redis also cannot expire a single set member; residual cleanup is application-driven.

> [!warning] Stale index members after TTL
> Do not assume TTL on the entity hash always leaves indexes pristine. Cleanup needs a running listener and delivered expiry events; missed events leave phantom ids in `people:firstname:…` sets until something removes them. See also [[What is the TimeToLive annotation in Spring Data Redis]] and [[How does Spring Data Redis store a RedisHash entity]].

> [!tip] Interview answer
> Redis cannot query arbitrary hash fields, so Spring Data Redis builds secondary indexes with `@Indexed`: a `SET` per value holds entity ids, and finders read that set then load hashes. Saves pay extra writes to maintain those sets; expiry cleanup depends on keyspace events, so indexes can go stale if the app misses the expiry notification.
