<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/SOLID #SRS

# What can violating SOLID principles lead to?

> [!abstract] Short answer
> The predictable outcomes are Martin's four design smells. Rigidity: one change forces a cascade of dependent changes. Fragility: seemingly unrelated parts break when you change one. Immobility: useful code is welded to its context and cannot be reused or extracted. Viscosity: the wrong way (a hack) is easier than the right way, so the codebase trains everyone to hack. Below them sit the everyday symptoms - god classes, shotgun surgery, brittle tests, merge hotspots - and, when the principles get worshipped instead of applied, the opposite failure: over-engineering.

## How each violation maps to a smell

Violating SRP welds multiple actors into one module, so any actor's change ripples through the shared file - rigidity, then merge hotspots on the same class. Violating LSP leaves landmines behind base-type references: clients work until the one subclass arrives, then break in "impossible" places - fragility that testing struggles to root out ([[How would you explain the Liskov substitution principle in SOLID]]). Violating ISP forces every client to recompile and redeploy over changes it never uses, and litter implementations with stub throws. Violating OCP turns every new requirement into an edit of tested code - each release re-opens everything, which is how regression risk compounds ([[How would you explain the open closed principle in SOLID]]). Violating DIP hard-wires policy to technology, so the same business rule cannot be extracted or tested without the database - immobility.

```d2
direction: right
v1: "SRP violated\nmulti-actor class" {
  width: 220
  height: 65
  style.fill: "#fde8e8"
}
v2: "DIP/OCP violated\npolicy -> detail" {
  width: 220
  height: 65
  style.fill: "#fde8e8"
}
v3: "LSP violated\nbroken substitutability" {
  width: 220
  height: 65
  style.fill: "#fde8e8"
}
s1: "rigidity, merge hotspots" {
  width: 240
  height: 55
}
s2: "immobility, hard testing" {
  width: 240
  height: 55
}
s3: "fragility, surprise breaks" {
  width: 240
  height: 55
}
v1 -> s1
v2 -> s2
v3 -> s3
```

**Fig. 1.** Violations are diagnosable by the smell they produce - which is also how you prioritize: fix the violation behind the pain you actually have.

## The opposite extreme: dogma produces its own rot

Applying the letters mechanically - interface per class, layers of abstraction nobody crosses, one-method-per-actor microclasses - trades rigidity for speculative generality: every behavior change now edits seven files of ceremony. That is viscosity in reverse (the right way is now the bureaucratic way) and it is the textbook [[What is overengineering and how does it affect enterprise software|over-engineering]] profile. The professional habit is to let the smell trigger the principle: measure the pain (change amplification, breakage patterns, reuse failures), name the violated principle, refactor the minimum that relieves it ([[What is refactoring]]). SOLID is a vocabulary for diagnosing why change hurts, not a construction standard to satisfy up front ([[What are coupling and cohesion and how do they affect maintainability]]).

> [!warning] "We follow SOLID, therefore the design is good" proves nothing
> Conformance is invisible in a snapshot - the principles are about how the code RESPONDS to change, which only history reveals. A team can also claim SOLID while violating it structurally: an interface exists (looks compliant) but the client still knows the concrete type (DIP missed), or a class has one method but three actors (SRP missed). Judge by change patterns - where edits cluster, what breaks together - not by the presence of interfaces ([[How would you explain the SOLID design principles as a set]]).

> [!tip] Interview answer
> Violations surface as Martin's four smells: rigidity, fragility, immobility, viscosity - showing up as god classes, shotgun surgery, brittle tests, and hot files. But I always add the mirror risk: mechanically applying the principles manufactures over-engineering. I use SOLID as diagnostics - the pain tells me which principle to apply, and the fix is the smallest refactor that removes the pain.
