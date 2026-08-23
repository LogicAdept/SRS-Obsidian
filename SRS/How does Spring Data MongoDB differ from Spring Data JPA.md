<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Spring/Data/JPA #SRS

# How does Spring Data MongoDB differ from Spring Data JPA?

> [!abstract] Short answer
> Both share the **Spring Data repository model** (derived queries, `CrudRepository` / paging). They differ in **store mapping and runtime**: JPA maps to **relational tables** via `@Entity` / `EntityManager`; MongoDB maps to **BSON documents** via `@Document` / `MongoTemplate`, with optional multi-document transactions through `MongoTransactionManager`.

## Shared repository surface

Method naming, paging, and custom `@Query` patterns feel familiar across modules. A derived finder looks the same on either side:

```java
public interface ProductRepository extends MongoRepository<Product, String> {
  List<Product> findByPriceLessThan(Double price);
}
```

**Listing 1.** Same Spring Data query-derivation style; Mongo uses `MongoRepository` and document ids (often `String` / `ObjectId`), not JPA’s typical generated `Long`.

Enable with `@EnableMongoRepositories` vs `@EnableJpaRepositories`.

## Mapping and low-level APIs

| Concern | Spring Data JPA | Spring Data MongoDB |
| --- | --- | --- |
| Domain marker | `@Entity`, `@Table`, `@Column` | `@Document`, `@Field`, `@Id` |
| Primary template | JPA `EntityManager` (+ Hibernate) | `MongoTemplate` / `MongoOperations` |
| Query language | JPQL / Criteria API / native SQL | MQL JSON, `Criteria`/`Query`, aggregations |
| Schema | Relational schema + DDL/migrations | Flexible documents; mapping is app-side |
| Transactions | Ubiquitous via `PlatformTransactionManager` / JPA | Multi-doc since MongoDB 4.0; wire `MongoTransactionManager` |

MongoDB’s `@Document` identifies a type persisted to a **collection** (name from `value`/`collection` or type default). JPA’s `@Entity` targets a **table** managed by the persistence provider.

```d2
direction: right
sd: "Spring Data\nRepositories" {
  style.fill: "#e3f2fd"
}
jpa: "JPA\n@Entity + EntityManager" {
  style.fill: "#fff3e0"
}
mongo: "MongoDB\n@Document + MongoTemplate" {
  style.fill: "#e8f5e9"
}
tables: "Tables / SQL" {
  style.fill: "#fce4ec"
}
docs: "Collections / BSON" {
  style.fill: "#f3e5f5"
}

sd -> jpa -> tables
sd -> mongo -> docs
```

**Fig. 1.** One repository abstraction; different mapping stacks and storage models.

## Transactions

JPA assumes transactional boundaries for most write paths. MongoDB supports multi-document ACID transactions on replica sets / sharded clusters (server 4.0+), but Spring does **not** turn them on by magic — you register **`MongoTransactionManager`** and use `@Transactional` (or session callbacks). Single-document writes already have atomicity at the document level without a multi-doc transaction.

> [!warning] Do not mix persistence annotations
> Putting **`@Entity`** on a Mongo document type (or expecting JPA lifecycle on `@Document`) does nothing useful and confuses both stacks. Use the annotations that belong to the module you configured.

> [!warning] Ids and “schema-less” still need discipline
> Mongo ids are often **`String`** (ObjectId hex) rather than auto-increment `Long`. “Schema-less” means the database does not enforce a table DDL — Spring Data still maps fields; inconsistent documents break converters and queries.

> [!tip] Interview answer
> Repository APIs look alike, but JPA talks tables through `@Entity` and `EntityManager`, while Spring Data MongoDB talks collections through `@Document` and `MongoTemplate`. Mongo multi-document transactions need MongoDB 4+ and a `MongoTransactionManager`; they are not the same default as JPA. Never annotate a Mongo type with `@Entity`.

See [[What is Spring Data JPA]], [[What is the difference between MongoRepository and MongoTemplate]], and [[How do you use multi-document transactions in Spring Data MongoDB]].
