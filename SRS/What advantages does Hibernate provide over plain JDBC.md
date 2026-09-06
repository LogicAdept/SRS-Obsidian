<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #Java/JDBC #SRS

# What advantages does Hibernate provide over plain JDBC?

> [!abstract] Short answer
> **JDBC** is the JDK API for **connect → send SQL → walk a `ResultSet`**. You write the SQL, bind parameters, map every column, and own commit/close. **Hibernate sits on that stack**: a `Session` **wraps a JDBC `Connection`**, maps **classes ↔ tables** (and Java types ↔ SQL types), **generates** the usual `INSERT`/`SELECT`/`UPDATE`/`DELETE`, and **hydrates a graph of objects**. You persist and mutate **entities**; dirty checking flushes SQL. Hibernate’s stated goal is to drop the **hand-crafted JDBC/SQL** for common persistence — it does **not** replace JDBC, and it does **not** hide SQL when you need native queries or `Session.doWork`.

## What JDBC makes you do

The JDBC tutorial’s loop is the contract: `DriverManager`/`DataSource` → `Connection` → `Statement`/`PreparedStatement` → `ResultSet`, then `getInt`/`getString` per column. There is **no** object graph, **no** identity map, **no** automatic `UPDATE` when a field changes. That is full control and also the boilerplate Hibernate is designed to remove.

```java
try (Connection con = DriverManager.getConnection(url, user, password);
     PreparedStatement ps = con.prepareStatement(
         "SELECT id, title FROM Events WHERE id = ?")) {
  ps.setLong(1, id);
  try (ResultSet rs = ps.executeQuery()) {
    if (rs.next()) {
      Event e = new Event();
      e.setId(rs.getLong("id"));
      e.setTitle(rs.getString("title")); // you map every column
    }
  }
}
```

**Listing 1.** Conceptual JDBC: you own SQL, the cursor, and the mapping into a Java object.

## What Hibernate adds on top of that connection

Architecture: in the **comprehensive** setup Hibernate obtains connections (`ConnectionProvider` over `DataSource`/`DriverManager`) and transactions; a **minimal** setup can still take connections you open. Either way:

| JDBC | Hibernate on the same connection |
| --- | --- |
| You write SQL | Mappings + `persist` / HQL / Criteria **generate** SQL (quickstart: `persist` → `INSERT`; `from Event` → `SELECT` then **instantiate and populate** entities) |
| Tabular `ResultSet` | **Object/relational mapping**: table rows → **entity graph** |
| You `UPDATE` explicitly | **Dirty checking**: change a **managed** instance; flush writes SQL. No extra “save” for that mutation |
| New object per `SELECT` | **Persistence context (L1)**: same id in one `Session` → **same instance**; first-level cache for navigation and id lookup |
| You load associations yourself | **Lazy proxies/collections** while the session is open |
| Vendor SQL in your DAOs | **`Dialect`** (e.g. `PostgreSQLDialect`) plus mappings to **encapsulate vendor-specific SQL**; Hibernate still lets you run **native** SQL |

`SessionFactory` optionally holds a **second-level** cache shared across sessions. `Transaction` abstracts JDBC vs JTA demarcation — the database isolation level is still the JDBC/DBMS one.

```d2
direction: right
app: "Application\npersist / query entities" {
  width: 220
  height: 110
  style.fill: "#e3f2fd"
}
session: "Session / EM\nmappings, L1, dirty check" {
  width: 240
  height: 110
  style.fill: "#fff3e0"
}
jdbc: "JDBC Connection\nPreparedStatement" {
  width: 220
  height: 110
  style.fill: "#e8f5e9"
}
db: "RDBMS" {
  width: 140
  height: 90
  style.fill: "#f3e5f5"
}

app -> session -> jdbc -> db
```

**Fig. 1.** Hibernate is the ORM layer; JDBC remains the wire to the database.

```java
sessionFactory.inTransaction(session -> {
  Event e = new Event("kickoff", now());
  session.persist(e);          // INSERT generated
  e.setTitle("renamed");       // dirty; UPDATE on flush
  Event same = session.find(Event.class, e.getId());
  // same == e  inside this persistence context
});
```

**Listing 2.** Conceptual: CRUD and identity without hand-written SQL. Hibernate still executes JDBC underneath.

## SQL is still there

Hibernate **does not hide SQL**. Native queries (and handwritten SQL for CRUD) exist specifically as a path from a JDBC app and for vendor features (window functions, CTEs, `CONNECT BY`). `session.doWork(connection -> { … })` runs **your** `PreparedStatement` on the session’s connection and transaction. Preface caveat: Hibernate is **most useful** with an **object domain model** in the Java middle tier; it is **not** the best fit when the app is **only** stored procedures in the database.

> [!warning] Generated SQL is still your SQL bill
> Automatic mapping does not mean “no JDBC cost.” You must be able to **see** the statements (`hibernate.show_sql` in the getting-started guide). Lazy graphs, missing fetch plans, and a large persistence context (hard references until `Session` close) are JDBC round-trips and memory you did not write by hand. For one hot query, native SQL or plain JDBC/`JdbcTemplate` is the documented escape hatch — not “Hibernate cannot do SQL.”

> [!tip] Interview answer
> JDBC is Connection, Statement, ResultSet, and manual column mapping. Hibernate wraps that Connection, maps entities to tables, generates the usual SQL, and keeps a persistence context so identity and dirty checking work. That kills typical CRUD boilerplate. I still drop to native SQL or doWork when I need vendor SQL or statement-level control, and I always look at the SQL Hibernate actually runs.

See [[What is Hibernate as an ORM framework]], [[What is JDBC]], [[When would you use JDBC instead of Hibernate in Spring]], [[What is Hibernate SessionFactory]], and [[How does the Hibernate first-level cache work in Spring]].
