<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS

# How do you build a dynamic Mongo query with Criteria?

> [!abstract] Short answer
> Add only the `Criteria` clauses your runtime filters need, combine them (typically with `$and`), wrap them in a `Query`, optionally attach `Pageable` and field projection, then run `mongoTemplate.find`. Use this when the predicate shape is not fixed at compile time.

## Build predicates at runtime

Spring Data MongoDB’s `Criteria` mirrors MongoDB operators (`is`, `gte`, `in`, …). `Query` holds criteria, sort, skip/limit, and projection. For optional filters, collect non-null conditions and AND them together instead of declaring dozens of derived repository method names.

```java
import static org.springframework.data.mongodb.core.query.Criteria.where;

List<Criteria> parts = new ArrayList<>();
if (filter.category() != null) {
  parts.add(where("category").is(filter.category()));
}
if (filter.status() != null) {
  parts.add(where("status").is(filter.status()));
}
if (filter.minPrice() != null) {
  parts.add(where("price").gte(filter.minPrice()));
}

Query query = parts.isEmpty()
    ? new Query()
    : new Query(new Criteria().andOperator(parts.toArray(Criteria[]::new)));

query.with(pageable);
query.fields().include("skuCode", "price", "status");

List<Product> rows = mongoTemplate.find(query, Product.class);
```

**Listing 1.** Optional filters → `$and` criteria → paginated, projected `find` (Spring Data MongoDB `Query` / `Criteria` API).

You can also chain `query.addCriteria(where(...))` for each present filter. Field names in criteria map through the domain model (`@Field`, nested paths like `address.city`). For static JSON-shaped queries, `BasicQuery` accepts a BSON string.

```d2
direction: right
filters: "Runtime filter DTO\n(nullable fields)" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
crit: "Criteria list\nwhere(...).is/gte/…" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
query: "Query\nwith(Pageable)\nfields().include(...)" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
find: "mongoTemplate.find\nor count for Page total" {
  width: 260
  height: 80
  style.fill: "#f3e5f5"
}

filters -> crit -> query -> find
```

**Fig. 1.** Dynamic search: only non-null filters become criteria; `Query` carries paging and projection into `MongoTemplate`.

## Pagination and pitfalls

`Query.with(Pageable)` applies sort, skip, and limit. Building a `Page` manually usually means **`find` plus `count` with the same criteria** (two round trips). Official `MongoTemplate.count` docs note that query offset/limit can affect the count result — use an unpaged query clone when you need the full match total.

Derived `MongoRepository` method names cannot express “include this clause only when the caller sent a value”; that is why teams reach for [[What is MongoTemplate]] or [[How do you write custom queries with Query and MongoTemplate]]. For the JPA-side analogue, see [[How do you handle dynamic queries in Spring Data JPA]].

> [!warning] Empty criteria means match all
> An empty `Query()` has no filter — it scans the collection (subject to paging). Guard “no filters provided” in the service layer if that is invalid. Projection `include`/`exclude` rules still apply: `_id` stays unless explicitly excluded.

> [!tip] Interview answer
> I build dynamic Mongo searches by accumulating `Criteria` for each optional filter, AND-ing them into a `Query`, adding `Pageable` and field includes, and calling `mongoTemplate.find`. Derived repository names cannot branch on which filters were passed; for a full `Page` I also run `count` with the same criteria.
