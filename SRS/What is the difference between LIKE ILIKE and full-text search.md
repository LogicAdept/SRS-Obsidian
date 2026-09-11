<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/Relational/PostgreSQL #SRS

# What is the difference between LIKE, ILIKE and full-text search?

> [!abstract] Short answer
> LIKE is literal pattern matching with wildcards (% any string, _ one char), case-sensitive; ILIKE is the same with case-insensitive matching; both scan strings and only B-tree prefix shapes (LIKE 'abc%') can use an index. Full-text search is linguistic: it stems and normalizes words into lexemes, matches relevance across documents, ranks results, and is served by GIN indexes — a different tool for a different question.

## The mechanics

| | LIKE / ILIKE | full-text search |
|---|---|---|
| Matches | literal substring pattern | stemmed lexemes |
| Case | literal / insensitive | per dictionary |
| Operators | %, _ | @@, tsquery syntax |
| Word forms | none (cats != cat) | stems (cats -> cat) |
| Ranking | none | ts_rank |
| Index | B-tree only for 'abc%' prefix; trigram for %x% | GIN over tsvector |

```sql
SELECT * FROM books WHERE title LIKE '%Wolf%';        -- literal, no index use
SELECT * FROM books WHERE title ILIKE '%wolf%';       -- + case folding
SELECT * FROM books
WHERE tsv @@ websearch_to_tsquery('english', 'wolves'); -- finds "Wolf", "wolverine"...
```

**Listing 1.** The same intent ("about wolves") is three different engines: FTS normalizes word forms, LIKE/ILIKE match characters.

- LIKE with a **leading wildcard** defeats B-tree indexes: the index orders by prefix, and `%x%` has none. Trigram indexes ([[How does a trigram index help SQL search]]) are the fix when substring search is the real requirement.
- LIKE 'abc%' uses a B-tree when the column's collation pattern matches, otherwise with text_pattern_ops operator classes — a per-column design decision ([[What PostgreSQL index types exist]]).

```d2
sub: "Find substring\n'%wolf%'" {width: 250; height: 70}
pre: "Find prefix\n'wolf%'" {width: 220; height: 70}
lin: "Find word forms\n'wolves running'" {width: 260; height: 70}
tr: "pg_trgm GIN" {width: 220; height: 60}
bt: "B-tree / text_pattern_ops" {width: 280; height: 60}
fts: "tsvector + GIN + ts_rank" {width: 280; height: 60}
sub -> tr
pre -> bt
lin -> fts
```

**Fig. 1.** The tool routing: substring, prefix, and linguistic queries want different structures.

## Choosing

Names, codes, autocomplete — substring semantics: ILIKE with a trigram index, or prefix search on a B-tree. Documents, descriptions, anything where "the user typed a word form" — full-text search with a stored tsvector column ([[How does full-text search work in PostgreSQL]] covers the pipeline). Log-style "somewhere in a huge string" searches at analytical scale move out of the OLTP engine entirely ([[How do you search logs in ClickHouse]]).

> [!warning] ILIKE is not "slow LIKE" and FTS is not "smart LIKE"
> ILIKE can use the same trigram or prefix indexes as LIKE; without an index both scan. And FTS will not find your substring at all: searching tsvector for "manufac" fails without prefix syntax, and it never matches inside a word. Mixing the two up in a design review — substring need served by FTS, or relevance need served by ILIKE — produces the classic "search is useless" complaints ([[What is pg_trgm]] for the middle ground).

> [!tip] Interview answer
> LIKE and ILIKE are literal pattern matching — case-sensitive and folded respectively — usable by indexes only for prefix shapes unless you add trigram indexes for contains. Full-text search normalizes words into stemmed lexemes, matches and ranks with @@ and ts_rank over a GIN index. Substring problems take ILIKE plus trigram; word-form relevance takes FTS.
