<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #Java/Persistence/JPA #Java/Annotations #SRS

# What association types exist in Hibernate?

> [!abstract] Short answer
> Hibernate/JPA entity associations are the four multiplicities: **`@ManyToOne`**, **`@OneToMany`**, **`@OneToOne`**, **`@ManyToMany`**. Each can be **unidirectional** or **bidirectional**. The database has **one** foreign key (or a **join table**); a bidirectional mapping still has **one owning side** (`@JoinColumn` / `@JoinTable`) and an **inverse** side marked **`mappedBy`**. Defaults: to-one is **`EAGER`**, collections **`LAZY`**. Cascade is **off** unless you set it. Hibernate’s usual parent–child pair is **`@ManyToOne` (owner) + `@OneToMany(mappedBy=…)`**.

## The four multiplicities

Associations join **entities** using relational join semantics.

| Annotation | Multiplicity | Typical SQL | Default `fetch` |
| --- | --- | --- | --- |
| **`@ManyToOne`** | many children → one parent | FK on the **child** table | **`EAGER`** |
| **`@OneToMany`** | one parent → many children | same FK, or a **link table** if unidirectional | **`LAZY`** |
| **`@OneToOne`** | one ↔ one | **unique** FK, **shared PK** (`@MapsId`), or join table | **`EAGER`** |
| **`@ManyToMany`** | many ↔ many | **join table** (`@JoinTable` on the owner) | **`LAZY`** |

`@ManyToOne` is the common case: it *is* a foreign key. `@OneToMany` without a mirroring `@ManyToOne` is **unidirectional**; Hibernate then uses a **link table**. With a child `@ManyToOne`, the pair is **bidirectional**: two navigations, **one** FK. **Every bidirectional association has exactly one owner** — for `@OneToMany`/`@ManyToOne` that owner is the **child** (`@ManyToOne`); the collection is `mappedBy`.

`@OneToOne`: unidirectional = FK on the “client” side. Bidirectional adds `mappedBy` on the inverse parent. Unique FK / shared primary key (`@MapsId`) are the usual physical mappings.

`@ManyToMany` **always** needs a link table. Either side of a bidirectional pair may own it; the other uses `mappedBy`. Hibernate notes that extra columns on the link belong in an explicit **link entity** (two `@ManyToOne`s), not on `@ManyToMany`.

```d2
direction: right
m2o: "@ManyToOne\nFK on child" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
o2m: "@OneToMany\ncollection" {
  width: 200
  height: 90
  style.fill: "#fff3e0"
}
o2o: "@OneToOne\nunique FK / shared PK" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
m2m: "@ManyToMany\njoin table" {
  width: 200
  height: 90
  style.fill: "#f3e5f5"
}

m2o -> o2m
```

**Fig. 1.** Four JPA association annotations; `@ManyToOne`/`@OneToMany` are the same FK seen from two ends when bidirectional.

```java
@Entity
class Person {
  @Id Long id;
  @OneToMany(mappedBy = "person", cascade = CascadeType.ALL, orphanRemoval = true)
  List<Phone> phones = new ArrayList<>();
}

@Entity
class Phone {
  @Id Long id;
  @ManyToOne
  @JoinColumn(name = "person_id")
  Person person;
}
```

**Listing 1.** Conceptual bidirectional one-to-many: child owns the FK; parent collection is `mappedBy`. Keep both sides in sync in the domain (add/remove helpers).

## Owning side, cascade, fetch

- **Owner** writes the FK / join-table rows. `mappedBy` is **ignored** for SQL updates of the link.
- **`cascade`** defaults to **no** operations. Hibernate: cascade **parent → children**, not the other way.
- **`orphanRemoval`** ( `@OneToMany` / `@OneToOne` ): removing a child from the association **deletes** the child row (default **`false`**).
- **`optional = false`** on to-one: relationship **must** exist (schema NOT NULL).
- **`LAZY` is a hint**; **`EAGER` is a requirement**. Collection default lazy; to-one default eager — a `find` of `Phone` will join/select `Person` unless you set `FetchType.LAZY`.

> [!warning] Unidirectional `@OneToMany` is not “the same mapping with one annotation”
> No `mappedBy` → Hibernate uses a **join table** and, on collection updates, may **delete all link rows and reinsert** the remainder. Bidirectional `@OneToMany` (child owns the FK) updates **one** column (`NULL` or a new parent). Inverse-side-only changes are **silent** in the database. Bidirectional `@OneToOne` with `LAZY` on the `mappedBy` side still often needs a **secondary select** to know if a child exists (N+1); Hibernate prefers unidirectional `@OneToOne` + `@MapsId` when you care about lazy.

> [!tip] Interview answer
> The four types are ManyToOne, OneToMany, OneToOne, and ManyToMany, each uni- or bidirectional. The database has one foreign key or a join table; mappedBy marks the inverse side so only the owner updates the link. I map parent–child as ManyToOne on the child plus OneToMany(mappedBy) on the parent, leave collections LAZY, and I do not treat unidirectional OneToMany as the default because of the extra join table.

See [[What is lazy fetch in JPA or Hibernate]], [[What is LazyInitializationException]], [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], and [[How would you explain DTO Entity]].
