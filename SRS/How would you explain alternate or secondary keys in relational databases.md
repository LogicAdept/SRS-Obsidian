<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/Indexes #SRS

# How would you explain alternate or secondary keys in relational databases

> [!abstract] Short answer
> An alternate key is a candidate key that was not chosen as the primary key but is still enforced unique — in SQL, a UNIQUE constraint. A secondary key is the corresponding index concept: any index other than the primary/clustered one. Both exist so rows are findable and unique by more than one attribute.

## Relational theory to SQL mapping

In relational theory, a table can have several candidate keys; the one you designate as primary leaves the others as alternate keys. SQL expresses an alternate key with a UNIQUE constraint, which creates a unique index that both enforces uniqueness and serves lookups — PostgreSQL's docs describe UNIQUE constraints adding a B-tree index on the column or group. Typical alternate keys: email on a users table whose PK is a surrogate id, or (tenant_id, external_ref) for an external identifier. A secondary key, strictly, is the index used for a non-primary access path: in InnoDB every index other than the clustered one is a secondary index, and its entries carry the primary key columns to relocate the row — the mechanism behind [[Is a primary key implemented as an index and why]].

```sql
CREATE TABLE users (
    id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email CITEXT NOT NULL,
    nick  TEXT   NOT NULL,
    UNIQUE (email),      -- alternate key
    UNIQUE (nick)        -- another alternate key
);
```

**Listing 1.** One primary key, two alternate keys; each UNIQUE constraint is a unique index and therefore a secondary access path.

## The two terms in one sentence, then the performance note

The clean formulation: alternate key is about which attribute sets are unique identifiers; secondary key is about which index you are not clustered by. The performance story follows from storage: in InnoDB a secondary index lookup hops through the primary key, so wide secondary keys and wide primary keys both cost; in SQL Server a nonclustered index on a clustered table stores the clustered key as its row locator, while on a heap it stores a physical RID; in PostgreSQL every index is secondary and carries heap TIDs. Covering turns a secondary key into a no-hop answer path, the INCLUDE design in [[How would you explain Covering index]], and uniqueness on the primary side is contrasted in [[What is the difference between PRIMARY KEY and UNIQUE constraints]].

> [!warning] "Secondary key" is not "a second primary key"
> The trap is calling an alternate key "another primary key": a table has exactly one primary key, but any number of alternate keys (UNIQUE constraints). Also, a secondary index need not be unique at all — most are not. In vendor glossaries (Oracle, MySQL, SQL Server) "secondary index" consistently means non-primary index, while "alternate key" is the theory/UNIQUE-constraint term; mixing them signals memorization, not understanding.

> [!tip] Interview answer
> Candidate keys not chosen as primary become alternate keys, enforced in SQL by UNIQUE constraints with their own unique indexes. Secondary key is the storage-side twin: any non-primary index, which in InnoDB carries the primary key to find the row and in PostgreSQL carries a heap pointer. So one table has one primary key, several alternate keys, and as many secondary indexes as its access paths need.
