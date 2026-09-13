<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Fetching #Java/Persistence/JPA/Fetching #SRS

# How do Hibernate lazy proxies work?

> [!abstract] Short answer
> A lazy association is not "loaded later" — it is replaced **immediately** by a runtime-generated subclass (bytecode instrumentation produces `Entity$HibernateProxy`) that holds only the identifier. Every method call on the proxy is intercepted: the first call that needs real state triggers one `SELECT`, the proxy loads the row and delegates everything to it — subsequent calls never hit the database again. Measured on Hibernate 6.6: `getReference(Entity.class, id)` returns a proxy with class `...RefEnt$HibernateProxy` for which `instanceof RefEnt` is true; reading the **identifier** executes **zero** SQL (with property access the id getter is served from the proxy's stored id), and the first read of any other field executes exactly one `SELECT`. The constraints follow from the mechanism: the entity needs a **no-arg constructor** (the proxy subclass is created reflectively), the class must not be `final` (nothing to subclass) and lazily-overridden methods must not be `final` (no interception), `getClass()` returns the proxy type rather than your entity type, and touching the proxy outside a live session throws `LazyInitializationException`.

## The interception contract, measured

The proxy is built at runtime — no build-time enhancement step is involved for the default path — and its behavior has exactly two states: **uninitialized** (holds id + session reference) and **initialized** (delegates to the loaded entity). The boundary between the two states is what surprises people:

| Operation on an uninitialized proxy | SQL | What happened |
| --- | --- | --- |
| `proxy.getClass().getName()` | 0 | the proxy type itself, `Entity$HibernateProxy` |
| `proxy instanceof Entity` | 0 | true — it is a subclass |
| `proxy.getId()` (property access) | **0** | identifier served from the stored id |
| `proxy.getId()` (field access) | 1 | interception is on methods; field access forces init |
| first non-id method (`getName()`, `getTags()`) | **1** | initialization: one SELECT, then delegation |

The identifier rule is why `getReference` is the cheap tool for **linking** rows: building an association to a parent you will never read in this unit of work needs no parent data — the proxy's id is enough for the foreign key, and no query runs unless someone touches state. The same mechanism powers `@ManyToOne(fetch = LAZY)` associations: a loaded child's `parent` field is an uninitialized proxy, not null and not a loaded row.

```java
RefEnt proxy = session.getReference(RefEnt.class, realId);  // no SQL
Long id = proxy.getId();                                    // no SQL (property access)
String name = proxy.getName();                              // 1 SELECT — initialization

// the classic trap in tests and logging:
System.out.println(proxy.getClass());   // class ...RefEnt$HibernateProxy, not RefEnt
```

**Listing 1.** The measured sequence: linking is free, state costs one query, and the runtime type is not the static type.

## The limits are the mechanism showing through

Each restriction is the subclass trick stating its precondition. A `final` entity class cannot be proxied — depending on the version and configuration you get an error at startup or at the first lazy association access, so mapping a `final` class with lazy associations is simply an invalid mapping; `final` methods are worse in a subtle way: the proxy *is* created, but calls to the final method are **not intercepted**, so the method runs against the uninitialized skeleton instead of triggering initialization — producing nulls or zero id fields with no exception to explain it. The no-arg constructor is the reflection entry point for instantiating the proxy subclass without calling your constructor logic (this is the same requirement that entity instantiation at load time has — it is not proxy-specific, but it is the reason you cannot replace it with a constructor full of business arguments). The `getClass()` trap hits equality logic and test assertions: code comparing `getClass()` of two arguments where one is a proxy fails, while `instanceof` holds — and `equals` implementations that compare classes must normalize (for example via `Hibernate.unproxy` or by comparing `instanceof`-style). Finally, everything above requires a **live session**: the proxy holds the session that created it; after the session closes, the interceptor has nowhere to load from, which is exactly the `LazyInitializationException` failure mode — the proxy's contract, not a random error.

> [!warning] DTO projections and final classes are complements, not rivals
> When the laziness of proxies gets in the way — large graphs, detached rendering, serialization — the fix is usually not more tuning but not fetching entities at all: project to DTOs in the query. Keeping entities non-final and with property-access id getters, on the other hand, keeps the proxy mechanism fully available where it does help.

> [!tip] Interview answer
> A lazy association is a bytecode-generated subclass holding only the id; the first non-identifier access is intercepted and triggers one SELECT, after which calls delegate to the real entity. Measured: getReference gives a HibernateProxy, instanceof holds, the id getter runs zero SQL under property access while the first state getter runs exactly one. From the mechanism follow the constraints: no final classes (nothing to subclass), no final methods on mapped getters (no interception — silent nulls), a no-arg constructor as the reflective entry point, getClass() returning the proxy type, and a live session requirement — after it closes you get LazyInitializationException. I use getReference for linking without loading and DTO projections when the graph should not be lazy at all.

See [[What is LazyInitializationException]], [[What is the difference between get() load() Hibernate]], [[What is the difference between JPA FetchType lazy and eager]], [[What are the drawbacks of lazy loading]], and [[What are the Hibernate fetching strategies]].
