<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SystemDesign/Consistency #SystemDesign/Atomicity #SRS

# What is the difference between atomicity and consistency

> [!abstract] Short answer
> Atomicity is the all-or-nothing guarantee about a transaction's execution: either every operation in it applies, or none does — no partial effects survive a crash or abort. Consistency is the guarantee about the data's content: a transaction moves the database from one valid state to another, preserving declared invariants and the semantics the application relies on. Atomicity is a mechanism (undo/redo); consistency is an outcome (rules held) — the A and C in ACID.

## Atomicity: all-or-nothing execution

Atomicity says nothing about what the transaction does right — only that it does not half-do it. Transferring 100 from A to B is two updates; if the process dies after debiting A, atomicity guarantees the debit is rolled back (undo via the transaction log) — the transfer either happened or did not, never "half happened". The mechanism is the database's recovery machinery: rollback segments or the WAL ([[What is the PostgreSQL WAL]]) record enough to undo an aborted transaction's changes, so failures — crashes, errors, explicit rollbacks — leave no trace of the partial work. Isolation is a different letter (interference between concurrent transactions) and durability another (committed work survives crashes); conflating them with atomicity is the common interview error. [[What is atomicity in ACID transactions]] develops the mechanism; [[How do you handle transaction isolation anomalies]] the separate isolation axis.

## Consistency: valid state to valid state

Consistency says what "done" means: the database's declared rules — constraints, foreign keys, uniqueness, and the application's semantic invariants like "the sum of accounts is unchanged by a transfer" — hold before and after the transaction. The database enforces what is declared (constraints reject a negative balance); the application must supply the rest (the double-entry invariant lives in the transfer logic, not in a constraint). This is why the letter C is philosophically odd: the database guarantees consistency only relative to the rules it knows. The distributed-systems sense of the word — replica agreement, the ladder in [[How would you explain consistency in distributed systems and data stores]] — is a different concept again, and the trap in this question: a transaction can be perfectly atomic yet leave data inconsistent (a constraint was never declared, or the application wrote nonsense atomically), and vice versa at the system level.

```text
transfer(100, A, B):
  atomicity  -> both UPDATEs apply or neither (undo on crash)
  consistency-> A+B total preserved, balance >= 0 constraints hold
  atomic alone does NOT imply the rules; rules must be declared/enforced
```

**Listing 1.** One transfer, two different guarantees named.

> [!warning] Atomic writes of wrong data are still wrong
> A crash-safe, all-or-nothing transaction that sets balance = -1000 is atomic and consistent-by-mechanism, yet violates the business rule — because consistency only covers declared invariants. Declaring constraints is part of the consistency design, not a database bonus.

> [!tip] Interview answer
> Atomicity is the execution guarantee — all operations apply or none do, backed by undo/WAL recovery. Consistency is the state guarantee — the transaction moves valid data to valid data, holding declared constraints and semantic invariants. Atomicity is the mechanism the database provides; consistency is the outcome shared between declared rules and application logic.
