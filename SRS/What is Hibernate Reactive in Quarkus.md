<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is Hibernate Reactive in Quarkus?

> [!abstract] Short answer
> `quarkus-hibernate-reactive` is Hibernate ORM over **non-blocking Vert.x SQL clients** instead of JDBC: the same mappings and query language, but every operation returns `Uni`/`Multi` and no thread is held while the database works. It pairs with the reactive datasource (`quarkus.datasource.reactive.*`), Panache's reactive variants (`PanacheReactiveEntity`/repositories returning `Uni`/`Multi`), and session/transaction handling via `@WithSession`/`@WithTransaction` — not the JTA `@Transactional` thread-bound model.

## What changes and what does not

The persistence model stays Hibernate: entities, JPQL/HQL, caching, lifecycle callbacks. What changes is the data access layer — "JDBC" is replaced by Vert.x reactive clients (PostgreSQL, MariaDB/MySQL, SQL Server, Oracle), so a query hands the event loop a callback and returns immediately, keeping the IO thread free ([[How does Quarkus decide which thread runs your code]]). Operations run on Vert.x contexts; sessions are bound to that context rather than to a thread's transaction. Blocking Hibernate and reactive Hibernate against the same database are separate stacks: enable/disable explicitly with `quarkus.hibernate-orm.jdbc.enabled=false` when only the reactive ORM should exist, and remember the reactive pool (`quarkus.datasource.reactive.max-size`) is not Agroal ([[Which connection pool does Quarkus use]]).

```java
// Shape of the reactive API (illustrative for the mechanism; runs against a reactive
// datasource with quarkus-hibernate-reactive + hibernate-reactive-panache on the classpath).
package demo;

import io.quarkus.hibernate.reactive.panache.Panache;
import io.quarkus.hibernate.reactive.panache.PanacheEntity;
import io.smallrye.mutiny.Uni;
import jakarta.persistence.Entity;

@Entity
public class Widget extends PanacheEntity {
    public String sku;
}

class WidgetService {
    Uni<Widget> load(long id) {
        return Panache.withTransaction(() ->
                Widget.<Widget>findById(id)            // Uni<Widget>, no thread blocked
                      .onItem().ifNull().failWith(() -> new IllegalStateException("missing")));
    }
}
// Contrast with the blocking side: the same method on Hibernate ORM returns Widget and
// holds a worker thread + Agroal connection for the duration of the query. Here the
// event loop continues serving other requests between the request and the row arriving.
```

**Listing 1.** The reactive shape: a transaction scoped as a `Uni` pipeline, an `findById` returning `Uni`, failure as an event in the chain ([[What is Mutiny in Quarkus]]). The verified blocking equivalent of the same flow — `Person.findById` inside `@Transactional` — is what makes the thread-holding difference concrete ([[What is Panache in Quarkus]]).

```d2
direction: right
blk: "Hibernate ORM (blocking)\nJDBC + Agroal pool\nworker thread held" {
  width: 320
  height: 75
  style.fill: "#fff3e0"
}
rea: "Hibernate Reactive\nVert.x SQL client\nreactive pool" {
  width: 300
  height: 75
  style.fill: "#e3f2fd"
}
w: "Worker thread pool\n@Blocking / plain endpoints" {
  width: 260
  height: 60
}
e: "Event loop\nUni/Multi endpoints" {
  width: 230
  height: 60
}
db: "Database" {
  width: 140
  height: 45
}
w -> blk -> db
e -> rea -> db
```

**Fig. 1.** Two complete, parallel stacks to one database: pick the row that matches your thread model — mixing them in one service is the design smell ([[How do transactions work in Quarkus]]).

## Where reactive pays, and the costs

Benefits concentrate at high connection counts with few threads: an event loop model scales to many concurrent queries without a matching worker-thread pool or JDBC pool, and memory per idle request is small. Costs: the whole call chain must stay non-blocking (no JDBC, no blocking HTTP inside), session semantics need `@WithSession` discipline, and combining pipelines can accidentally share one reactive transaction across parallel branches — a documented pitfall producing "unpredictable behavior" with `Uni.combine()`/`Uni.join()`.

> [!warning] @Transactional does not manage reactive transactions
> The JTA interceptor binds transactions to the calling thread; a reactive pipeline leaves that thread immediately, so the transaction would end before the database work completes. The reactive stack uses `@WithTransaction` (and `@WithSession`/`@WithSessionOnDemand`) — people porting services from blocking Hibernate keep `@Transactional` and discover writes vanish or sessions close mid-pipeline. The mirrored error: blocking calls (JDBC, `await().indefinitely()` on the event loop) inside a reactive chain stall the loop for everyone.

> [!tip] Interview answer
> Hibernate Reactive is the same Hibernate — mappings, HQL, caching — but its data access layer is Vert.x non-blocking SQL clients instead of JDBC, so every operation returns Uni or Multi and no thread waits on the database. In Quarkus it pairs with the reactive datasource and Panache's reactive variants, sessions live on Vert.x contexts, and transactions are @WithTransaction rather than the thread-bound JTA @Transactional. The rule I apply: one stack per service — blocking JDBC with Agroal, or reactive clients, not both.
