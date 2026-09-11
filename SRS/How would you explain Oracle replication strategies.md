<!--
reps: 0
priority: 0
-->
#Databases/Relational/Oracle #SystemDesign/Reliability #SystemDesign/Availability #SRS

# How would you explain Oracle replication strategies

> [!abstract] Short answer
> Oracle's flagship replication strategy is Data Guard: a standby database kept in sync with the primary by shipping redo (the Oracle WAL equivalent), in three protection modes — Maximum Protection (sync, zero data loss), Maximum Performance (async, default), and Maximum Availability (sync when possible, falling back to async). Standbys can be physical (block-for-block copies, openable read-only as Active Data Guard replicas) or logical (SQL-level, table-shaped). The same sync/async/semi-sync spectrum as other engines, named in Oracle terms.

## Data Guard: redo transport and protection modes

Data Guard streams redo records from the primary to standby databases over "redo transport services", and the protection mode is exactly the replication timing knob in [[How would you explain database replication strategies]]: Maximum Protection requires the standby to acknowledge every transaction synchronously — a primary cannot commit if the standby is unreachable, so data loss is zero and availability can suffer; Maximum Performance ships redo asynchronously — writes never wait, and the standby may lag by the transport delay; Maximum Availability commits synchronously while a standby responds and degrades to asynchronous when it does not, restoring sync when the standby catches up — semi-synchronous by policy. Physical standbys apply redo block-for-block and are byte-identical, which makes them usable as read-only reporting replicas when opened Active Data Guard style; logical standbys transform redo into SQL, allowing table-level shaping and rolling upgrades at the cost of datatype and DDL restrictions. Redo itself is the same machinery behind [[What is the PostgreSQL WAL]]-style durability: the log of changes is the replication payload.

## Where the other strategies fit

Inside a single cluster, Oracle RAC (Real Application Clusters) is not replication but shared-storage clustering — many instances mount one database, scaling connections and availability rather than copying data. Beyond Data Guard, Oracle historically offered Streams and Advanced/multi-master Replication for logical, bidirectional replication (multi-leader topology with conflict resolution) — both deprecated in favor of GoldenGate, Oracle's CDC platform for heterogeneous, low-latency logical replication across systems. The strategy decision follows the same axes as any engine: zero-data-loss and site failover (Data Guard sync/availability modes), read offload to replicas (Active Data Guard), heterogeneous distribution and integration (GoldenGate). Cross-engine context: [[How would you explain database replication strategies]] gives the general taxonomy, [[How would you explain MySQL replication strategies]] and [[How would you explain PostgreSQL replication strategies]] the concrete analogues.

```text
Maximum Protection:  commit waits for standby ack        (loss = 0)
Maximum Performance: commit returns; redo ships async    (loss = lag)
Maximum Availability: sync while possible, else async    (semi-sync)
physical standby: block-for-block, read-only open (Active DG)
logical standby:  SQL-level redo, table subset, rolling upgrades
```

**Listing 1.** Data Guard's modes and standby types in one view.

> [!warning] A protection mode is an availability commitment, not a setting
> Maximum Protection turns a standby outage into a primary write outage — by design. Modes are chosen against a written availability and data-loss budget; changing one silently changes what "committed" means for every application on the database.

> [!tip] Interview answer
> Oracle's answer is Data Guard: redo shipped to standbys in Maximum Protection (sync, zero loss), Maximum Performance (async, default) or Maximum Availability (sync with async fallback) modes; physical standbys serve read-only traffic via Active Data Guard, logical ones support rolling upgrades. Heterogeneous, low-latency distribution is GoldenGate — same sync/async tradeoffs as everywhere, in Oracle vocabulary.
