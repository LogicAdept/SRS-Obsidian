<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How does `SUPPORTS` transaction propagation work?

> [!abstract] Short answer
> **`Propagation.SUPPORTS` joins an existing transaction when one is active; otherwise it runs non-transactionally.** It never starts a transaction. Spring recommends using it carefully — with transaction synchronization enabled, a `SUPPORTS` scope can still share the caller’s JDBC `Connection` or Hibernate `Session` even though no new physical transaction begins.

## Join or run bare

Spring’s `TransactionDefinition.PROPAGATION_SUPPORTS` and `Propagation.SUPPORTS` both say: support a current transaction; **execute non-transactionally if none exists**.

Typical use: read helpers or queries that **participate** when the caller already opened a unit of work but do not need to **create** one when called alone.

```d2
direction: down
withTx: "Caller has active TX\nSUPPORTS joins it" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
noTx: "No active TX\nSUPPORTS runs\nnon-transactionally" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}

withTx -> noTx
```

**Fig. 1.** `SUPPORTS` adapts to the caller’s transaction presence; it never becomes the starter.

```java
@Service
public class ProductQueryService {

    @Transactional(propagation = Propagation.SUPPORTS, readOnly = true)
    public Product findById(UUID id) {
        return repository.findById(id).orElseThrow();
    }
}

@Service
public class CatalogFacade {

    @Transactional
    public void refreshCatalog(UUID tenantId) {
        Product p = products.findById(tenantId); // joins facade TX
        cache.put(p);
    }
}

// Called directly with no outer @Transactional:
products.findById(id); // non-transactional path
```

**Listing 1.** Conceptual: same method joins a facade transaction or runs without one when invoked standalone.

## Not the same as “no `@Transactional`”

For transaction managers with **transaction synchronization**, Spring notes that `SUPPORTS` is **slightly different** from having no transaction at all: it still defines a scope where synchronization may apply, so the same JDBC connection or Hibernate session can be shared for the whole `SUPPORTS` method.

Spring also warns: do not nest `REQUIRED` or `REQUIRES_NEW` inside a `SUPPORTS` scope without careful manager configuration — you can hit synchronization conflicts at runtime.

When **no** transaction exists, a `SUPPORTS` method that performs writes executes **non-transactionally**: there is no unit-of-work rollback if a later statement fails. Contrast [[How does REQUIRED transaction propagation work]], which would start a transaction instead.

> [!warning] Standalone writes under `SUPPORTS` are not atomic
> Without an outer transaction, each JDBC statement may autocommit independently. Do not use `SUPPORTS` on write paths that can be called without a caller-owned boundary unless partial persistence is acceptable.

> [!warning] Self-invocation skips propagation
> `this.findById(...)` from a `@Transactional` method on the same class does not apply `SUPPORTS` through the proxy. See [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **`SUPPORTS` joins an existing transaction or runs without one — it never creates a transaction.** Good for read helpers that should see the caller’s unit of work but stay cheap when called alone. With synchronization enabled it still shares resources with the caller; standalone writes are not rolled back as a group.
