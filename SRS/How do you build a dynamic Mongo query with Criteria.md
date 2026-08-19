<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

For optional filters, dumps build a list of Criteria, combine them, wrap in Query (optionally with Pageable and field includes), then mongoTemplate.find.

```java
List<Criteria> and = new ArrayList<>();
if (f.category() != null) and.add(Criteria.where("category").is(f.category()));
if (f.status() != null) and.add(Criteria.where("status").is(f.status()));
if (f.minPrice() != null) and.add(Criteria.where("price").gte(f.minPrice()));
Query query = new Query(criteria).with(pageable);
query.fields().include("skuCode").include("price").include("status");
List<Product> rows = mongoTemplate.find(query, Product.class);
```

Use this when the predicate set is known only at runtime.
> [!warning] Unverified traps from the dump
> - Derived method names cannot branch on which filters were passed.
> - Count and find are often two template calls when you build a Page by hand.
