<!--
reps: 0
priority: 0
-->
#Databases #SRS

# How would you explain what a database management system provides

> [!abstract] Short answer
> **A DBMS turns raw storage into a safe, shared, queryable resource: it controls storage and retrieval, executes queries, enforces transactions and constraints, coordinates concurrent access, recovers after crashes, and manages security and backups.** The application declares *what* data it wants; the DBMS supplies *how* to make that correct and fast.

## The subsystem list, from top down

At the top sits the **query processor**: it parses SQL, plans it (choosing indexes, join order, scan methods — visible in PostgreSQL's EXPLAIN or MySQL's EXPLAIN), and executes it. Below that, the **transaction manager** provides ACID semantics: atomicity through rollback of unfinished work, isolation through MVCC or locking (PostgreSQL uses multiversion snapshots; InnoDB offers four isolation levels with gap and next-key locks), and durability through a **write-ahead log** — PostgreSQL's WAL, InnoDB's redo log — which is fsynced before a commit returns.

The **storage engine** decides the physical layout: heap or clustered tables, page sizes (8 kB in PostgreSQL, 16 kB in InnoDB), and index structures such as B-trees. The **constraint system** — primary and foreign keys, unique, CHECK, NOT NULL — rejects invalid data at write time, which is why [[How do you add constraints to a database]] is a DBMS feature and not an application convention. Around these sit **concurrency control** (locks, snapshots, deadlock detection), **recovery** (crash replay from the log), **access control** (roles, privileges, row-level security), and **administration** tooling: backup and point-in-time recovery, replication, statistics collection.

```d2
direction: down
api: "SQL interface\n(parse, plan, execute)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
tx: "Transactions\nACID · isolation · locks" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
storage: "Storage engine\nheap / B-tree · buffers" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
wal: "Log and recovery\nWAL / redo · backup" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
api -> tx
tx -> storage
storage -> wal: "log before apply"
```

**Fig. 1.** A DBMS stacks a query interface over transaction management over physical storage, with the write-ahead log guarding every change.

## Why not put this in the application

Reimplementing "just store rows in files" means rewriting lock tables, crash replay, cache eviction, and query optimization — poorly. The DBMS concentrates forty years of engineering on exactly the problems applications get subtly wrong: torn pages on crash, lost updates under load, plans that fall off a cliff after a statistics change. When the DBMS is a relational one it also gives you the relational model — data as sets of tuples over declared domains — which is what normalization and SQL both build on.

> [!warning] The DBMS provides mechanics, not business meaning
> A foreign key guarantees referential integrity, but it cannot know that "canceled orders must keep their line items for audit" is your business rule. Teams that assume the database "protects everything" skip CHECK constraints and write broken invariants in application code that three services bypass. Know which guarantees you enabled — isolation level, constraint set, durability settings like `synchronous_commit` — and which the default configuration does **not** give you.

Compare this role with the definition card [[What is a database]], and with the query-side view in [[How do you use EXPLAIN ANALYZE in SQL]].

> [!tip] Interview answer
> A DBMS provides storage and retrieval under guarantees: a query language with a planner, ACID transactions with isolation and a write-ahead log for durability, concurrency control via MVCC or locks, constraints for integrity, plus recovery, security, and backup machinery. It means the application states what it wants and the DBMS makes it correct, consistent, and fast.
