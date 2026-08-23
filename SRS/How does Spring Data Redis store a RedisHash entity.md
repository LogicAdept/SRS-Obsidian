<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Java/Annotations #SRS

# How does Spring Data Redis store a RedisHash entity?

> [!abstract] Short answer
> A **`@RedisHash`** entity is persisted as a Redis **hash** at key **`keyspace:id`**, with property fields flattened into hash entries (plus a **`_class`** type field). Spring Data also maintains **helper sets** for the keyspace and for **`@Indexed`** properties, and can apply a **TTL** when configured.

## Hash key and fields

`@RedisHash("people")` sets the keyspace. Together with `@Id` (or a property named `id`), the repository stores the entity at `people:<id>` via `HMSET` / hash write. Nested properties are flattened into hash fields; `_class` records type information for mapping.

```java
@RedisHash("people")
public class Person {

  @Id String id;
  @Indexed String firstname;
  String lastname;
}

public interface PersonRepository extends CrudRepository<Person, String> {}
```

**Listing 1.** Domain type + CRUD repository (`@EnableRedisRepositories` wires the infrastructure).

On first save (anatomy docs), Redis roughly receives:

1. **Hash** `people:<uuid>` — fields `_class`, `id`, `firstname`, `lastname`, …
2. **Keyspace set** `people` — member `<uuid>` (all ids in that keyspace)
3. **Secondary index set** `people:firstname:rand` — member `<uuid>` (if `@Indexed`)
4. **Index bookkeeping** `people:<uuid>:idx` — members that name the index keys to clean on update/delete

Optional expiry comes from `@RedisHash(timeToLive = …)` or `@TimeToLive` — see [[How do you store a Redis value with a TTL]] and [[What is the TimeToLive annotation in Spring Data Redis]].

```d2
direction: right
entity: "@RedisHash Person\nid + fields" {
  style.fill: "#e3f2fd"
}
hash: "Redis Hash\npeople:id" {
  style.fill: "#e8f5e9"
}
idx: "SET people:firstname:…" {
  style.fill: "#fff3e0"
}
ks: "SET people\n(all ids)" {
  style.fill: "#f3e5f5"
}

entity -> hash
entity -> idx
entity -> ks
```

**Fig. 1.** Entity payload lives in one hash; indexes and keyspace membership are separate Redis keys.

## Repositories vs `RedisTemplate`

Use **`CrudRepository`** + `@RedisHash` for simple entity CRUD and indexed finders. Use **`RedisTemplate`** / `opsFor*` when you need lists, sorted sets, streams, pub/sub, or ad-hoc commands outside the repository model — see [[What is the difference between RedisHash and RedisTemplate]].

> [!warning] Replace rewrites the whole hash
> Saving an existing entity **deletes** the old hash and recreates it so stale fields disappear. Unmapped hash fields written outside Spring Data are lost on the next repository save. Indexes are cleaned and rebuilt via the `:idx` helper set.

> [!warning] Indexes are not hash fields
> `@Indexed` data lives in **separate SET keys**, not inside the entity hash. Deleting only the hash key by hand leaves orphan index members until you go through the repository (or clean indexes yourself).

> [!tip] Interview answer
> Spring Data Redis maps `@RedisHash` types to a Redis hash at `keyspace:id`, stores `_class` plus flattened properties, and keeps SET helpers for the keyspace and `@Indexed` finders. TTL can sit on the hash. Repositories suit CRUD; reach for `RedisTemplate` for other Redis structures.

See [[How do Indexed fields work in a Spring Data Redis repository]], [[What is the difference between RedisHash and RedisTemplate]], and [[How do you store a Redis value with a TTL]].
