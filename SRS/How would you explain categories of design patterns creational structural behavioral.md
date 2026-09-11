<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Patterns/GoF/Structural #Patterns/GoF/Behavioral #SRS

# How would you explain categories of design patterns creational structural behavioral

> [!abstract] Short answer
> The GoF catalog groups its 23 patterns **by intent**: **creational** patterns provide object-creation mechanisms, **structural** patterns assemble classes and objects into larger flexible structures, **behavioral** patterns distribute algorithms and responsibilities between objects.

## The three intent groups

Creational patterns abstract the construction process: Factory Method lets subclasses decide which class to instantiate, Abstract Factory produces families of related objects, Builder constructs complex objects step by step, Prototype copies existing instances, and Singleton guarantees a single instance with a global access point. Structural patterns care about composition: Adapter converts interfaces, Bridge splits abstraction from implementation, Composite treats trees uniformly, Decorator layers behavior, Facade simplifies a subsystem, Flyweight shares state to save memory, and Proxy controls access to a target. Behavioral patterns organize communication: Chain of Responsibility passes requests along handlers, Command turns a request into an object, Iterator traverses collections, Mediator centralizes interaction, Memento snapshots state, Observer broadcasts events, State switches behavior with internal state, Strategy swaps algorithms, Template Method fixes an algorithm skeleton, and Visitor separates algorithms from object structures. Each group is also surveyed card by card in [[What are examples of creational design patterns]], [[What are examples of structural design patterns]], and [[What are examples of behavioral design patterns]].

```d2
direction: right
creational: "Creational\nhow objects\nget created" { width: 210; height: 90; style.fill: "#e3f2fd" }
structural: "Structural\nhow objects\ncompose structures" { width: 210; height: 90; style.fill: "#fff3e0" }
behavioral: "Behavioral\nhow objects\ndivide duties" { width: 210; height: 90; style.fill: "#e8f5e9" }
creational -> structural -> behavioral: by intent
```

**Fig. 1.** One catalog, three questions: creation, composition, and communication.

## Where the classification stops

Intent-based grouping is not the only axis. On the scale axis, the lowest-level patterns are idioms bound to one language, while the highest-level architectural patterns can organize an entire application in any language — the GoF set sits between those poles. This is why classification questions sometimes expect the words idiom and architectural pattern, not just the three groups.

> [!warning] Intent decides membership, not code shape
> Adapter and Strategy produce nearly identical code — a class holding a reference to another and delegating to it — yet one is structural and the other behavioral, because the problem each solves differs. Answering "they look the same, so they are the same category" is the classic trap here.

> [!tip] Interview answer
> GoF patterns split by intent into three categories. Creational — how objects are created: Factory Method, Abstract Factory, Builder, Prototype, Singleton. Structural — how they compose into structures: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy. Behavioral — how they share work: Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor.
