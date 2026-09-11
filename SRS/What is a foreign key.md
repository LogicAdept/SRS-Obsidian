<!--
reps: 0
priority: 0
-->
#Databases/Keys #SRS

# What is a foreign key

> [!abstract] Short answer
> **A foreign key is a column (or column set) in one table whose values must match values of a referenced key — usually the primary key — of another (or the same) table, so the DBMS itself rejects rows that point at nothing.** It is the relational model's mechanism for cross-referencing relations, stated as a constraint instead of application discipline.

## The contract and its enforcement

Codd's 1970 definition still frames it: a foreign key of relation R is a domain whose elements are values of the primary key of some relation S — and S may be R itself (self-reference). Concretely, PostgreSQL and InnoDB enforce it as a declarative constraint: every insert or update of the referencing column checks the referenced key (that check is why missing indexes on foreign keys hurt write throughput); deleting or updating a referenced row follows the declared referential action — `CASCADE` removes the children, `SET NULL` empties the pointer, `RESTRICT`/`NO ACTION` refuses the delete. The classic NULL subtlety has its own drill in [[Can a column referenced by a foreign key be NULL]].

```sql
CREATE TABLE orders (
  id         int PRIMARY KEY,
  customer_id int NOT NULL REFERENCES customers(id)
                ON DELETE RESTRICT
);
CREATE TABLE order_lines (
  order_id int REFERENCES orders(id) ON DELETE CASCADE,
  sku      text,
  PRIMARY KEY (order_id, sku)
);
```

**Listing 1.** Two referential policies: a customer with orders cannot be deleted (RESTRICT), while deleting an order cascades to its lines.

```d2
direction: right
c: "customers(id)\nPK" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
o: "orders(customer_id)\nFK REFERENCES customers" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
c -> o: "every FK value\nmust exist in PK"
```

**Fig. 1.** The arrow is a guarantee maintained by the engine: an order cannot exist for a customer id that is not in customers.

Beyond integrity, foreign keys carry semantic weight: they document the model, and they anchor joins — the join predicate `orders.customer_id = customers.id` is exactly the constraint's arrow. The relational-algebra view of the same idea is that a foreign key lets a tuple of one relation reference a tuple of another while staying inside the model's key discipline: see [[How would you explain the relational data model and Codd rules basics]].

> [!warning] "We skip FKs for performance / flexibility" trades a hard guarantee for a rumor
> Dropping foreign keys moves integrity to application code — and every code path that ever writes the table (scripts, backfills, two services, a support engineer in psql) must be perfect forever. The common performance claim ("FK checks are slow") mostly dissolves once the referenced key is indexed — which you want anyway for the reverse lookup. The honest compromise is deferred checks, not absence; and note the direction trap: a foreign key guards the *child* pointing at an existing parent — it cannot enforce "parent must have at least one child", which is an application-level invariant.

The key family around it: [[What is a primary key and how do you choose one]], [[How would you explain candidate keys in relational databases]], and cardinalities built from FKs in [[What relationship types exist between database tables]].

> [!tip] Interview answer
> A foreign key is a declarative constraint: a column or column set in one table whose values must exist as a referenced key in another table — or the same one, for self-reference. The engine validates every write and applies the declared referential action on deletes: CASCADE, SET NULL, or RESTRICT. It turns "rows must point at real parents" from code convention into a database guarantee.
