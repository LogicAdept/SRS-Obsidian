<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Session #SRS

# How does Hibernate order SQL statements on flush?

> [!abstract] Short answer
> Flush does **not** replay your call order. Pending changes sit in the **`ActionQueue`** as typed action lists, and flush executes them in a **fixed order: inserts → updates → collection element deletions → collection element insertions → deletes** (each group preserving the order operations were queued). The order exists to keep **foreign keys satisfiable without deferred constraints**: a parent is inserted before its children, orphaned collection rows are deleted before fresh ones are inserted, and everything is deleted before the parent row goes. Two things bypass the queue entirely: **bulk HQL/JPQL `UPDATE`/`DELETE`** (no entity actions, no callbacks, stale first-level cache) and **`IDENTITY` inserts**, which execute immediately on `persist` ([[Why does GenerationType.IDENTITY disable JDBC batching]]) and therefore cannot be reordered with the rest.

## The order and why it is safe

```text
1. INSERT   entities, in persist order
2. UPDATE   entities (dirty checking results)
3. DELETE   collection rows  (removals, orphanRemoval)
4. INSERT   collection rows  (new elements)
5. DELETE   entities, in remove order
```

**Listing 1.** ActionQueue execution order on one flush.

Read it as a **dependency ordering**: step 1 puts parent rows in place so child `INSERT`s in step 4 can reference them; step 3 clears replaced collection rows before step 4 re-adds them (no duplicate-key fight between "the old tag row" and "the new tag row"); step 5 deletes parents **last**, after every dependent row is gone. Reorder a graph any way you like in Java — move a child from order A to order B, delete an invoice line and add two new ones, swap a `@OneToOne` — and the queue still produces constraint-safe SQL, on ordinary (non-deferred) foreign keys.

```java
Order order = em.find(Order.class, id);
order.getLines().clear();
order.getLines().add(new Line("sku-9", 2));   // same flush:
// DELETE order_lines WHERE order_id = ?      (step 3)
// INSERT INTO order_lines ...                (step 4)
```

**Listing 2.** Replace-all on a collection is one delete batch plus one insert batch — never interleaved row-by-row.

## What this means for your code

**Error timing moves.** A constraint violation surfaces at **flush** (commit time), not at the mutating call — a `DataIntegrityViolationException` at commit references an action queued seconds earlier. Debug accordingly: the Java statement that "caused" it is only the one that queued the action.

**One flush per transaction is the norm; multiple flushes segment the queue.** Call `flush()` mid-transaction (or rely on auto-flush before a query — [[What is Hibernate dirty checking]] covers `FlushMode.AUTO` overlap detection) and the pending batch executes *now*, in queue order, and a new queue starts. For **large writes** the segmentation is deliberate: flush+clear every N entities to keep the persistence context and the batch windows bounded ([[What is Hibernate performance tuning]] sizes the windows).

**`IDENTITY` inserts ignore all of this.** They fire at `persist` time, *before* the queue exists for them — which is also why a graph mixing `IDENTITY` children and `SEQUENCE` parents can execute its first insert earlier than any code that assumed queue order.

**Bulk operations do not enqueue at all.** `UPDATE ... WHERE` in HQL is one JDBC statement against the table: no dirty checking, no lifecycle callbacks ([[When do JPA entity lifecycle callbacks fire]] maps which transitions they do cover), no version bump of affected entities, and the **first-level cache is now stale** for rows it holds — mixing bulk writes with entity reads in one transaction is the classic source of "it shows the old value" bugs.

> [!warning] "I removed the parent, why did children go first?"
> They did not — collection element deletions (step 3) ran before the parent delete (step 5), which is what allowed the parent delete to succeed. If you see the *opposite* in logs, look for `CascadeType` misconfiguration or an `orphanRemoval` mapping that leaves rows for the database's own `ON DELETE` rule to clean. The queue order is a contract; when reality disagrees, the mapping, not the database, made the choice.

> [!tip] Interview answer
> Flush executes pending changes in a fixed ActionQueue order — inserts, updates, collection deletes, collection inserts, entity deletes — so foreign keys stay satisfiable without deferred constraints: parents before children, replaced collection rows out before new ones in, parents deleted last. Call order does not matter, error timing does: violations surface at flush. Two exceptions bypass the order — identity-id inserts run immediately on persist, and bulk HQL updates run as single statements with no callbacks and a stale first-level cache. For big writes I flush and clear in windows to bound the context and keep batches meaningful.

See [[What is Hibernate dirty checking]], [[What is Hibernate entity lifecycle states]], [[Why does GenerationType.IDENTITY disable JDBC batching]], and [[When do JPA entity lifecycle callbacks fire]].
