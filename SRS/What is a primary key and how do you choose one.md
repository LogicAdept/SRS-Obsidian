<!--
reps: 0
priority: 0
-->
#Databases/Keys #SRS

# What is a primary key and how do you choose one

> [!abstract] Short answer
> **A primary key is the candidate key chosen as a row's official identity: non-NULL, unique, minimal, and immutable by convention.** When several candidate keys exist, choose one by stability and narrowness — natural identifiers (email, SSN) change or leak; the default engineering answer is a meaningless surrogate (`bigint identity/sequence`, UUIDv7), with a unique constraint kept on the natural key.

## The rules, then the choice

Codd's 1970 paper frames the mechanism: a relation typically has one or more nonredundant domain combinations that uniquely identify each tuple — candidate keys; when more than one exists, one is "arbitrarily selected and called the primary key". SQL engines wrap that in hard guarantees: `PRIMARY KEY` = UNIQUE + NOT NULL, one per table, and rows become addressable by it. Uniqueness alone is not enough — the candidates' family and terminology live in [[How would you explain candidate keys in relational databases]], and the non-NULL edge in [[Can the same primary key value appear in two rows of one table]].

Choosing among candidates weighs four properties: **stability** (never changes over the row's life — renaming a natural value must not rewrite the foreign keys pointing at it), **simplicity/minimality** (short, single-column keys make cheaper indexes and smaller child-table FKs), **meaning-free-ness** (nothing outside the database may ever need the value to mean something), and **generation control** (no dependence on external systems). Natural keys that fail stability or privacy tests (emails change; national ids leak) push teams to surrogates: a sequence-backed `bigint` — compact, monotonic, index-friendly — or a UUID when ids must be generated outside the DB, preferably a time-ordered variant (UUIDv7) so B-tree inserts stay append-mostly.

```sql
CREATE TABLE users (
  id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  -- surrogate
  email text NOT NULL UNIQUE                              -- natural key kept honest
);
```

**Listing 1.** The default pattern: a meaningless surrogate as the primary key, with the natural identifier retained under a UNIQUE constraint — not discarded.

```d2
direction: right
nat: "Natural candidates\nemail · tax id · slug" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
judge: "Stable? Minimal?\nMeaning-free? Controlled?" {
  width: 250
  height: 100
  style.fill: "#fff3e0"
}
sur: "Surrogate PK\nidentity bigint / UUIDv7\n+ UNIQUE on natural key" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
nat -> judge -> sur: "usually fails one test"
```

**Fig. 1.** The selection pipeline: natural candidates rarely pass all four tests, so the surrogate wins — with the natural key kept as a uniqueness guarantee over the data itself.

> [!warning] "Add an id column" does not fix a wrong natural key — it hides it
> A table with a surrogate PK still needs a real business key under UNIQUE, or duplicates the surrogate was supposed to prevent reappear (two users, one email). And the surrogate's cost shows in clustering: with InnoDB's clustered index the primary key is physically the row order — a random UUID scatters inserts across the tree and bloats page splits, which is why UUID *version* choice is a performance question, not fashion. Composite natural keys are legitimate where the combination truly identifies the row (junction tables) — see [[How would you explain composite keys in relational databases]].

Relationships downstream of this choice: [[What is a foreign key]], [[What relationship types exist between database tables]], and the secondary-key view in [[How would you explain alternate or secondary keys in relational databases]].

> [!tip] Interview answer
> The primary key is the chosen candidate key: unique, non-NULL, minimal, immutable in practice. When several candidates exist I prefer a surrogate — identity bigint, or UUIDv7 when ids must come from the application — and keep the natural identifier under a UNIQUE constraint. Reasons: surrogates never need to change, keep child FKs narrow, and with clustered engines a monotonic key keeps inserts append-only.
