<!--
reps: 0
priority: 0
-->
#Databases/SQL/DDL #Databases/Relational/PostgreSQL #SRS

# How would you explain CREATE TABLE syntax in SQL

> [!abstract] Short answer
> **`CREATE TABLE` defines a new table: its columns, their types, the constraints, and the storage/partitioning strategy.** The SQL standard form is `CREATE TABLE name (column_def, ..., table_constraint, ...)`; PostgreSQL extends it with `IF NOT EXISTS`, `GENERATED ALWAYS AS IDENTITY`, `STORED` generated columns, `PARTITION BY`, `TABLESPACE`, `WITH (storage_parameters)`, and `INHERITS`. Each column has a name, a type, and optional modifiers (`NOT NULL`, `DEFAULT`, `PRIMARY KEY`, `UNIQUE`, `CHECK`, `REFERENCES`, `GENERATED ... AS IDENTITY`).

## The major clause families

```sql
CREATE [ TEMPORARY | TEMP | UNLOGGED ] TABLE [ IF NOT EXISTS ] name (
    column_name data_type [ COLLATE collation ]
        [ column_constraint [, ...] ]
        [ GENERATED ALWAYS AS (expr) STORED
        | GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ (seq_options) ] ]
    [, ...]
    [ table_constraint [, ...] ]
)
[ PARTITION BY { RANGE | LIST | HASH } ( column_list ) ]
[ WITH ( storage_parameter = value [, ...] ) ]
[ TABLESPACE tablespace_name ]
```

**Listing 1.** The PostgreSQL `CREATE TABLE` synopsis. The column list mixes column definitions and table constraints in any order; the optional trailing clauses control partitioning, storage parameters, tablespace, and (not shown) inheritance.

The column constraints are `NOT NULL`, `NULL`, `DEFAULT expr`, `PRIMARY KEY`, `UNIQUE`, `CHECK (expr)`, `REFERENCES other(col) [MATCH ...] [ON DELETE ...] [ON UPDATE ...]`, `GENERATED ALWAYS AS (expr) STORED`, and `GENERATED ... AS IDENTITY`. The table constraints are the same except they apply to one or more columns (`PRIMARY KEY (a, b)`, `UNIQUE (a, b)`, `CHECK (a < b)`, `FOREIGN KEY (a, b) REFERENCES other(c, d)`, `EXCLUDE USING ...`).

```d2
direction: right
name: "table name\n[IF NOT EXISTS]" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
cols: "column definitions\nname + type + constraints" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
cons: "table constraints\nPRIMARY KEY / UNIQUE / CHECK / FK / EXCLUDE" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
opt: "options\nPARTITION BY / WITH / TABLESPACE / INHERITS" {
  width: 320
  height: 70
  style.fill: "#fce4ec"
}
name -> cols -> cons -> opt
```

**Fig. 1.** The `CREATE TABLE` clause families. After the name comes a parenthesized list of column definitions and table constraints in any order, followed by optional clauses for partitioning, storage parameters, tablespace, and inheritance.

## Verified on PostgreSQL 17.11

A single `CREATE TABLE` for `departments` and `employees` that exercises most clause families, plus a partitioned `events` table. The introspection queries confirm what the schema ended up with.

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS employees CASCADE")
    adm.execute("DROP TABLE IF EXISTS departments CASCADE")
    adm.execute("DROP TABLE IF EXISTS events CASCADE")

    adm.execute("""
        CREATE TABLE departments (
            dept_id   int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name      text NOT NULL UNIQUE,
            budget    numeric(12,2) CHECK (budget >= 0)
        )
    """)
    adm.execute("""
        CREATE TABLE employees (
            emp_id    bigserial PRIMARY KEY,
            dept_id   int NOT NULL REFERENCES departments(dept_id) ON DELETE CASCADE,
            email     text,
            salary    numeric(10,2),
            hired_at  date NOT NULL DEFAULT CURRENT_DATE,
            terminated_at date,
            CONSTRAINT email_unique UNIQUE (email),
            CONSTRAINT salary_sane CHECK (salary > 0),
            CONSTRAINT term_after_hire CHECK (terminated_at IS NULL OR terminated_at >= hired_at)
        )
    """)
    adm.execute("""
        CREATE TABLE events (
            id bigint,
            occurred_at timestamptz NOT NULL,
            payload jsonb
        ) PARTITION BY RANGE (occurred_at)
    """)
    adm.execute("""
        CREATE TABLE events_2026_01 PARTITION OF events
            FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')
    """)
    adm.execute("CREATE TABLE IF NOT EXISTS departments (dept_id int, name text)")
    print("CREATE TABLE IF NOT EXISTS on existing table: no error (notice issued)")

