<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS

# How do you perform aggregation with Spring Data MongoDB?

> [!abstract] Short answer
> Build a pipeline with `Aggregation.newAggregation(…)` (stages such as `match`, `group`, `sort`, `lookup`), then run **`mongoTemplate.aggregate(agg, collection, OutputType.class)`** and read `getMappedResults()`. This is the aggregation framework API — not a derived repository finder.

## Pipeline in Java, execute with `MongoTemplate`

Spring Data MongoDB wraps MongoDB’s aggregation pipeline in typed **`AggregationOperation`** stages instead of hand-written BSON arrays.

```java
import static org.springframework.data.mongodb.core.aggregation.Aggregation.*;

Aggregation agg = newAggregation(
    match(Criteria.where("status").is("completed")),
    group("customerId").sum("amount").as("total"),
    sort(Sort.Direction.DESC, "total"));

AggregationResults<OrderTotal> results =
    mongoTemplate.aggregate(agg, "orders", OrderTotal.class);

List<OrderTotal> totals = results.getMappedResults();
```

**Listing 1.** Fluent stage chain + `MongoTemplate.aggregate` (Spring Data MongoDB aggregation reference).

Pass the **collection name** explicitly, or supply an input domain class to `newAggregation(Class, …)` / overloads so `MongoTemplate` derives the collection from `@Document`. If both class and collection name are given, the **explicit collection wins**. Map output to a dedicated DTO (`OrderTotal`) or to `Document` when fields are ad hoc.

```d2
direction: right
stages: "match → group → sort\n→ lookup …" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
agg: "Aggregation\nnewAggregation(…)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
tmpl: "mongoTemplate.aggregate" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
out: "AggregationResults\n→ mapped DTOs" {
  width: 240
  height: 70
  style.fill: "#f3e5f5"
}

stages -> agg -> tmpl -> out
```

**Fig. 1.** Java stages compile to a MongoDB pipeline; the template runs `aggregate` and maps BSON to your output type.

Use **`aggregateStream`** when you want cursor-backed streaming instead of loading all results into memory. Complex pipelines may still use raw `Aggregation.stage(String json)` or BSON `Document` stages when the fluent helpers do not expose a operator.

> [!warning] Not a derived query method
> `findByStatus` cannot express `$group` / `$lookup`. Aggregation belongs on `MongoTemplate` (or a custom repository fragment), not on a declarative `MongoRepository` method name alone.

See [[What is MongoTemplate]], [[How do you map a Java class to a MongoDB document in Spring Data]], and [[How do you build a dynamic Mongo query with Criteria]].

> [!tip] Interview answer
> I chain stages with `Aggregation.newAggregation` — `match`, `group`, `sort`, `lookup` — and execute with `mongoTemplate.aggregate(pipeline, "orders", MyResult.class)`. The output type can be a POJO or `Document`. It is pipeline work on the template, not a derived finder.
