<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Language/Modifiers/Abstract #Java/OOP #SRS

# Can a JPA entity class be abstract?

> [!abstract] Short answer
> **Yes.** An `@Entity` may be an **abstract class or a concrete class**. An abstract entity is mapped and **queryable**; queries and `EntityManager` operations on that type run over its **concrete subclasses**. You cannot `new` it. That is different from `@MappedSuperclass`, which is **not** an entity, has **no** table, and **must not** be a query target. `abstract` in Java: [[How would you explain the abstract keyword in Java]]. Records cannot be entities: [[Can you use a Java record as a JPA entity]].

## Mapped and queryable; only `new` is forbidden

The entity class is annotated `@Entity` (or listed as an entity in XML). It must be a non-`final` top-level class or static nested class, with a `public` or `protected` no-arg constructor, and with no `final` methods or persistent instance variables. An enum, record, or interface cannot be an entity. **Abstract** satisfies non-`final`; you still need the no-arg constructor on the abstract class.

An abstract entity differs from a concrete entity **only** in that it cannot be directly instantiated. It is still mapped as an entity. A query whose target is the abstract type operates over and/or retrieves instances of concrete subclasses. Polymorphic associations to the abstract type are allowed. What JPA is: [[What is the Java Persistence API JPA]]. Inheritance in the language: [[What is inheritance]].

```d2
direction: down
abs: "@Entity abstract Employee\nmapped, queryable, no new" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
ft: "@Entity FullTimeEmployee" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
pt: "@Entity PartTimeEmployee" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
msc: "@MappedSuperclass\nnot an entity, no table, not queryable" {
  width: 300
  height: 55
  style.fill: "#ffcdd2"
}
abs -> ft
abs -> pt
```

**Fig. 1.** Abstract `@Entity` is a persistent type in the hierarchy. `@MappedSuperclass` is mapping reuse only.

```java
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class Employee {
    @Id
    protected Integer empId;

    protected Employee() {}

    protected Employee(Integer empId) {
        this.empId = empId;
    }
}

@Entity
public class FullTimeEmployee extends Employee {
    protected Integer salary;

    protected FullTimeEmployee() {}

    public FullTimeEmployee(Integer empId, Integer salary) {
        super(empId);
        this.salary = salary;
    }
}
```

**Listing 1.** Abstract root entity plus a concrete subclass. `em.persist(new FullTimeEmployee(1, 90_000))` is legal; `new Employee(...)` is not.

```java
// Conceptual: type of the query is the abstract entity
// SELECT e FROM Employee e
// em.find(Employee.class, 1)
```

**Listing 2.** Conceptual. Both operate on concrete subclass rows. Returned instances have a concrete runtime class (`FullTimeEmployee`, …).

If `@Inheritance` is omitted, the default strategy is `SINGLE_TABLE` (one table, discriminator column). `JOINED` and `TABLE_PER_CLASS` are the other options. The abstract root still needs an `@Id` on the hierarchy: [[What is the JPA Id annotation]].

## Not a mapped superclass, not a plain abstract Java class

`@MappedSuperclass` may also be abstract or concrete. It is **not** a persistent type: no table, not queryable, and must not be passed to `EntityManager` or `Query` operations. Its mappings are applied to entity subclasses. Persistent relationships declared there must be unidirectional. Use it when several entities share fields **without** a polymorphic entity type.

A **non-entity** superclass (no `@Entity`, no `@MappedSuperclass`) may be abstract too. Its state is **not** persistent; mapping annotations on it are ignored. That is not “an abstract entity.”

You still persist **instances**, so `persist`/`merge` need a concrete subclass object. A field typed `Employee` can hold a `FullTimeEmployee`. Abstract vs interface as a Java choice stays a language question: [[When should you use an abstract class versus an interface]].

> [!warning] `@MappedSuperclass` is not an abstract entity
> `SELECT e FROM Super e` is illegal if `Super` is only a mapped superclass. If you need `FROM Employee` and associations to `Employee`, the root must be `@Entity`, even if it is `abstract`.

> [!warning] The provider still needs a no-arg constructor
> `abstract` blocks `new Employee()` in your code. It does not drop the JPA rule: `public` or `protected` `Employee() {}` on the abstract class, and the same on concrete subclasses.

> [!warning] Abstract does not mean “no table”
> Under `SINGLE_TABLE`, the hierarchy shares one table. Under `JOINED`, the abstract root has its own table and subclass tables join to it. “Abstract ⇒ no table” is the mapped-superclass rule, not the entity rule.

> [!tip] Interview answer
> Yes. JPA allows abstract and concrete entity classes. An abstract `@Entity` is mapped and can be queried; the provider returns concrete subclass instances, and you never instantiate the abstract type yourself. That is not `@MappedSuperclass`, which shares mappings but is not an entity and is not queryable. You still provide a public or protected no-arg constructor on the abstract class.
