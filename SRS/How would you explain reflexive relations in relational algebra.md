<!--
reps: 0
priority: 0
-->
#Databases/RelationalAlgebra #SRS

# How would you explain reflexive relations in relational algebra

> [!abstract] Short answer
> **A reflexive relation is one whose foreign key points into its own table — tuples referencing other tuples of the same relation (employee → manager).** In relational algebra terms the same relation appears on both sides of an operation; in SQL it is queried with a self-join, aliasing the table twice so the engine treats it as two copies.

## The mechanics: same relation, two roles

Codd's foreign-key definition explicitly allows the referenced relation to be the same one. The modeling use is hierarchies and chains inside one entity set: `employees(id, name, manager_id REFERENCES employees(id))` — every manager is also an employee. Algebraically, finding each employee with their manager's name is a theta-join of employees with itself on `e.manager_id = m.id`; because a relation cannot join to itself "as itself" twice in the algebra's naming discipline, SQL requires distinct aliases — `FROM employees e JOIN employees m ON e.manager_id = m.id` — which materializes the two *roles* the relation plays. Codd anticipated exactly this with role-qualified domains (sub.part / super.part) for relations using the same domain twice.

```sql
-- one table, two roles: the self-join
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

**Listing 1.** Reflexive access in SQL: the LEFT JOIN keeps the CEO, whose manager_id is NULL, instead of dropping the row.

Two refinements matter in practice. **Acyclic vs recursive:** manager chains form a tree; listing someone's *entire* reporting line is not a join but a recursive traversal — SQL expresses it with a recursive CTE, the algebra's transitive-closure territory in [[How would you explain transitive relations in relational algebra]]. **Integrity direction:** a reflexive FK enforces "manager must be an existing employee", but cannot forbid cycles (A manages B manages A) — the engine validates each edge, not the graph shape.

```d2
direction: right
emp: "employees (id, name,\nmanager_id -> employees.id)" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
e: "alias e: the managed" {
  width: 210
  height: 80
  style.fill: "#fff3e0"
}
m: "alias m: the manager" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
emp -> e
emp -> m
e -> m: "e.manager_id = m.id"
```

**Fig. 1.** One stored relation plays two roles in the join; the aliases are the algebra's way of naming the two participations of the same relation.

> [!warning] Reflexive ≠ symmetric ≠ "rows equal themselves"
> The mathematical term "reflexive" (every element relates to itself) misleads here: a manager relation is not mathematically reflexive — most employees do not manage themselves. The database meaning that survives interviews is structural: the FK target is the same table. Do not confuse the self-join trick with uniqueness either: nothing stops `manager_id = id` unless a CHECK forbids it — decide explicitly whether self-management is legal.

The relational backdrop: [[How would you explain the relational data model and Codd rules basics]]; the key that makes the loop enforceable: [[What is a foreign key]]; the recursive follow-up: [[How would you explain transitive relations in relational algebra]].

> [!tip] Interview answer
> A reflexive relation references itself: its foreign key targets its own primary key, as in employees.manager_id. Queries need a self-join with two aliases — the table playing both the managed and the manager role — and a LEFT JOIN to keep root rows. The constraint validates each reference but not the graph, so cycles and full hierarchy walks need CHECKs and recursive CTEs respectively.
