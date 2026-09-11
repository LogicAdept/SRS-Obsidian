<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/IoC #SRS

# What is the difference between inversion of control and a service locator?

> [!abstract] Short answer
> A service locator is a PULL design: your class asks a locator object to fetch each dependency it needs - the decision and the lookup stay inside your code. Dependency injection is the PUSH design that inverts that control: an assembler hands dependencies to your class - typically through the constructor - and your class never knows where they came from. Martin Fowler's article that named "dependency injection" frames exactly this contrast; both approaches decouple classes from concrete implementations, but injection keeps the dependency explicit and the class locator-free, which is why containers prefer it.

## The mechanics side by side

With a locator, the class calls `Services.paymentGateway()` whenever it needs the gateway. The class still DEPENDS on the locator - a global-ish singleton whose API every class must know - and the dependency graph is invisible: nothing in the constructor says this class talks to billing. With injection, the assembler constructs the graph: `new CheckoutService(gateway)` - the requirement is stated in the signature, the source of the implementation is decided outside, and the class runs identically with a test fake. Fowler's summary: "with service locator the application class asks for it explicitly by a message to the locator; with injection there is no request - the object appears in properties that mean to be used."

```java
// Service locator: pull - hidden dependency
class CheckoutService {
    public Receipt checkout(Cart cart) {
        PaymentGateway gw = ServiceLocator.paymentGateway();  // static reach-out
        return gw.charge(cart.total());
    }
}

// Dependency injection: push - declared dependency
class CheckoutService {
    private final PaymentGateway gateway;
    CheckoutService(PaymentGateway gateway) { this.gateway = gateway; }
}
```

**Listing 1.** Conceptual. Same behavior, different ownership of the lookup: the locator version couples every class to `ServiceLocator` and hides the dependency; the injected version states it and lets the caller choose the implementation.

## Why containers chose injection - and where a locator still fits

Fowler's decisive argument is testability plus explicitness: with injection, the constructor IS the dependency list, so a reviewer sees requirements at a glance and a test passes fakes with no framework. A locator can also be testable (reset its registry), but nothing in the TYPE system reveals what a class will fetch at runtime - failures surface late. A locator also decides what "well-known" means: it works cleanly when the locator is a stable, widely agreed registry in the codebase; injection works when construction is centralized - which is exactly what an IoC container is ([[How would you explain what an inversion of control container is]]). Spring's `ApplicationContext.getBean()` is the classic locator-shaped API - legitimate for framework code and main-method bootstrapping, an anti-pattern inside business classes ([[What is the Spring inversion of control container]]).

> [!warning] "The container gives me DI, so getBean() everywhere is the same thing"
> Using the container as a giant locator re-imports the pull design: business classes coupled to `ApplicationContext`, dependencies hidden from signatures, and unit tests forced to boot a context to fetch collaborators - the inversion exists in the framework, but your code quietly opted out of it. The second confusion: calling the locator pattern "IoC" without qualifiers. Strictly, a locator is one way to get inversion-ish decoupling of implementation from interface, but the control stays with your class; the containers' promise is that control moves OUT ([[What is the difference between inversion of control and ApplicationContext]]).

> [!tip] Interview answer
> Service locator: my class asks a registry for dependencies - coupling survives, just rerouted, and the dependency list is hidden. Injection: an assembler pushes dependencies in through the constructor, so requirements are explicit and implementation choice lives outside the class. That explicitness is why containers standardize on injection, and why I reserve getBean-style lookup for bootstrap code, not business classes.
