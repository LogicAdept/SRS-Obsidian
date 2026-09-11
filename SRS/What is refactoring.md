<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SRS

# What is refactoring?

> [!abstract] Short answer
> Refactoring is changing a codebase's internal structure to make it easier to understand and cheaper to modify - without changing its observable behavior. Martin Fowler's canonical definition stresses the mechanics: it is "a series of small behavior-preserving transformations", each one small enough to be nearly risk-free, whose sequence can restructure significant code. Refactoring is a working mode, not a project: you refactor to enable a change, to understand code, or as you review - with a test suite as the safety net that proves behavior stayed put.

## The mechanism that makes it safe

Two properties define genuine refactoring. Behavior preservation: external behavior is the spec - same outputs, same exceptions, same performance envelope within reason - and the test suite (ideally self-testing code built up over time) is what checks it continuously. Smallness: each named transformation - extract method, move method, inline class, replace conditional with polymorphism - is a step you can see correct in one glance; correctness compounds across steps instead of gambles. That is why a "big refactor" on a branch for three weeks is usually a rewrite wearing the name: the small-steps property, and the constant green build, are the actual discipline ([[How would you argue for refactoring a legacy system versus rewriting it]]).

```java
// Before: comment does the naming, logic buried in the caller
if (p.score > 100 && p.age >= 18 && p.country.equals("US")) { ... }

// After two refactorings: extract method + rename - behavior identical
if (isEligibleForPremium(p)) { ... }

private boolean isEligibleForPremium(Player p) {
    return p.score > 100 && p.age >= 18 && p.country.equals("US");
}
```

**Listing 1.** Conceptual. One extract-method step: the condition gets a name and an owner, callers read intent, and the compiler plus tests confirm nothing else moved.

## When you refactor - and when you do not

Fowler's rule of thumb: refactor opportunistically. Preparatory - "make the change easy, then make the easy change": right before a feature lands in a messy area. Comprehension - while reading, name what you deciphered so the next reader skips the decoding. Review-fixup - during code review of your own branch. What refactoring is NOT: fixing bugs or adding features (those change behavior - refactoring is deliberately interleaved with them, but is distinct work); rewriting from scratch; and never a scheduled phase in a healthy codebase - "we will refactor next quarter" usually means tests are missing and the debt compounds. The famous application is complexity: refactor when change amplification or reading cost appears, not on aesthetic impulse ([[What is overengineering and how does it affect enterprise software]]).

> [!warning] "We refactored and added a feature in one commit" - then nobody can review either
> Mixing behavior changes with structural moves in one change destroys both reviewability and bisectability: a regression cannot be attributed to the feature or the move. The craft rule is sequenced commits - structural transformation first, proven green; behavioral change second. The second lie: "refactoring made it slower is still refactoring" - observable behavior includes performance within the envelope callers rely on; a transformation that tanks latency changed behavior and must justify itself as such ([[What is refactoring]]).

> [!tip] Interview answer
> Refactoring is behavior-preserving restructuring in small, named, individually safe steps, with tests proving nothing observable changed - Fowler's definition. I refactor opportunistically: preparatory before a feature, comprehension while reading, review-fixup on my own branch, and I keep structural and behavioral changes in separate commits. It is a continuous discipline, not a project phase, and its ceiling is exactly the quality of the test suite.
