<!--
reps: 0
priority: 0
-->
#Databases #SRS

# What is a database

> [!abstract] Short answer
> **A database is an organized collection of related information treated as a unit, managed so that applications can store, update, and retrieve it reliably.** The software that provides that management — storage layout, querying, transactions, recovery, access control — is the DBMS; "PostgreSQL" or "MySQL" name DBMS products, not the data itself.

## The definition in practice

The line between "data" and "a database" is organization. A folder of CSV files holds data, but nobody coordinates two processes writing the same file, and nothing stops a half-written export from lying about totals. A database is the collection of information **plus the guarantee that it stays consistent**: the storage is structured so related pieces can be found and joined, concurrent readers and writers are coordinated, and committed changes survive a crash. That is why the classic definition emphasizes the purpose — to collect, store, and retrieve **related** information — rather than the medium it lives on.

The DBMS is what delivers those guarantees. PostgreSQL, MySQL, Oracle Database, SQL Server, MongoDB, and Redis are all DBMS products; they differ in the data model they expose (relational tables, documents, key-value), but each controls where bytes live, answers queries against them, and hides the messy parts — page layouts, caches, crash recovery — from applications. An application sees a connection, a query language, and a transaction boundary; the DBMS owns everything below that line.

```d2
direction: right
app: "Application\n(sends SQL / queries)" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
dbms: "DBMS\nquery processing · transactions\nlocks · WAL / recovery · security" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
disk: "Stored data\n(organized collection)" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
app -> dbms: "query / commit"
dbms -> disk: "reads and writes pages"
```

**Fig. 1.** The application talks to the DBMS, and only the DBMS touches the stored collection — that boundary is what makes the data safe to share.

## What the DBMS layer actually buys you

Concretely, a DBMS provides: a declarative query language (SQL for relational systems) so you ask *what* you want, not *how to scan*; **transactions** with ACID semantics so multi-step changes are all-or-nothing; **concurrency control** (MVCC in PostgreSQL and InnoDB) so readers and writers do not clobber each other; **durability** via write-ahead logging, so a committed transaction survives a power cut; **constraints** (foreign keys, unique, CHECK) so invalid data is rejected at the border; and administration features — backup, replication, access control. None of these come free with a file format; each is a subsystem the product maintains for you.

> [!warning] "Database" in job titles usually means the DBMS
> People say "the database is down" when the **server process** (the DBMS) is down, and "we moved the database to another host" when they moved the DBMS instance. The data collection itself can also be meant — as in "the production database holds 2 TB". Which one is meant is almost always clear from context, but in interviews be precise: the data is the collection, the DBMS is the software managing it, and a *schema* is the structure imposed on it.

See [[How would you explain what a database management system provides]] for the DBMS subsystem list, and [[What is a database index and why does it speed up queries]]-adjacent mechanics in [[How do database indexes work at a high level]] for the first example of what the DBMS does under a query.

> [!tip] Interview answer
> A database is an organized collection of related information managed as a unit. The DBMS is the software that manages it — it owns storage, query processing, transactions, concurrency, and recovery, and exposes a query language to applications. PostgreSQL or MongoDB are DBMS products; the term "database" often names the instance in speech, but strictly it is the data collection and its structure.
