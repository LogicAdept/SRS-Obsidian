<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Mapping #Java/Persistence/JPA/Mapping #SRS

# How do you choose a JPA inheritance mapping strategy?

> [!abstract] Short answer
> Three table layouts, plus "no entity at all". **`SINGLE_TABLE`** (the default): one table for the whole hierarchy with a **discriminator column**; fastest queries (zero joins) but subclass columns must be **nullable** and cannot carry `NOT NULL` or unique constraints — integrity moves into the app. **`JOINED`**: one table per class joined on the shared id; normalized, constraints per class, but polymorphic loads pay **N−1 joins** per level. **`TABLE_PER_CLASS`**: every concrete class gets a full copy of inherited columns; polymorphic queries become **`UNION`** of all tables and id generation must be shared — rarely the right answer. **`@MappedSuperclass`** maps inherited fields to each subclass's own table with **no polymorphism** at all. Decide by query pattern and constraint needs, not by aesthetics.

## The trade-off triangle

| | `SINGLE_TABLE` | `JOINED` | `TABLE_PER_CLASS` |
| --- | --- | --- | --- |
| Discriminator | required | optional | none |
| Subclass columns | nullable, no constraints | own table, constraints OK | own table, constraints OK |
| Polymorphic query | one table scan | joins per depth level | `UNION` over all tables |
| Storage | sparse rows, many nulls | normalized | duplicated inherited columns |
| Id generation | one table | one table | shared generator across tables; `IDENTITY` unusable |

```java
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
@DiscriminatorColumn(name = "kind")
public abstract class Payment {
    @Id @GeneratedValue Long id;
    BigDecimal amount;
}

@Entity
public class CardPayment extends Payment {
    @Column(nullable = false) String last4;   // impossible in SINGLE_TABLE
}
```

**Listing 1.** Under `JOINED`, `LAST4` can be `NOT NULL` in its own table; under the default `SINGLE_TABLE` the column lives in the shared `PAYMENT` table and must accept nulls for every non-card row.

## How the choice actually gets made

**Query pattern dominates.** If most reads are polymorphic — "all payments this month, whatever the type" — `SINGLE_TABLE` wins because the whole hierarchy is one table and the discriminator filters it. If most reads are **per-subclass** and the subclass data is wide or heavily constrained, `JOINED` keeps each table small and truthful, and the join cost is two tables, not five. `TABLE_PER_CLASS` only makes sense when polymorphic queries are rare, the hierarchy is shallow, and inherited state is small — otherwise the `UNION` scans every table with every column.

**Constraint honesty is the second axis.** A `SINGLE_TABLE` hierarchy cannot express "a card payment always has a card token" in the schema; the row for a `TransferPayment` simply has `NULL` there. Some teams add **check constraints** on `(discriminator, column)` pairs manually; that is schema surgery outside the mapping, and every provider-specific trick moves you further from any future migration. With `JOINED` the constraint is ordinary.

**Depth amplifies join cost.** A three-level `JOINED` hierarchy loads a leaf with two joins, and **every** polymorphic query joins them all. Hibernate mitigates with fetch joins only when you ask; the baseline cost is structural. Wide-and-flat hierarchies hurt `SINGLE_TABLE` differently: dozens of sparse columns make the shared table wide for every row type and index maintenance pays for nulls too.

## Gotchas worth naming

The **default is `SINGLE_TABLE`** — omitting `@Inheritance` silently puts subclasses into the shared table, which surprises teams who assumed per-class tables. Discriminator values have **no foreign key**; they are a string/number switch, so renaming a class's discriminator is a data migration, not a refactor. Under `TABLE_PER_CLASS` you cannot use `IDENTITY` ([[Why does GenerationType.IDENTITY disable JDBC batching]] explains the strategy's constraints in another context): each table would mint its own ids and collide across the union — use a shared sequence. And `@MappedSuperclass` is not a strategy: it produces **no table and no polymorphic queries** for the base class — it is field reuse, which is exactly right for audit columns and exactly wrong for a domain hierarchy you query by base type.

> [!warning] Polymorphic `ManyToOne` hides the same decision
> An association to a base type forces the strategy on every load. A lazy `ManyToOne` to the base loads a proxy that resolves through discriminator or joins on first touch — the layout you chose for storage becomes the runtime cost of *every* association navigation, not just direct queries.

> [!tip] Interview answer
> `SINGLE_TABLE` trades schema integrity for speed: one table, discriminator switch, nullable subclass columns, no per-class constraints, best polymorphic reads. `JOINED` trades joins for normalization: one table per class, constraints hold, polymorphic queries join per level. `TABLE_PER_CLASS` unions full copies of each concrete table and needs a shared id generator, so I treat it as a niche choice. I decide by read pattern — polymorphic-heavy goes single table, constraint-heavy or wide subclass data goes joined — and I remember the default is single table even if you write nothing.

See [[Can a JPA entity class be abstract]], [[What is the JPA Id annotation]], [[What is the JPA Table annotation and its attributes]], and [[Why does GenerationType.IDENTITY disable JDBC batching]].
