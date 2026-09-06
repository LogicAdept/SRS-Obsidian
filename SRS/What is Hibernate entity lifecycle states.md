<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate/Session #SRS

# What is Hibernate entity lifecycle states?

> [!abstract] Short answer
> An entity’s **lifecycle state** is its relation to a **persistence context** (`Session` / `EntityManager`) and to the database. **JPA** names four: **new** (Hibernate: **transient**), **managed** (**persistent**), **detached**, and **removed**. Current **`Session`** Javadoc frames three with respect to one open session — **transient**, **persistent**, **detached** — and treats **`remove`** as marking a persistent instance for deletion until flush, after which it is **transient** again. Only **managed** instances are identity-unique in that context, dirty-checked, and flushed. Transitions are **`persist`**, **`find`/`get`/query**, field mutation, **`detach`/`evict`/`clear`/close**, **`merge`**, and **`remove`**.

## Four names, one persistence context

A persistence context is a set of entity instances in which **for a given type + primary key there is at most one instance**. Hibernate’s **`Session`** *is* that context (and a JPA **`EntityManager`**).

| State | In the context? | Persistent identity | Meaning |
| --- | --- | --- | --- |
| **New / transient** | No | Typically none yet (unless you assigned the id) | `new` only. No row yet. |
| **Managed / persistent** | Yes | Yes | Associated with this `Session`. **May not have a row yet** (after `persist`, before flush). `find` / `get` / a query return this state. Field changes are dirty-checked. |
| **Detached** | No | Yes | Was persistent; context closed, **`clear`**, **`detach`/`evict`**, or a **deserialized copy**. Mutations are not tracked. |
| **Removed** | Yes | Yes | Still associated, **scheduled for `DELETE`** at flush/commit. JPA: still a lifecycle state until the row goes. |

`contains(entity)` is true only for a **managed** instance of **this** context.

```d2
direction: right
tr: "Transient\n(new)" {
  width: 140
  height: 70
  style.fill: "#eceff1"
}
mg: "Managed\n(persistent)" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
dt: "Detached" {
  width: 140
  height: 70
  style.fill: "#fff3e0"
}
rm: "Removed" {
  width: 140
  height: 70
  style.fill: "#ffebee"
}

tr -> mg: persist
mg -> dt: detach / close
dt -> mg: merge\n(copy)
mg -> rm: remove
rm -> tr: flush DELETE
```

**Fig. 1.** Application-visible states. `merge` returns a **different** managed instance; the detached object stays detached.

## How you move between them

**Become managed.** `persist` makes a **new** instance persistent and queues an **`INSERT`** (generated ids may appear only at flush, depending on the generator). `persist` on an already managed instance is a no-op on that instance but still **cascades** `PERSIST`. `persist` on **removed** **undoes** the deletion. `find` / `get` / HQL-JPQL load into the context (or return the instance already there).

**Stay managed.** There is **no** `update()` for a managed entity. Mutate fields; [[What is Hibernate dirty checking]] at flush writes SQL. `refresh` overwrites memory from the database.

**Leave the context.** `detach` / `evict` (Session synonym), `clear` (all instances; **cancels** pending insert/update/delete), close the session, or serialize (the copy is detached; the original may still be managed). Unflushed changes on a detached instance **are not** written.

**Come back.** `merge` **copies** new or detached state onto a **managed** instance and **returns that instance**. The object you passed does **not** become associated. Since **Hibernate 7**, older Session operations that reattached a detached instance (`save` / `update` / `saveOrUpdate`) are **gone**; use **`merge`**.

**Delete.** JPA `remove` requires a **managed** instance (new is ignored; already-removed is ignored). Hibernate `Session.remove` **also accepts detached** unless you run in **fully JPA-compliant** mode.

```java
Person p = new Person();          // transient / new
session.persist(p);               // managed; INSERT at flush
p.setName("Ada");                 // still managed — no update()
session.flush();

session.detach(p);                // detached
p.setName("Ada Lovelace");        // not tracked
Person managed = session.merge(p); // copy onto a managed instance
managed.setName("Ada L.");        // this one will flush
session.remove(managed);          // removed → DELETE at flush
```

**Listing 1.** Conceptual transitions on a `Session`. Keep using the **return value** of `merge`.

Two open sessions never share one Java instance for the same id. Touching a **LAZY** association after detach is [[What is LazyInitializationException]]. **`StatelessSession`** has **no** persistence context, so this lifecycle does not apply.

> [!warning] merge() does not “reattach this object”
> After `merge(detached)`, keep writing on the **returned** managed instance. Changing the original detached graph does nothing until you merge again. Closing the session (typical end of `@Transactional`) detaches **everything**; a setter on a controller-held entity is not an `UPDATE`. Hibernate 7 will not compile `save`/`update`/`saveOrUpdate`. JPA `remove(detached)` is illegal; native `Session.remove` may still accept it.

> [!tip] Interview answer
> Hibernate entities are transient, managed, detached, or removed relative to the Session, which is the persistence context. persist and find put an instance in the context, where dirty checking writes changes at flush with no update call. close, clear, or detach make it detached; merge copies that state onto a different managed instance and is the only reattach path in Hibernate 7. remove schedules a DELETE while the instance is still in the context; JPA forbids remove on detached, Hibernate Session does not unless you force JPA compliance.

See [[What is Hibernate dirty checking]], [[How does the Hibernate first-level cache work in Spring]], [[What is Hibernate as an ORM framework]], [[What is Hibernate SessionFactory]], [[What is LazyInitializationException]], and [[What is the difference between JPA as a specification and Hibernate]].
