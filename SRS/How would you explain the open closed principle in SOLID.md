<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/SOLID #SRS

# How would you explain the open closed principle in SOLID?

> [!abstract] Short answer
> OCP - coined by Bertrand Meyer in 1988 and central in Robert Martin's work - says a module should be open for extension but closed for modification: you add new behavior by adding new code that plugs into stable abstractions, not by editing tested code and re-releasing it. In practice: when a new requirement arrives as another variation of something, the design should let you implement the variation behind an interface the system already calls.

## The mechanism: abstraction is the closure

The closure comes from depending on abstractions. If billing calls a `PaymentMethod` interface, adding PayPal means writing a new implementation - billing code is untouched, so it cannot regress. If billing instead switches on an enum and edits every `if` chain, every payment change reopens tested code. Martin's OCP article frames it exactly this way: the goal is to design modules that never need changing when requirements extend in the directions you anticipated - and honest about the limit: you cannot close a module against every conceivable change, only against the axis of variation you can see ([[What is the Strategy pattern used for]]).

```java
interface ShippingRate { Money cost(Parcel p); }

final class GroundRate implements ShippingRate { ... }
final class AirRate implements ShippingRate { ... }

// New requirement (overnight shipping) = new class, zero edits here:
final class OvernightRate implements ShippingRate { ... }

class Checkout {
    private final ShippingRate rate;          // closed: stable dependency
    Checkout(ShippingRate rate) { this.rate = rate; }
    Money total(Parcel p) { return rate.cost(p).add(handling()); }
}
```

**Listing 1.** Conceptual. The `ShippingRate` abstraction closes `Checkout` against new rate kinds; extension happens by adding implementations, which is the OCP move.

## Cost and boundaries

Abstraction has a price: parameter objects, interfaces, and indirection that a reader must follow. Closing every seam "just in case" manufactures that price everywhere - the speculative-generalization smell, which is over-engineering wearing SOLID's badge. The working method: watch which axis actually keeps changing (payment kinds, export formats, notification channels), close THAT one with an abstraction, and leave the rest concrete until it hurts. OCP also composes with the rest of SOLID - it is the payoff you get when DIP points dependencies at abstractions and LSP keeps the implementations substitutable ([[How would you explain the Dependency Inversion Principle in SOLID]]).

> [!warning] "OCP means never edit existing code" is the interview-fatal reading
> Every real change edits something - configuration, wiring, the new class itself. The principle scopes to behavior-bearing modules behind stable abstractions, not to the whole repository. The second trap: switch-cases are not automatically OCP violations; a closed set of two variants with no growth expected is better left concrete than abstracted on faith ([[What can violating SOLID principles lead to]]).

> [!tip] Interview answer
> OCP: extend by adding code plugged into stable abstractions, not by rewriting tested modules - Meyer coined it, Martin made it a design driver. I apply it selectively: find the axis that keeps changing, put an interface there, inject the variants. Closing every seam speculatively costs more than it saves, so the skill is choosing where the system is worth being closed.
