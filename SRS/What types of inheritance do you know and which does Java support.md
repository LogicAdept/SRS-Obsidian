<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #SRS

# What types of inheritance do you know and which does Java support

> [!abstract] Short answer
> The usual taxonomy: **single** (one parent), **multilevel** (chained: A→B→C), **hierarchical** (one parent, several children), **multiple** (two or more parents at once), and **hybrid** (combinations of the above). For **classes** Java supports single, multilevel and hierarchical — every class has exactly one direct superclass. **Multiple class inheritance is banned** — two parents mean duplicated state and ambiguous members: the diamond problem. Multiple *type* inheritance exists only through **interfaces** — stateless, and since Java 8 able to carry default behavior, with the compiler forcing explicit resolution when two defaults collide ([[Does Java support multiple inheritance for classes]], [[How does Java model multiple inheritance with interfaces]]).

## The taxonomy, mapped to Java

- **Single**: `class B extends A`. The everyday case, and the whole chain bottoms out at `Object` ([[Do Java classes inherit from Object explicitly or implicitly]]).
- **Multilevel**: `A → B → C` — each class inherits transitively; `new C()` is an `A`, a `B` and a `C`.
- **Hierarchical**: one superclass, many direct subclasses (`D extends A` next to `B extends A`) — the standard shape of framework type families.
- **Multiple (of classes)**: **not supported.** C++ needed virtual inheritance and explicit disambiguation to live with it; Java chose one-superclass plus interfaces instead.
- **Multiple/hybrid (of types)**: `class C implements I, J` — many contracts at once; `interface I extends J, K` composes contracts. Interfaces have no instance fields, so there is no state diamond to resolve; the only conflict is two **default methods** with the same signature, which will not even compile in an implementing class until it overrides.

```java
class A {}
class B extends A {}          // multilevel: A -> B -> C
class C extends B {}          // hierarchical: D also extends A
class D extends A {}

interface Elected { default String role() { return "elected"; } }
interface Appointed { default String role() { return "appointed"; } }

// class Manager implements Elected, Appointed {}   // would NOT compile: unrelated defaults

class Manager implements Elected, Appointed {      // diamond of behavior: must resolve
    @Override public String role() { return Elected.super.role() + " + " + Appointed.super.role(); }
}

public class Demo {
    public static void main(String[] args) {
        System.out.println("multilevel: " + (new C() instanceof B) + ", " + (new C() instanceof A));
        System.out.println("hierarchical: " + (new D() instanceof A));
        System.out.println("diamond resolved: " + new Manager().role());
    }
}
```

**Listing 1.** Class-side types (multilevel, hierarchical) and the interface diamond with its explicit resolution.

```text
multilevel: true, true
hierarchical: true
diamond resolved: elected + appointed
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_8`): transitive substitutability holds up the class chain, and the default-method conflict is resolved by an override that composes both supertypes via `Elected.super.role()`.

## Why the diamond matters at interview

The question is really "why did Java restrict inheritance, and what did it give back?" The banned part: two superclasses means two copies of instance state and two inherited bodies for the same signature — ambiguity by construction. Java chose one superclass plus interfaces instead. Mentioning `default`-method resolution (`X.super.m()`) and the no-state property of interfaces is what separates a recited answer from a real one ([[What is the difference between extends and implements in Java]]).

> [!warning] "Java has no multiple inheritance" is imprecise — and examinable
> Java has no multiple inheritance **of classes**. It has multiple inheritance **of type** (interfaces) and, since Java 8, multiple inheritance **of behavior** (defaults). The fully wrong version adds "so there is no diamond problem in Java" — there is one, exactly in interface defaults, and the compiler stops compilation until you resolve it ([[What is the difference between inheritance and polymorphism]]).

> [!warning] Hybrid does not mean "anything goes"
> Even the legal shapes can be misused: a five-level chain is usually a design failure dressed as taxonomy, and twenty siblings overriding each other's internals is white-box reuse. The taxonomy classifies *structure*; substitutability ([[How would you explain the Liskov substitution principle in SOLID]]) decides whether the structure is sound.

```d2
direction: down
a: "A" { width: 110; height: 32 }
b: "B" { width: 110; height: 32; style.fill: "#e3f2fd" }
c: "C" { width: 110; height: 32 }
d: "D" { width: 110; height: 32 }
el: "Elected: role()" { width: 170; height: 36; style.fill: "#fff8e1" }
ap: "Appointed: role()" { width: 180; height: 36; style.fill: "#fff8e1" }
m: "Manager — must override role()" { width: 280; height: 38; style.fill: "#e8f5e9" }
a -> b: "extends"
b -> c: "extends (multilevel)"
a -> d: "extends (hierarchical)"
el -> m: "implements"
ap -> m: "implements"
```

**Fig. 1.** Left: single-parent class shapes Java allows. Right: the diamond Java allows only in interfaces — with forced explicit resolution.

> [!tip] Interview answer
> The classic types are single, multilevel, hierarchical, multiple and hybrid. Java classes support the first three — one direct superclass per class, chains and sibling hierarchies are fine, everything rooted at Object. Multiple inheritance of classes is banned because two parents mean duplicated state and ambiguous members — the diamond problem. Instead, Java allows multiple inheritance of type through interfaces, and since Java 8 even of behavior through default methods; when two defaults clash, the class must override and can delegate explicitly with Interface.super.method. So the precise phrasing: no multiple class inheritance, but real multiple type and behavior inheritance via interfaces.
