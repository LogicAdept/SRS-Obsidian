<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #Java/OOP/Polymorphism #SRS

# What is the difference between inheritance and polymorphism

> [!abstract] Short answer
> **Inheritance** is a *structural relation between classes*: `Child extends Parent` — the child inherits members, is substitutable, and Java wires it into one superclass. **Polymorphism** is a *run-time behavior of calls*: one call site written against a supertype executes different bodies depending on the actual object. Inheritance is how types are related; polymorphism is what happens when you invoke through the related type. They usually travel together — but not always: interfaces give polymorphism with no class inheritance, and inheritance gives you **no** polymorphism for fields and static methods, which resolve at compile time ([[What is inheritance]], [[What is polymorphism]]).

## What dispatches and what does not

The clean experiment: one object of run-time class `Child`, held in a `Parent` variable, calling three things that *look* inherited the same way. The overridden **instance method** dispatches — the JVM picks the body from the run-time class (`invokevirtual`). The **field** does not — fields are resolved by the compile-time type, so the `Parent` field wins. The **static method** does not either — statics are called on the declared type with no receiver. So "inheritance gives polymorphism" is true for exactly one member kind: overridden instance methods ([[What mechanisms implement polymorphism in Java]], [[What is the difference between static and dynamic binding in Java]]).

```java
class Parent {
    String label = "parent-field";              // fields are NOT polymorphic
    static String who() { return "Parent.who"; } // statics are NOT dispatched
    String greet() { return "hello from " + getClass().getSimpleName(); }
}

class Child extends Parent {
    String label = "child-field";               // hides the parent field
    static String who() { return "Child.who"; }  // hides the parent static
    @Override String greet() { return "hello from " + getClass().getSimpleName(); }
}

public class Demo {
    public static void main(String[] args) {
        Parent p = new Child();
        System.out.println("greet(): " + p.greet());        // run-time body: Child
        System.out.println("label:  " + p.label);            // compile-time type: Parent field
        System.out.println("who():  " + p.who());            // static call resolved on Parent
    }
}
```

**Listing 1.** One `Child` object, three member accesses through a `Parent` reference.

```text
greet(): hello from Child
label:  parent-field
who():  Parent.who
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_4`): only the instance method shows the run-time class. If fields and statics behaved polymorphically, all three lines would print `Child` values.

## The other direction: polymorphism without class inheritance

An `implements` clause creates no superclass below `Object`, yet a loop over the interface dispatches per run-time class — subtype polymorphism is a property of the **type system**, not of `extends`. Java uses this constantly: a strategy lambda, a `Comparator`, a `List` behind which sit `ArrayList` or `LinkedList`. Inheritance's real contributions are *reuse* of implementation and a place in one class hierarchy; polymorphism's contribution is *open behavior* behind a fixed contract. Liskov's behavioral-subtyping requirement is what makes the combination safe: a subclass may only narrow preconditions and narrow post-behavior so that every property provable about supertype objects still holds — otherwise the dispatch you get is a bug factory, not a feature ([[How would you explain the Liskov substitution principle in SOLID]], [[Where should you prefer inheritance versus aggregation]]). The formal rule set: [[What does behavioral subtyping require beyond matching signatures]].

> [!warning] "Polymorphism = inheritance" fails the field/static follow-up
> If a candidate equates them, the natural trap is `Parent p = new Child(); p.field` or `p.staticMethod()` — both resolve on `Parent`. Saying "the child's field/method is used" contradicts the output above. The precise sentence: *overridden instance methods* dispatch on the run-time class; everything else binds statically ([[Which OOP principle does method overriding illustrate]]).

> [!warning] Inheritance without polymorphism is possible too
> `final` classes and `final` methods accept no override — you get pure implementation reuse and type substitutability, with no dynamic body selection. And in Java every class inherits from `Object` whether you care or not; using that inheritance for polymorphism is a choice made by *designing overridable instance methods*, not by `extends` alone ([[Why is Java described as not purely object oriented]]).

```d2
direction: right
p: "Parent p = new Child()" { width: 240; height: 38 }
g: "greet() -> Child body" { width: 210; height: 34; style.fill: "#e8f5e9" }
l: "label -> Parent field" { width: 200; height: 34; style.fill: "#fff8e1" }
s: "who() -> Parent static" { width: 200; height: 34; style.fill: "#fff8e1" }
p -> g: "instance: run-time class"
p -> l: "field: compile-time type"
p -> s: "static: compile-time type"
```

**Fig. 1.** Same object, same reference: one member kind dispatches dynamically, two bind statically.

> [!tip] Interview answer
> Inheritance is the class relation — a subclass extends one superclass, inherits its members and is substitutable. Polymorphism is call behavior — through a supertype reference, the same invocation runs the body of the actual run-time class. They overlap only for overridden instance methods: fields and static methods are resolved by compile-time type even in an inheritance chain, and interfaces provide polymorphism with no class inheritance at all. So I say: inheritance structures types, polymorphism behaves dynamically, and the pair is safe only when the subclass honors the supertype's behavioral contract.
