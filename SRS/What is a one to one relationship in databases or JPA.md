<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Mapping #Databases/Relational #SRS

# What is a one to one relationship in databases or JPA?

> [!abstract] Short answer
> **One-to-one** means each row (or entity) on side A relates to **at most one** on side B, and each on B to at most one on A. In a relational schema that is a **foreign key with a unique constraint**, or a **shared primary key**. In JPA it is **`@OneToOne`**. The **owning** side holds the FK; the inverse side uses **`mappedBy`**. Default **`fetch` is EAGER**. What JPA is: [[What is the Java Persistence API JPA]]. Contrast collections: [[What is an example of a one to many relationship in databases or JPA]].

## Unique FK or the same primary key

Jakarta Persistence lists four cardinalities: one-to-one, one-to-many, many-to-one, many-to-many. `@OneToOne` is a single-valued association with one-to-one multiplicity. It usually maps:

- a **unique foreign key** (join column(s) plus a unique constraint), or
- a **shared primary key** (`@MapsId` / `@Id` on the relationship: the dependent entity’s identity is the parent’s).

A join table is allowed but is a **non-default** mapping (`@JoinTable`). Default bidirectional mapping: owner table `A` has an FK to `B` named `{association}_{B_pk}`, **with a unique key** on that column. Without uniqueness, the same FK shape is many-to-one: [[What are JPA fetch types for entity associations]] does not change cardinality.

For bidirectional one-to-one, the **owning** side is the side that contains the FK. The other side sets `mappedBy` to that attribute. Flush writes the owning side. You must keep both in-memory references consistent. `cascade = REMOVE` and **`orphanRemoval`** are portable on `@OneToOne` (and `@OneToMany` only): [[How would you explain CascadeType.ALL]].

```d2
direction: down
emp: "EMPLOYEE\nPK + unique FK cubicle_id" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
cub: "CUBICLE\nPK" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}
emp -> cub: "at most one cubicle"
```

**Fig. 1.** Default 1:1: unique FK on the owning table, not a join table.

```java
@Entity
public class Employee {
    @Id
    private Long id;

    @OneToOne
    @JoinColumn(name = "CUBICLE_ID", unique = true)
    private Cubicle cubicle;

    protected Employee() {}
}

@Entity
public class Cubicle {
    @Id
    private Long id;

    @OneToOne(mappedBy = "cubicle")
    private Employee resident;

    protected Cubicle() {}
}
```

**Listing 1.** Bidirectional `@OneToOne`. `Employee` owns the unique FK. `Cubicle.resident` is inverse.

```java
@Entity
public class Employee {
    @Id
    private Integer id;

    @OneToOne
    @MapsId
    private EmployeeInfo info;

    protected Employee() {}
}
```

**Listing 2.** Conceptual. Shared primary key: `EmployeeInfo` uses the same id as `Employee`. An instance cannot be persisted until the parent reference is set.

Default **`fetch = EAGER`**: `find(Employee)` must load `Cubicle` and then that cubicle’s EAGER graph. Set `LAZY` if you do not always need the other row.

> [!warning] Unique is what makes it one-to-one
> A non-unique FK is many-to-one, even if you wrote `@OneToOne`. Schema generation should emit a unique constraint; an existing table without it will store two children for one parent.

> [!warning] mappedBy does not write the database
> Updates follow the owning (FK) side. Nulling only `cubicle.resident` leaves `EMPLOYEE.CUBICLE_ID` set. Shared-PK dependents also cannot `persist` until the parent association is assigned.

> [!tip] Interview answer
> One-to-one means at most one related row on each side. In SQL that is a unique foreign key or a shared primary key. In JPA you map it with OneToOne: the owning side has the FK, the other side uses mappedBy. Fetch defaults to EAGER, and cascade REMOVE or orphanRemoval is legal because the target is privately owned.
