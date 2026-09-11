<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #SRS

# What are examples of creational design patterns

> [!abstract] Short answer
> The GoF creational set is five patterns: **Factory Method, Abstract Factory, Builder, Prototype, Singleton**. Each trades a direct constructor call for a controlled creation mechanism, which makes the code more flexible to change later.

## The catalog set and when each pays

Factory Method puts a creation hook in a superclass so subclasses decide the concrete type. Abstract Factory creates families of related objects without committing to their concrete classes — switching the whole family means switching the factory. Builder constructs a complex object step by step and produces different representations from the same construction code; it is the standard cure for a telescoping constructor with a dozen optional parameters. Prototype copies an initialized instance instead of constructing from scratch, useful when construction is expensive or the configuration matters more than the class. Singleton restricts a class to one instance with a global access point, typically for a shared resource — and, as [[Why is the singleton pattern often labeled an anti pattern]] discusses, that convenience has a well-known price.

```d2
direction: right
fm: "Factory Method\nsubclass picks\nthe type" { width: 190; height: 90; style.fill: "#e3f2fd" }
af: "Abstract Factory\nfamilies of\nrelated objects" { width: 190; height: 90; style.fill: "#e3f2fd" }
b: "Builder\nstep by step\nconstruction" { width: 190; height: 90; style.fill: "#fff3e0" }
p: "Prototype\ncopy an\nexisting object" { width: 190; height: 90; style.fill: "#fff3e0" }
s: "Singleton\none instance,\nglobal point" { width: 190; height: 90; style.fill: "#e8f5e9" }
fm -> af -> b -> p -> s: the five creational patterns
```

**Fig. 1.** The five creational patterns, from delegation of creation to its strict restriction.

> [!warning] Singleton is not the Spring singleton
> The GoF Singleton is a class-level restriction enforced by a private constructor, while a Spring singleton is a scope of the container: one bean instance per container. Identifying them is a common interview mistake — see [[How does a Spring singleton differ from the Gang of Four Singleton pattern]].

> [!tip] Interview answer
> Creational patterns: Factory Method — subclasses choose the concrete class; Abstract Factory — families of related products; Builder — step-by-step construction of complex objects; Prototype — cloning instead of constructing; Singleton — one shared instance with a global access point. All of them replace a bare constructor call with a controlled creation mechanism.
