<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate #SRS

# What is the difference between save(), persist(), merge(), update()?

> [!abstract] Short answer
> **`persist`** (JPA) makes a **new** instance **managed**; INSERT happens at **flush/commit**; it returns **`void`**. **`merge`** (JPA) **copies** new or detached state onto a **managed instance it returns** — the object you passed stays detached. Hibernate **`save` / `update` / `saveOrUpdate` are removed in Hibernate 7** (`persist` / `merge` replace them). Old `save` assigned an id and returned it; old `update` reattached **the same** detached instance. Spec vs native: [[What is the difference between JPA as a specification and Hibernate]].

## JPA persist and merge; Hibernate leftovers

**`EntityManager.persist`:** a **new** entity becomes managed and will be **inserted** when the persistence context syncs. Already-managed: ignored (cascade still runs). **Removed:** becomes managed again. **Detached:** `EntityExistsException` now, or `EntityExistsException` / `PersistenceException` at flush/commit. Hibernate `Session.persist`: for generated ids, the id **may be assigned only at flush**, depending on the generator. Cascade: `PERSIST` / `ALL`: [[How would you explain CascadeType.ALL]].

**`EntityManager.merge`:** copy state into the persistence context. **Detached** → managed `X'` (load or new copy) with the **same id**. **New** → managed copy (later INSERT). **Managed** → that instance is returned; cascade still runs. **Removed** → `IllegalArgumentException` (or commit fails). The argument is **not** associated with the session. Unfetched `LAZY` fields are **ignored** on merge. Version is checked on merge and/or flush.

**Hibernate 6:** `Session.save` / `update` / `saveOrUpdate` were **deprecated**. **Hibernate 7:** they are **gone**. Migration: `save` → `persist`; `update` → `merge`; `saveOrUpdate` → `persist` if transient, `merge` if detached. Old `save`: persist transient, **first assign** a generated id, **return** that id (`CascadeType.SAVE_UPDATE`). Old `update`: take a **detached** instance and make **that same object** persistent; **exception** if the session already has that id.

```d2
direction: down
new: "new / transient" {
  width: 140
  height: 36
}
det: "detached" {
  width: 120
  height: 36
}
persist: "persist\nsame object, managed" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
merge: "merge\nreturns managed copy" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
new -> persist
new -> merge
det -> merge
```

**Fig. 1.** `persist` keeps your instance. `merge` returns a different managed instance. Do not `persist` a detached entity.

```java
em.persist(book);                 // book is managed; INSERT later
Book managed = em.merge(detached); // use managed, not detached
detached.setTitle("x");           // will NOT flush — wrong object
```

**Listing 1.** Conceptual. Hibernate 7 has no `session.save` / `session.update`.

Spring Data `CrudRepository.save` is **another** method: it may persist or merge and you must **use the returned instance**. It is not JPA `persist`.

> [!warning] merge does not attach the argument
> `Book b2 = em.merge(b1);` — keep **`b2`**. Continuing to mutate `b1` is a silent lost-update. Classic `session.update(b1)` *did* attach `b1`; `merge` does not.

> [!warning] persist(detached) is illegal
> Interview sheets say “persist is for new, merge for detached.” Correct. Persisting a detached instance is `EntityExistsException` (possibly delayed). Adding a detached child to a `cascade=PERSIST` parent fails the same way at flush — `merge` the child first.

> [!tip] Interview answer
> persist makes a new entity managed and inserts at flush; it returns void and may delay id generation. merge copies detached or new state onto a managed instance it returns; you must keep that return value. Hibernate save returned an id and update reattached the same object; both are removed in Hibernate 7 in favor of persist and merge.
