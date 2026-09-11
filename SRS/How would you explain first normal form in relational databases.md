<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# How would you explain first normal form in relational databases

> [!abstract] Short answer
> **1NF requires every column to hold a single atomic value of one type — no repeating groups, no comma-packed lists, no nested tables.** Each row is uniquely addressable by a key over single-valued columns; that is what makes rows updatable, indexable, and joinable one at a time.

## What violates 1NF and what the fix looks like

A `phone_numbers` column containing `"+7 900 000-00-00, +7 911 111-11-11"` violates 1NF: two facts share one cell, so "find the account with phone X" needs string matching instead of an index, changing one phone means rewriting the whole string, and a third phone has nowhere to go without widening the column. The same applies to nested structures packed into TEXT/JSON *as the primary access path* — Codd's original point in 1970 was to replace such "non-simple domains" with relations: move the repeated fact into its own table keyed by the parent.

```sql
-- violates 1NF: repeating group packed into one cell
CREATE TABLE contacts_bad (
  id      int PRIMARY KEY,
  name    text,
  phones  text            -- "900...,911..." -- two facts, one cell
);

-- 1NF: one fact per row, keyed by parent
CREATE TABLE contacts (
  id      int PRIMARY KEY,
  name    text
);
CREATE TABLE contact_phones (
  contact_id int REFERENCES contacts,
  phone      text,
  PRIMARY KEY (contact_id, phone)
);
```

**Listing 1.** The 1NF repair of a repeating group: the phones become rows of their own relation, each addressable and indexable.

```d2
direction: right
bad: "contacts_bad\nphones: 'a,b,c'\none cell, many facts" {
  width: 250
  height: 90
  style.fill: "#ffebee"
}
good: "contacts + contact_phones\none fact per row\nindexable, FK-able" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
bad -> good: "decompose"
```

**Fig. 1.** 1NF is the gateway form: until cells are atomic, 2NF and 3NF — which talk about dependencies of fields on keys — cannot even be evaluated.

> [!warning] Atomic is relative to how you query — and JSON columns are not automatically a 1NF violation
> A date stored as DATE is atomic; the same timestamp split into three columns (`day`, `month`, `year`) is a worse violation of the same principle in reverse. And modern engines blur the line by design: PostgreSQL's arrays and JSONB, MySQL's JSON, MongoDB's documents — the value in the cell is *one value of a complex type* with its own query operators. The honest interview position: 1NF is about not packing independently-addressable facts into one string where you then need them as rows; a JSONB column queried as a document is a deliberate data-modeling choice, not the repeating-group disease.

The next two rungs depend on this one: [[How would you explain second normal form in relational normalization]] and [[How would you explain third normal form in relational databases]]; the whole ladder in [[What is normalization]].

> [!tip] Interview answer
> First normal form demands atomic, single-typed cells — no repeating groups or comma-packed lists — so each fact is its own row in some relation, addressable by key. The fix for a phone-list cell is a child table with one row per phone. Note the nuance: arrays and JSONB are typed single values with real operators; 1NF is violated when independently addressable facts hide inside one string.
