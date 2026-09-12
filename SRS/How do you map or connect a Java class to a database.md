<!--
reps: 0
priority: 0
-->
#Java/JDBC #Java/Persistence/JPA #Java/Annotations #SRS

# How do you map or connect a Java class to a database?

> [!abstract] Short answer
> **Connect** the application with JDBC: a **`DataSource` / `DriverManager`** yields a **`Connection`** (session). JDBC does **not** map a class to a table — you **copy columns** from a **`ResultSet`** into a POJO (or a Spring `RowMapper`). **Map** a class with **Jakarta Persistence**: annotate it **`@Entity`**, give it **`@Id` / `@EmbeddedId`**, optional **`@Table`**. An entity typically **is a table**; an instance **is a row**. Records, enums, and interfaces **cannot** be entities.

## Connect: JDBC session, not an ORM

`Connection` is a **session** with a database ([[How do you establish a database connection in Java]], [[How do you integrate a database with a Java application]]). You run SQL with statements and read **1-based** columns via `getXxx` ([[How are database query results processed in JDBC]]). Any “mapping” is **your** code (or [[What is a RowMapper in Spring JDBC]]):

```java
import java.sql.ResultSet;
import java.sql.SQLException;

public final class PersonRow {
    public static Person from(ResultSet rs) throws SQLException {
        return new Person(rs.getInt("id"), rs.getString("name"));
    }
}

public record Person(int id, String name) {}
```

**Listing 1.** Conceptual JDBC: a record is a fine **row DTO**. That is not an entity mapping.

## Map: `@Entity` is object/relational metadata

Jakarta Persistence is an **O/R mapping** facility. An **entity** is a lightweight persistence domain object: **typically a table**, each instance **a row**. The programming artifact is the **entity class**, annotated `jakarta.persistence.Entity` ([[How would you explain DTO Entity]], [[What is JDBC, an implementation or a specification]]).

Jakarta Persistence 4.0 `@Entity` requires the class to:

- be a **non-`final`** top-level class or **static** inner class
- have a **public or protected no-arg constructor**
- have **no `final` methods or persistent instance variables**

An **enum, record, or interface may not** be an entity ([[Can you use a Java record as a JPA entity]]). Abstract classes **may**. Every entity needs **`@Id` or `@EmbeddedId`**. Fields are persistent by default; **`@Transient`** or Java `transient` opts out. **`@Table`** names the primary table; **`@SecondaryTable`** adds more. Access type follows whether mapping annotations sit on **fields** or **getters**.

```java
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "person")
public class PersonEntity {
    @Id
    private Integer id;
    private String name;

    protected PersonEntity() {}

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }
}
```

**Listing 2.** Conceptual JPA entity. Clients should use methods, not fields; the provider may use field or property access depending on annotation placement.

```d2
direction: right
jdbc: "JDBC\nConnection + ResultSet\nyou copy columns" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
jpa: "JPA @Entity\nclass ↔ table\ninstance ↔ row" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
db: "Database" {
  width: 140
  height: 90
  style.fill: "#e3f2fd"
}

jdbc -> db
jpa -> db
```

**Fig. 1.** Same database, two contracts. JDBC never treats your class as a mapped table. JPA metadata does.

Basic attributes map to **columns**; associations map to **FKs / join tables**. Lazy vs eager is a **hint**. JPA still needs a JDBC driver and usually a `DataSource` under the persistence unit — mapping does not replace **connect**.

> [!warning] Putting `@Entity` on a JDBC DTO does not “JDBC-map” it
> JDBC has no entity annotation. `@Entity` is Jakarta Persistence. A `record` works as a JDBC row type and is **illegal** as an entity.

> [!warning] Entity rules are structural, not optional style
> No-arg `public`/`protected` constructor, non-`final` class, non-`final` persistent members, at least one `@Id` / `@EmbeddedId`. Skip `@Id` and it is not a complete entity. Map annotations on **either** fields **or** getters consistently so access type is unambiguous.

> [!warning] Do not share a JDBC `Connection` as if it were an entity manager
> A `Connection` is a session you **close**. Concurrent servlet threads must not share it ([[How do you connect to a database and add logging in a servlet]]). JPA uses a persistence context; that is a different lifecycle.

> [!tip] Interview answer
> JDBC connects with a `Connection` and you copy `ResultSet` columns into objects yourself. To map a class to a table you use JPA: `@Entity`, `@Id`, optional `@Table`. An entity is typically a table and an instance is a row. Records cannot be entities; JDBC DTOs can be records.

## See also

- [[What is Hibernate entity lifecycle states]]
- [[What is the difference between Spring JDBC and Spring Data JPA]]
- [[Can a JPA entity class be abstract]]
