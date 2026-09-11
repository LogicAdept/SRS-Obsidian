<!--
reps: 0
priority: 0
-->
#Databases/Relational/MySQL #SystemDesign/Reliability #SystemDesign/Availability #SRS

# How would you explain MySQL replication strategies

> [!abstract] Short answer
> MySQL's core strategy is single-leader asynchronous replication: the source writes a binlog and replicas pull and apply it, returning immediately without waiting — fast writes with replication lag. Strategy upgrades: semi-synchronous replication waits for one replica to acknowledge receipt; GTID-based replication names transactions globally so failover and repairs no longer track file offsets; Group Replication provides a multi-leader quorum cluster. Row-based, statement-based and mixed binlog formats define what is shipped.

## Async as the base, semi-sync as the middle

Default MySQL replication is asynchronous: the source commits and returns; replica threads (I/O thread into its relay log, SQL thread applying) trail behind. Reads through replicas are therefore potentially stale — the read-side consequence described in [[What is eventual consistency]] — and a source crash can lose transactions that had not shipped. Semi-synchronous replication closes most of that gap: the source waits until at least one replica has received (not necessarily applied) the transaction's events, with a wait point configurable at AFTER_SYNC (acknowledge before committing to storage engines) or AFTER_COMMIT; if no semi-sync replica responds within the timeout, the source degrades to asynchronous rather than blocking — availability preserved, guarantee temporarily softened. This is the semi-sync strategy of [[How would you explain database replication strategies]] implemented as a pair of plugins, and it is the standard answer when "we can lose nothing but cannot pay full synchronous latency".

## Binlog formats, GTIDs and Group Replication

What is shipped depends on the binlog format: statement-based logs the SQL text (small, but nondeterministic statements can diverge), row-based logs the changed rows (deterministic, larger — the modern default), mixed switches per statement. GTID-based replication gives every transaction a global identifier (source's UUID plus sequence number), so a replica knows exactly which transactions it has — failover becomes "the most advanced GTID wins" and a new replica repositions itself automatically instead of hunting binlog file offsets; delayed replicas are a related strategy for recovering from logical corruption. Group Replication goes further: servers form a quorum-based group (Paxos-backed) where transactions are certified across members — a multi-leader or single-leader cluster with automatic failure detection and election, trading write latency for built-in availability. Scaling read traffic stays the classic pattern ([[How do NoSQL databases scale compared with SQL databases]]'s replica stage), while splitting writes moves to sharding ([[How would you explain horizontal database sharding]]).

```text
async:     source commits -> returns; replicas apply later (lag, loss risk)
semi-sync: source waits for 1 replica recv (AFTER_SYNC/COMMIT), else falls back
GTID:      id = source_uuid:seq -> failover by GTID comparison, no offsets
Group Rep.: quorum certification, auto election (multi/single leader)
```

**Listing 1.** The strategy ladder: async → semi-sync → GTID → Group Replication.

> [!warning] "Received" is not "applied"
> Semi-synchronous acknowledgement means the replica holds the transaction, not that clients reading it will see it — replication lag and read-your-writes still need handling (sticky reads, GTID waits such as WAIT_FOR_EXECUTED_GTID_SET). Assume the guarantee one level weaker than the feature name suggests.

> [!tip] Interview answer
> MySQL replicates single-leader asynchronously through the binlog by default — fast, with lag and loss risk. I add semi-sync when one acknowledged replica matters, GTIDs to make failover and repositioning automatic, row-based format for determinism, and Group Replication when we need a quorum cluster with automatic election — the same sync/async tradeoffs as every engine, in MySQL's ladder.
