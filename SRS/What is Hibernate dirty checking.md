<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Session #SRS

# What is Hibernate dirty checking?

> [!abstract] Short answer
> **Dirty checking** is Hibernate’s automatic detection that a **managed** entity’s state no longer matches the database snapshot. You **mutate fields**; you do **not** call `update`/`save`. At **flush**, Hibernate schedules an **`UPDATE`** (`EntityUpdateAction`) for each dirty instance. Default algorithm: keep the **last known DB state**, then **diff every managed entity** at flush (catches in-place `Date` mutation). Bytecode enhancement can make the entity **track dirty attributes** instead. SQL is **write-behind** — often **not** run at the setter. **`StatelessSession` has no dirty checking.**

## Managed state, then flush

Only **persistent/managed** instances in the **persistence context (L1)** are dirty-checked. Transient objects need `persist`; detached ones need `merge` (or a new load). There is **no** extra “make this change persistent” API for a managed entity.

Flush **synchronizes** the context with the database: queued state changes become `INSERT` / `UPDATE` / `DELETE`. Default **`FlushMode.AUTO`**: flush **before commit**, and before an HQL/JPQL query that **overlaps** pending actions. `COMMIT` delays until commit (query overlap is unspecified in JPA). `MANUAL` waits for `session.flush()`. Hibernate also has **`ALWAYS`**. `IDENTITY` ids still insert **on `persist`**, not at commit.

```java
Person p = session.find(Person.class, id);
p.setName("John Doe");   // no session.update
session.flush();         // or commit — then UPDATE
```

**Listing 1.** Conceptual: a setter on a managed instance is enough; flush emits SQL.

Default **`UPDATE` lists every column except the id**, even if you changed one field. That keeps a stable prepared statement (and version/optimistic-lock columns in the mix). Downside: unused indexes may still be touched. **`@DynamicUpdate`**: generate SQL with **only columns being updated** — fewer columns, **runtime SQL generation** cost.

```d2
direction: right
set: "Setter on\nmanaged entity" {
  width: 180
  height: 90
  style.fill: "#e3f2fd"
}
snap: "Snapshot vs current\n(or enhanced flags)" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
flush: "Flush\nEntityUpdateAction" {
  width: 200
  height: 90
  style.fill: "#e8f5e9"
}
sql: "JDBC UPDATE" {
  width: 160
  height: 80
  style.fill: "#f3e5f5"
}

set -> snap -> flush -> sql
```

**Fig. 1.** Dirty checking decides the `UPDATE`; flush (not the setter) runs it.

## How dirtiness is computed

| Mode | Mechanism |
| --- | --- |
| **Diff-based (default)** | Snapshot at load/write; at flush, compare **every** managed entity. Thorough for types that mutate internally (`java.util.Date`). Cost grows with **L1 size**. |
| **Bytecode in-line tracking** | Enhancement adds dirty flags on the class; flush **asks the entity** what changed. Faster on large contexts if you do not rely on silent internal mutation. |

Turn it **off** for an instance: **`session.setReadOnly(entity, true)`** — no snapshot, **not** dirty-checked, field mutations **not** persisted — or **`evict`/`detach`**. A read-only **session** / `FlushMode.MANUAL` avoids useless work on a read path.

**`StatelessSession`**: **no** persistence context, **no** write-behind, **no** automatic dirty checking. Changes are **`update(entity)`** (or insert/delete) **immediately**.

Flush **order** is the **`ActionQueue`**, not call order (inserts can run **before** deletes).

> [!warning] A setter is an UPDATE, even if you never “save”
> After `find`, `setEmail` inside `@Transactional` **will** flush an `UPDATE` on commit. Mutating a `java.util.Date` **in place** (`setTime`) is still dirty under snapshot comparison. A huge persistence context makes **every** flush walk **every** managed instance. `@DynamicUpdate` does not skip that walk; it only shrinks the SQL. Detached graphs and `StatelessSession` do **not** get this behavior — there is no snapshot.

> [!tip] Interview answer
> Dirty checking means Hibernate notices that a managed entity changed and issues UPDATE at flush, with no update() call. By default it diffs a snapshot of every entity in the persistence context, which is why a large Session is expensive. I use read-only or evict when I will not write, DynamicUpdate when I want fewer columns in the SQL, and StatelessSession when I want explicit, synchronous updates with no first-level cache.

See [[How does the Hibernate first-level cache work in Spring]], [[What are Hibernate first and second level cache tiers]], [[What is Hibernate entity lifecycle states]], and [[What is Hibernate as an ORM framework]].
