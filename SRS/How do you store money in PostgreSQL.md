<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DataTypes #SRS

# How do you store money in PostgreSQL?

> [!abstract] Short answer
> Use numeric — exact, arbitrary-precision decimal arithmetic — typically numeric(12,2) or wider for currency amounts, plus a currency column when multiple currencies exist. Avoid float and double precision (binary rounding errors) and avoid the money type (locale-dependent output, fixed fractional precision, casts that surprise). bigint of minor units is the alternative when scale is fixed and performance matters.

## Why numeric

Floating-point types store binary fractions; 0.1 has no exact binary form, so sums and comparisons drift. numeric stores decimal digits exactly — `0.1 + 0.2 = 0.3` holds — at the cost of slower arithmetic and variable storage. The precision/rounding guarantees are what accounting requires; the general numeric-type mechanics are in [[For which SQL numeric types are addition and subtraction invalid]] for the integer cousins.

```sql
CREATE TABLE payments (
  id           bigint GENERATED ALWAYS AS IDENTITY,
  amount       numeric(12,2) NOT NULL CHECK (amount >= 0),
  currency     char(3) NOT NULL,       -- ISO 4217
  PRIMARY KEY (id, currency)
);
```

**Listing 1.** The standard shape: numeric amount plus explicit currency; the composite key blocks one row carrying two currencies.

## The rejected alternatives

- **money type**: 8 bytes, fixed fractional precision determined by the lc_monetary locale setting — values dumped and restored under a different locale misrender, and the documentation itself warns the type is locale-sensitive. Its range caps at about 92 trillion with 2 digits. Division truncates toward zero. Legitimate niche: throwaway single-locale reporting.
- **float4/float8**: binary rounding — `WHERE amount = 0.1` misses rows; summation drifts. Never for money.
- **bigint minor units** (cents): exact and fast, but every API, report and export must remember the scale; mixed-scale currencies (JPY has none) add traps.

```d2
exact: "numeric\nexact decimal arithmetic\nslower, variable size" {width: 300; height: 90}
int: "bigint minor units\nexact, fast, scale in app" {width: 300; height: 90}
bad: "float / money\nrounding drift / locale traps" {width: 310; height: 90}
```

**Fig. 1.** The decision map: numeric by default, integer minor units at scale, never float or money.

## Rounding discipline

Decide and centralize rounding: SQL ROUND with explicit digits per operation (banker's rounding rules differ across jurisdictions); never chain float conversions through ORMs. Arithmetic between numeric values stays numeric; a single float operand poisons the expression to double precision.

> [!warning] numeric does not fix application-level float bugs
> Storing numeric(12,2) does not help if the app computes in float64 before the INSERT, or if the ORM maps numeric to a float. The precision chain must be end-to-end: decimal types in the application, numeric in the database, explicit rounding at defined points. Auditors find the gaps ([[What is the difference between PostgreSQL and ClickHouse]] — analytical engines with float defaults are a different trap again).

> [!tip] Interview answer
> numeric — exact decimal arithmetic, typically numeric(12,2) with an ISO currency column — is the default; bigint minor units is the high-volume alternative. Reject float for binary rounding and reject money for its locale-dependent output and precision rules. Rounding policy lives in one place, end to end, including the application types.
