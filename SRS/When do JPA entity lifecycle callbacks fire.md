<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Session #Java/Persistence/JPA #SRS

# When do JPA entity lifecycle callbacks fire?

> [!abstract] Short answer
> Seven hooks fire on **entity lifecycle transitions driven by the persistence context**: `@PrePersist`/`@PostPersist`, `@PreUpdate`/`@PostUpdate`, `@PreRemove`/`@PostRemove`, `@PostLoad`. **`Pre`** callbacks run inside the ongoing operation **before** the SQL effect (before the `INSERT`/`UPDATE`/`DELETE` is emitted, in the same transaction), **`Post`** run after it (after insert or at commit time for deferred actions — do not build timing logic on `Post*`). They fire on **`persist`/`merge`/`remove`/`find`/refresh/load** — and they do **not** fire for **bulk HQL `UPDATE`/`DELETE`**, which bypasses entity loading entirely. Callbacks may live on the entity (no-arg methods) or in external classes wired with **`@EntityListeners`**; exceptions from a `Pre` callback abort the operation and roll back the transaction. Classic use: audit timestamps. Heavy logic belongs to module-level listeners, not to callbacks that pretend to be transactions.

## The trigger map

| Callback | Fires on | Typical use |
| --- | --- | --- |
| `@PrePersist` | before `INSERT` (at `persist` for identity ids, at flush otherwise) | set `createdAt`, defaults |
| `@PostPersist` | after `INSERT` becomes effective | light notifications |
| `@PreUpdate` | before `UPDATE` at flush | set `updatedAt` |
| `@PostUpdate` | after `UPDATE` becomes effective | — |
| `@PreRemove` | before `DELETE` (or at `remove` for immediate effects) | snapshot/archive |
| `@PostRemove` | after `DELETE` | — |
| `@PostLoad` | after state loaded into a managed entity | derived field init |

Three timing subtleties matter in practice. First, **`@PrePersist` and `@PreUpdate` are flush-time events for sequence-based ids** — if you rely on `createdAt` being set the moment you call `persist`, you are wrong on exactly the id strategies where batching matters ([[Why does GenerationType.IDENTITY disable JDBC batching]] explains when inserts run early). Second, **`@Post*` for updates and deletes runs when the action executes, which with write-behind may be well after the mutation call** — code that "sends the event" in `@PostUpdate` runs inside the flush, inside the transaction, not when the business operation returns. Third, **`merge` fires `@PrePersist`/`@PreUpdate` on the target depending on whether the state becomes a new insert or an update** — detached-graph merges may surprise you with one or the other per entity.

## Listeners, ordering, and limits

```java
public class TimestampsListener {
    @PrePersist void onCreate(Object e) { setCreated(e); }
    @PreUpdate void onUpdate(Object e)  { setUpdated(e); }
}

@Entity
@EntityListeners(TimestampsListener.class)
class Order {
    @Id @GeneratedValue Long id;
    @PrePersist void also() { version = 0; }   // entity's own callbacks
}
```

**Listing 1.** External listener plus entity callback. The order for one event: default listeners (from mapping metadata), mapped-superclass listeners and callbacks, `@EntityListeners` in declaration order, then the entity's own methods.

Hard limits, all from "the callback runs inside the provider's own flush/load machinery": no access to the `EntityManager` for new operations (the persistence context is mid-flush — persisting *another* entity from `@PrePersist` is undefined-behavior territory), no guarantee about ordering relative to other pending actions beyond the `ActionQueue` rules ([[How does Hibernate order SQL statements on flush]] is the mechanism that schedules the SQL these callbacks bracket), and **no execution at all for bulk queries** — a mass `UPDATE` in HQL touches millions of rows and fires zero callbacks, zero dirty checking, zero validation. Teams who discover this in production move the invariant to a database trigger or keep bulk operations out of paths that need side effects.

**Rollback semantics**: a runtime exception from a `Pre` callback aborts the operation and marks the transaction rollback-only; the entity state is left *not* persisted. Treat `Pre` callbacks as validation gates — cheap, deterministic checks — and never as a place for remote calls, long computations, or anything that would make flush latency spike.

## Callbacks vs real tooling

For **audit trails** (who changed what, with history), callbacks only stamp time — a full history needs versioned copies of rows or an event stream ([[What is Envers and how do you audit entity changes]] covers the versioned-copies approach). For **cross-entity orchestration**, callback order between different entities during one flush is an implementation detail of the flush queue — building business flows on it produces code that breaks on the first reorder. The honest separation: callbacks for **invariants of this entity's own state**, module listeners for **reaction to state changes**, integration messaging for **other systems**.

> [!warning] A callback is not an event bus
> `@PostUpdate` runs inside the flush, inside the transaction, possibly before other pending actions of the same commit. Publishing to a message broker from there couples the broker's availability to your flush, and the message may still be followed by a rollback of everything else in the transaction. Outbox-style tables written by the same transaction — read by a relay — exist precisely because of this.

> [!tip] Interview answer
> Lifecycle callbacks bracket the SQL the persistence context emits: `Pre*` before the insert/update/delete in the same transaction, `Post*` after it becomes effective, `@PostLoad` after loading. They fire on entity-driven operations only — bulk HQL bypasses them completely, which is the gotcha people hit first. I use them for timestamps and cheap invariants on the entity's own state, via `@EntityListeners` so the domain class stays clean, and I never call the `EntityManager`, the network, or other entities' flushes from inside — anything heavier belongs to outbox tables or module-level listeners.

See [[What is Hibernate entity lifecycle states]], [[What is Hibernate dirty checking]], [[What is Envers and how do you audit entity changes]], and [[How does Hibernate order SQL statements on flush]].
