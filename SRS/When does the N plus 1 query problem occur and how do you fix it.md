<!--
reps: 0
priority: 0
-->
#ORM #Problems/Persistence #Java/Persistence #SRS

# When does the N plus 1 query problem occur and how do you fix it

> [!abstract] Short answer
> **N+1 happens when you run 1 query to fetch a list of N rows and then issue one additional query per row — usually because lazy associations get loaded inside a loop.** It shows up with ORMs (Hibernate navigation triggers per-row SELECTs) but any hand-rolled loop over rows does the same. Fixes: `JOIN FETCH` or an entity graph to load the association in one round trip, batch fetching as a middle ground, and (for reads) DTO projections that select exactly the columns needed.

## The shape of the problem

The cost is not just N+1 round trips — it is N+1 *network round trips plus N prepared-statement executions*, which turns linear into terrible as N grows.

```d2
direction: right
q1: "1 query\nselect all authors" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
loop: "for each author:\nselect books where author_id = ?" {
  width: 320
  height: 100
  style.fill: "#ffebee"
}
sum: "Total: 1 + N queries\nN = number of authors" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
fix: "JOIN FETCH / @EntityGraph\nselect authors join books" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
one: "Total: 1 query" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
q1 -> loop -> sum
loop -> fix -> one
```

**Fig. 1.** The loop multiplies round trips; a single joined query collapses them.

A real run of the shape — the loop below is exactly what lazy ORM navigation executes behind the scenes:

```java
// H2 in-memory DB, 2 authors, 3 books
ResultSet rs = st.executeQuery("select id, name from authors");   // the "1"
queries++;
while (rs.next()) {
    int id = rs.getInt(1);
    PreparedStatement ps = cn.prepareStatement(
        "select title from books where author_id = ?");
    ps.setInt(1, id);
    ResultSet brs = ps.executeQuery();    // the "+1" per row
    queries++;
    while (brs.next()) brs.getString(1);
    ps.close();
}
System.out.println("queries after loop: " + queries + " total");
```

**Listing 1.** Verified on JDK 21 with H2:

```java
queries so far: 1          // the JOIN version returned all rows in this one query
queries after loop: 4 total (2 setup + 1 per author)
```

**Listing 2.** Two authors already doubled the query count; in production N is a page size of 50, 100, 500 — each row pays a round trip.

In Hibernate terms the trigger is navigation: `for (Author a : authors) a.getBooks()` fires a SELECT per author because `@OneToMany` defaults to lazy. The same shape appears without any ORM: a repository method returning IDs followed by a `findById` per element.

> [!warning] The page renders fine in dev — then the data grows
> Why it survives code review: with 5 test authors the loop costs 6 queries and nobody notices; the explosion arrives with production data and is reported as "the API got slow" rather than a bug. Two subtleties people miss. First, `JOIN FETCH` on a `@OneToMany` multiplies rows and can silently cap results — a paginated query with a fetch join throws or truncates because the database can't page a cartesian product correctly; the right tool for paged collections is `@EntityGraph` with fetch-size/batching (`@BatchSize(size=...)`) or `hibernate.default_batch_fetch_size` which turns N selects into N/size `IN (...)` queries. Second, DTO projections (`select new AuthorSummary(...)`) are not a workaround hack — they are the correct design when you never intend to modify entities, because they skip persistence-context bookkeeping entirely. Detection: Hibernate statistics, datasource-proxy, or logging `org.hibernate.SQL` plus a warning on duplicate statements — the query count is the signal, as the demo shows. Related: [[Which ways can Java applications talk to a database]], [[What is object relational mapping ORM]], [[How do you define a native query in Spring Data JPA]].

> [!tip] Interview answer
> **N+1: one query for the list, then one extra query per row — classic cause is lazy-loading an association while iterating. Real fix: load it in one round trip with JOIN FETCH or an entity graph; batch fetching turns N selects into IN-clause batches; DTO projections drop the entity machinery for read paths. Detect it by counting SQL statements in tests or with a proxy — the page that works with 5 rows dies with 500.**