with psycopg.connect(DSN, autocommit=True) as r:
    cur = r.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'employees'
        ORDER BY ordinal_position
    """)
    print("employees columns:")
    for row in cur.fetchall():
        print(f"  {row[0]:18s}  {row[1]:20s}  nullable={row[2]}  default={row[3]}")

    cur = r.execute("""
        SELECT conname, contype
        FROM pg_constraint
        WHERE conrelid = 'employees'::regclass
        ORDER BY conname
    """)
    print("employees constraints:")
    for row in cur.fetchall():
        kind = {'p':'PRIMARY KEY','f':'FOREIGN KEY','u':'UNIQUE','c':'CHECK','x':'EXCLUDE'}[row[1]]
        print(f"  {row[0]:30s}  {kind}")

    cur = r.execute("""
        SELECT relname, relkind, partstrat
        FROM pg_class c
        LEFT JOIN pg_partitioned_table p ON p.partrelid = c.oid
        WHERE relname IN ('events','events_2026_01')
        ORDER BY relname
    """)
    print("partitioning:")
    for row in cur.fetchall():
        print(f"  {row[0]:20s}  relkind={row[1]}  partstrat={row[2]}")

    cur = r.execute("""
        SELECT c.column_name, c.identity_generation
        FROM information_schema.columns c
        WHERE c.table_name = 'departments' AND c.identity_generation IS NOT NULL
    """)
    print("identity columns in departments:")
    for row in cur.fetchall():
        print(f"  {row[0]}  generation={row[1]}")
```

**Listing 2.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
CREATE TABLE IF NOT EXISTS on existing table: no error (notice issued)

employees columns:
  emp_id              bigint                nullable=NO  default=nextval('employees_emp_id_seq'::regclass)
  dept_id             integer               nullable=NO  default=None
  email               text                  nullable=YES  default=None
  salary              numeric               nullable=YES  default=None
  hired_at            date                  nullable=NO  default=CURRENT_DATE
  terminated_at       date                  nullable=YES  default=None

employees constraints:
  email_unique                    UNIQUE
  employees_dept_id_fkey          FOREIGN KEY
  employees_pkey                  PRIMARY KEY
  salary_sane                     CHECK
  term_after_hire                 CHECK

partitioning:
  events                relkind=p  partstrat=r
  events_2026_01        relkind=r  partstrat=None

identity columns in departments:
  dept_id  generation=ALWAYS
```
**Listing 3.** Verified on PostgreSQL 17.11. The `employees` table has a `bigserial` PK (auto-created sequence + `NOT NULL`), a `NOT NULL` FK with `ON DELETE CASCADE`, a `DEFAULT CURRENT_DATE`, two `CHECK` constraints (one a column-level expression, one a multi-column check), and a `UNIQUE` constraint. The `events` table is partitioned by `RANGE (occurred_at)`; its partition `events_2026_01` has `relkind=r` (regular table) and `partstrat=NULL` (it is a partition, not a partitioned table). The `departments` table uses `GENERATED ALWAYS AS IDENTITY` instead of `serial` — the modern, SQL-standard way to get an auto-incrementing column.

## `serial` vs `GENERATED ALWAYS AS IDENTITY`

PostgreSQL offers two ways to get an auto-incrementing column. `serial` / `bigserial` is the original PostgreSQL extension: it creates a sequence, sets the column's `DEFAULT` to `nextval(seq)`, and grants the same owner. `GENERATED ... AS IDENTITY` is the SQL-standard syntax added in PostgreSQL 10. It also creates a sequence, but the sequence is tied to the column (`OWNED BY`) and the column is implicitly `NOT NULL`. `IDENTITY` columns are easier to manage (`ALTER TABLE ... ALTER COLUMN ... RESTART WITH n`) and are portable to other SQL-standard databases. For new schemas, prefer `IDENTITY`; for compatibility with existing PostgreSQL code or with ORMs that expect `serial`, use `serial`.

## Partitioning and `PARTITION OF`

A partitioned table is created with `PARTITION BY { RANGE | LIST | HASH } (column_list)`. Each partition is created with `CREATE TABLE part PARTITION OF parent FOR VALUES ...`. The partition's columns and constraints are inherited from the parent; you can add additional constraints per partition. PostgreSQL 17 supports partition-wise joins, partition pruning at plan time, and runtime pruning. A partition can itself be partitioned (sub-partitioning). See [[How do you add a column to a large PostgreSQL table without downtime]] for how partitioning helps with online schema changes on large tables.

> [!warning] `CREATE TABLE IF NOT EXISTS` is a notice, not an error — and it does not check schema
> If a table with the same name already exists, `CREATE TABLE IF NOT EXISTS` emits a `NOTICE` and does nothing — even if the column definitions in the new `CREATE TABLE` are completely different from the existing one. This is intentional: the command is for idempotent migrations. The trap is using it in CI to "ensure the table exists" and missing that the table's schema has drifted. Always pair `IF NOT EXISTS` with a separate `ALTER TABLE` migration step that brings the schema to the desired shape; do not rely on `IF NOT EXISTS` to enforce schema.

> [!warning] A `CHECK` constraint is satisfied by `NULL`
> A `CHECK (col > 0)` constraint passes when `col IS NULL`, because the expression evaluates to `NULL`, which is treated as "not false" by the SQL standard. To enforce that a column is both non-null and positive, you need both `NOT NULL` and `CHECK (col > 0)`. This is a common interview trap — `CHECK` does not enforce non-nullity. See [[How do generated columns work in PostgreSQL]] for the same rule applied to generation expressions.

> [!warning] `UNIQUE` and `PRIMARY KEY` on a partitioned table must include the partition key
> PostgreSQL 17 requires that every unique constraint on a partitioned table includes all the partition key columns. The reason is that uniqueness must be enforceable per-partition — without the partition key in the unique constraint, two rows in different partitions could violate uniqueness without either partition noticing. This is a frequent surprise when migrating a non-partitioned table to a partitioned one: a `UNIQUE (email)` constraint that worked on the original table must become `UNIQUE (email, occurred_at)` (or whatever the partition key is) on the partitioned version, which weakens the uniqueness guarantee. The standard fix is a separate unique index on a non-partitioned "lookup" table or to enforce uniqueness at the application layer.

> [!tip] Interview answer
> `CREATE TABLE` defines a new table: column definitions (name + type + constraints) and table constraints (`PRIMARY KEY`, `UNIQUE`, `CHECK`, `FOREIGN KEY`, `EXCLUDE`), followed by optional clauses like `PARTITION BY`, `WITH (storage_parameters)`, and `TABLESPACE`. PostgreSQL offers `serial`/`bigserial` (legacy) and `GENERATED ... AS IDENTITY` (SQL standard) for auto-incrementing columns, and supports `GENERATED ALWAYS AS (expr) STORED` for generated columns. `IF NOT EXISTS` is a notice, not an error, and does not check schema. `CHECK` is satisfied by `NULL`; pair it with `NOT NULL` for non-null-and-positive. On a partitioned table, `UNIQUE` and `PRIMARY KEY` must include the partition key. Related: [[How would you explain DDL DML and DCL in SQL]] and [[What is an exclusion constraint in PostgreSQL]].
