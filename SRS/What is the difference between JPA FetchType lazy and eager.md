<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Fetching #Java/Annotations #SRS

# What is the difference between JPA FetchType lazy and eager?

> [!abstract] Short answer
> **`FetchType.EAGER`** is a **requirement**: when the entity is loaded, that attribute **must** be loaded too. **`FetchType.LAZY`** is a **hint**: load it **when first accessed** — the provider is **allowed** to fetch it immediately anyway. Defaults: **`@OneToMany` / `@ManyToMany` → LAZY**; **`@ManyToOne` / `@OneToOne` (and `@Basic`) → EAGER**. Catalog of association fetch: [[What are JPA fetch types for entity associations]]. Lazy mechanics: [[What is lazy fetch in JPA or Hibernate]].

## Requirement versus hint

Jakarta Persistence defines `enum FetchType { LAZY, EAGER }`. The same `fetch` element appears on `@OneToOne`, `@OneToMany`, `@ManyToOne`, `@ManyToMany`, `@Basic`, and `@ElementCollection`.

- **EAGER** — the persistence provider **must** eagerly fetch that data when the owning entity is loaded. The default fetch graph is the **transitive closure** of every `FetchType.EAGER` attribute (explicit or defaulted). An entity is “loaded” only when all EAGER attributes are loaded.
- **LAZY** — a hint that data **should** be fetched on **first access**. The implementation **may still fetch it eagerly**. After the persistence context closes, uninitialized lazy state is not safely usable: [[What is LazyInitializationException]], [[What are the drawbacks of lazy loading]].

EAGER does **not** mean “one big SELECT.” The provider may use extra queries. LAZY does **not** mean “never a join.” A query `join fetch`, an entity graph, or the provider’s own plan can load a LAZY association immediately.

```d2
direction: right
eager: "EAGER\nmust load with the entity" {
  width: 240
  height: 50
  style.fill: "#ffe0b2"
}
lazy: "LAZY\nhint: load on first access" {
  width: 250
  height: 50
  style.fill: "#e3f2fd"
}
eager -> lazy: "not opposites in SQL"
```

**Fig. 1.** EAGER is mandatory inclusion in the default fetch graph. LAZY is a delay hint, not a ban on eager SQL.

```java
@ManyToOne                          // default EAGER — loaded with Employee
Department department;

@OneToMany(mappedBy = "department") // default LAZY — collection may wait
List<Employee> employees;
```

**Listing 1.** Conceptual. To-one defaults EAGER; collections default LAZY. Override `fetch` only when the default is wrong for **every** use of the entity.

> [!warning] EAGER is not “N+1”; walking LAZY collections is
> Default **EAGER** on `@ManyToOne` / `@OneToOne` over-fetches (and can explode via the default fetch graph). **N+1 selects** usually come from iterating parents and touching a **LAZY** collection each time. Fix query-specific needs with **`join fetch`** or an **entity graph**, not by marking every association EAGER.

> [!warning] “Always LAZY” does not override the spec defaults
> If you omit `fetch`, to-one associations are still **EAGER**. Saying “we use lazy loading” without setting `FetchType.LAZY` on `@ManyToOne` / `@OneToOne` is false for those mappings.

> [!tip] Interview answer
> EAGER means the provider must load that association when it loads the entity. LAZY is only a hint to load on first access, and the provider may ignore it. Collections default to LAZY, many-to-one and one-to-one default to EAGER. Prefer LAZY mappings and fetch what a use case needs in the query, instead of making associations EAGER globally.
