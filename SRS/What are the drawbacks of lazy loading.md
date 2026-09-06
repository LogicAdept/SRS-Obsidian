<!--
reps: 0
priority: 0
-->
#Persistence/ORM #Java/Persistence/JPA/Fetching #Java/Persistence/Hibernate #SRS

# What are the drawbacks of lazy loading?

> [!abstract] Short answer
> Lazy associations delay SQL until you navigate them. The costs: **unfetched state is not safely usable once the persistence context ends** (Hibernate throws **`LazyInitializationException`**), **N+1 selects** when you walk a list of parents, **`LAZY` is only a hint**, unfetched lazy fields are **ignored on `merge`**, and lazy graphs **do not serialize portably across vendors**. Fetch types: [[What are JPA fetch types for entity associations]].

## What you give up when fetch is delayed

JPA `FetchType.LAZY` means the provider *should* load data on first access. **EAGER** must load with the entity; **LAZY** may still be fetched immediately. After the persistence context closes, detached instances may only use non-LAZY attributes and state already accessed or loaded by an entity graph. Unfetched associations are not in that set. Hibernate implements the closed-session case as `LazyInitializationException`: an uninitialized proxy or collection was touched without an open stateful `Session`. `Session` docs: a proxy loads **if and only if** it is still associated with an open session. [[What is LazyInitializationException]]

A common SELECT fetch is one extra query per association when it is first touched. Hibernate calls that pattern **N+1**: one query for the roots, then one per lazy association you hit in a loop. HQL/JPQL **`join fetch`** (or an entity graph) is how you collapse that. Fetching **two collections** in parallel with fetch joins can explode into a Cartesian product.

```d2
direction: down
q1: "select o from Order o\n(1 query)" {
  width: 200
  height: 45
}
loop: "for each Order\norder.getLines()" {
  width: 200
  height: 45
}
n: "N more SELECTs" {
  width: 180
  height: 40
  style.fill: "#ffcdd2"
}
q1 -> loop -> n
```

**Fig. 1.** Lazy collections turn a list of parents into N+1 SQL unless you `join fetch` or batch.

```java
List<Order> orders = em.createQuery("select o from Order o", Order.class)
        .getResultList();
em.close();
int n = orders.get(0).getLines().size(); // Hibernate: LazyInitializationException
```

**Listing 1.** Conceptual. Same loop **inside** an open context is N+1 selects, not an exception.

`merge` must **ignore** LAZY fields that were never fetched, so a detached graph can silently drop association state. Serializing lazy entities and merging them in another vendor’s runtime is **not** required to interoperate; portable code that crosses vendors must not use lazy loading.

Keeping a `Session` open for the whole HTTP request only to dodge `LazyInitializationException` fights the rule that a session is **short-lived** and holds hard references. Initialize what the caller needs (`join fetch`, entity graph, or `Hibernate.initialize` while the session is open) instead.

> [!warning] Closed context, uninitialized proxy
> After `close` / `detach` / transaction-scoped commit, navigating a never-fetched lazy association is not portable. Hibernate’s answer is `LazyInitializationException`. Catching it in the UI is not a fetch strategy.

> [!warning] LAZY does not mean “no SQL now”
> The provider may eager-load a LAZY mapping. You still pay N+1 when it *does* delay and you iterate. Default `@ManyToOne` EAGER has the opposite problem (join bomb): [[What are JPA fetch types for entity associations]].

> [!tip] Interview answer
> Lazy loading postpones association SQL, so once the persistence context is gone those proxies are unusable — Hibernate throws LazyInitializationException. Walking a list of parents then hits N+1 queries unless you join fetch or use an entity graph. LAZY is only a hint, merge skips unfetched lazy fields, and lazy graphs are not portable across vendors when serialized.
