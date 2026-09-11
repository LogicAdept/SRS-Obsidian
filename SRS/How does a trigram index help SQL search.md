<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/Relational/PostgreSQL #SRS

# How does a trigram index help SQL search?

> [!abstract] Short answer
> It converts substring and fuzzy search from "scan every row and run string matching" into "look up the shared trigrams in an inverted index". A search term is decomposed into three-character windows; the index (GIN or GiST over trigram operator classes) finds rows containing those windows, so even `LIKE '%term%'` with a leading wildcard becomes an index lookup instead of a full scan.

## The mechanism in one pass

1. Normalize the pattern: lowercase per collation, ignore non-alphanumerics, pad word edges.
2. Extract trigrams: `"maria"` produces ` ma`, `mar`, `ari`, `ria`, `ia `.
3. The trigram index maps each trigram to candidate rows.
4. The executor unions/intersects the candidates and rechecks the actual string condition.

```d2
term: "Pattern '%aria%'" {width: 220; height: 60}
tri: "Trigrams:  ma, mar, ari, ria, ia " {width: 330; height: 60}
gin: "GIN trigram index\ncandidate rows per trigram" {width: 320; height: 80}
res: "Recheck LIKE on candidates\nresult set" {width: 300; height: 70}
term -> tri -> gin -> res
```

**Fig. 1.** The index narrows the world to candidate rows; the final LIKE still runs, but on a tiny fraction of the table.

## Why plain indexes cannot do this

A B-tree orders values lexicographically, so it can serve prefix search only (`LIKE 'abc%'`) — the common substring case with a leading `%` is invisible to it ([[What is the difference between LIKE ILIKE and full-text search]]). Trigram indexing throws away order and indexes fragments instead, which is exactly the shape substring queries need. The PostgreSQL implementation is pg_trgm ([[What is pg_trgm]]); the same idea powers dedicated search engines' n-gram analyzers.

Index-method choice follows the GIN-versus-GiST tradeoff: GIN for read-heavy search with the pending list smoothing writes, GiST when update volume dominates and the lossy recheck is acceptable ([[What is the difference between GIN and GiST indexes in PostgreSQL]]). Trigram indexes also index case-folded text, so a single structure serves both exact-case and case-insensitive queries — one reason they displace ad-hoc lower() expression indexes for search workloads.

## Where it fits

- Small-to-medium tables, autocomplete, admin filters, typo-tolerant lookups: trigram GIN inside the OLTP database.
- Full ranked document retrieval: full-text search structures instead ([[How does full-text search work in PostgreSQL]]).
- Massive log/text search with built-in trigram or n-gram acceleration: engines designed for it ([[How does ClickHouse accelerate LIKE and substring search]], [[How do you optimize substring search in SQL]]).

> [!warning] Short patterns defeat trigrams
> A two-character search term produces at most a couple of trigrams (with padding), so candidate sets explode and the plan may fall back to a scan. Also remember the pattern recheck: for very common trigrams the index returns huge candidate lists. Search-term length and trigram selectivity belong in every trigram performance review.

> [!tip] Interview answer
> A trigram index inverts strings into three-character fragments, so a substring or fuzzy pattern becomes lookups of its trigrams plus a small recheck — the only index structure in standard SQL that makes leading-wildcard LIKE fast. B-trees only do prefix search; trigrams cover contains, ILIKE, regex fragments and similarity.
