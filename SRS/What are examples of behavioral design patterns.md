<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What are examples of behavioral design patterns

> [!abstract] Short answer
> The GoF behavioral set is ten patterns: **Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor**. They are about algorithms and the assignment of responsibilities — who does what, and how objects talk.

## The catalog set

Chain of Responsibility passes a request along a line of handlers until one processes it. Command turns a request into a stand-alone object, which enables queues, scheduling, and undo. Iterator traverses a collection without exposing its internals — the Java `Iterator` interface is the everyday example. Mediator replaces a web of direct object links with one hub. Memento snapshots and restores an object's state without leaking its internals. Observer defines subscription so a publisher can notify many subscribers. State makes an object change behavior as its internal state changes. Strategy makes a family of algorithms interchangeable. Template Method fixes the algorithm skeleton in a superclass and lets subclasses override steps. Visitor separates an algorithm from the object structure it walks. The most drilled members get their own cards — [[What is Observer]], [[What is the Strategy pattern used for]], and [[How would you explain the Command design pattern]].

## Four ways to connect a sender and a receiver

The catalog itself contrasts four of these patterns by how they link senders to receivers: Chain of Responsibility passes the request sequentially through potential receivers until one handles it; Command builds a one-way connection through a command object; Mediator removes direct links and forces communication through itself; Observer lets receivers subscribe and unsubscribe dynamically. This contrast is a compact way to answer "how do these differ" without reciting definitions.

```d2
direction: right
cor: "Chain of Responsibility\nforward until handled" { width: 230; height: 80; style.fill: "#e3f2fd" }
cmd: "Command\nrequest as an object" { width: 220; height: 80; style.fill: "#fff3e0" }
med: "Mediator\none hub object" { width: 190; height: 80; style.fill: "#e8f5e9" }
obs: "Observer\ndynamic subscriptions" { width: 220; height: 80; style.fill: "#fff3e0" }
cor -> cmd -> med -> obs: sender to receiver styles
```

**Fig. 1.** Four connection styles among the behavioral patterns, from a linear chain to live subscriptions.

> [!warning] MVC is not a GoF behavioral pattern
> MVC is an architectural pattern for structuring whole applications; the Spring card [[What design patterns does the Spring Framework use]] lists it alongside GoF names, but the GoF catalog itself contains no MVC. Calling MVC "one of the ten behavioral patterns" is a recognizable mistake.

> [!tip] Interview answer
> Behavioral patterns distribute responsibilities: Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor. A clean mental grouping is by communication style — chains, command objects, mediators, subscriptions — plus the behavior-switching pair State and Strategy and the structure-walking Visitor.
