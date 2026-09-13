<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Queries #Security/AppSec/Injection #SRS

# How do you prevent SQL injection in Hibernate queries?

> [!abstract] Short answer
> The same principle as at the JDBC level, one layer up: **user input must travel as a bound parameter, never as query text**. HQL/JPQL and Criteria queries that use named or positional parameters are safe by construction — the parameter value can change the *data* compared, but can never become *syntax*. The measured proof: a native-style query built by concatenation with input `x' OR '1'='1` returned **every row** of the table (the tautology became part of the SQL), while the same input passed as a bound parameter returned **zero rows** (it was compared as a literal string). The remaining Hibernate-specific holes are few but real: **native queries** built by string concatenation (no HQL parsing stands between you and the database), **string-built IN lists** ("comma-join user ids into the text"), and everything that *cannot* be parameterized at all — **`ORDER BY`/column names and sort directions** — which must come from a **server-side allowlist**, not from the client. Spring Data adds no magic: `@Query` with `:param` is safe, `@Query` with concatenated or SpEL-injected fragments is not.

## Where the boundary actually is

Injection is possible exactly where input can cross from the *value* channel into the *syntax* channel. With bound parameters the driver/provider sends the query text and the values separately; the database compiles the text first and only then substitutes values — a value containing `OR '1'='1` is just a string to compare against. Concatenation hands the attacker the compiler: their characters are parsed as SQL/HQL grammar before any value exists. Hibernate adds a nuance that surprises people who "know HQL is safe": **HQL injection is still injection** — a concatenated HQL query can be broken by an input containing a quote just like SQL, and the payload then executes against your database with the dialect's syntax. HQL with parameters protects you; HQL with `+` does not.

| Query style | Input as parameter | Input concatenated | Verdict |
| --- | --- | --- | --- |
| HQL/JPQL `where e.name = :n` | safe | **injectable** | parameterize — no exceptions |
| Criteria API / JPA Criteria | safe (literals as parameters) | n/a — predicates are typed calls | intrinsically structured |
| Native SQL via Hibernate | safe (`setParameter`) | **injectable** — and closest to raw SQL | treat like JDBC |
| Spring Data `@Query("… = :n")` | safe | **injectable** (and SpEL in `orderBy` needs care) | same rules, repository edition |
| `ORDER BY` / column / direction | **impossible to bind** | — | **allowlist** on the server |

```java
// measured: input = x' OR '1'='1
String broken = "select p from Person p where p.name = '" + input + "'";
em.createQuery(broken, Person.class).getResultList();          // 2 rows — the whole table leaked

em.createQuery("select p from Person p where p.name = :n", Person.class)
  .setParameter("n", input)                                    // 0 rows — value, not syntax
  .getResultList();

// the non-bindable case: sort — allowlist, never the raw request value
private static final Set<String> SORTABLE = Set.of("name", "createdAt");
String sort = SORTABLE.contains(requested) ? requested : "name";
```

**Listing 1.** The measured pair plus the rule for the one place parameters cannot reach: sorting columns are chosen from a fixed set, directions from `asc`/`desc`, everything else falls back to a default.

## The three realistic leak paths in ORM codebases

**Native queries with concatenated input** — the classic "HQL can't do this window function" escape hatch where the developer reverts to string habits; the fix is `setParameter` in native queries too (positional or named parameters work there), or `@NativeQuery` with parameters in Spring Data. **String-assembled IN lists** — joining ids with commas into the query text both injects (if the ids ever come from outside) and, even with trusted ids, churns the query plan cache with per-size texts; a bound `:ids` collection parameter is both the safe and the plan-cache-friendly answer. **Dynamic sorting** — the UI sends "sort by `name; drop table`" or simply `"total"` where the entity has no such field: binding cannot help because identifiers are syntax; the only defense is a fixed map from client-facing sort keys to known-safe column expressions. None of these are Hibernate defects — they are the value/syntax boundary, which every query API shares; Hibernate merely offers more doors into the syntax channel than plain JDBC, so the discipline must be stated explicitly in code review ([[How does PreparedStatement mitigate SQL injection compared to Statement]] is the same story one layer down).

> [!warning] "But the input comes from our own UI" is not a defense
> Client-controlled values reach the server through every layer of tooling — proxies, exports, integrations, admins with curl. Parameterization costs nothing measurable and removes the entire attack class; allowlisting sorts costs one lookup. There is no performance or convenience argument on the concatenation side — only habit.

> [!tip] Interview answer
> Injection is prevented by keeping user input in the value channel: bound named or positional parameters in HQL, JPQL, native queries, and Spring Data @Query alike — measured, a concatenated query with a tautology payload returned every row while the bound parameter returned zero, because the payload compiled into syntax in the first case and stayed a literal in the second. Criteria is structured by construction. The two places parameters cannot help: identifier positions — ORDER BY columns and directions — which must come from a server-side allowlist, and nothing else. String-built IN lists are both an injection risk and a plan-cache hazard, so they get a bound collection parameter. HQL is not "safe by default" — it is safe exactly as far as the parameters discipline goes.

See [[How does PreparedStatement mitigate SQL injection compared to Statement]], [[What kinds of queries can Hibernate run]], [[What is the Hibernate query plan cache]], [[How would you explain @Query JPQL vs native SQL]], and [[What is the difference between JPQL and Hibernate HQL]].
