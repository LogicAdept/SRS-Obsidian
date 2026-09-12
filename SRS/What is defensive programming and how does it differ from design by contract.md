<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Methodologies/DesignByContract #SRS

# What is defensive programming and how does it differ from design by contract?

> [!abstract] Short answer
> **Defensive programming** distrusts everything: every unit re-validates every input, at every layer, forever. **Design by contract** distributes obligations instead: the caller owes the precondition, the callee owes the postcondition given it — and a failed precondition is a **caller bug** that should fail loudly at the guilty site ([[How would you explain programming by contract and preconditions]]). Meyer's OOSC makes the objection structural: defensive checks can never be complete — "defensive programming is never satisfied". The pragmatic synthesis: hard validation at untrusted boundaries, contracts inside.

## The defensive posture and its costs

The defensive style adds checks because no layer trusts another: the service re-checks what the controller validated, the repository re-checks what the service validated. Three costs follow. **Bug masking**: the second check absorbs the failure the first check should have exposed, so the violation surfaces far from its cause, as a subtle downstream anomaly instead of a crash at the faulty call. **Noise**: every method carries guard clauses that repeat the class's own invariants ([[What is a representation invariant and abstraction function]]). **Impossibility of completion**: another layer can always be imagined, so the checking never bottoms out — Meyer's point that the posture cannot be satisfied, only abandoned.

## The contract posture

DbC replaces unlimited suspicion with an **obligations table**. The precondition defines what the caller must guarantee — it is the caller's duty and the callee's benefit: inside the method, the precondition may be *assumed*. The postcondition is the callee's duty. If a precondition fails, the bug is in the caller, and the correct behavior is to fail fast *there* — the assertion that throws is the most precise possible error report, locating the guilty call site rather than the eventual symptom ([[Why are clear behavioral contracts important in Java APIs]]). Contracts also make the overriding rule explicit: weaken preconditions, strengthen postconditions — never the reverse ([[What does behavioral subtyping require beyond matching signatures]]).

## Where defense is right

The boundary of the system faces input with **no shared contract**: HTTP requests, queue messages, user files, third-party APIs. There, validation is not duplicated distrust — it is the negotiation that *establishes* a contract for the inside of the system. The anti-pattern is not boundary validation; it is re-validating the same already-contracted values at every internal layer. Inside, Java's `assert` (disabled by default in production) expresses internal contracts cheaply, while boundary code throws explicit exceptions ([[When is the assert detail expression evaluated]]).

```d2
direction: down
edge: "boundary\nUNTRUSTED input\nvalidate everything" {
  width: 300
  height: 64
  style.fill: "#fff3e0"
}
core: "inside the system\ncontracts hold\npreconditions assumed" {
  width: 300
  height: 64
  style.fill: "#e8f5e9"
}
fail: "violation inside = caller bug\nfail fast at the call site" {
  width: 320
  height: 56
  style.fill: "#ffebee"
}
edge -> core: "validated once, contract established"
core -> fail
```

**Fig. 1.** Defense lives at the wall where trust ends; contracts govern the inside.

```java
// BOUNDARY: untrusted input, no contract yet — validate everything
public void handle(Request r) {
    if (r == null || r.amount() == null || r.amount().signum() < 0)
        throw new BadRequestException("amount required, non-negative");
    process(r.amount());                     // from here on, contracts apply
}

// INSIDE: contracted code assumes the precondition — no re-validation
/** @pre amount != null && amount.signum() >= 0 */
private void process(Money amount) {
    // caller's obligation already paid; straight to the domain logic
}
```

**Listing 1.** Conceptual. The boundary negotiates the contract; internal code assumes it — one validation, one guilty site on violation.

> [!warning] "Defensive programming means validating at the system boundary" is false
> That boundary validation is the contract-*compatible* part. Full defensiveness means **re-validating everywhere** — the second check masks the first fault site, hides the guilty caller, and cannot be completed. The distinguishing question is whether a check *establishes a contract* for the inside or merely duplicates one that already holds ([[How would you explain programming by contract and preconditions]]).

> [!tip] Interview answer
> Defensive programming checks everything everywhere and never bottoms out; design by contract splits obligations — caller pays preconditions, callee guarantees postconditions, and a precondition failure is a caller bug that crashes loudly at the guilty call site. I validate untrusted input at the boundary once, then rely on contracts and assertions inside, so bugs surface where they were caused, not three layers downstream.
