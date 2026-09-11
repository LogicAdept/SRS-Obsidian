<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# How do you optimize a search query over several columns

> [!abstract] Short answer
> The shape decides the tool. Fixed columns with AND: one composite in equality-then-sort order. OR across columns: expect bitmap combination at best and prefer rewriting as UNION ALL of per-column indexed seeks. One search term across many columns: one expression — a concatenated or generated searchable field — indexed with FTS or trigram, so a single index serves the term.

## The three shapes and their fixes

AND-shaped predicates with fixed columns are the composite case: (a, b, c) in workload order, per [[What is the leftmost prefix rule for composite indexes]]. OR across different columns is where naive designs die: `WHERE name = ? OR email = ? OR phone = ?` cannot use any single B-tree, and PostgreSQL's combination machinery answers it only through BitmapOr of per-column indexes, per [[How does OR across columns affect index use]] — workable, but the planner may still prefer a scan. The rewrite that restores seeks is UNION ALL of three sargable queries (one per column, each with its own index), deduplicated as needed, because each branch becomes a cheap index range scan. A single term searched across name, email, and phone is better served by materializing one searchable value — a generated column concatenating normalized fields, indexed with tsvector or trigram — so the API's one box maps to one index, per [[How do you optimize substring search in SQL]].

```sql
-- one search box over three columns: one indexed expression
ALTER TABLE contacts ADD COLUMN search_text text
    GENERATED ALWAYS AS (name || ' ' || email || ' ' || coalesce(phone,'')) STORED;
CREATE INDEX idx_contacts_fts ON contacts USING gin (to_tsvector('simple', search_text));

SELECT * FROM contacts
WHERE to_tsvector('simple', search_text) @@ to_tsquery('simple', 'smith');
```

**Listing 1.** Materializing the searchable union converts multi-column search into a single indexed lookup.

## What the planner does when you do nothing

Without help, the multi-column OR becomes a bitmap OR of index scans — if all columns are indexed — or a sequential scan with a filter; MySQL's Index Merge union covers the same shape with its own limits, per [[How do you combine several indexes in one query]]. The UNION ALL rewrite trades plan elegance for guaranteed seeks but changes pagination and total-row semantics (duplicates across branches need DISTINCT or dedup logic), which interacts with [[How does LIMIT interact with ORDER BY and indexes]]. The scale escape — an external search engine over denormalized documents — is the boundary decision in [[When should you use Elasticsearch instead of SQL search]], and the per-endpoint design discipline is in [[How do you design indexes for a search API]].

> [!warning] "OR always kills the index" is outdated, but so is trusting it blindly
> Modern planners do combine indexes for OR — that is exactly what BitmapOr and Index Merge exist for. The caveat stands: combination is costed, loses row order, and degrades to scans when one OR branch is non-sargable (a function on a column or a leading wildcard poisons its branch, per [[What is sargability in SQL]]). The structural fixes — UNION ALL branches or a materialized search field — are how you make the fast path deterministic.

> [!tip] Interview answer
> I classify the query first. AND over fixed columns: one composite, equality first, sort last. OR over different columns: per-column indexes with bitmap combination at best, but I usually rewrite as UNION ALL of indexed seeks for deterministic speed. One term over many columns: materialize a concatenated or generated searchable field and index it with FTS or trigram, so the API's single box maps to one index.
