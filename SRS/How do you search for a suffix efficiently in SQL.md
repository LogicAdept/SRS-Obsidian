<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# How do you search for a suffix efficiently in SQL

> [!abstract] Short answer
> A suffix pattern (LIKE '%smith') cannot seek a normal index because the order is anchored at the wrong end. Store a reversed copy of the column, index it, and query LIKE reverse('%smith') which becomes an anchored prefix on the reversed value — or use a trigram index, which handles suffix patterns without the trick.

## The reversed-index trick

The B-tree orders strings left to right, so '%smith' hides the range start — the same failure as any leading wildcard, per [[Why does LIKE with a leading wildcard not use a B-tree index]]. Reversing the data flips the anchoring: 'htims%' is a prefix in the reversed order and therefore a seekable range. The pattern is: add a generated or maintained column (or an expression index on reverse(col)), index it, and rewrite the query's needle through reverse() on the constant side only. In PostgreSQL an expression index on (reverse(email)) serves WHERE email LIKE reverse('%smith') directly; MySQL 8 supports functional indexes on (REVERSE(email)) similarly. The needle must be normalized the same way the index is (case folding included), or the two orders disagree — the normalization pitfall from [[How do you implement case-insensitive search efficiently]].

```sql
-- PostgreSQL: expression index on the reversed value
CREATE INDEX idx_domain_rev ON contacts (reverse(email));
SELECT * FROM contacts
WHERE reverse(email) LIKE reverse('%@gmail.com');  -- seeks 'moc.liamg@%'
```

**Listing 1.** The constant is reversed at runtime; the stored side is pre-reversed, so the predicate becomes an anchored prefix.

## The trigram alternative and the decision

pg_trgm indexes three-character groups regardless of position, so '%suffix%' patterns — including suffix-only — are index-supported once the GIN/GiST trigram index exists, with no schema change beyond the index itself, per [[How does a trigram index help SQL search]]. Choose the reverse trick when you want the smallest index for a fixed single-suffix workload (domains, file extensions, phone suffixes); choose trigram when patterns vary and generality is worth the size. If the suffix is really a token in free text, full-text search is the better frame entirely, per [[When should you use full-text search instead of LIKE]]. Either way, verify the plan seeks rather than scans, the discipline in [[What is sargability in SQL]].

> [!warning] The reverse trick breaks on normalization mismatches
> Case folding, Unicode, and locale all enter the comparison: reverse('Smith') does not match an index built on reverse of a lowercased value unless both sides fold identically. Also, each new suffix shape needs its needle reversed — a query with a leading constant (LIKE 'ab%') will not use the reversed index at all, so you end up maintaining two indexes for both directions unless trigrams cover the workload.

> [!tip] Interview answer
> Suffix patterns cannot seek a forward-ordered index, so I flip the anchoring: index reverse(column) and query with reverse of the needle, turning '%@gmail.com' into a prefix seek. Alternatively a trigram index handles suffix and contains patterns without schema changes at the cost of a bigger index. I check the plan confirms a range scan, and I keep normalization consistent on both sides.
