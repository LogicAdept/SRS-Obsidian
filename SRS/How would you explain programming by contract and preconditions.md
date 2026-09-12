<!--
reps: 0
priority: 0
-->
#Methodologies/DesignByContract #SRS

# How would you explain programming by contract and preconditions?

> [!abstract] Short answer
> Design by Contract (DbC), introduced by Bertrand Meyer, treats every method call as a contract between caller and callee with three clause types. Preconditions state what must be true before the call - they are the caller's obligation and the callee's benefit ("I may assume this"). Postconditions state what the callee guarantees after the call - its obligation. Class invariants must hold for every instance before and after every operation. Together they make assumptions executable: Eiffel, the language DbC was designed for, checks them natively at runtime, and violations are bugs located at the exact call site that caused them.

## The obligations-and-benefits structure

The contract reframes an API call as mutual duties. If the precondition `amount >= 0` holds, the caller has paid its obligation and earns the postcondition guarantee - the callee "promises" the result and may skip re-checking what the precondition already assures. If the precondition fails, the contract is void and the callee is entitled to fail fast - the bug is the caller's, and the assertion that throws is the most precise possible error message. The Eiffel official description is that contracts make the "expected behavior of every component explicitly defined, checked, and enforced" and turn correctness into "a structural property of the system" rather than something testing samples after the fact.

```java
public Money withdraw(Money amount) {
    // precondition: amount positive and covered
    if (amount.isNegative() || amount.greaterThan(balance)) {
        throw new IllegalArgumentException("precondition violated: amount");
    }
    ...
    // postcondition: balance decreased exactly by amount
    assert balance.minus(amount).equals(before) : "postcondition violated";
    return amount;
}
```

**Listing 1.** Conceptual. Precondition checked eagerly with a thrown error (the caller's bug); postcondition as an assertion the method guarantees on return.

## Inheritance: the strengthen/weaken rule

Contracts compose with polymorphism through one rule: a subclass may weaken preconditions and strengthen postconditions, never the reverse - otherwise code written against the superclass contract breaks when handed a subclass instance. That is DbC's restatement of the Liskov substitution principle, and it is the sharpest interview connection to make ([[How would you explain the Liskov substitution principle in SOLID]]). Contracts also document themselves: the clauses are precise, checked, and cannot drift from the docs, which is the property formal "documentation that cannot lie" claims rest on. The contrasting posture and where each belongs: [[What is defensive programming and how does it differ from design by contract]].

> [!warning] "Java assertions = Design by Contract" is false
> Java has no native DbC: `assert` is disabled by default at runtime and is a debugging aid, not an enforcement mechanism. What Java offers are idioms - `Objects.requireNonNull` for the most common precondition, validation in constructors, optional annotation-based frameworks - none of which carry DbC's method-level rigor out of the box. Meyer's own position is that DbC "only delivers its full value when it is native to the language"; in Java you approximate it with disciplined, documented checks ([[Why are clear behavioral contracts important in Java APIs]]).

> [!tip] Interview answer
> Design by Contract makes method calls two-party contracts: preconditions the caller must satisfy, postconditions the callee guarantees, and class invariants holding throughout - all executable, so violations surface at the exact faulty call instead of as corrupt state later. Subclasses may only weaken preconditions and strengthen postconditions, which is LSP phrased contractually. Eiffel enforces it natively; in Java I approximate it with requireNonNull-style checks and fail-fast validation.
