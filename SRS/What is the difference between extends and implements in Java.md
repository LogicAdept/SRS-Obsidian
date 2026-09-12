<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Interfaces #SRS

# What is the difference between extends and implements in Java

> [!abstract] Short answer
> **`extends`** establishes *class inheritance*: a class extends **one** superclass and inherits its implementation — fields, method bodies, constructors' behavior — becoming its subtype. **`implements`** establishes *interface realization*: a class implements **many** interfaces, inheriting **no state**, promising the declared methods (or inheriting default bodies since Java 8). Both create subtyping — either type may be used where the supertype is declared — but `extends` copies *capability*, `implements` copies *contract*. One more meaning: interfaces **extend** other interfaces (many at once), and type-parameter bounds use `extends` for both classes and interfaces ([[What is inheritance]], [[Why are interfaces important in object oriented design]]).

## The four shapes

1. **Class extends class** — one parent, implementation reuse + polymorphism: `class Dog extends Animal`. Java forbids `extends` of two classes because two parents mean two sets of state ([[Does Java support multiple inheritance for classes]]).
2. **Class implements interfaces** — many contracts, no state: `class Dog extends Animal implements Pet, Guide`. Note the syntax rule: `extends` clause first, `implements` second; an abstract class may leave some interface methods unimplemented, a concrete one may not.
3. **Interface extends interfaces** — contracts compose: `interface ObedientPet extends Pet, Trainable`. Here multiple inheritance is *allowed* because interface constants are stateless; conflicting default methods are resolved by the compiler forcing an override in the inheriting interface or class ([[What types of inheritance do you know and which does Java support]]).
4. **Type-parameter bounds** — `<T extends Comparable<T>>` uses `extends` even for interface bounds: in generics, `extends` means "any subtype of", never `implements`.

```java
interface Pet { String name(); }
interface Trainable { void train(); }
interface ObedientPet extends Pet, Trainable {}    // interfaces extend many interfaces

class Animal { String kind() { return "animal"; } }

class Dog extends Animal implements ObedientPet {   // extends ONE class, implements MANY
    public String name() { return "Rex"; }
    public void train() { System.out.println(name() + " learns a trick"); }
}

public class Demo {
    public static void main(String[] args) {
        Dog d = new Dog();
        System.out.println(d.kind() + " named " + d.name());
        d.train();
        System.out.println("Pet? " + (d instanceof Pet) + " | Animal? " + (d instanceof Animal)
                + " | ObedientPet? " + (d instanceof ObedientPet));
    }
}
```

**Listing 1.** All three relations on one class: superclass inheritance, multi-interface realization, interface composition.

```text
animal named Rex
Rex learns a trick
Pet? true | Animal? true | ObedientPet? true
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_9`): `Dog` is a subtype of all three — behavior came from the superclass and the interfaces' contract.

## Choosing between them

The design read: `extends` spends the **single-inheritance budget** and couples you to a parent's implementation — worth it only for a true is-a with substitutability ([[Where should you prefer inheritance versus aggregation]]). `implements` costs nothing structurally — many contracts, no state, no fragile-base coupling — which is why API design in Java leans interface-first: types like `List`, `Comparable`, `AutoCloseable` are contracts, and implementations `extends` something else entirely. Since Java 8, default methods blur the *code* difference (interfaces carry behavior), but not the **state** difference: interface fields are `public static final` constants only, so an interface can never own per-object state — the reason Java's diamond of interfaces is safe while the diamond of classes was banned ([[How does Java model multiple inheritance with interfaces]]).

> [!warning] "implements means no code" was true before Java 8 — say it carefully now
> Default methods let an interface ship behavior (`Comparator.reversed`, `Iterable.forEach`). The precise modern sentence: `implements` inherits **no state** and no constructor behavior; it may inherit **default method bodies** unless overridden. Saying flatly "interfaces have no implementation" at a 2026 interview is an instant correction ([[What mechanisms implement polymorphism in Java]]).

> [!warning] Access and modifiers differ too
> Interface methods are implicitly `public`; implementations must declare them `public`. Interfaces cannot be instantiated, extended by a class twice, or hold instance fields; a class cannot `extends` a `final` class; and since Java 17 `sealed` types restrict *who* may `extends` or `implements` them — the `permits` clause is the modern employer of both keywords ([[Which has the highest abstraction level among class abstract class and interface]]).

```d2
direction: right
animal: "Animal" { width: 130; height: 34 }
dog: "Dog" { width: 120; height: 34; style.fill: "#e3f2fd" }
pet: "Pet" { width: 110; height: 34; style.fill: "#fff8e1" }
tr: "Trainable" { width: 130; height: 34; style.fill: "#fff8e1" }
ob: "ObedientPet" { width: 150; height: 34 }
animal -> dog: "extends"
pet -> ob: "extends"
tr -> ob: "extends"
ob -> dog: "implements"
```

**Fig. 1.** One `extends` arrow from a class; `implements` pulls in a whole interface family.

> [!tip] Interview answer
> extends builds class inheritance: one superclass, inherited fields and method bodies, real is-a coupling — and Java allows only one of them. implements realizes interfaces: many at once, no state, a contract to fulfill — with default methods providing inherited behavior since Java 8. Interfaces extend other interfaces multiply, and generic bounds use extends for any subtype. Both give subtyping and polymorphism; the difference is state and coupling — extends copies capability from one parent, implements promises many contracts — which is why APIs are designed interface-first and extends is reserved for true is-a.
