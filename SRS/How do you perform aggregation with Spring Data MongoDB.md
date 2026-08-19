<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Build an Aggregation by chaining stages such as match, group, sort, and lookup, then run it with mongoTemplate.aggregate() and map to a target class. Dumps present this as a fluent Java API instead of raw pipeline JSON.

```java
Aggregation agg = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("status").is("completed")),
    Aggregation.group("customerId").sum("amount").as("total")
);
AggregationResults<Document> results = mongoTemplate.aggregate(agg, "orders", Document.class);
```
> [!warning] Unverified traps from the dump
> - Aggregation pipelines are a MongoTemplate job in these dumps, not a derived finder.
> - The output type can be Document or a dedicated result class.
