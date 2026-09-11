<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the N plus 1 problem in SQL?

> [!abstract] Short answer
> The **N+1 problem** is an application-side pattern: one query fetches a list of N entities, then the code issues one additional query *per entity* to load its related data — N+1 round trips where one joined or batched query would do. It is the client-side twin of a correlated subquery: correct results, cost proportional to N.

The SQL side already showed the shape — a correlated subquery is the engine looping over the outer rows ([[What is a correlated subquery and why can it be slow]]); N+1 is the same loop performed over the network by application code, which is strictly worse because every iteration also pays latency and connection-pool overhead. ORMs make it endemic: Hibernate emits one SELECT per lazily-accessed association unless fetching is configured (JOIN FETCH, entity graphs, batch size) — the Spring Data JPA reference documents exactly these fetch-declaration options for query methods. The verified demo reproduces the arithmetic outside any ORM: iterating six customer ids issues six per-row lookups (the "1" list plus "+N" probes) versus one joined fetch; the statement counters show 6 versus 1 for the same 8 rows. Detection: per-request SQL counts and logs (an interceptor in Spring, `count` in Hibernate statistics), latency that scales with list size, and plans full of near-identical single-row probes. Fixes, in order: JOIN FETCH or entity-graph fetch for associations you always need; `IN`-batch loading for optional ones; caching only after batching fails to cut the count.

```java
import java.util.List;
import java.util.HashMap;
import java.util.Map;

/** Verified on JDK 21: statement counts for per-row vs joined access. */
public class NPlusOneDemo {
    static int statements = 0;
    static List<String> findOrdersByCustomer(int customerId) {
        statements++;                       // one SELECT per customer: the "+N"
        if (customerId == 1) return List.of("o101", "o102");
        if (customerId == 2) return List.of("o103");
        if (customerId == 3) return List.of("o104", "o105", "o108");
        if (customerId == 5) return List.of("o109", "o110");
        return List.of();
    }
    static Map<Integer, List<String>> findAllOrdersJoined() {
        statements++;                       // one JOIN query: the "1"
        Map<Integer, List<String>> m = new HashMap<>();
        m.put(1, List.of("o101", "o102"));
        m.put(2, List.of("o103"));
        m.put(3, List.of("o104", "o105", "o108"));
        m.put(5, List.of("o109", "o110"));
        return m;
    }
    public static void main(String[] args) {
        List<Integer> customerIds = List.of(1, 2, 3, 4, 5, 6);
        statements = 0;
        int rows = 0;
        for (int id : customerIds) rows += findOrdersByCustomer(id).size();
        System.out.println("N+1: statements=" + statements + " rows=" + rows);
        statements = 0;
        Map<Integer, List<String>> joined = findAllOrdersJoined();
        int joinedRows = joined.values().stream().mapToInt(List::size).sum();
        System.out.println("join: statements=" + statements + " rows=" + joinedRows);
    }
}
// Output (JDK 21):
// N+1: statements=6 rows=8
// join: statements=1 rows=8
```

**Listing 1.** Verified on JDK 21. Same eight order rows: the per-customer loop issues six statements (one per id, plus the initial list), the joined fetch issues one. Multiply the loop length by pool latency to see the production impact.

```d2
direction: right
a: "1 query
list of N entities" {width: 190; height: 70}
b: "N queries
one per entity" {width: 170; height: 70}
c: "N+1 round trips
latency x N" {width: 190; height: 70}
d: "1 JOIN query
same rows, one trip" {width: 200; height: 70}
a -> b -> c
a -> d
```

**Fig. 1.** Two access plans for the same data: the loop path costs one trip per entity; the join path collapses the whole pattern into a single statement.

> [!warning] ORMs hide the loop — profiling must count statements, not lines
> Lazy associations make N+1 appear without any visible loop in the developer's code: the "loop" is property access spread across view rendering. The reliable detector is a statement counter per request (Hibernate statistics, datasource proxy); by the time page latency shows it, the query log already contains N near-identical SELECTs ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> N+1 is fetching a list with one query and then issuing one query per list item for its relations — N+1 round trips for data one join would return. It is the application-side analog of a correlated subquery, and ORMs produce it silently through lazy loading. I detect it with per-request SQL counts rather than eyeballing code, fix associations that are always needed with JOIN FETCH or entity graphs, batch the optional ones with IN loading, and keep caching as the last resort.
