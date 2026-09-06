<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Fetching #Java/Persistence/Hibernate #SRS

# What is lazy fetch in JPA or Hibernate?

> [!abstract] Short answer
> **Lazy fetch** means associated state is **not required** when the entity is loaded; it **may** be loaded **on first access**. In JPA that is **`FetchType.LAZY`**: a **hint**, not a ban on eager SQL. Hibernate implements it with **uninitialized proxies/collections** that load only while they are associated with an **open `Session`**. Defaults: **`@OneToMany` / `@ManyToMany` LAZY**; **`@ManyToOne` / `@OneToOne` EAGER**. Catalog of types: [[What are JPA fetch types for entity associations]].

## Delay until navigation — if the provider honors the hint

`FetchType` has two values. **EAGER** is a requirement: that association must be fetched with the entity. **LAZY** tells the provider data **should** be fetched when first accessed; the implementation **may still fetch it eagerly**. After the persistence context ends, only non-LAZY attributes and already-accessed/graph-fetched state are safely available. Spec vs Hibernate APIs: [[What is the difference between JPA as a specification and Hibernate]].

Hibernate `Session`: an association not yet loaded is an **uninitialized proxy**. Invoking a method on it loads the row **if and only if** the proxy is tied to an open session. Otherwise Hibernate throws **`LazyInitializationException`**: [[What is LazyInitializationException]]. Drawbacks (N+1, detach, merge): [[What are the drawbacks of lazy loading]]. LAZY vs EAGER as a pair: [[What is the difference between JPA FetchType lazy and eager]].

```d2
direction: down
find: "em.find(Department)\ncollection not required" {
  width: 240
  height: 50
}
touch: "department.getEmployees()\n.first()" {
  width: 240
  height: 50
}
sql: "SELECT … FROM Employee\nWHERE department_id = ?" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
find -> touch -> sql
```

**Fig. 1.** Lazy collection: first SQL for the parent, second SQL when the collection is used (SELECT fetch). `join fetch` can fold this into one query.

```java
@Entity
public class Department {
    @Id
    private Long id;

    @OneToMany(mappedBy = "department") // fetch = LAZY by default
    private Set<Employee> employees = new HashSet<>();

    protected Department() {}
}

Department dept = em.find(Department.class, 1L);
int n = dept.getEmployees().size(); // extra SELECT while em is open
em.close();
dept.getEmployees().size(); // Hibernate: LazyInitializationException
```

**Listing 1.** Conceptual. Default lazy `@OneToMany`. Access inside the context may hit N+1 if you do this in a loop; access after `close` fails in Hibernate.

JPQL **`join fetch`**, a **load/fetch graph**, or Hibernate **`Hibernate.initialize`** (session still open) pull the association before detach. Fetching two collections in one query with parallel fetch joins can Cartesian-explode.

> [!warning] LAZY does not mean “no join, ever”
> The provider is allowed to eager-load a LAZY mapping. Mapping `fetch = LAZY` is not a query plan. `@ManyToOne` is **EAGER** unless you set LAZY.

> [!warning] Proxy plus closed Session
> Hibernate loads a proxy only on an open stateful `Session`. Closing the session and then touching `getEmployees()` is `LazyInitializationException`, not a JPA type. Do not keep a session open for the whole request just to hide that; fetch what the caller needs first.

> [!tip] Interview answer
> Lazy fetch postpones loading an association until you navigate it. In JPA, FetchType.LAZY is only a hint; collections default to it, ManyToOne does not. Hibernate uses proxies that work only inside an open Session — after close you get LazyInitializationException. Walking a list of parents without join fetch is the N+1 problem.
