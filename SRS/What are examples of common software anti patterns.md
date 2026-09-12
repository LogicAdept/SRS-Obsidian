<!--
reps: 0
priority: 0
-->
#Patterns/AntiPatterns #SRS

# What are examples of common software anti patterns

> [!abstract] Short answer
> The set interviewers usually expect: **design-level** - God object, Poltergeist, Magic number, Big Ball of Mud, Golden Hammer, Lava Flow, Copy-paste programming - and **organizational** - Analysis Paralysis, Death by Planning, Smoke and Mirrors, Fire Drill. For each name you should be able to name one symptom and one refactoring direction.

## Design and code level

* **God object** - a single class handles all control in the program instead of control being distributed across classes. Symptom: a `Manager` or `Service` class with thousands of lines touching persistence, formatting, and workflow at once. Direction: split responsibilities by the domain concepts the class is actually juggling.
* **Poltergeist** - ephemeral controller classes that only exist to invoke methods on other classes and then die. Symptom: `Coordinator` or `Helper` classes with no state and no behavior of their own. Direction: give the responsibility to a class that keeps it, or delete the intermediary.
* **Magic number** - a literal with an important yet unexplained meaning, replaceable by a named constant. Symptom: `if (status == 3)`. Direction: named constant or enum.
* **Big Ball of Mud** - a system that lacks a perceivable architecture. Symptom: module boundaries exist only in package names; everything references everything. Direction: carve out boundaries around data or business capability, usually incrementally.
* **Golden Hammer** - forcing one familiar technology onto every problem. Symptom: everything becomes a scheduled job or everything becomes JSON blobs. Direction: choose per problem constraints, not per resume.
* **Lava Flow** - dead or misunderstood code that nobody dares remove. Symptom: commented-out blocks and "do not touch" methods. Direction: tests plus deletion.
* **Copy-paste programming** - duplicated logic that drifts apart with each fix. Direction: extract the shared abstraction once two or three copies stabilize.

Each entry above is only an antipattern because the definition in [[What is an antipattern]] holds for it: common, superficially effective, and replaceable by a documented alternative. The refactoring directions overlap with [[Which principles help you write clean maintainable code]], and the honest cost of patterns themselves is catalogued in [[What are downsides of design patterns]].

```d2
direction: right
design: "Design and code" {
  width: 250
  height: 70
  style.fill: "#e3f2fd"
}
org: "Organizational" {
  width: 250
  height: 70
  style.fill: "#fff3e0"
}
god: "God object\nPoltergeist\nMagic number" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
mud: "Big Ball of Mud\nGolden Hammer\nLava Flow" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
pm: "Analysis Paralysis\nDeath by Planning\nSmoke and Mirrors" {
  width: 240
  height: 100
  style.fill: "#fff3e0"
}
fire: "Fire Drill\nViewgraph Engineering\nThrow It Over the Wall" {
  width: 250
  height: 100
  style.fill: "#fff3e0"
}
design -> god
design -> mud
org -> pm
org -> fire
```

**Fig. 1.** The catalog splits into failures of structure you can see in the codebase and failures of process you see in the calendar.

## Organizational level

The 1998 AntiPatterns book moved the idea past code: **Analysis Paralysis** (endless modeling before any build), **Death by Planning** (effort goes into plans, not software), **Viewgraph Engineering** (slide decks substitute for working code), **Smoke and Mirrors** (demos and prototypes oversold by sales), **Fire Drill** (long monotony punctuated by short crises), and **Throw It Over the Wall** (imposing practices or artifacts on developers without buy-in).

```java
// God object symptom: one class decides, persists, formats, and notifies
class OrderManager {
    void place(Order o) {
        validate(o);            // business rules
        saveToDatabase(o);      // persistence
        renderInvoice(o);       // presentation formatting
        sendEmails(o);          // notifications
    }
}
```

**Listing 1.** Conceptual sketch of a God object; each responsibility above belongs to a different module with its own reason to change.

> [!warning] "Singleton is always an antipattern" is an overstatement
> The standard criticism of Singleton is concrete: global mutable state, hidden dependencies, and painful unit tests. That is why it is the classic example of a pattern often applied as an antipattern - but the claim "always" is false, and the GoF pattern itself is not on the antipattern list. See [[Why is the singleton pattern often labeled an anti pattern]] for the precise charge sheet.

> [!tip] Interview answer
> I would group the answers: at the design level - God object, Poltergeist, Magic number, Big Ball of Mud, Golden Hammer, Lava Flow, Copy-paste programming; at the process and organizational level - Analysis Paralysis, Death by Planning, Smoke and Mirrors, Fire Drill. For any name I quote, I give a concrete symptom in code or in the schedule and the refactoring direction, because naming without a documented alternative is exactly what separates a critique from an antipattern entry.
