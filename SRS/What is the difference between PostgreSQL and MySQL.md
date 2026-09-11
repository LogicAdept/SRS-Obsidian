<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Relational/MySQL #SRS

# What is the difference between PostgreSQL and MySQL?

> [!abstract] Short answer
> PostgreSQL is one engine with one storage layer, a strict SQL-standard orientation, rich native types (arrays, jsonb, ranges, UUID, network), and MVCC snapshot isolation throughout. MySQL is engine-plural by history (InnoDB the default), reads slightly more lenient on SQL dialect, uses REPEATABLE READ with InnoDB's MVCC by default, and historically separates its feature set per engine. Replication: MySQL's classic binlog replication versus PostgreSQL's physical streaming plus logical replication.

## The structural differences

| Dimension | PostgreSQL | MySQL (InnoDB) |
|---|---|---|
| Storage engines | one | pluggable (InnoDB default) |
| Concurrency | MVCC, versions in heap | MVCC, undo logs; RR default |
| Isolation default | Read Committed | REPEATABLE READ |
| Types | arrays, jsonb, ranges, uuid, inet, composites | JSON type, simpler scalar set |
| DDL | transactional for most statements | implicit commit on DDL |
| Index types | B-tree, GIN, GiST, SP-GiST, BRIN, hash | B-tree (+ FULLTEXT, SPATIAL) |
| Replication | streaming physical + logical | binlog-based (statement/row) |
| Case sensitivity | unquoted identifiers fold to lower | table names per OS setting; strings per collation |

The isolation point deserves precision: InnoDB's default REPEATABLE READ uses consistent snapshots plus next-key locking against phantoms; PostgreSQL's RR is snapshot-only with serialization errors on write conflicts ([[How would you explain Repeatable Read PG]], [[What are SQL transaction isolation levels]]).

```d2
pg: "PostgreSQL\nsingle engine\nstandard-first, rich types" {width: 300; height: 90}
my: "MySQL\nengine plurality (InnoDB)\nweb-scale heritage" {width: 300; height: 90}
both: "Both: MVCC, InnoDB/PG b-trees,\nreplication ecosystems" {width: 380; height: 80}
pg -> both
my -> both
```

**Fig. 1.** The 2020s reality: convergence on the big things, divergence in types, DDL semantics and replication models.

## Practical divergences developers hit

- DDL: PostgreSQL can run ALTERs inside transactions and roll them back; MySQL DDL commits implicitly — schema migrations behave differently ([[How do you add a column to a large PostgreSQL table without downtime]] for the PG-side care).
- Grouping: MySQL historically allowed loose GROUP BY (ONLY_FULL_GROUP_BY toggles it); PostgreSQL enforces the standard strictly.
- String case: LIKE is case-sensitive in PostgreSQL (ILIKE exists), collation-dependent in MySQL.
- Upsert dialect: INSERT ... ON DUPLICATE KEY UPDATE versus ON CONFLICT ([[How does UPSERT work in PostgreSQL]]).
- Ecosystem defaults: the migration checklist lives in [[How would you migrate an application from MySQL to PostgreSQL]]; the replication comparison in [[How would you explain MySQL replication strategies]] and [[How would you explain PostgreSQL replication strategies]].

> [!warning] "MySQL is faster, PostgreSQL is stricter" is a 2010s meme
> Modern MySQL 8 is a serious MVCC engine and modern PostgreSQL scales writes well; measured workloads decide. The durable differences are structural: transactional DDL, type richness, index variety and the two replication families — not a blanket speed verdict. Choosing by meme produces migrations that fix nothing ([[How would you explain common ways to optimize SQL queries]] — the workload decides there too).

> [!tip] Interview answer
> Structurally: PostgreSQL is a single engine with strict standards behavior, transactional DDL, rich types and index families (GIN, GiST, BRIN), Read Committed default and snapshot RR without phantoms. MySQL's InnoDB defaults to REPEATABLE READ with next-key locking, has engine plurality, non-transactional DDL, and binlog-based replication. Replication and migration ergonomics differ more today than raw performance.
