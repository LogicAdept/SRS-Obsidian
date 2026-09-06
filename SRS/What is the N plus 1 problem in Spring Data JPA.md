<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/Hibernate/Fetching #SRS

# What is the N plus 1 problem in Spring Data JPA?

> [!abstract] Short answer
> **N+1** means **one query** loads N parents, then **N more queries** load each lazy association when you touch it (or when serialization / OSIV does). Common with Spring Data `findAll` + lazy `@OneToMany` / `@ManyToOne`. Fix by **fetching what you need in fewer round-trips** (JOIN FETCH, `@EntityGraph`, batch size, DTO projection) — not by flipping everything to `EAGER`.

## How it shows up

```text
SELECT * FROM orders;                    -- 1
SELECT * FROM lines WHERE order_id = ?;  -- × N
```

Hibernate docs call select-style fetching for associations the classic **N+1** pattern: a secondary `SELECT` per association access. Symptoms: slow endpoint, logs full of nearly identical SELECTs, worse under Open EntityManager in View when Jackson walks getters after the service method returns.

```d2
direction: right
q1: "1 query\nparents" {
  style.fill: "#e3f2fd"
}
loop: "for each parent\ntouch lazy assoc" {
  style.fill: "#fff3e0"
}
qn: "N queries\nchildren" {
  style.fill: "#fce4ec"
}

q1 -> loop -> qn
```

**Fig. 1.** One list load plus one query per parent association access.

## Remedies (prefer in this order of intent)

| Approach | Effect |
| --- | --- |
| **`JOIN FETCH` / Criteria fetch** | Load association in the **same** query |
| **`@EntityGraph`** | Fetch/load graph on repository methods without stuffing every JPQL string |
| **DTO / interface projection** | Select only needed columns; often **no** lazy graph at all |
| **`@BatchSize` / batch fetching** | Still extra selects, but **batched** `IN (…)`, not one-per-parent |
| **Keep associations `LAZY`** | Hibernate recommends lazy by default; fetch **per use case** |

Global `FetchType.EAGER` on collections often **moves** N+1 (or cartesian products) rather than removing the design problem — Hibernate notes eager associations omitted from a JPQL query can still cause secondary selects.

```java
@EntityGraph(attributePaths = "lines")
List<Order> findByCustomerId(Long customerId);
```

**Listing 1.** Ad-hoc entity graph on a derived finder (Spring Data JPA) to pull `lines` with the orders.

> [!warning] Controllers + OSIV amplify N+1
> Returning entities and letting Jackson + Open EntityManager in View initialize lazies turns every JSON field walk into potential extra SQL. Map to DTOs inside the transaction instead.

> [!tip] Interview answer
> N+1 is one query for N parents plus N lazy-load queries. I fix it with JOIN FETCH or `@EntityGraph` for that use case, or a DTO projection so I never touch the lazy graph. `@BatchSize` softens it; blanket `EAGER` is usually the wrong default.

See [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], [[Should you return JPA entities from a Spring controller]], [[What are Spring Data JPA projections]], and [[What is Open Session In View in Spring]].
