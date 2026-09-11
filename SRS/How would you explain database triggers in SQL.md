<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **trigger** is procedural code bound to a table event: `CREATE TRIGGER name BEFORE|AFTER|INSTEAD OF INSERT|UPDATE|DELETE ON table FOR EACH ROW BEGIN ... END` (statement-level forms exist). Uses: audit logging, denormalized counters, enforcing complex invariants, computed-column upkeep. Costs: hidden write-time work, cascade complexity, and debugging opacity — modern designs prefer explicit constraints and application/services logic where possible ([[What integrity constraints exist in SQL]]).

The verified demo shows the canonical use: an AFTER UPDATE trigger appends to an audit table automatically — two UPDATEs produce two log rows with the schema, not the application, guaranteeing completeness. PostgreSQL's trigger documentation draws the taxonomy interviewers probe: timing BEFORE/AFTER/INSTEAD OF, granularity FOR EACH ROW versus FOR EACH STATEMENT, transition tables (REFERENCING NEW TABLE / OLD TABLE) for set-level access in statement triggers, and the firing-order caveat (multiple triggers fire in name order — a fragile dependency). The design judgment is the real question. Triggers guarantee *completeness* — audit logs and counter maintenance that survive every code path, including manual SQL — which no application layer can promise; that is their irreplaceable niche. Against them: they run synchronously inside the write's transaction (trigger latency is write latency), they are invisible in code review (the "what else happens on UPDATE?" surprise), they cascade (trigger writes firing more triggers), and they complicate migrations and replication ([[What harmful SQL patterns or pitfalls do you know]]). SQLite's version is smaller-scoped (row triggers only, RAISE for errors) but the same semantics — which the demo uses. The alternative stack: CHECK constraints for row invariants, FK cascades for referential actions, application events or transactional outbox for cross-service reactions — triggers where completeness inside the database is the requirement.

```sql
CREATE TABLE emp2 (id INTEGER PRIMARY KEY, name TEXT, salary NUMERIC);
CREATE TABLE audit_log (at TEXT, what TEXT);
INSERT INTO emp2 VALUES (1,'Greta',5000);
CREATE TRIGGER trg_salary AFTER UPDATE OF salary ON emp2
BEGIN
  INSERT INTO audit_log VALUES (datetime('now'), 'salary changed for ' || NEW.name);
END;

UPDATE emp2 SET salary = 5200 WHERE id = 1;
SELECT what FROM audit_log;
-- salary changed for Greta
UPDATE emp2 SET salary = 5300 WHERE id = 1;
SELECT COUNT(*) FROM audit_log;
-- 2
```

**Listing 1.** Verified on SQLite 3.53.1. Two unrelated UPDATEs from the client produce two audit rows — the trigger fires per row change regardless of who issues it; that completeness is the feature.

```d2
direction: right
w: "UPDATE emp2" {width: 140; height: 60}
t: "trigger fires
AFTER UPDATE OF salary" {width: 230; height: 80}
l: "audit_log INSERT
same transaction" {width: 180; height: 80}
c: "write commits
(data + log together)" {width: 200; height: 80}
w -> t -> l -> c
```

**Fig. 1.** The trigger rides the same transaction as the write: log and data commit atomically — the completeness guarantee that makes audit triggers worth their opacity.

> [!warning] Trigger work is invisible until it is the bottleneck — or the bug
> The UPDATE that "takes 3ms" may run three triggers writing three tables; the migration that "hangs" may fire a per-row trigger over 50M rows. Inventory triggers per table (PostgreSQL: pg_trigger; SQLite: sqlite_master), document their cost in the schema, and resist nesting trigger-on-trigger chains ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> A trigger is table-bound procedural code fired on INSERT, UPDATE or DELETE — before or after, per row or per statement — and my demo is the classic one: an AFTER UPDATE trigger keeping an audit log complete, in the same transaction as the write. I value triggers where completeness inside the database is the requirement: audit trails, invariant enforcement nothing can bypass. I weigh them against their costs — hidden write-time latency, debugging opacity, cascades — and reach for constraints, FK cascades or application events first, triggers when the guarantee must live in the database.
