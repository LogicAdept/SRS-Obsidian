<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How would you explain MVCC PostgreSQL?

> [!abstract] Short answer
> Explain it as a design tradeoff: instead of locking rows for readers, PostgreSQL stores multiple versions of every row and lets each transaction select the version that existed when its snapshot was taken. The payoff is that a reporting query never blocks an `UPDATE` and vice versa; the cost is that cleanup becomes a background job — hence VACUUM, autovacuum, bloat, and the wraparound safety net.

## The one-sentence model

"PostgreSQL never overwrites a row in place. `UPDATE` inserts a new version and expires the old one; `DELETE` just expires it. Readers filter versions by snapshot, so they see a consistent view without locks." The full visibility mechanics live in [[What is MVCC in PostgreSQL]] and [[What are xmin and xmax in PostgreSQL]].

```d2
mvcc: "MVCC model" {width: 260; height: 80}
pro: "Wins\n- readers never block writers\n- no read locks, no lock queues\n- consistent snapshots for reports\n- rollback is cheap (no undo)" {width: 330; height: 150}
con: "Costs\n- dead tuples need VACUUM\n- bloat under long transactions\n- every update rewrites the row\n- wraparound must be managed" {width: 330; height: 150}
mvcc -> pro
mvcc -> con
```

**Fig. 1.** The interview answer should always present both sides: snapshot isolation wins, garbage-collection costs.

## Why not locks

Engines that keep one copy of a row (the classic "lock reader or writer" approach) either block readers behind writers or maintain undo segments to reconstruct pre-update images for readers. PostgreSQL chose the other route: pay space for versions up front and let vacuum reclaim them later. Rollback is then trivial — the old versions were never destroyed — which is also why a huge rolled-back transaction is fast to abort but leaves many dead tuples to vacuum.

## What it implies for the application

Isolation levels are snapshot rules, not lock rules: Read Uncommitted degenerates to Read Committed, and Repeatable Read sees no phantom reads, as covered in [[How does Repeatable Read prevent phantom reads in PostgreSQL]]. Write conflicts surface as serialization errors instead of long lock waits.

Follow-up questions come in a predictable set, and each maps to a specific mechanism: "where do old versions live?" — in the heap itself, stamped and later vacuumed ([[What is a dead tuple in PostgreSQL]]); "why does my table never shrink?" — vacuum reuses space but does not return it ([[What is the difference between VACUUM and VACUUM FULL]]); "what blocks cleanup?" — the oldest snapshot ([[Why do long-running transactions hurt PostgreSQL]]); "how do 32-bit transaction IDs survive?" — freezing plus wraparound protection ([[What is transaction ID wraparound in PostgreSQL]]). Answering the tradeoffs with these five mechanics is what separates a real understanding from the buzzword.

And every session that keeps a snapshot open — an idle-in-transaction session, a replication slot, a long prepared transaction — holds the vacuum horizon, described in [[Why do long-running transactions hurt PostgreSQL]].

> [!warning] Do not call MVCC "optimistic locking"
> Optimistic locking is an application pattern (check a version column, retry on conflict). MVCC is an engine storage strategy. Mixing these terms in an interview signals memorized buzzwords; if you need the application-level pattern, that is explicit locking or version checks, not MVCC.

## The two-sentence version for warm-up answers

"PostgreSQL stores old versions of rows so every reader sees a consistent snapshot without locks; writers add versions instead of overwriting. The garbage collector for those versions is VACUUM." From there the interviewer's next question picks the branch: isolation details ([[What are SQL transaction isolation levels]]), cleanup economics ([[What is autovacuum in PostgreSQL]]), or the physical layer ([[What are xmin and xmax in PostgreSQL]]).

> [!tip] Interview answer
> MVCC means PostgreSQL keeps old row versions so readers can work off a snapshot while writers keep writing — no read locks in either direction. You get clean isolation semantics and cheap rollback, and you pay with dead tuples, VACUUM and autovacuum, bloat if transactions hold snapshots, and wraparound management for the 32-bit transaction counter.
