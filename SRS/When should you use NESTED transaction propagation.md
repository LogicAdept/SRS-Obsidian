<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# When should you use `NESTED` transaction propagation?

> [!abstract] Short answer
> Use **`Propagation.NESTED`** when a **sub-step may fail** but the **outer unit of work should continue** — for example one bad item in a batch or optional validation — while still committing **only with the outer transaction**. Prefer it over **`REQUIRES_NEW`** when you want **one connection** and accept that **outer rollback undoes nested work**. Use **`REQUIRES_NEW`** when inner rows must **survive** outer failure.

## Partial undo inside one commit boundary

`NESTED` fits “try this sub-work; if it fails, roll back **only that slice** and keep going” **inside a single physical transaction** (JDBC savepoint when supported). The outer method can catch the inner failure and continue; the whole unit still commits or rolls back together at the end.

Good fits:

* **Optional side effects** (audit attempt, enrichment) where failure should not poison the whole TX like nested `REQUIRED` would
* **Per-item processing** in a loop where one item failing should not mark the entire batch rollback-only
* **Same-connection** scenarios where `REQUIRES_NEW`’s second connection is undesirable

```java
@Service
public class ImportService {

    @Transactional
    public void importBatch(List<Row> rows) {
        for (Row row : rows) {
            try {
                validator.validateNested(row); // NESTED in ValidatorService
                repository.save(map(row));
            } catch (ValidationException ex) {
                // NESTED rolled back to savepoint; continue with next row
            }
        }
    }
}
```

**Listing 1.** Conceptual cross-bean pattern: inner failure rolls back to savepoint, outer batch continues. Mechanism: [[How does NESTED transaction propagation work]].

## Choose `NESTED` vs `REQUIRES_NEW`

| Need | Use |
| --- | --- |
| Partial undo; outer may still commit | **`NESTED`** (savepoint) |
| Inner must **commit independently** before outer ends (audit/outbox survives outer rollback) | **`REQUIRES_NEW`** |
| One connection; outer rollback OK to undo nested work | **`NESTED`** |
| Second connection / pool headroom acceptable | **`REQUIRES_NEW`** |

See [[What is the difference between NESTED and REQUIRES_NEW propagation]] and [[What is the difference between NESTED and REQUIRED propagation]].

## Preconditions

Confirm **savepoint support** on your stack — primarily `DataSourceTransactionManager` and a JDBC driver that supports savepoints. Without that, `NESTED` cannot deliver partial rollback — [[Does NESTED propagation require JDBC savepoints]].

With **no outer transaction**, `NESTED` behaves like `REQUIRED` and simply starts one — [[What happens if NESTED is used when no current transaction exists]].

> [!warning] Do not use `NESTED` for independent audit/outbox
> If business failure must **not** undo the inner row, you need an **independent commit** — **`REQUIRES_NEW`**, not `NESTED`. Outer rollback always discards nested work in the same physical transaction.

> [!warning] Self-invocation skips `NESTED`
> `this.validateNested(row)` does not create a savepoint boundary. Call through another bean or use AspectJ mode — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **Use `NESTED` when a sub-step should fail locally without aborting the whole outer transaction, and you still want one commit at the end.** It is the savepoint pattern. Use `REQUIRES_NEW` when inner work must commit even if the outer rolls back. Verify savepoint-capable JDBC setup first.
