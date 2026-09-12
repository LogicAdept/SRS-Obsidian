<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Polymorphism #SRS

# What is the difference between abstraction and polymorphism

> [!abstract] Short answer
> **Abstraction** is about the *interface between parts*: clients work with a simplified view — a named set of operations — while irrelevant detail stays behind it. **Polymorphism** is about *execution*: one call written against that view runs different bodies depending on the actual object. They operate at different levels and compose: abstraction defines the common type, polymorphism is the run-time behavior you get when you call through it. A `Shape` variable is abstraction; `s.area()` running `Circle.area` for one object and `Rect.area` for another is subtype polymorphism ([[What is polymorphism]], [[What is abstraction]]).

## Two lenses on the same two lines of code

Read a loop over `Shape[]` through both lenses at once. The **type** `Shape` is the abstraction: it hides each subclass's formula and promises one operation, `area()`. The **call** `s.area()` is polymorphic: the compiler checks only that `Shape` declares `area`, and the JVM picks the body by the run-time class — the same mechanism behind overriding ([[What is the difference between static and dynamic binding in Java]], [[How would you explain dynamic runtime polymorphism in Java]]). Removing either destroys the design: drop the common abstraction and there is no single loop to write — you call each concrete type by hand; drop polymorphism and the loop exists but every iteration would run the *same* body.

```java
interface Shape {                    // the abstraction: what every shape can do
    double area();
}

class Circle implements Shape {
    private final double r;
    Circle(double r) { this.r = r; }
    public double area() { return Math.round(Math.PI * r * r * 100.0) / 100.0; }
}

class Rect implements Shape {
    private final double w, h;
    Rect(double w, double h) { this.w = w; this.h = h; }
    public double area() { return w * h; }
}
```

**Listing 1.** The interface is the abstraction; the two implementations provide the different bodies.

```text
area = 3.14
area = 6.0
manual: 3.14, 6.0
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_3`): the loop over `Shape` runs two different `area` bodies through one call site; the last line shows the same calls without the shared abstraction — possible for two shapes, unwritable as a loop for N.

## Why interviewers force the distinction

Because the two words get used interchangeably and each claims the other's job. Abstraction is a **design activity**: choosing which operations to expose and which detail to suppress — it exists without any inheritance (an interface over one implementation, a module API, even a method signature). Polymorphism is a **language mechanism**: in Java chiefly subtype polymorphism through overriding, plus compile-time overloading (ad hoc) and generic type parameters (parametric) ([[What mechanisms implement polymorphism in Java]]). Abstraction is *how you see* an object; polymorphism is *how the object responds*. The classic ad-hoc polymorphism trap: overloaded methods feel polymorphic but resolve at compile time — nothing about the run-time object picks the body ([[Which OOP principle does method overriding illustrate]]).

> [!warning] "Abstraction means abstract class" — the most common lie
> The `abstract` keyword is one tool among several. A fully concrete class that publishes a narrow, meaningful API is abstracting; an `abstract` class that leaks its internals is not. Abstraction is judged from the client side: can the client be written without knowing the implementation? That is also why an interface over a single implementation is still useful — it *fixes the vocabulary* of the boundary ([[When should you use an abstract class versus an interface]]).

> [!warning] Abstraction without polymorphism is common — and fine
> A `Connection` interface with one `TcpConnection` implementation is pure abstraction: clients depend on the contract, and there is (today) exactly one body per operation. Saying "no second implementation means the abstraction is useless" misreads the purpose: the value is the fixed boundary and the suppressed detail, with substitutability as a *possible* later payoff ([[Why are interfaces important in object oriented design]]).

```d2
direction: down
client: "client code" { width: 160; height: 34 }
shape: "Shape.area()  <- abstraction" { width: 260; height: 38; style.fill: "#e3f2fd" }
c: "Circle.area()" { width: 150; height: 34; style.fill: "#e8f5e9" }
r: "Rect.area()" { width: 130; height: 34; style.fill: "#e8f5e9" }
client -> shape: "one call"
shape -> c: "if run-time Circle"
shape -> r: "if run-time Rect"
```

**Fig. 1.** Abstraction is the middle node clients see; polymorphism is the fan-out beneath it chosen per run-time class.

> [!tip] Interview answer
> Abstraction is the design view: clients work against a simplified contract and never see the detail behind it. Polymorphism is the mechanism where one call written against that contract executes different bodies depending on the run-time class. They are layers of the same design, not synonyms: the interface is the abstraction, the dynamic dispatch behind it is subtype polymorphism. Abstraction can exist without polymorphism — one implementation behind an interface — and polymorphism needs a shared abstraction to be usable, which is why you design abstractions first and get flexible dispatch as the payoff.
