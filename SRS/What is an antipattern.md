<!--
reps: 0
priority: 0
-->
#Patterns/AntiPatterns #SRS

# What is an antipattern

> [!abstract] Short answer
> An antipattern is a commonly used, recurring "solution" that looks reasonable at first but reliably does more harm than good, **and** for which a documented, repeatable, effective alternative exists. Andrew Koenig coined the term in 1995 by inverting the GoF idea of a design pattern.

## Two traits that make it an antipattern

A bad habit or a one-off mistake is not an antipattern. Both traits must hold:

1. **Commonly used, superficially effective.** The process, structure, or way of acting appears appropriate at first and is adopted repeatedly, but its drawbacks outweigh its benefits.
2. **A working alternative exists.** There is another way to solve the same problem that is documented, repeatable, and effective where the antipattern is not. Without the alternative, the critique is just renaming the problem.

Like patterns, antipatterns carry a rule of three: the solution must have been observed at least three times before it earns the name. This keeps the catalog limited to recurring traps rather than personal pet peeves.

```d2
direction: down
cand: "Candidate approach" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
rec: "Recurring\n(seen 3+ times)?" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
look: "Looks effective\nat first?" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
worse: "Drawbacks\noutweigh benefits?" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
alt: "Documented, repeatable\nalternative exists?" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
anti: "Antipattern" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}
just: "Just a bad idea\nor a mistake" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
cand -> rec
rec -> look: yes
look -> worse: yes
worse -> alt: yes
alt -> anti: yes
rec -> just: no
alt -> just: no
```

**Fig. 1.** Both defining traits are checked against the same recurrence bar as a design pattern; failing either leaves you with an ordinary mistake, not a named antipattern.

## Where the catalog comes from

Koenig introduced the term in 1995, inspired by the GoF book that catalogued reliable design solutions. The 1998 book AntiPatterns popularized the idea and widened the scope past software design into software architecture and project management; later authors extended it to organizational and cultural failure modes.

Well-known examples on the software side include:

* **God object** - one class concentrates control and knowledge of the whole program.
* **Magic number** - an important literal whose meaning is unexplained in the code.
* **Poltergeist** - ephemeral controller classes that exist only to invoke methods on other classes.
* **Big Ball of Mud** - a system with no perceivable architecture.

On the project management side the same book lists Analysis Paralysis, Death by Planning, Viewgraph Engineering, Smoke and Mirrors, and Fire Drill, among others. The concrete catalog lives in [[What are examples of common software anti patterns]].

The positive counterpart of the term matters for interviews: an antipattern is defined against the pattern idea, so it helps to know [[What are the main characteristics of software design patterns]] and the honest [[What are downsides of design patterns]] before judging either.

```java
// Magic number antipattern and its documented alternative
double price = qty * 0.9;          // what is 0.9?
double price2 = qty * DISCOUNT;    // named constant: intent is visible
```

**Listing 1.** The refactoring direction for a magic number is the named constant; every antipattern entry is expected to carry such an alternative.

> [!warning] Labeling is not refactoring
> Two popular lies: first, "anything I dislike is an antipattern" - both defining traits must hold, including the documented alternative. Second, "naming the antipattern fixes it" - Big Ball of Mud systems are still common in practice because business pressure, developer turnover, and software entropy keep them alive; documentation only helps when it includes the way out.

A worked example of the same distinction: [[Why is the singleton pattern often labeled an anti pattern]] shows a legitimate pattern whose usual application fails both traits when it smuggles global state into a codebase.

> [!tip] Interview answer
> An antipattern is a recurring, commonly used approach that looks effective but costs more than it delivers, and a documented, repeatable alternative exists to replace it. The term was coined by Andrew Koenig in 1995 as an inversion of design patterns, and the 1998 AntiPatterns book extended it from code design to architecture and project management. It differs from a plain bad idea by being common, recurring, and having a known fix.
