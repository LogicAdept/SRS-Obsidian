<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #SRS

# What is Envers and how do you audit entity changes?

> [!abstract] Short answer
> **Envers** is the Hibernate module that writes **entity history automatically**: mark a class **`@Audited`** and every insert/update/delete of that entity stores a **versioned copy of its state** in an audit table (`ENTITY_AUD`), linked to a **global revision** (`REVINFO`) that gets one row per transaction touching audited data. Reads go through the **`AuditReader`**: entity state at revision N, the list of revisions that touched an entity, diff queries ("who changed price between r10 and r20"). Semantics you must know: history rows are written by the **same transaction** as the change (strong consistency, extra write cost per row); **bulk HQL operations bypass audit** exactly as they bypass lifecycle callbacks; and audit history is **entity state history** — not a messaging log and not a substitute for an outbox. Configuration is annotation-driven, with `@NotAudited` exclusions and optional **modified-flag columns** per field.

## The model: versioned copies + a revision clock

Two table kinds carry the history. The **`_AUD` table** mirrors each audited entity's columns plus **`REV`** (revision number) and **`REVTYPE`** (`0` add, `1` mod, `2` del) — a delete writes a tombstone row, not a row removal. The **revision table** assigns a monotonic revision number per transaction, with a timestamp (and any custom data you configure — user name is the classic extension via a revision listener). Together they answer "state at revision N" by taking the newest `_AUD` row with `REV ≤ N` per primary key — the same as-on-date reconstruction any temporal design needs, prebuilt.

```java
@Entity
@Audited(withModifiedFlag = true)     // adds MOD_xx flag columns per field
public class Contract {
    @Id @GeneratedValue Long id;
    BigDecimal monthlyFee;

    @NotAudited                       // skip noisy, non-historical fields
    Set<AccessLog> accessLogs;
}

// "what did this contract look like at revision 42?"
Contract past = AuditReaderFactory.get(entityManager)
        .find(Contract.class, id, 42);
```

**Listing 1.** Audited entity and a point-in-time read. `withModifiedFlag` writes a boolean per column so "which fields changed in this revision" becomes a query, not a diff in application code.

## Queries the reader supports — and what they cost

The audit query API covers the standard historical needs: **entity at revision**, **revisions of an entity** (with metadata: timestamp, revision type, custom data), **entities modified in a revision**, and **restricted history queries** ("contracts whose fee was raised between r10 and r20") — all executed against the `_AUD` tables with the same SQL engine, so indexes on `(id, rev)` decide their speed. The cost side is mechanical: **every audited write copies the changed row** — write amplification proportional to audit table width. High-churn tables (counters, status watermarks) should be `@NotAudited` or carried by an event log instead: auditing is for **meaningful state**, not for every row that ever moved.

## The bypass list — the same three blind spots

Envers hooks the same entity-level machinery as lifecycle callbacks, so it inherits the same exclusions ([[When do JPA entity lifecycle callbacks fire]] lists them for callbacks):

1. **Bulk HQL `UPDATE`/`DELETE`** writes no history rows — a mass price update leaves the audit trail empty for exactly the change that touched the most rows.
2. **Native SQL** is invisible to it, by construction.
3. **Collection tables of value mappings** (element collections) need explicit `@Audited` on the collection; forgetting it silently drops history for that part of the aggregate.

The consistent rule: anything that bypasses the entity layer bypasses the audit layer. Where bulk paths are unavoidable, the audit requirement moves to a **trigger**, a CDC stream, or an explicit write to the history table in the same transaction — decided per path, not assumed.

## Audit history vs event log vs outbox

Three mechanisms, three questions. **Envers** answers *"what was the state of this row over time?"* — temporal queries, diffs, compliance — inside the same transaction, same database. An **event log** answers *"what happened, in what order, for other systems?"* — it is a messaging concern, and Envers rows are not messages: nothing consumes them downstream, they are queryable state. An **outbox** answers *"how do I publish the fact of this change atomically?"* — an integration concern ([[When do JPA entity lifecycle callbacks fire]] contrasts callbacks with outbox relays for the same reason). Teams conflate them and end up querying audit tables for integration logic or shipping messages from history tables; keep the questions separate and the mechanisms stay small.

> [!warning] Same transaction, same latency budget
> History rows commit atomically with the change — that is the feature: a rolled-back transaction leaves no phantom history. The price is that flush time includes the audit copies; a wide audited entity with modified flags turns one logical `UPDATE` into two rows' worth of writes. Measure with the audit tables populated at production widths, not with empty ones.

> [!tip] Interview answer
> Envers versions entities automatically: `@Audited` writes a copy of the row to an `_AUD` table with a revision number and type, one global revision per transaction, and the `AuditReader` answers point-in-time finds, per-entity revision lists, and diff queries. It commits atomically with the change, so history is never ahead of the data — for the cost of a row copy per write. The blind spots are the entity-layer ones: bulk HQL and native SQL bypass it entirely. I use it for compliance-grade state history of meaningful entities, keep event-log and outbox concerns on their own mechanisms, and flag high-churn fields `@NotAudited` so the write amplification stays proportional.

See [[When do JPA entity lifecycle callbacks fire]], [[What is Hibernate entity lifecycle states]], [[What is Hibernate dirty checking]], and [[How does Hibernate order SQL statements on flush]].
