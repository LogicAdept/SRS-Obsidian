<!--
reps: 0
priority: 0
-->
#Databases #SRS

# How does Liquibase manage database schema changes

> [!abstract] Short answer
> **Liquibase turns schema changes into changesets — ordered, identifiable units stored in changelog files — and applies only the ones the target database has not yet run, tracking everything in the DATABASECHANGELOG table.** The changelog is the schema's version history; the tracking table is the ledger of what already happened on *this* database.

## The moving parts

A **changelog** is the root file listing changes; teams split it per feature and include the parts from the master file, which is Liquibase's mechanism for minimizing conflicts between teams. A **changeset** is the unit of change — create table, add column, any change type — uniquely identified by author + id + changelog path; the id does not order anything, file order does. Formats: XML, YAML, JSON, or plain SQL. Liquibase reads the **DATABASECHANGELOG** table (plus DATABASECHANGELOGLOCK) to know which changesets this database has already applied, then runs the pending ones with the `update` command; since 4.27 a DATABASECHANGELOGHISTORY table adds history beyond the ledger. Attributes control execution: preconditions sanity-check the state before destructive work, contexts and labels filter which changesets run in which environment, `runInTransaction` (on by default) wraps a changeset in a transaction, and `runAlways`/`runOnChange` re-execute on demand. Rollback is defined per changeset — declared inverse operations, generated for supported change types, or written by hand.

```xml
<changeSet id="1" author="vlad">
  <createTable tableName="orders">
    <column name="id" type="bigint"/>
    <column name="status" type="varchar(20)"/>
  </createTable>
</changeSet>
```

**Listing 1.** The atomic unit: one changeset, one change type — Liquibase records author:id plus file in DATABASECHANGELOG and never silently re-runs it.

```d2
direction: right
cl: "Changelog file(s)\nordered changesets" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
liq: "Liquibase update\ncompare with ledger" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
db: "DATABASECHANGELOG\nwhat already ran here" {
  width: 270
  height: 90
  style.fill: "#e8f5e9"
}
pending: "Pending changesets\napplied in order" {
  width: 230
  height: 80
  style.fill: "#ffebee"
}
cl -> liq
liq -> db: "read"
liq -> pending: "diff"
```

**Fig. 1.** The engine's loop: declared history minus recorded history equals what runs now — the same ledger idea as Flyway's schema history table.

> [!warning] The ledger is the source of truth — do not edit applied changesets
> Once a changeset is in DATABASECHANGELOG, editing its body creates a checksum mismatch (clearCheckSum territory) or silently diverging schemas; the fix for a mistake is a new changeset, not a rewrite. Second trap: putting several change types in one changeset — if the second statement fails you are inside a half-run unit (auto-commit boundaries vary by platform), which is why Liquibase's own best practice is one change per changeset. Related discipline: two branches adding changesets is a merge-ordering problem, covered in [[What merge strategies are important in database development]].

The comparison with Flyway: [[What is the difference between Liquibase and Flyway]]; the deployment choreography around migrations: [[How do you do blue-green deployments that include a database]].

> [!tip] Interview answer
> Liquibase keeps schema history as changelogs of changesets — each uniquely identified by author, id, and file — and maintains a DATABASECHANGELOG ledger per database. Update diffs declared against recorded and applies only pending changesets, with contexts and labels gating environments and per-changeset rollbacks defined or generated. Applied changesets are immutable; mistakes get new forward changesets.
