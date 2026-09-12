<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the specification pattern in DDD?

> [!abstract] Short answer
> A specification encapsulates a business rule as a predicate object: `isSatisfiedBy(candidate)` answers yes or no, and specifications compose with and, or, and not into named rules. The same rule object then serves three uses - validating a candidate in memory, filtering a collection, and expressing a query - instead of the rule being rewritten three times in three dialects.

## The mechanism

A specification is a tiny object with one question in it. Its power comes from composition: primitive specs (adult, sufficient income) combine into policy specs (loan-eligible) that read like the ubiquitous language and carry no duplication. In Java the pattern maps naturally onto `Predicate<T>` with default combinators; the modeling content is the named constants and the vocabulary, not the machinery. The rule lives once; validation code, batch filtering, and query translation all reference the same object.

```java
@FunctionalInterface
interface Spec extends Predicate<Applicant> {
    default Spec and(Spec other) { return a -> this.test(a) && other.test(a); }
    default Spec or(Spec other)  { return a -> this.test(a) || other.test(a); }
    default Spec negate()        { return a -> !this.test(a); }
}

static final Spec ADULT = a -> a.age() >= 18;
static final Spec RICH  = a -> a.income() >= 3_000;

Spec loanApproved = ADULT.and(RICH);       // composed rule, named in domain terms
System.out.println(loanApproved.test(new Applicant(30, 3500, true)));   // true
```

**Listing 1.** Verified on JDK 21.0.12.1: an applicant aged 30 with 3500 income passes `ADULT.and(RICH)`; the 17-year-old with 5000 fails, the 25-year-old with 2000 fails - the composed rule reads as one domain sentence.

```d2
direction: down
adult: "ADULT\nage >= 18" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
rich: "RICH\nincome >= 3000" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
and: "AND" {
  width: 120
  height: 60
  style.fill: "#fff3e0"
}
policy: "LoanApproved\nnamed policy spec" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
uses: "validation | batch filter | query" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}
adult -> and
rich -> and
and -> policy
policy -> uses
```

**Fig. 1.** Primitive specs compose into a named policy; the policy object then feeds validation, filtering, and query translation from one definition.

## Three uses, one rule

In-memory validation is the trivial use. Batch filtering in memory composes the same objects over a stream. The third use - query translation - is where implementations earn their keep: a specification interface with an expression tree lets infrastructure walk the spec and translate it into SQL or a JPA criteria tree, so the same `loanApproved` filters both an in-memory list and a database table. That translation trick is exactly what Spring Data JPA's `Specification` generalizes for queries ([[What are Spring Data JPA Specification queries]]), and the DDD pattern is its source of shape. When a rule must also be enforced inside an aggregate transaction, the aggregate keeps its own check; the specification layers policy on top for selection and validation across aggregates - it does not replace aggregate invariants ([[What are aggregate aggregate root entity and value object in DDD]]).

> [!warning] Spec trees rot into query builders
> Two failure directions. First: strings and flags instead of objects - "status == active AND vip == true" repeated in five services is the rule duplication the pattern exists to kill, not a lightweight alternative. Second: over-composition - twenty-level spec trees become an internal DSL only their author can read. If a spec composes more than a handful of primitives, the missing concept wants its own named spec; and if a spec exists purely to make one query faster, it is a query in costume, not a domain rule.

> [!tip] Interview answer
> A specification turns a business rule into a predicate object with and, or, not combinators: `ADULT.and(RICH)` becomes a named LoanApproved policy. One object then validates candidates, filters batches, and translates into a query - Spring Data JPA Specifications are the mainstream version of it. It complements aggregate invariants: specs select and validate across aggregates, aggregates enforce inside themselves.

