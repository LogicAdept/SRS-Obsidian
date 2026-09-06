<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Mapping #Java/Annotations #SRS

# How would you explain CascadeType.ALL?

> [!abstract] Short answer
> **`jakarta.persistence.CascadeType.ALL`** on a relationship is the same as **`cascade = {PERSIST, MERGE, REMOVE, REFRESH, DETACH}`**. `EntityManager.persist`, `merge`, `remove`, `refresh`, and `detach` then propagate to the associated entities (and **flush** still applies **persist** to associations marked `PERSIST` or `ALL`). The default `cascade` is **empty**. `ALL` does **not** include **`orphanRemoval`**.

## What ALL actually does

`CascadeType` is the enum used by the `cascade` element of `@OneToOne`, `@OneToMany`, `@ManyToOne`, and `@ManyToMany`. Operations run on the **source** entity; they are applied to **referenced** entities only when that association lists the matching type or `ALL`. What JPA is: [[What is the Java Persistence API JPA]].

- **`PERSIST`** — `persist(parent)` makes new children managed too. If the parent is already managed, it is ignored, but persist **still cascades**. Flush also persists new referenced instances when the association is `PERSIST` or `ALL`.
- **`MERGE`** — `merge(parent)` merges referenced children.
- **`REMOVE`** — `remove(parent)` marks referenced children removed. They are deleted at flush or commit. If the parent is **new**, it is ignored, but remove **still cascades**.
- **`REFRESH`** / **`DETACH`** — `refresh` and `detach` follow the same associations.

`ALL` is a parent-child convenience, not a schema `ON DELETE CASCADE`. Composition mappings: [[What is an example of a one to many relationship in databases or JPA]], [[What is a one to one relationship in databases or JPA]].

```d2
direction: down
all: "cascade = CascadeType.ALL" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
persist: "PERSIST\npersist + flush" {
  width: 170
  height: 50
}
merge: "MERGE" {
  width: 170
  height: 40
}
remove: "REMOVE\nremove parent → remove children" {
  width: 220
  height: 50
}
refresh: "REFRESH" {
  width: 170
  height: 40
}
detach: "DETACH" {
  width: 170
  height: 40
}
orphan: "orphanRemoval\nseparate mapping element" {
  width: 220
  height: 50
  style.fill: "#ffcdd2"
}
all -> persist
all -> merge
all -> remove
all -> refresh
all -> detach
```

**Fig. 1.** `ALL` is the five `EntityManager` operations. `orphanRemoval` is not a `CascadeType`.

```java
@Entity
public class Customer {
    @Id
    private Long id;

    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL)
    private Set<Order> orders = new HashSet<>();

    protected Customer() {}

    public Customer(Long id) {
        this.id = id;
    }

    public void addOrder(Order order) {
        orders.add(order);
        order.setCustomer(this);
    }
}

@Entity
public class Order {
    @Id
    private Long id;

    @ManyToOne
    @JoinColumn(name = "CUST_ID")
    private Customer customer;

    protected Order() {}

    public Order(Long id) {
        this.id = id;
    }

    void setCustomer(Customer customer) {
        this.customer = customer;
    }
}
```

**Listing 1.** `ALL` on the parent `OneToMany`. `em.persist(customer)` persists new orders; `em.remove(customer)` removes those orders. The `@ManyToOne` has no `cascade`.

## Not the same as dropping a child from the collection

`orphanRemoval` is a **boolean** on `@OneToOne` / `@OneToMany` (default `false`). When it is `true`, removing a target from the relationship (collection remove or setting the association to `null`) applies **`remove` at flush**. If you `remove` the parent, `orphanRemoval` also cascades remove to the targets, so you do not need `cascade = REMOVE` for that path.

`CascadeType.ALL` does **not** turn that on. With only `ALL`, taking an `Order` out of `customer.getOrders()` does not delete the `Order` row; you would still `em.remove(order)` (and keep both sides of a bidirectional association consistent). `orphanRemoval` is meant for privately owned children. Portable code must not reassign an orphaned entity to another parent. It does not apply if the orphan is already detached, new, or removed.

> [!warning] ALL includes REMOVE
> `em.remove(customer)` deletes **every associated `Order`**, not just the foreign keys. That is the usual interview trap on a `OneToMany`. `cascade = REMOVE` (and therefore `ALL`) should be used only on `OneToOne` / `OneToMany`; applying it to `ManyToMany` or `ManyToOne` is **not portable** — you can delete a shared parent or the “other” many-to-many entity. There is no portable guarantee of one SQL `DELETE` per child; each associated instance is still removed at flush or commit, which is expensive on a large collection.

> [!warning] ALL is not database ON DELETE CASCADE
> Cascades are persistence-context operations. They do not replace a database foreign-key `ON DELETE` rule, and they do not delete a child merely because you dropped it from the collection unless `orphanRemoval = true`.

> [!tip] Interview answer
> ALL means persist, merge, remove, refresh, and detach all cascade along that association. Persist the parent and new children are persisted; remove the parent and those children are removed too, which is why you put it on a privately owned OneToMany, not on ManyToMany. Orphan removal is a separate flag: it deletes a child when you take it out of the collection, which ALL by itself does not do.
