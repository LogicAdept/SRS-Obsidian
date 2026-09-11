<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you emulate RIGHT JOIN using only LEFT JOIN support?

> [!abstract] Short answer
> `A RIGHT JOIN B` is definitionally `B LEFT JOIN A` with the same condition: the *right* table's rows all survive, so swapping the operands and using LEFT yields an identical result. Right joins exist for syntactic comfort when reading `FROM a JOIN b JOIN c` chains left to right; logically they add no power beyond LEFT.

The proof is one line in the standard's definition: RIGHT is specified as LEFT with sides exchanged. Practical reasons to know the emulation: MySQL has no `FULL JOIN` but has RIGHT (still needs UNION emulation); SQLite added both only in 3.39, so code targeting older builds must swap tables; Oracle's historical style keeps joins left-facing. Reading chains is the honest use case for RIGHT: `a JOIN b ON ... RIGHT JOIN c ON ...` keeps all of `c` without rewriting the FROM list. But team conventions usually forbid RIGHT entirely — mixed left/right chains are hard to read, and every RIGHT can be mechanically rewritten as LEFT with swapped operands ([[What kinds of SQL JOIN exist]]). Verified equality of the two forms is a two-query exercise: run both, diff the outputs — they must be row-for-row identical including column order of *selected* expressions.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris');
INSERT INTO orders VALUES (101,1),(102,1),(106,NULL);

SELECT c.name, o.id AS order_id FROM customers c
RIGHT JOIN orders o ON o.customer_id = c.id ORDER BY o.id;
-- Alice|101
-- Alice|102
-- |106
SELECT c.name, o.id AS order_id FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id ORDER BY o.id;
-- Alice|101
-- Alice|102
-- |106
```

**Listing 1.** Verified on SQLite 3.53.1 (RIGHT JOIN available since 3.39). The native RIGHT JOIN and the swapped LEFT JOIN return byte-identical results — order 106 with a NULL customer survives in both, padded on the customers side.

```d2
direction: right
a: "customers
left operand" {width: 160; height: 70}
b: "orders
right operand" {width: 160; height: 70}
r1: "customers RIGHT JOIN orders
= all orders survive" {width: 250; height: 70}
r2: "orders LEFT JOIN customers
= all orders survive" {width: 250; height: 70}
a -> r1
b -> r1
b -> r2
a -> r2
```

**Fig. 1.** The same pair of tables feeds two syntactic forms that define the same surviving set: "all of orders, matched customers" — only the FROM order differs.

> [!warning] Swapping sides also swaps column prefixes in SELECT and ORDER BY
> After rewriting `a RIGHT JOIN b` as `b LEFT JOIN a`, every `a.col` reference must be updated to the new alias layout, including outer references in ORDER BY and enclosing queries. Mechanical rewrites that only touch the FROM clause produce "no such column" errors or, worse, bind to a same-named column of the other table ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> RIGHT JOIN is LEFT JOIN with the operands swapped — the definition guarantees identical results, so any RIGHT can be emulated on engines without it by reversing the FROM order and writing LEFT. That matters on old SQLite (pre-3.39) and for FULL joins on MySQL or Oracle. In reviews I prefer keeping all joins left-facing for readability, and I treat RIGHT mainly as the tool for keeping a later table of a join chain intact without reshuffling the FROM list.
