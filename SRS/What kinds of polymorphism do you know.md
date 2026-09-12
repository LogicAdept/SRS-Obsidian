<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Polymorphism #SRS

# What kinds of polymorphism do you know?

> [!abstract] Short answer
> The taxonomy goes back to Strachey (1967) and Cardelli–Wegner (1985). **Universal** polymorphism: one body serves many types — **parametric** (generics: `List<T>` is compiled once, erased) and **inclusion** (subtype: an override is selected from the run-time class — the OOP pillar, [[What is polymorphism]]). **Ad-hoc** polymorphism: a *different* body per case — **overloading** (the compiler picks the most specific signature) and **coercion** (`int` widened to `long`). Java has all four; only inclusion dispatches at run time.

## Ad-hoc: a body per case

Overloading lets one name carry several bodies; the compiler resolves the call site to exactly one signature using the **compile-time** argument types ([[How would you explain method overloading in Java]]). No run-time mechanism is involved — two overloads are simply two unrelated methods sharing a name. Coercion is the silent sibling: `1 + 2L` converts `int` to `long` per built-in rule. Ad-hoc is "poly" in name only: the set of cases is finite and fixed per declaration.

## Parametric: one body, all types

Generics define one algorithm parameterized by type arguments: `Collections.swap` works for every `List<T>` with a single compiled body. Under erasure there is *one* `List` class at run time regardless of instantiation — the sandbox output shows `List.of(1)` reporting class `List12` ([[How would you explain covariance of generic and return types in Java]]). Bounds (`<T extends Comparable<T>>`) restrict the type parameter's capabilities — bounded polymorphism — without giving up the single-body property.

## Inclusion: the OOP mechanism

An override is selected by **dynamic lookup from the run-time class** — the third piece of [[What mechanisms implement polymorphism in Java]]. Universal in the strict sense: one declared contract (`Shape.area()`) serves every present and future subtype uniformly, which is exactly what makes the mechanism open-ended ([[What is the difference between static and dynamic binding in Java]]).

```d2
direction: down
poly: "polymorphism" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
uni: "universal\none body, many types" {
  width: 240
  height: 56
  style.fill: "#e8f5e9"
}
adh: "ad-hoc\na body per case" {
  width: 240
  height: 56
  style.fill: "#fff3e0"
}
par: "parametric\ngenerics, erased" {
  width: 220
  height: 48
}
inc: "inclusion\noverriding, dynamic" {
  width: 220
  height: 48
}
ov: "overloading\ncompile-time pick" {
  width: 220
  height: 48
}
co: "coercion\nint -> long" {
  width: 200
  height: 48
}
poly -> uni: "uniform"
poly -> adh: "per case"
uni -> par
uni -> inc
adh -> ov
adh -> co
```

**Fig. 1.** Cardelli–Wegner's tree mapped to Java features. Only the inclusion branch involves the run-time class of the receiver.

```java
class Printer {
    String show(String s) { return "overload:show(String) chosen"; }
    String show(Object o) { return "overload:show(Object) chosen"; }
}
class Greeter   { String greet() { return "base body"; } }
class Rude extends Greeter { @Override String greet() { return "override body"; } }
```

**Listing 1.** The three players: two overloads (ad-hoc), one override pair (inclusion), plus a generic `List` for the parametric branch.

```text
overload:show(String) chosen
overload:show(Object) chosen
override body
1 class=List12
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_11`): the overload is fixed by the compile-time type of the argument — `o` typed `Object` selects `show(Object)` even though it holds `"x"`; the override dispatches on the run-time class; the erased `List` reports `List12`.

> [!warning] "Overloading is run-time polymorphism" is false
> Overload resolution is a **compile-time** match on declared argument types; nothing re-selects at run time ([[What is the difference between static and dynamic binding in Java]]). Only overriding participates in dynamic dispatch. The classic trap: calling `show(o)` where `o` is an `Object` variable holding a `String` runs the `Object` overload — exactly what the sandbox output shows.

> [!tip] Interview answer
> I name three families. Ad-hoc: overloads and coercions — a different body per case, resolved statically at the call site. Parametric: generics — one erased body serving every type argument uniformly. Inclusion or subtype polymorphism: overriding dispatched on the receiver's run-time class — the OOP pillar. The universal/ad-hoc split is the deep one: generics and overriding scale to unbounded type sets with one body; overloading never leaves its declared cases.
