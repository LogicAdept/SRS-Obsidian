<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SRS

# What is DRY, KISS, YAGNI?

> [!abstract] Short answer
> Three rules for not building rot. DRY - "every piece of knowledge must have a single, unambiguous, authoritative representation within a system" (Hunt and Thomas, The Pragmatic Programmer, 1999): the same fact must not be written in several places that can drift apart. KISS - keep it simple, stupid: prefer the simplest design that works, a principle popularized by Lockheed Skunk Works engineer Kelly Johnson. YAGNI - "you aren't gonna need it", the Extreme Programming mantra (Ron Jeffries): do not build a capability now on the speculation that you will need it later.

## What each one actually forbids

DRY forbids duplicated KNOWLEDGE, not duplicated text. Two loops that happen to look similar are fine; a customer's credit limit appearing in the validation service, the invoice template, and a stored procedure is a defect - change it in one place and the others silently disagree. The unit is "a piece of knowledge", which is why the cure is usually an abstraction that OWNS the fact, not de-duplicating identical strings. KISS forbids cleverness without payoff: extra layers, frameworks, and generalization that solve no present problem and tax every reader. YAGNI forbids speculative capability: the third parameter that "someday" needs overriding, the interface with one implementation "for later" - Fowler's phrasing: a capability you presume you need in the future should not be built now ([[What is overengineering and how does it affect enterprise software]]).

```d2
direction: right
dry: "DRY\none authoritative\nrepresentation" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
kiss: "KISS\nminimum complexity\nthat works" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
yagni: "YAGNI\nnothing speculative" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
dry -> kiss: "less moving parts"
yagni -> kiss: "nothing to simplify"
```

**Fig. 1.** They converge: represent each fact once, build only what is needed now, keep the result simple.

## How they pull together - and against each other

Together they define "just enough": YAGNI caps what you build, KISS caps how you build it, DRY caps how many places a fact lives. The conflicts are the interview gold. DRY vs KISS: de-duplicating two coincidentally similar ten-line blocks behind a parameterized abstraction adds indirection for no knowledge saved - when the similarity is accidental, duplication is cheaper than the wrong abstraction (the "wrong abstraction" lesson: wait for the second REAL change). DRY vs YAGNI: building a configuration system so the credit limit becomes "single-sourced everywhere" invents machinery for a flexibility nobody asked for. The tiebreaker is knowledge vs text: consolidate facts that must change together; leave coincidental similarity alone.

> [!warning] "DRY means no code may ever look similar" produces monsters
> The classic injury is premature abstraction: two call sites share a shape, someone fuses them behind a boolean parameter, then the third call site needs a different shape - and the abstraction accretes flags until nobody can touch it. That is worse than the duplication it replaced. The second confusion: DRY across SYSTEM boundaries - client and server cannot share source, so the contract (schema, API definition) is the authoritative representation, and duplicated generated code on each side does not violate DRY at all.

> [!tip] Interview answer
> DRY says every piece of knowledge gets one authoritative representation - I hunt facts that can drift, not lookalike code. KISS says pick the simplest workable design and skip the cleverness. YAGNI says do not build speculative capability now. Applied together they prevent both rot and gold-plating ([[What is overengineering and how does it affect enterprise software]]), and when they collide I decide by asking whether a similarity is real shared knowledge or accident - then [[What is refactoring|refactor]] only on evidence.
