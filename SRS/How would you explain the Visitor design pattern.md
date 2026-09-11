<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# How would you explain the Visitor design pattern

> [!abstract] Short answer
> Visitor separates an **algorithm from the object structure it runs on**: the new behavior lives in a visitor class with one method per element type, and each element exposes an `accept(visitor)` method that calls the visitor back with its own type — **double dispatch** picking the right method without instanceof chains.

## The mechanism and why accept exists

The visitor interface declares `visitCity`, `visitIndustry`, and so on — one method per element class. Each element implements `accept(Visitor v)` with a one-line body: `v.visitCity(this)`. That callback is the whole trick. A plain loop holds elements through the base type, so overloaded `visit` calls would all bind to the base-class overload at compile time; instanceof-and-cast chains would work but must be repeated at every use site. Double dispatch fixes it: the first dispatch is the polymorphic `accept` call on the element, the second is the overloaded `visit` call inside it, and because the element passes `this`, the runtime type decides which overload runs. The behavior payoff mirrors the Command pattern — the catalog calls Visitor a more powerful Command — operations become objects: one visitor exports the graph to XML, another computes totals, and elements never change.

```java
interface Element { void accept(Visitor v); }

record City(String name) implements Element {
    public void accept(Visitor v) { v.visitCity(this); }
}

class XmlExportVisitor implements Visitor {
    public void visitCity(City c)   { /* emit <city> */ }
    public void visitIndustry(Industry i) { /* emit <industry> */ }
}

for (Element e : graph) e.accept(new XmlExportVisitor());
```

**Listing 1.** The loop is clean because `accept` routes each element to the matching visit method — the element's runtime type makes the second dispatch.

## The trade-off the interview expects

Visitor adds behavior across a class hierarchy without editing the hierarchy — the Open/Closed win. The cost is symmetric and harsh: **adding or removing an element class requires updating every visitor**, since the interface enumerates all element types. It also fits only stable hierarchies — document ASTs, compiler trees, geographic graphs — and visitors may lack access to private element state, forcing accessors the element might not want to expose. The contrast with a pattern that wraps one call at a time is in [[How would you explain the Command design pattern]], and the family overview in [[What are examples of behavioral design patterns]].

> [!warning] The double-dispatch name-drop trap
> Saying "double dispatch means calling two methods" fails the follow-up "how". The precise answer: dispatch one is the virtual `accept` on the element, dispatch two is the overloaded `visit` inside it, and the point is defeating compile-time overload resolution on a base-typed variable. A second trap: claiming you can add new element types freely — that is exactly the direction Visitor does not support; it supports adding new operations.

> [!tip] Interview answer
> Visitor puts an operation into a visitor class with one visit method per element type, and elements call back via accept — v.visitX(this) — which is double dispatch that picks the right overload despite the base-typed loop variable. You add operations without touching element classes, but every new element class means editing all visitors, so it suits stable structures like ASTs.
