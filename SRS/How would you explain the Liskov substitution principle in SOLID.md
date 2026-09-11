<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/SOLID #SRS

# How would you explain the Liskov substitution principle in SOLID?

> [!abstract] Short answer
> LSP says a subtype must be usable everywhere its base type is promised, without the caller knowing or caring which implementation it got. Barbara Liskov stated it in 1987 (formalized in her 1994 "Data Abstraction and Hierarchy" paper with Wing) as behavioral substitutability: the subtype may weaken preconditions and strengthen postconditions, never the reverse. Robert Martin brought it into SOLID, and its practical test is simple - if client code needs `instanceof` checks or conditional logic to survive certain subclasses, the hierarchy violates LSP.

## The contract view: strengthen and weaken

Substitution works through contracts. The subtype may ACCEPT MORE than the base required (weakened precondition) and may PROMISE MORE than the base did (strengthened postcondition); it may not demand more from callers nor promise less to them. Break the rule and code written against the base contract silently corrupts state when handed the derived object - the failure is in the HIERARCHY's design, not in the client that "should have checked". This is exactly Design by Contract's inheritance rule ([[How would you explain programming by contract and preconditions]]), and it is why LSP is about behavior, not signatures: Java's compiler enforces method signatures, but nothing in the type system enforces the behavioral part.

```java
class Rectangle {
    protected int w, h;
    public void setWidth(int w)  { this.w = w; }
    public void setHeight(int h) { this.h = h; }
    public int area() { return w * h; }
}

class Square extends Rectangle {          // classic LSP violation
    public void setWidth(int w)  { this.w = this.h = w; }   // surprises Rectangle clients
    public void setHeight(int h) { this.w = this.h = h; }
}

// Client written against the base contract:
int grow(Rectangle r) { r.setWidth(5); r.setHeight(4); return r.area(); } // 20, or 16 for Square
```

**Listing 1.** Conceptual. Mathematically a square IS a rectangle; behaviorally `Square` breaks `Rectangle`'s contract that the setters are independent. The client's expectation - not the geometry - defines substitutability.

## What substitution must preserve

Beyond pre/postconditions, LSP constrains visible behavior contracts: invariants of the base must hold in the subtype, and historical constraints must be respected - a subtype must not allow state the base treats as impossible. The JDK shows the escape hatch: `List.of` returns a list whose `add` throws `UnsupportedOperationException`, which does NOT break LSP because the base `List` contract itself declares `add` an optional operation that may refuse - substitution legality is settled by what the base contract says, and narrowing beyond it (or claiming the base promised something it did not) is where hierarchies rot ([[What is the Object equals contract]]).

> [!warning] "LSP = compilers catch violations" is false
> The compiler only checks signatures; LSP violations are BEHAVIORAL and pass compilation happily - a `Penguin extends Bird` whose `fly` throws `UnsupportedOperationException` compiles cleanly and detonates at runtime. The second trap: "fixing" LSP with `instanceof` in clients. Downstream type checks are the symptom and the punishment - they mean the hierarchy forced clients to know things the base contract did not say; the cure is redesign: split the hierarchy, compose instead of inherit ([[How does composition differ from inheritance]]), or move the misbehaving method out of the base ([[How would you explain common guidelines for using inheritance in OOP]]).

> [!tip] Interview answer
> LSP is behavioral substitutability: through a base-type reference, every subtype must honor the base contract - possibly accepting less demanding callers and promising stronger results, never the reverse. The Square-Rectangle case shows math intuition is not the test; client expectations are. If clients need instanceof to survive a subclass, the hierarchy is broken and I redesign it rather than patching with type checks.
