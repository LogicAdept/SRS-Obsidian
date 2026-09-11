<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# What is the difference between prefix search and contains search

> [!abstract] Short answer
> Prefix search matches strings that begin with a term (LIKE 'term%'); contains search matches strings that include the term anywhere (LIKE '%term%'). The difference is structural, not cosmetic: a prefix is a contiguous range in lexicographic order and seeks a B-tree; contains has no contiguous range and needs trigram, token, or full-text structures.

## Why one seeks and the other cannot

Sorted order puts all 'term...' strings together, so the engine can compute a lower and upper bound for the prefix and read exactly that range — PostgreSQL documents B-tree support for LIKE 'foo%' with the anchoring caveat and opclass requirement. '%term%' describes a set with no bound: matches can sit anywhere in the string, so the B-tree's order carries no information about where they are. That is why the two query shapes route to different index types, and why the same column can be fast for autocomplete and hopeless for free-text containment on a plain B-tree. The deeper mechanism of the failure is in [[Why does LIKE with a leading wildcard not use a B-tree index]].

```sql
-- prefix: B-tree range, cheap, index-friendly
SELECT * FROM products WHERE sku LIKE 'AB-%';
-- contains: needs pg_trgm GIN or FTS, not the B-tree
SELECT * FROM products WHERE name LIKE '%wrench%';
```

**Listing 1.** Same operator, different predicate shape, different access path.

## Choosing the structure for contains

For '%term%' the PostgreSQL answer set is: pg_trgm GIN/GiST for arbitrary substring and similarity search including ILIKE; tsvector-based full-text search when the unit is a word with stemming and ranking; an external engine when relevance and scale outgrow the database — the comparison in [[When should you use full-text search instead of LIKE]] and the decision menu in [[How do you optimize substring search in SQL]]. Suffix search ('%term') is a prefix search on a reversed copy, per [[How do you search for a suffix efficiently in SQL]]. ClickHouse has no B-tree prefix magic at all and leans on skip/text indexes, described in [[How does ClickHouse accelerate LIKE and substring search]].

> [!warning] "Just add an index" does not upgrade prefix to contains
> A B-tree index cannot serve contains no matter how it is configured, because the structure is ordered by whole-string comparison. The other trap: anchoring matters — 'term%' versus '%term%' is a one-character change that switches the access path from a range scan to a full scan. Autocomplete features silently regress when someone "fixes" the query by adding a leading wildcard.

> [!tip] Interview answer
> Prefix search bounds a range of the lexicographic order, so it seeks a B-tree like 'abc%'. Contains search '%abc%' matches anywhere in the string, so there is no range to seek and the B-tree is useless for it. For contains you change structures: trigram indexes for substring work, full-text search for word-level semantics, or an external search engine at scale.
