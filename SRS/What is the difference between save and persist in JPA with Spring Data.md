<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/JPA #SRS

# What is the difference between save and persist in JPA with Spring Data?

> [!abstract] Short answer
> **`EntityManager.persist`** makes a **new** entity managed (insert on flush). **`CrudRepository.save`** is Spring Data’s convenience: it calls **`persist`** when the entity is **new**, otherwise **`merge`**. So `save` is not a synonym for `persist` — it may merge and return a **different instance**.

## JPA operations

| API | Role |
| --- | --- |
| **`persist(entity)`** | New instance → managed; scheduled insert. Already-managed instances are ignored (cascade may still run). Returns `void` — same object becomes managed. |
| **`merge(entity)`** | Copy state of a **new or detached** instance into the persistence context; returns a **managed** instance that may be a **different Java object**. Can load from DB if needed. |

There is no separate “update” call on managed entities: change fields while managed and flush/commit.

## What Spring Data `save` does

Spring Data JPA docs: `save` uses `persist` if the entity has **not yet been persisted**, else `merge`. Newness comes from id/version inspection, `Persistable.isNew()`, or custom `EntityInformation`.

```java
@Transactional
public <S extends T> S save(S entity) {
  if (entityInformation.isNew(entity)) {
    entityManager.persist(entity);
    return entity;
  } else {
    return entityManager.merge(entity);
  }
}
```

**Listing 1.** `SimpleJpaRepository.save` — persist vs merge branch (Spring Data JPA).

```d2
direction: right
save: "repository.save(e)" {
  style.fill: "#e3f2fd"
}
isNew: "isNew?" {
  style.fill: "#fff3e0"
}
persist: "em.persist(e)\nsame instance" {
  style.fill: "#e8f5e9"
}
merge: "em.merge(e)\nuse returned ref" {
  style.fill: "#fce4ec"
}

save -> isNew
isNew -> persist: "yes"
isNew -> merge: "no"
```

**Fig. 1.** Repository `save` chooses JPA `persist` or `merge` from entity state detection.

## Why merge surprises people

- After `merge`, keep working with the **returned** managed entity, not necessarily the argument you passed.
- Merge can trigger a **SELECT** to load the current row, then apply state — costlier than mutating an already-managed instance.
- Wrong “new” detection (e.g. manually assigned non-null ids) sends new rows through **`merge`** instead of **`persist`**.

Call `persist` (or ensure `isNew()` is correct) when you know the instance is brand new and you want that path. Prefer `save` in repository code for the usual CRUD API.

> [!warning] Assigned ids look “not new”
> Default rules treat a non-null id as existing → `merge`. For assigned identifiers, implement **`Persistable`** (or equivalent) so `save` still **`persist`s** new rows — see Spring Data JPA entity-persistence docs.

> [!tip] Interview answer
> `persist` is JPA for new entities. Spring Data `save` calls `persist` or `merge` depending on whether the entity is new. Merge returns a managed copy — always use the return value. `save` is not “just persist.”

See [[What is the difference between save and saveAll in Spring Data]], [[What is the difference between save and saveAndFlush in Spring Data JPA]], and [[What are the pros and cons of EntityManager versus Spring Data JPA repositories]].
