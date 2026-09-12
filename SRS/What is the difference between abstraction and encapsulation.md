<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Encapsulation #SRS

# What is the difference between abstraction and encapsulation

> [!abstract] Short answer
> **Abstraction** answers *what*: it defines the simplified view a client works with — which operations exist and which details are irrelevant to them. **Encapsulation** answers *how it is protected*: state and the methods guarding it live in one unit, and the internals are unreachable from outside. The two cooperate at one boundary: abstraction designs the visible contract, encapsulation makes the wall behind it solid — an abstraction without encapsulation is a wish, encapsulation without abstraction is a sealed box with no meaningful API ([[What is abstraction]], [[What is encapsulation]]).

## Same class, two different questions

Take a temperature type. The *abstraction* is the contract: a client knows `reading()` and `warmBy(delta)` — and nothing about Celsius scales, storage, or validation. The *encapsulation* is the enforcement: `celsius` is private, every mutation funnels through a guard that rejects values below absolute zero, so the invariant is checked in exactly one place. Ask the design questions separately and the difference stops sounding academic: "what does the client see?" — abstraction; "can the client bypass the rules?" — encapsulation. Java puts the first in interfaces and API shape, the second in access modifiers and field discipline ([[How would you explain encapsulation in object oriented design]]).

```java
interface Thermometer {                    // abstraction: the visible contract
    double reading();
    void warmBy(double delta);
}

class CelsiusThermometer implements Thermometer {   // encapsulation: hidden state + guards
    private double celsius;                        // never exposed directly
    CelsiusThermometer(double c) { setCelsius(c); }
    void setCelsius(double c) {
        if (c < -273.15) throw new IllegalArgumentException("below absolute zero");
        this.celsius = c;
    }
    public double reading() { return celsius; }
    public void warmBy(double delta) { setCelsius(this.celsius + delta); }
    public String toString() { return celsius + " C"; }
}
```

**Listing 1.** The interface is the abstraction; the private field plus the guard is the encapsulation. Clients see only the top line.

```text
25.0 C
invariant guarded: below absolute zero
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_7`): the contract serves the client; the wall rejects the illegal mutation.

## Why they are routinely confused

Both hide things, so words blur. The clean split used by the classic texts: abstraction is about **removing detail from the client's view** (an interface can abstract even with a single implementation, and methods abstract without any objects); encapsulation is about **hiding implementation and state** (information hiding — the module's internals are nobody else's business). They can exist separately, which proves they are different: a fully encapsulated "God class" that hides its state but offers a sprawling 60-method API has encapsulation with *bad* abstraction; a public interface over a class of public mutable fields is abstraction with *no* encapsulation. Real design scores both: narrow contract plus solid wall — which is exactly why the pair appears together in the OOP principles list ([[What are the main oop principles]], [[What is the difference between abstraction and polymorphism]]).

> [!warning] "Encapsulation = getters and setters" inverts the idea
> Auto-generating an accessor pair per field reproduces the public-field problem with extra syntax: the API still exposes raw state, so invariants cannot be enforced anywhere. Encapsulation starts from *operations* — what can this object be asked to do — and state access shrinks to what those operations need. A class that is genuinely just data should be a record and stop pretending ([[How would you explain problems with public mutable fields in Java]]).

> [!warning] Abstraction is judged from the client side, not by the `abstract` keyword
> An `abstract class` with leaky internals is bad abstraction; a concrete class behind a clean one-method interface is good abstraction. And encapsulation is binary at the edge: one leaked mutable reference — a returned internal collection, a constructor storing a caller's array — and the wall has a hole regardless of how many `private` keywords you wrote ([[What is the difference between shallow and deep copying in Java]]).

```d2
direction: down
client: "client" { width: 130; height: 32 }
contract: "abstraction: reading(), warmBy()" { width: 310; height: 38; style.fill: "#e3f2fd" }
wall: "encapsulation: private state + guard" { width: 330; height: 38; style.fill: "#e8f5e9" }
client -> contract: "sees only this"
contract -> wall: "enforced by this"
```

**Fig. 1.** Two questions, one boundary: the blue layer is what the client knows; the green layer is what keeps the promise.

> [!tip] Interview answer
> Abstraction is the design view — it defines which operations clients see and hides irrelevant detail behind a contract. Encapsulation is the protection — state and the rules over it are locked inside one unit, so the rules are enforced in one place and nothing outside can bypass them. They differ in question and job: abstraction answers what the client sees, encapsulation ensures the client cannot get around it. A getter-and-setter class with private fields but raw state access has no real encapsulation; an interface nobody can implement safely has abstraction without a wall. Good design needs both: a narrow contract, and a boundary that actually holds.
