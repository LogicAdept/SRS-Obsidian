<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/DependencyInjection #Methodologies/Principles/SOLID #SRS

# What is the difference between dependency injection and dependency inversion?

> [!abstract] Short answer
> They are different kinds of thing that cooperate. Dependency injection (DI) is a MECHANISM: an assembler passes a class's dependencies to it - usually via constructor - instead of the class constructing or looking them up; Fowler's 2004 article fixed the name. Dependency Inversion (DIP) is a DESIGN PRINCIPLE about dependency direction: high-level policy and low-level detail should both depend on abstractions, with the abstraction owned by the policy side. You can inject concrete classes with no abstraction (DI without DIP), and you can depend on an abstraction supplied by a factory with no container (DIP without DI); together they are the standard implementation - DI as the how, DIP as the what-and-why.

## Principle vs mechanism, precisely

DIP speaks about the SHAPE of the dependency graph: which way the source-level arrows point. Its two statements - "high-level modules should not depend upon low-level modules; both should depend upon abstractions" and "abstractions should not depend upon details" - are satisfied by any wiring technique that leaves the policy independent of the detail: hand-built factories, plugin registries, a `main` that assembles everything, or a container. DI speaks about HOW an object receives its collaborators: pushed in from outside, not pulled from inside. The mechanism is principle-agnostic - `new CheckoutService(new StripeGateway())` is textbook DI and violates DIP the moment CheckoutService is the policy that should not know Stripe exists ([[How would you explain the Dependency Inversion Principle in SOLID]]).

```d2
direction: right
dip: "DIP - design principle" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
abs: "abstraction owned by\nhigh-level policy" {
  width: 260
  height: 70
}
di: "DI - wiring mechanism" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
impl: "concrete adapters\ninjected at the edge" {
  width: 260
  height: 70
}
dip -> abs: "dictates the shape"
di -> impl: "supplies the objects"
abs -> di: "DI is how you typically\nrealize DIP"
```

**Fig. 1.** DIP decides what the dependencies should look like; DI is the wiring step that delivers them.

## The four combinations, as a quick test

DI + DIP: the usual container setup - policy declares an interface it owns, an adapter implements it, the container injects the adapter ([[How can you apply dependency injection with a Spring bean]]). DI without DIP: constructor-injected concrete `PostgresOrderRepository` - wiring is clean, but policy is welded to the technology. DIP without DI: the policy calls `OrderRepositoryFactory.create()` - the arrow still points to the abstraction, no injector anywhere. Neither: `new PostgresOrderRepository()` inside the service - the classic tight coupling both ideas exist to remove ([[How would you explain dependency injection]]). This quadrant is a strong interview answer because it shows the two concepts are orthogonal rather than synonyms ([[What is the difference between dependency injection and inversion of control]]).

> [!warning] "We inject an interface, therefore DIP is satisfied" - the ownership check fails most teams
> Creating an interface that mirrors the concrete class and injecting it leaves the POLICY depending on an abstraction phrased in the DETAIL's vocabulary - the arrow still points the wrong way in spirit; DIP requires the abstraction to serve the policy's needs, named in the policy's language. The mirror-image error: calling any use of `new` "a DIP violation" - constructing stable, dependency-free value objects is fine; the principle targets policy-to-technology edges, not object creation as such ([[What is the Strategy pattern used for]]).

> [!tip] Interview answer
> Dependency injection is the mechanism - an assembler hands dependencies in through the constructor instead of the class looking them up. Dependency inversion is the principle - both policy and detail depend on abstractions the policy owns. I can inject concretes without inverting anything, and I can invert with plain factories and no injector; in practice the container does injection, and DIP tells it which abstraction to wire.
