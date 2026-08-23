<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS

# Why is PostFilter a performance trap?

> [!abstract] Short answer
> **`@PostFilter` runs the method first**, then removes return-value elements in memory. A repository call still **loads the full collection from the database**; forbidden rows are dropped only **after** fetch and method work — wasted I/O, memory, and CPU on large result sets.

## Execute first, filter second

Method-security docs describe **`@PostFilter`** as filtering **from the return value** after invocation: each element is tested as **`filterObject`** in SpEL, and failing entries are removed from the collection returned to the caller.

That ordering means:

1. The **entire method body runs** (including **`findAll()`**, **`SELECT *`**, aggregation, mapping).
2. The **AOP interceptor** walks the returned collection/array/map/stream and drops unauthorized elements.

Unauthorized rows you never return were still **loaded and processed**.

```java
@PostFilter("filterObject.owner == authentication.name")
public Collection<Account> readAccounts(String... ids) {
    return accountRepository.findByIdIn(ids); // full result set fetched first
}
```

**Listing 1.** Official pattern — filtering happens on the returned collection, not in the SQL.

```d2
direction: right
call: "Method runs\n(DB loads all rows)" {
  width: 220
  height: 70
  style.fill: "#fce4ec"
}
post: "@PostFilter\nin-memory drop" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
client: "Smaller collection\nto caller" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}

call -> post -> client
```

**Fig. 1.** Database cost is paid before security trimming.

## Safer alternatives for large lists

| Approach | When |
|---|---|
| **`@PreAuthorize`** on a narrow query method | Block unauthorized calls before work |
| **`@PreFilter`** | Shrink **input** collections before the method body (updates/batch args) |
| **Query-level predicate** | Push **`owner = ?`** (or SpEL via **`SecurityEvaluationContextExtension`**) into JPA/Criteria/SQL so the DB never returns forbidden rows |
| **`@PostAuthorize`** on single-object reads | One row — post-check cost is bounded |

**`@PostAuthorize`** on a write method is already discouraged when DB mutations happen before the check. **`@PostFilter`** on a wide read has the same **“work first, authorize trim second”** cost profile at scale.

> [!warning] One forbidden row still costs a full scan
> Even if **one** element fails **`filterObject`**, you may have loaded **thousands** from the database. Logs look like “security works” while latency and connection pool pressure grow. Prefer **`WHERE`** clauses tied to **`authentication.name`** (or ACL/`hasPermission` with a selective query) for list endpoints. See [[What is the difference between returnObject and filterObject]] and [[What is SecurityEvaluationContextExtension]].

> [!tip] Interview answer
> @PostFilter executes the method and hits the database for the full result set, then filters in memory. It is fine for small collections but a performance trap on large lists — use query-level authorization or @PreAuthorize instead of post-hoc collection trimming.
