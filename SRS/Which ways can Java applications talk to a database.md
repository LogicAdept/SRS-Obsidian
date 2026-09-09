<!--
reps: 0
priority: 0
-->
#Java/Persistence #SRS

# Which ways can Java applications talk to a database

> [!abstract] Short answer
> **Everything funnels through JDBC — the Java SE API of `Connection`, `PreparedStatement`, `ResultSet` and drivers. On top of it: JPA/ORM (Hibernate) for object mapping, Spring Data JPA repositories for declarative queries, Spring JdbcTemplate for thin SQL, jOOQ for type-safe SQL DSL, MyBatis for explicit SQL mapping.** Choose by how much SQL control versus mapping automation you want.

## The layers, bottom up

JDBC is the contract between Java and a vendor driver; every framework above it issues JDBC calls eventually. The layers only differ in who writes the SQL and who maps the rows.

```d2
direction: right
code: "Your code\nrepositories / entities / queries" {
  width: 290
  height: 90
  style.fill: "#e3f2fd"
}
fw: "Framework\nJPA-Hibernate | Spring Data | JdbcTemplate | jOOQ | MyBatis" {
  width: 380
  height: 100
  style.fill: "#fff3e0"
}
jdbc: "JDBC API\nConnection, PreparedStatement, ResultSet" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
drv: "Vendor driver\nPostgreSQL / MySQL / H2" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
code -> fw -> jdbc -> drv
```

**Fig. 1.** The stack: framework choice changes the source of SQL, but `Connection` and the driver remain the floor.

A real round trip through raw JDBC — the shape every framework hides:

```java
try (Connection cn = DriverManager.getConnection("jdbc:h2:mem:demo", "sa", "")) {
    PreparedStatement ps = cn.prepareStatement(
        "select a.name, b.title from authors a join books b on b.author_id = a.id order by b.id");
    ResultSet rs = ps.executeQuery();
    while (rs.next()) {
        System.out.println(rs.getString(1) + " -> " + rs.getString(2));
    }
}
```

**Listing 1.** Run on JDK 21 with the H2 in-memory database:

```java
Kathy -> Core Java
Josh -> Effective Java
Josh -> Java Concurrency
```

**Listing 2.** Real SQL, real rows: this exact `PreparedStatement` → `ResultSet` loop is what JPA's `find`, a Spring Data query method, and a jOOQ DSL query all compile down to.

> [!warning] "Which one should we use" is a control-versus-automation decision, not a fashion contest
> The traps hide at the boundaries. First, there is no "JPA versus JDBC" — JPA sits ON JDBC; arguing them as alternatives is a category error, and calling a native query from JPA still uses the same driver. Second, mixing layers naively doubles work: Hibernate-managed entities updated through raw `JdbcTemplate` UPDATEs bypass the persistence context, so stale entities and lost updates appear; pick a primary layer per use case and cross it deliberately (native queries, bulk operations) — see [[When does the N plus 1 query problem occur and how do you fix it]] for where pure ORM hurts. Third, SQL semantics leak through every layer: row-mapping frameworks will happily build an N+1 shape or a cartesian join that no library catches. Framework specifics: [[Which Java ORM frameworks do you know]] for the mapping stack, [[How do JDBC interface types such as Statement and PreparedStatement differ]] and [[How are database query results processed in JDBC]] for the floor, and [[How do you configure a DataSource in Spring]] for wiring the pooled entry point in real apps.

> [!tip] Interview answer
> **At the bottom is always JDBC: Connection, PreparedStatement, ResultSet, a vendor driver. Above it you pick per project: JPA/Hibernate for object mapping and persistence-context management, Spring Data JPA repositories for declarative queries over JPA, JdbcTemplate for thin explicit SQL, jOOQ for a type-safe SQL DSL, MyBatis for hand-written SQL with mapping. They are layers, not rivals — everything ends as a JDBC call.**

