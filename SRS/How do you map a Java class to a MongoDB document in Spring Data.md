<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Annotations #SRS

# How do you map a Java class to a MongoDB document in Spring Data?

> [!abstract] Short answer
> Mark the class with `@Document` (optional `collection` name), put `@Id` on the primary key field mapped to MongoDB `_id`, and use `@Field` when the BSON property name differs from the Java field. This is Spring Data MongoDB mapping — not JPA `@Entity` / `@Column`.

## Core mapping annotations

`MappingMongoConverter` turns POJOs into BSON documents. Without `@Document`, mapping still works on first save, but classpath scanning cannot pre-build metadata (small first-save cost).

```java
@Document(collection = "users")
public class User {

  @Id
  private String id;

  @Indexed(unique = true)
  @Field("email_address")
  private String email;

  private int age;
}
```

**Listing 1.** Collection name, `_id` mapping, custom field name, and index metadata (Spring Data MongoDB object mapping).

Default collection name: **simple class name with lowercase first letter** (`User` → `users` is wrong in docs - it's `user` not `users`. The dump used "users" as explicit collection which is fine. Docs say `com.test.Person` → `person` collection.

For `_id`: `@Id` on a property; if absent, driver may assign `ObjectId`. Use `@MongoId` when you need explicit control over id conversion types.

```d2
direction: right
java: "Java class\n@Document @Id @Field" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
conv: "MappingMongoConverter" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
bson: "MongoDB document\ncollection + _id + fields" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

java -> conv -> bson
```

**Fig. 1.** Annotations drive metadata; the converter maps nested objects inline (not DBRef by default).

## Indexes and production notes

`@Indexed` and `@CompoundIndex` declare index definitions on the type. **Automatic index creation is disabled by default** — enable it explicitly in configuration if you want startup `createIndex` calls; many teams manage indexes with migrations instead.

Nested objects embed as subdocuments. `@Document` also supports SpEL in `collection` for per-tenant collection names. Persist via `MongoRepository.save` or `MongoTemplate.save`.

> [!warning] Not JPA semantics
> Do not mix `@Entity` / `@Column` expecting MongoDB storage. `@Field("email_address")` sets the BSON key; without it, the converter typically uses the Java property name. Relying on auto-created indexes in production without reviewing `IndexCreation` settings can surprise you at deploy time.

See [[What is MongoRepository]], [[What is MongoTemplate]], and [[How do you build a dynamic Mongo query with Criteria]].

> [!tip] Interview answer
> I map a Java type with `@Document` and `@Id` for `_id`, optionally `@Field` for BSON names. Default collection is the decapitalized class name unless I set `collection`. Index hints use `@Indexed` / `@CompoundIndex`, but auto index creation is off by default — I enable or manage indexes deliberately.
