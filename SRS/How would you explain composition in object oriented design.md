<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP #SRS

# How would you explain composition in object oriented design

> [!abstract] Short answer
> **Composition** is building a complex object out of parts the object **owns**: the whole creates its parts, holds them in fields, exposes behavior by combining them, and their **life cycle is bound to the whole** — parts are born inside, are not shared, and die with it. It is the strongest form of the has-a relation: stronger than **aggregation**, where the part exists independently and may be shared ([[What is the difference between composition and aggregation]]). Alongside inheritance it is the second inter-class relation of object-oriented design — the one GoF tells you to prefer for reuse ([[Why is composition often recommended over inheritance]]).

## The mechanism: ownership, not just fields

A composed part has three signatures at once. **Created by the whole**: `Order.add` constructs `OrderLine` internally — no external code can hand the order a foreign line or keep a reference to one. **Encapsulated state**: the parts live in a private field; the whole's API is the only way in, which is what makes the whole's invariants enforceable ([[How would you explain encapsulation in object oriented design]]). **Bound life cycle**: `clear()` drops the lines, and nothing else in the program even knows they existed — "delete the order" automatically deletes its lines. In UML this is the *filled diamond* on the whole; aggregation's hollow diamond means the part came from outside and outlives the association.

```java
import java.util.ArrayList;
import java.util.List;

class OrderLine {
    final String sku; final int qty;
    OrderLine(String sku, int qty) { this.sku = sku; this.qty = qty; }
    public String toString() { return qty + "x " + sku; }
}

class Order {                                       // COMPOSITION
    private final List<OrderLine> lines = new ArrayList<>();
    void add(String sku, int qty) { lines.add(new OrderLine(sku, qty)); }  // parts born inside
    void clear() { lines.clear(); }                  // parts die with the whole
    public String toString() { return "Order" + lines; }
}

class Player {
    final String name;
    Player(String name) { this.name = name; }
}

class Team {                                        // AGGREGATION
    private final List<Player> roster = new ArrayList<>();
    void sign(Player p) { roster.add(p); }          // part made outside, shared in
    void disband() { roster.clear(); }              // players survive the team
    public String toString() { return "Team" + roster; }
}
```

**Listing 1.** Same shape of code, different ownership: `Order` manufactures its own lines; `Team` only registers players that exist independently.

```text
Order[2x JDK-21, 1x SSD-1T]
after clear(): Order[]
player still exists: Ada
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_2`): clearing the order destroys its parts, while the aggregated player outlives the disbanded team.

## Why design leans on it

Composition is how object systems scale beyond two or three levels of inheritance. Each part is a small unit with its own invariants; the whole composes behaviors instead of inheriting implementations, so changes stay local — modify `OrderLine` and no subclass of `Order` silently breaks. It is also the natural home of **run-time flexibility**: parts can be interfaces, so the same whole works with different implementations injected per environment or per test ([[What are alternatives to class inheritance]]). Real frameworks treat composition as the default modeling tool: a JPA entity "owns" its embedded values and cascaded children, a UI container owns its child widgets, an HTTP server owns its handler registry.

> [!warning] A field is not automatically composition
> Ownership decides. `Car` with `private final Engine engine = new Engine()` composes; `Car` that receives an `Engine` from the caller aggregates (or injects). Interviewers probe exactly this: "who creates the part, and who may see it?" If the answer is "someone else, and everyone", you have aggregation or plain association — not composition ([[What do in OOP expressions is-a and has-a]]).

> [!warning] Composition does not give you substitutability by itself
> Delegating to a concrete `Engine` field only reuses one implementation. The polymorphic payoff appears when the part is an **interface**: `Car` composed over `Motor` works with any `Motor` — and then you are programming to an abstraction, which is the actual engine of flexibility ([[What mechanisms implement polymorphism in Java]]).

```d2
direction: right
order: "Order (whole)" { width: 190; height: 36 }
l1: "OrderLine" { width: 150; height: 34; style.fill: "#e8f5e9" }
l2: "OrderLine" { width: 150; height: 34; style.fill: "#e8f5e9" }
player: "Player" { width: 140; height: 34; style.fill: "#fff8e1" }
team: "Team" { width: 130; height: 36 }
order -> l1: "owns (filled diamond)"
order -> l2: "owns"
team -> player: "uses (hollow diamond)"
```

**Fig. 1.** Composition: parts are created and destroyed with the whole. Aggregation: the part is referenced but owned by no one.

> [!tip] Interview answer
> Composition models a whole-part relation where the whole owns its parts: it creates them, hides them behind its API, and their life cycle is bound to its own — deleting the whole deletes the parts. That differs from aggregation, where the part exists independently and is just referenced. Design-wise, composition keeps changes local, enforces invariants at the whole's boundary, and behind interfaces it gives run-time flexibility that inheritance cannot — which is why the classic advice is to favor composition over class inheritance and reserve inheritance for true is-a relations.
