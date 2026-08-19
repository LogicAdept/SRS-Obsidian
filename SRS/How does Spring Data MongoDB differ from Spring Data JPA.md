<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Repository concepts stay the same; mapping and runtime differ because documents are not tables.

Annotations: JPA uses @Entity, @Table, @Column. MongoDB uses @Document, @Field, @Id.

Transactions: MongoDB multi-document transactions exist since v4.0 but are not enabled by default and are handled differently from JPA.

Schema: MongoDB is schema-less. Spring Data MongoDB maps Java objects to JSON/BSON.

Template: JPA leans on EntityManager. MongoDB uses MongoTemplate for lower-level work and aggregations.

Derived queries still look the same:

```java
public interface ProductMongoRepository extends MongoRepository<Product, String> {
    List<Product> findByPriceLessThan(Double price);
}
```
> [!warning] Unverified traps from the dump
> - Do not put @Entity on a Mongo document type in these dumps.
> - Id is typically String mapped to ObjectId, not a generated Long.
