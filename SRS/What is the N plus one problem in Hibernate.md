<!--
reps: 0
priority: 0
-->
#Problems/Persistence #Java/Persistence/Hibernate/Fetching #SRS

# What is the N plus one problem in Hibernate?

> [!abstract] Short answer
> The **N+1 problem** is Hibernate’s **select-fetch** strategy: **1** SQL statement loads **N** parents, then **one extra `SELECT` per parent** loads a lazy (or un-fetched eager) association — **N+1** round-trips. Fetching chapter: a **separate select per association** “is generally termed N+1.” Classic loop: `for (Order o : orders) o.getLines().size()`. HQL without **`join fetch`** hits the same “n+1 selects” problem. **`EAGER` does not save you** on a query: omitted eager associations still get **one secondary select each**. Fix the **use case** with **`JOIN FETCH`**, an entity graph, or a **DTO** — not by mapping everything eager (and two collections at once add [[What is MultipleBagFetchException and how do you fetch two collections|a bag-fetch constraint]]).

## One list, then N selects

Load 10 `Department`s, then touch `department.getEmployees()` on each. Default **`FetchMode.SELECT` / lazy proxy**: **1** query for departments + **10** for collections = **11**. `@BatchSize` collapses those 10 into a few `IN (…)` selects — **better than N+1**, still **worse than one `JOIN FETCH` or DTO** (Fetching chapter). **`@Fetch(SUBSELECT)`** reruns the owner query as a subselect to fill **all** collections of that role in the persistence context.

The same pattern is a **lazy `@ManyToOne`**: 1 query for cats, then **N** queries for `getOwner()`. It is [[What is lazy fetch in JPA or Hibernate]] **working as designed** — delayed select — until you **loop**.

**`find` + `EAGER` to-one** often **joins**. A **JPQL/HQL query** that does **not** `JOIN FETCH` that same association still emits a **secondary select per row** so EAGER is honored **before** the result is returned. Forget that for a list of 50 employees → **51** statements. Prefer mapping associations **`LAZY`** and fetching **per query**.

```d2
direction: down
q1: "SELECT departments\n(1 query)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
loop: "for each department\ngetEmployees()" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
qn: "N × SELECT employees" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}

q1 -> loop -> qn
```

**Fig. 1.** N+1 is select-per-association, not “Hibernate is slow.”

## Kill it for this transaction

HQL **`join fetch` / `left join fetch`** loads the association **in the same SQL join** and **overrides laziness**. Inner fetch **drops** roots with no association; **left** keeps them. Safe: several **to-ones** in one query, or **one nested collection** chain. **Two collections in parallel** → **cartesian product** of rows. Do **not** `WHERE`-filter a fetched collection (it would look **incomplete** in memory). Fetch joins are **illegal in subqueries**. Hibernate **6+** **deduplicates** join-fetch duplicate roots **in memory** — do **not** use `distinct` for that.

Also: entity graphs ([[What is JOIN FETCH and EntityGraph in Spring Data JPA]]), `Hibernate.initialize` **inside** the session (still N+1 if you initialize in a loop), `default_batch_fetch_size` / `@BatchSize`. Measure with **`Statistics.getEntityFetchCount()` / collection fetch** ([[What is Hibernate performance tuning]]).

```java
List<Book> books = session.createSelectionQuery(
    "select b from Book b left join fetch b.publisher",
    Book.class)
    .getResultList();
// books.get(i).getPublisher() does not fire N extra SELECTs
```

**Listing 1.** Conceptual: one query, publisher initialized. A second `join fetch` of a **collection** in the same query is the cartesian trap.

> [!warning] EAGER is a hidden N+1 on lists
> Mapping `@ManyToOne(EAGER)` “so I never see LazyInitializationException” still **selects per row** for queries without `JOIN FETCH`. Two `join fetch` collections multiply rows. `@BatchSize` **masks** the smell; it does not make a 1-query graph. Pagination (`setFirstResult`/`setMaxResults`) **plus collection fetch join** is a **row-vs-entity** mismatch — don’t page that query.

> [!tip] Interview answer
> N+1 means one query for N parents plus one select per parent for an association, usually lazy collections or to-ones in a loop. Eager mapping does not fix list queries; Hibernate still issues secondary selects unless I JOIN FETCH. I keep associations LAZY, fetch the graph this use case needs in one query or a DTO, and use @BatchSize only as a safety net. Two collection fetch joins in one query are a cartesian product, not a solution.

See [[What is lazy fetch in JPA or Hibernate]], [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], [[What is Hibernate performance tuning]], [[What is LazyInitializationException]], [[What is the N plus 1 problem in Spring Data JPA]], and [[What are Hibernate first and second level cache tiers]].
