<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #SRS

# Why was object oriented programming favored by the industry for so long

> [!abstract] Short answer
> Because it matched the **economics and the problems of its era**, not because it was theoretically supreme. Four forces stacked up. **Modeling**: organizing a system around the nouns of the domain — objects, their types and responsibilities — made big systems explainable to teams and to customers. **State and invariants**: the dominant applications of the 1980s–2000s (GUIs, enterprise transaction systems) were piles of stateful things, and encapsulated objects with guarded state fit them naturally. **Ecosystems**: managed runtimes arrived wearing an OO suit — Smalltalk-80, then Java in 1995 with GC plus a huge class library — so choosing the paradigm also bought the toolchain. **Maintenance economics**: modularity and substitutability promised that change stays local — the selling point that justified adoption at scale.

## The maintenance argument, made concrete

The founding texts justified OO not by runtime power but by *change*. The classic modularity criteria — decomposability, composability, and above all **continuity**: a small change in requirements should hit one module, not ten — score well for designs built around objects with protected state and substitutable types. The demo that convinced a generation: an application loop written once against an interface, extended by *adding a class* — no modification of proven code, exactly the open-closed effect managers pay for.

```java
interface Shape { String render(); }

class Circle implements Shape { public String render() { return "draw circle"; } }
class Rect implements Shape { public String render() { return "draw rect"; } }

class App {                                    // written once, closed for modification
    void drawAll(Shape[] shapes) {
        for (Shape s : shapes) System.out.println(s.render());
    }
}

public class Demo {
    public static void main(String[] args) {
        new App().drawAll(new Shape[] { new Circle(), new Rect() });
        System.out.println("-- new type arrives --");
        class Triangle implements Shape {      // extension without touching App
            public String render() { return "draw triangle"; }
        }
        new App().drawAll(new Shape[] { new Circle(), new Triangle() });
    }
}
```

**Listing 1.** The extensibility promise in eleven lines: `App` never learns about `Triangle`.

```text
draw circle
draw rect
-- new type arrives --
draw circle
draw triangle
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_6`): the second run adds a new kind of object and the unchanged loop handles it — the maintenance property that sold the paradigm.

## Why "for so long", and why the wind shifted

The lock-in compounded: OO skills, OO frameworks (Swing, EJB, Spring), OO persistence (ORMs), OO design curricula — each made the next adoption cheaper; **interface-based contracts** also happened to fit component markets and big-team division of labor. The shift started from inside: GoF's own advice — favor composition over inheritance — hardened into a critique of deep hierarchies; concurrency made hidden mutable state expensive (threads *do not care about your objects*); and the web era's data-shaped problems wanted records, JSON mapping and pure transformations, not inheritance trees — so Java absorbed lambdas, streams, records and sealed types ([[What are the advantages and disadvantages of object oriented programming]], [[What are the main paradigms programming]]). OOP was not displaced; its monopoly was.

> [!warning] "OOP won because it is objectively best" is the wrong answer
> The honest framing: it won because domain modeling, encapsulated state and an ecosystem of managed runtimes fit the dominant problems and team economics of its time. Claiming superiority as an absolute triggers the senior follow-up — "then why did every mainstream OO language add lambdas, records and streams?" — and you should be ready to answer with the state-organization argument, not ideology ([[What is the difference between inheritance and polymorphism]]).

> [!warning] Do not oversell "objects model the real world"
> The marketing line "the world is made of objects" was always shaky — the world is also made of processes, rules and data flows. The durable version is narrower: objects model *systems of interacting stateful components*, which is what enterprise software mostly was. Shapes, accounts and widgets were the sweet spot; JSON trees and pipelines were not ([[What is OOP]]).

```d2
direction: right
f1: "domain modeling\n(nouns, teams)" { width: 220; height: 50 }
f2: "encapsulated state\nfits GUI/enterprise" { width: 230; height: 50; style.fill: "#e3f2fd" }
f3: "managed runtimes\nSmalltalk, Java 1995" { width: 230; height: 50 }
f4: "maintenance economics\nlocal change, substitutability" { width: 250; height: 50; style.fill: "#e8f5e9" }
f1 -> f2: "compounded"
f2 -> f3: "shipped as"
f3 -> f4: "justified by"
f4 -> f1: "lock-in loop"
```

**Fig. 1.** Four reinforcing forces — each made the next adoption cheaper, which is why the dominance lasted decades.

> [!tip] Interview answer
> OOP dominated because it fit its era on four levels: it modeled domains as interacting objects, which scaled to teams; encapsulated state matched the stateful GUI and enterprise systems of the time; managed runtimes with huge libraries shipped as OO — Java made the paradigm the default; and its modularity and substitutability promised local change, the maintenance property businesses pay for. The dominance loosened when its costs bit: deep inheritance proved brittle, hidden mutable state fought concurrency, and data-shaped problems wanted records and pipelines — so mainstream languages absorbed functional and data-oriented features. OOP stopped being the monopoly, not the tool.
