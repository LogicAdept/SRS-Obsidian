<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Polymorphism #SRS

# What is double dispatch and how do you implement it in Java?

> [!abstract] Short answer
> Java dispatches dynamically on the **receiver only**; the run-time type of an *argument* never influences method selection — overloads are fixed at compile time ([[How would you explain method overloading in Java]]). **Double dispatch** selects behavior by two run-time types at once (receiver + argument). Java achieves it with the **Visitor idiom**: `element.accept(v)` dispatches on the element's run-time class, then `v.visit(this)` dispatches again — on an argument whose static type is now the exact element class ([[What mechanisms implement polymorphism in Java]]).

## Why single dispatch is not enough

`Shape c = new Circle(); exporter.export(c)` — the call compiles to `export(Shape)`, because `c`'s *declared* type fixes the signature. At run time nothing re-selects: the fallback body runs for every shape. The information "this is really a `Circle`" is present in the object header and ignored by the call. A chain of `instanceof` checks or a pattern `switch` recovers the type manually, at the cost of centralizing all type knowledge in one place ([[What is the difference between static and dynamic binding in Java]]).

## The two-step routing of Visitor

Each element class overrides `accept`: `Circle.accept` calls `v.visit(this)` — and inside `Circle.accept`, the expression `this` has *static* type `Circle`. So the second call dispatches to `visit(Circle)` normally, as a virtual call on `v` with an exactly-typed argument. Two dynamic lookups in a row — receiver, then re-dispatched argument — produce the double dispatch. The sandbox run contrasts both routes: the direct overloaded call lands in the fallback for both shapes; the `accept` route reaches the right `visit` for each.

## Where it earns its keep

Visitor shines when the **type set is stable and closed** and operations keep growing — compilers over an AST, exporters over document nodes — and when the operation wants to traverse relationships between element types ([[What are alternatives to class inheritance]]). The modern Java alternative for simple cases is an exhaustive pattern `switch` over a sealed hierarchy, which achieves type-specific behavior without an `accept` protocol ([[What are switch expressions]]). The deep trade-off between the two shapes is the expression problem ([[What is the expression problem]]).

```d2
direction: right
c1: "client\nc: Shape = new Circle()" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
a1: "dispatch 1\nc.accept(v)\nrun-time class: Circle" {
  width: 230
  height: 72
  style.fill: "#fff8e1"
}
a2: "dispatch 2\nv.visit(this)\nstatic type here: Circle" {
  width: 240
  height: 72
  style.fill: "#e8f5e9"
}
c1 -> a1: "virtual on receiver"
a1 -> a2: "virtual on v, typed argument"
```

**Fig. 1.** Two chained virtual calls: the second one sees `this` as a `Circle` at compile time, so overload selection and dispatch agree.

```java
interface Shape { String accept(Exporter v); }
class Circle implements Shape {
    public String accept(Exporter v) { return v.visit(this); }   // this: static type Circle
}
class Square implements Shape {
    public String accept(Exporter v) { return v.visit(this); }
}
class Exporter {
    String visit(Shape s)  { return "visit(Shape): fallback"; }
    String visit(Circle c) { return "visit(Circle): json-circle"; }
    String visit(Square s) { return "visit(Square): json-square"; }
}
```

**Listing 1.** The full protocol: overloads on `Exporter` plus an `accept` override per element.

```text
direct:  visit(Shape): fallback / visit(Shape): fallback
accept:  visit(Circle): json-circle / visit(Square): json-square
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_12`): the direct route hits the fallback for both shapes — the argument's run-time type is invisible; the `accept` route reaches the exact `visit` per shape.

> [!warning] "Overloading gives you dispatch on the argument" is false
> Overload resolution reads the **compile-time** type and finishes before the object exists; at run time nothing re-selects among overloads. That is precisely why the direct route above returns the fallback and why the `accept` detour exists. Believing overloads dispatch at run time is one of the two classic dispatch confusions — the other being fields, which never dispatch at all ([[What is the difference between inheritance and polymorphism]]).

> [!tip] Interview answer
> Java does single dispatch: the receiver's run-time class picks the method; the argument's run-time type plays no role because overloads are fixed at compile time. Double dispatch routes through two virtual calls — `accept()` dispatches on the element, then `visit(this)` dispatches on an argument that is now statically the exact type. That is the Visitor machinery, and I use it when a stable type set faces many growing operations.
