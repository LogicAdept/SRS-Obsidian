<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #ProgrammingLanguages #SRS

# What is duck typing and how does Java differ from it?

> [!abstract] Short answer
> Duck typing — "if it walks like a duck and quacks like a duck, it is a duck" — judges an object by the **methods it actually has at call time**, not by any declared type; it is *run-time structural typing* in dynamic languages like Python or JavaScript. Java is **nominal**: a type must explicitly declare it implements an interface; two classes with byte-identical shapes but no declaration are unrelated. The practical difference is *when* a shape mismatch surfaces: compile time in Java, run time in duck-typed code ([[How would you explain static typing in Java]]).

## The duck mechanics

In a duck-typed language a function that calls `x.quack()` accepts anything with a `quack` — no interface, no declaration, no check before the call runs. The first invocation is the type check: a missing method becomes a run-time error (`AttributeError`, `TypeError`). The style makes small code fast to write and composes well with dynamic objects, but the set of valid inputs is invisible: nothing in the code states what the function needs, so refactoring a method name surfaces breakage only at run time — in the path that happens to execute ([[What is the difference between static and dynamic binding in Java]] — dispatch resolves late, but in Java the *set* of candidates was still compile-checked).

## Nominal Java: declaration is the type

Java asks the mirror question: not "does the object have `quack()`?" but "did its class **declare** the interface?". Two classes each with `quack()` are unrelated unless both name the interface; conversely, declaring it without the method is a compile error. Interfaces are the nominal contract — the declared shape, compiler-enforced at every call site ([[Why are interfaces important in object oriented design]]). The cost is ceremony (a type must be written up front); the payoff is that every duck-check the dynamic languages defer to run time already happened — the compiler is the duck checker.

## The typing spectrum

Place languages on one axis: **run-time structural** (Python, Ruby, JS — shape checked at call time), **compile-time structural** (Go — any type with the right method set satisfies an interface without declaration), **compile-time nominal** (Java, C#). Java can *emulate* run-time duck typing with reflection — look up the method by name and invoke it — but that abandons typing rather than providing a structural variant: no interface, no compile check, and failure surfaces as a reflective exception in production. Sealed hierarchies and pattern switches do not change the answer; they remain nominal constructs ([[What is polymorphism]]).

```d2
direction: right
rt: "run-time structural\nPython / JS\nshape checked at call time" {
  width: 250
  height: 72
  style.fill: "#ffebee"
}
ct: "compile-time structural\nGo\nmethod set satisfies interface" {
  width: 250
  height: 72
  style.fill: "#fff8e1"
}
nom: "compile-time nominal\nJava\ndeclaration required" {
  width: 240
  height: 72
  style.fill: "#e3f2fd"
}
rt -> ct: "check moves earlier"
ct -> nom: "declaration required"
```

**Fig. 1.** The spectrum: where the shape check happens decides where a mismatch hurts.

```java
interface Quacks { String quack(); }

class Duck  implements Quacks { public String quack() { return "quack"; } }
class Robot { public String quack() { return "beep"; } }   // identical shape, NOT a subtype

static String sound(Quacks q) { return q.quack(); }

// sound(new Robot())            -> compile error: nominal typing does the duck check
// robot.getClass().getMethod("quack").invoke(robot)  -> "beep": reflection abandons the check
```

**Listing 1.** Conceptual. `Robot` has the duck's method and still is not a `Quacks` — nominal typing; reflection can force the call, moving the failure to run time without adding any typing ([[What is polymorphism]]).

> [!warning] "Java has duck typing through reflection" is false
> Reflection bypasses typing instead of providing a structural one: the shape check does not move, it **disappears** — no interface is satisfied, nothing is verified until the reflective call throws in production. Structural typing exists as a compile-time concept (Go's interfaces); Java has interfaces with declarations ([[Why are interfaces important in object oriented design]]).

> [!tip] Interview answer
> Duck typing decides suitability by available methods at call time — run-time structural typing; Java decides by declared type — nominal. A class with the same method set but no `implements` is unrelated in Java, and that is the point: every shape mismatch the dynamic language defers to run time, the Java compiler settles at build time. When I need duck-like flexibility in Java, I model the expectation as a small interface and let the compiler do the duck check.
