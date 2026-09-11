<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is pg_repack?

> [!abstract] Short answer
> An open-source PostgreSQL extension that removes table and index bloat online — the functional alternative to VACUUM FULL and CLUSTER without their long ACCESS EXCLUSIVE lock. It builds a compacted copy of the table while it stays writable, using triggers to catch concurrent changes, swaps the files at the end with only a brief exclusive lock, and requires a primary key or unique index on the table.

## How it works

1. Creates a temporary log table and an AFTER trigger on the target to record concurrent DML.
2. Copies the live data into a compacted copy (ordered per the chosen key, optionally CLUSTER order).
3. Creates the indexes on the copy.
4. Applies the changes accumulated in the log during the copy.
5. Briefly locks the table (ACCESS EXCLUSIVE), performs the final delta apply, and swaps the relfiles — the original bloated files are dropped.

```bash
pg_repack -d appdb -t orders          # online rebuild of one table
pg_repack -d appdb -t orders -o id    # online CLUSTER by id
pg_repack -d appdb -k                  # skip superuser check (owner-run)
```

**Listing 1.** Typical invocations; the tool must connect as a superuser (or use the owner-run flag with the extension installed).

```d2
src: "Bloated table\nwritable during whole run" {width: 300; height: 80}
cp: "Compact copy built\ntriggers log concurrent DML" {width: 330; height: 80}
apply: "Replay logged changes" {width: 280; height: 70}
swap: "Brief exclusive lock\nswap files, drop old" {width: 300; height: 80}
src -> cp -> apply -> swap
```

**Fig. 1.** The long phases run under normal DML; only the final swap needs the exclusive lock for a moment.

## Requirements and costs

- A primary key or unique index on the target table (the repack trigger and delta apply need it).
- Free disk roughly the size of the table plus its indexes during the run.
- Extra write amplification while the trigger is active; the copy phase competes for I/O — run it in low-load windows anyway.
- It cannot fix everything: tables without a usable key, and some catalog-heavy cases fall back to advice or refusal; permission model requires superuser or the documented owner setup.

The alternative ladder: tune autovacuum to prevent bloat ([[What is autovacuum in PostgreSQL]]), drop partitions when the schema allows ([[How does PostgreSQL declarative partitioning work]]), plain VACUUM for garbage collection ([[What is the difference between VACUUM and VACUUM FULL]]), and pg_repack when a rewrite is needed but VACUUM FULL's lock ([[What is ACCESS EXCLUSIVE in PostgreSQL]]) is unacceptable.

> [!warning] "Online" does not mean "free"
> pg_repack holds locks only briefly but consumes I/O and write capacity throughout, on a table whose every DML now also feeds a log table. Running it on the hottest table at peak traffic slows production and can stretch the final delta-apply window. And if the run dies mid-way it cleans up its copies — but the bloat remains exactly as it was.

> [!tip] Interview answer
> pg_repack is the online bloat remover: it copies the table into a compacted replacement while triggers log concurrent DML, replays the delta, and swaps files under a momentary exclusive lock. It needs a PK or unique index, free disk for the copy, and real I/O headroom — the production alternative to VACUUM FULL when downtime is not on the table.
