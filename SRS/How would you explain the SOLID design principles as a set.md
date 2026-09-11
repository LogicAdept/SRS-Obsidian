<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/SOLID #SRS

# How would you explain the SOLID design principles as a set?

> [!abstract] Short answer
> SOLID is five object-oriented design principles named by Robert C. Martin (the acronym was coined by Michael Feathers) that all attack the same enemy: unhealthy dependencies that make code rigid and hard to change. Single Responsibility - one reason to change per module; Open-Closed - extend behavior without editing existing code; Liskov Substitution - subtypes must be safely usable through their base type; Interface Segregation - clients should not depend on methods they do not use; Dependency Inversion - high-level policy and low-level detail both depend on abstractions. They are heuristics for managing dependencies, not laws - the craft is knowing which one pays off for the pain you actually have.

## The five, in dependency-management order

Read as a sequence, SOLID escalates from class design to architecture. SRP and ISP shape classes and interfaces so a change touches one module ([[How would you explain the single responsibility principle in SOLID]], [[How would you explain the Interface Segregation Principle in SOLID]]). LSP keeps inheritance safe so the type system can be trusted ([[How would you explain the Liskov substitution principle in SOLID]]). OCP and DIP use abstraction to direct dependencies: OCP says the code is open for extension but closed for modification ([[How would you explain the open closed principle in SOLID]]); DIP says which direction the dependencies should point - policy should not depend on detail ([[How would you explain the Dependency Inversion Principle in SOLID]]).

```d2
direction: right
srp: "SRP\none reason to change" {
  width: 210
  height: 75
  style.fill: "#e3f2fd"
}
lsp: "LSP\nsafe substitution" {
  width: 210
  height: 75
  style.fill: "#fff3e0"
}
isp: "ISP\nno unused dependencies" {
  width: 210
  height: 75
  style.fill: "#e8f5e9"
}
ocp: "OCP\nextend, do not modify" {
  width: 210
  height: 75
  style.fill: "#fff3e0"
}
dip: "DIP\ndepend on abstractions" {
  width: 210
  height: 75
  style.fill: "#e3f2fd"
}
srp -> lsp -> isp -> ocp -> dip: "class design -> architecture"
```

**Fig. 1.** The five principles form a gradient: from how one class is shaped (SRP) to how whole modules depend on each other (DIP).

## How to use them without dogma

The set works as a diagnostic vocabulary: when a change ripples through ten files, some SOLID rule was violated somewhere - usually dependencies pointing the wrong way or a class serving several actors. In reviews, name the violated principle and the concrete pain, then decide whether the fix is worth it now. Applied blindly they produce interface-per-class ceremony and speculative abstraction - the over-engineering failure mode. The principles describe direction, not dosage: move your design toward them as the pain appears ([[What can violating SOLID principles lead to]]).

> [!warning] "SOLID-compliant" is not a virtue by itself
> A codebase can satisfy all five letters and still be a mess - or violate one deliberately and be better for it (a tiny script does not need DIP; a stable DTO does not need five interfaces). The principles were extracted from successful designs, not imposed before writing code. The honest interview answer names the smell first, the principle second: "every feature touches this class because it serves three actors - that is an SRP violation" - never "we must add an interface here because SOLID".

> [!tip] Interview answer
> SOLID is Martin's five dependency-management principles under a Feathers acronym: SRP, OCP, LSP, ISP, DIP. I read them as one idea at five scales - keep dependencies pointing toward stable abstractions so changes stay local. I apply them as diagnostics for real pain, not as checkboxes, because mechanical application just trades rigidity for over-engineering.
