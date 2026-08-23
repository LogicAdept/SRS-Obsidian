<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What is the difference between `NESTED` and `REQUIRES_NEW` propagation?

> [!abstract] Short answer
> **`NESTED` stays on one physical transaction and uses a JDBC savepoint for partial rollback. `REQUIRES_NEW` suspends the outer transaction and opens a separate physical transaction that can commit independently.** Outer rollback undoes `NESTED` work; already-committed `REQUIRES_NEW` work survives. `REQUIRES_NEW` also takes an extra connection while the outer TX stays suspended.

## One TX with savepoint vs two independent TXs

| | `NESTED` | `REQUIRES_NEW` |
| --- | --- | --- |
| Physical transactions | **One** (shared with outer) | **Two** (inner independent) |
| Mechanism | JDBC **savepoint** | **Suspend** outer + new TX |
| Inner can commit before outer ends | **No** | **Yes** |
| Outer rollback undoes inner | **Yes** (same physical TX) | **No** (if inner already committed) |
| Extra connection while inner runs | **No** (same connection) | **Yes** (typical JDBC setup) |

Spring’s reference docs: `NESTED` uses a single physical transaction with savepoints; `REQUIRES_NEW` always uses an independent physical transaction that can commit or roll back separately.

```d2
direction: right
nested: "NESTED\n1 physical TX\n+ savepoint" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
newTx: "REQUIRES_NEW\n2 physical TXs\ninner may commit" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
outerRb: "Outer rollback" {
  width: 180
  height: 60
  style.fill: "#ffebee"
}
nUndo: "NESTED work\nundone" {
  width: 180
  height: 60
  style.fill: "#ffebee"
}
rKeep: "Committed REQUIRES_NEW\nwork kept" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

nested -> outerRb -> nUndo
newTx -> outerRb -> rKeep
```

**Fig. 1.** Choose `NESTED` for partial undo inside one commit; `REQUIRES_NEW` for independent commit.

```java
@Service
public class OrderService {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);

        // NESTED: optional audit — roll back to savepoint on failure, same TX
        audit.tryRecordNested(order);

        // REQUIRES_NEW: audit/outbox — commits even if this method later fails
        audit.recordIndependent(order);

        throw new PaymentException("fail outer");
    }
}
```

**Listing 1.** Conceptual names only — real beans need **cross-bean** proxy calls for either propagation to apply.

## Operational requirements

**`NESTED`** needs savepoint-capable JDBC setup — primarily `DataSourceTransactionManager` and a driver that supports savepoints. See [[Does NESTED propagation require JDBC savepoints]].

**`REQUIRES_NEW`** needs suspension support and **pool headroom** for a second connection while the outer transaction remains suspended — see [[Why can REQUIRES_NEW exhaust the connection pool]] and [[Why can REQUIRES_NEW deadlock when inner and outer touch the same rows]].

Testing independent inner commit: [[How do you test that REQUIRES_NEW commits independently of the outer transaction]].

Contrast with joining `REQUIRED`: [[What is the difference between NESTED and REQUIRED propagation]].

> [!warning] `NESTED` is not “lightweight `REQUIRES_NEW`”
> Inner `NESTED` success does **not** persist independently of the outer transaction. If the outer rolls back later, nested rows disappear even when the inner scope completed cleanly.

> [!warning] Self-invocation breaks both
> `this.nested()` / `this.requiresNew()` on the same class bypasses the proxy; neither savepoints nor a second physical transaction appear. See [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **`NESTED` = one physical transaction + savepoint for partial rollback; outer rollback still undoes nested work. `REQUIRES_NEW` = separate physical transaction that can commit while the outer is open; outer rollback does not undo an already-committed inner.** `NESTED` reuses one connection; `REQUIRES_NEW` typically needs another while the outer is suspended.
