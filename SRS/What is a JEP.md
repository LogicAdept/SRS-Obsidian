<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What is a JEP

> [!abstract] Short answer
> **JEP stands for JDK Enhancement Proposal — the numbered, tracked unit of change for the JDK.** Every feature, removal, or infrastructure effort (modules, virtual threads, ZGC, even build/test work) is written up as a JEP, goes through a status pipeline (`Candidate` → `Targeted` → `Integrated` → `Completed`), and the set of targeted JEPs is what a JDK release actually contains. Reading the JEP index is how you answer "what's in Java N" precisely.

## How a change becomes a release entry

A proposal starts as a `Draft`, becomes a `Candidate` once scoped, and is `Targeted` to a specific JDK by the release leads. Implementation and review happen under that target; at GA the JEP is `Integrated` and later `Completed`. A JEP can also be **withdrawn** before it ever ships — string templates (JEP 430) previewed in 21, previewed again as 459, and the third-preview JEP 465 was withdrawn, so the feature left the platform without ever being finalized ([[What is a preview feature in Java]]).

JEP numbers are proposal IDs, not version numbers: JEP 444 (virtual threads final) landed in 21, JEP 400 (UTF-8 by default) in 18, JEP 519 (compact object headers product) in 25. Big platform efforts often span several JEPs across releases — Amber (language), Loom (concurrency), Panama (native interop) — and some JEPs are invisible to users (CI, tests, GC interface work) ([[What is an incubator module]]).

```d2
direction: right
d: "Draft" {
  width: 120
  height: 50
}
c: "Candidate" {
  width: 140
  height: 50
}
t: "Targeted to JDK N" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
i: "Integrated at GA" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
w: "Withdrawn\n(430 string templates)" {
  width: 210
  height: 60
  style.fill: "#ffcdd2"
}
d -> c
c -> t
t -> i
t -> w: "may never ship"
```

**Fig. 1.** The JEP pipeline. `Targeted` names the release; `Integrated` means it shipped. A targeted JEP can still be withdrawn — string templates never finalized.

```java
// Conceptual — release content is read from the JEP index, not computed.
// Examples of JEP number -> release mapping (interview-dense ones):
// JEP 261 modules            -> JDK 9
// JEP 248 G1 default         -> JDK 9
// JEP 254 compact strings    -> JDK 9
// JEP 400 UTF-8 by default   -> JDK 18
// JEP 444 virtual threads    -> JDK 21
// JEP 519 compact headers    -> JDK 25
```

**Listing 1.** Conceptual mapping crib: the JEP number is stable across the process and never renumbered; the release column is what changes when a JEP slips a train.

> [!warning] JEP number is not a version and not a feature guarantee
> Saying "JEP 444 is Java" is meaningless without the release, and "it has a JEP" does not mean it shipped — proposals die at every stage, including after preview. Also do not equate JEP count with size: infrastructure JEPs (build, test, docs) outnumber user-visible features in most releases. Interview answers that cite a JEP should cite the release it landed in ([[What was new in Java 21]]).

> [!tip] Interview answer
> **A JEP is the JDK's tracked enhancement unit — numbered proposal with a lifecycle from candidate to targeted to integrated.** A release is its set of targeted JEPs; numbers like 444 or 519 are proposal IDs, not versions, and proposals can be withdrawn — string templates previewed twice and never shipped. I read the JEP index per release rather than trusting memory.
