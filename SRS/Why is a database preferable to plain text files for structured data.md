<!--
reps: 0
priority: 0
-->
#Databases #SystemDesign/Tradeoffs #SRS

# Why is a database preferable to plain text files for structured data

> [!abstract] Short answer
> A database is preferred over files because it provides, out of the box, the four things structured data needs: transactions (atomic, durable multi-row changes), indexed access (queries without scanning everything), concurrent access with isolation (many readers and writers on consistent rules), and a schema with constraints that keeps the data valid. Files give you raw bytes and none of these guarantees — you end up rebuilding a database by hand.

## Guarantees a file cannot give

Atomicity is the first wall: updating a balance in a file means rewriting a region — a crash midway leaves a torn record. A database makes multi-row changes all-or-nothing with a write-ahead log, so a crash recovers to a consistent state ([[What are the ACID properties of database transactions]] names the whole set). Concurrency is the second: two processes appending to or rewriting one file corrupt it; a database arbitrates with locking or MVCC so writers do not clobber readers ([[What is MVCC in PostgreSQL]] shows the mechanism). Integrity is the third: types, NOT NULL, UNIQUE, foreign keys — constraints declared once and enforced on every write, whereas a file's validity lives in whoever last wrote it. The fourth is access: indexed lookups (see [[What is a database index and why does it speed up queries]]) find rows among millions in log time, while a text file needs a full scan or a hand-rolled index.

## What the file actually costs

The comparison is not aesthetics but the engineering you inherit. With a database you get a query language (ad-hoc analysis without new code), backup and recovery tooling, replication for availability ([[How would you explain database replication strategies]]), access control, and a mature planner. With files you rebuild each of those yourself — locking, partial-write recovery, secondary indexes, permissions — and every one of those reinventions becomes a bespoke, untested component. Files remain the right answer for genuinely unstructured or streaming data (logs, blobs, event archives), and that is exactly the boundary: structured, shared, mutable data goes to a database; unstructured or immutable bulk goes to files or object storage, often referenced from the database.

```text
crash during write:  file -> torn/partial record, manual repair
                     DB   -> transaction rolls back (WAL redo/undo)
two writers:         file -> lost update / interleaved corruption
                     DB   -> isolation (locks or MVCC) serializes effect
find rows:           file -> O(n) scan
                     DB   -> O(log n) index lookup + query planner
```

**Listing 1.** Three routine scenarios and where the plain file already fails.

> [!warning] The file format is not the problem — the missing guarantees are
> CSV or JSON is perfectly readable; the failure modes are torn writes, lost updates and unenforced validity. If your "file database" grows locking and journaling code, you are writing a database with worse tooling.

> [!tip] Interview answer
> A database packages the guarantees structured data needs — atomic durable transactions, concurrency control, declared constraints, indexed queries — plus tooling for backup, replication and access control. Files give raw bytes and none of that, so you would reimplement each guarantee poorly; files stay right only for unstructured or immutable bulk data.
