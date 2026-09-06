<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #Java/Persistence/JPA #SRS

# What is the difference between get() load() Hibernate?

> [!abstract] Short answer
> Classic **`Session.get(Class, id)`** loads a **fully fetched** instance **now** (or **`null`**). Classic **`Session.load(Class, id)`** returned a **proxy** and hit the database **on first non-id access**. In Hibernate **7**, **`load(Class, id)` is removed** — use **`getReference()`** (same idea as JPA). **`get()` is deprecated** — use **`find()`**, which also returns **`null`** and never an uninitialized proxy. Hibernate vs JPA APIs: [[What is the difference between JPA as a specification and Hibernate]].

## Fetch now vs assume it exists

`Session.find` / deprecated `get`: return the persistent instance with that id, or **`null`**. If it is already in the persistence context, that instance is reused. The result is **never uninitialized**. It may come from the **session or second-level cache** (`LockMode.NONE`); it is not “always a SQL round trip.”

`Session.getReference` (JPA `EntityManager.getReference`): return a reference **assuming** the row exists. It **must not** access the datastore just to build the reference, so you often get a **proxy** initialized when a non-identifier method runs — the same lazy-proxy story as associations: [[What is lazy fetch in JPA or Hibernate]]. If the row is missing, JPA throws **`EntityNotFoundException` when state is first accessed** (a provider **may** throw at the `getReference` call). Hibernate’s `ObjectNotFoundException` JavaDoc: do **not** use `getReference` to test existence; use **`find()`**.

Hibernate **7.0**: `Session.load` methods with `get`/`load(Class, id)` semantics were **removed** in favor of `getReference`. A remaining **`load(Object object, Object id)`** **copies** DB state **into a transient instance you pass in** — not the old “return a proxy” API.

```d2
direction: down
id: "id = 1L" {
  width: 120
  height: 36
}
find: "find / get\nfully fetched or null" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
ref: "getReference / old load\nproxy, DB later" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
id -> find
id -> ref
```

**Fig. 1.** `find`/`get` resolve existence now. `getReference`/old `load` assume the row is there.

```java
Book found = session.find(Book.class, 1L);      // null if missing; initialized
Book ref = session.getReference(Book.class, 1L); // proxy; no SELECT yet
String title = ref.getTitle();                   // SELECT; EntityNotFoundException if no row
```

**Listing 1.** Conceptual. Prefer `find` / `getReference` over deprecated `get` and removed `load(Class, id)`.

> [!warning] load(Class, id) is gone; load(instance, id) is a different method
> Interview sheets still say “load returns a proxy.” On Hibernate 7 that method is **`getReference`**. `session.load(new Book(), id)` fills a **transient** object. Mixing the two is a wrong answer.

> [!warning] get() is not “always hit the database”
> `find`/`get` may satisfy `LockMode.NONE` from cache. They **do** guarantee a fully fetched instance or `null`. Touching a `getReference` proxy after the session is closed is **`LazyInitializationException`**: [[What is LazyInitializationException]].

> [!tip] Interview answer
> get loaded the entity immediately and returned null if the id was missing. load returned a proxy and failed later if the row did not exist. In Hibernate 7, say find versus getReference: find is the JPA get, getReference is the old load. Do not call getReference to check that a row exists.
