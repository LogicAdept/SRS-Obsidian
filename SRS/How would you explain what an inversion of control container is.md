<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/IoC #SRS

# How would you explain what an inversion of control container is?

> [!abstract] Short answer
> An IoC container is a framework component that instantiates, configures, wires, and manages the lifecycle of your objects - so your code never decides when and how its collaborators get built. The "inversion" is Fowler's Hollywood-principle point: with a framework, the framework calls you - "don't call us, we'll call you" - instead of your code calling a library when you choose. Typical examples: Spring's `ApplicationContext`, Jakarta EE's CDI container, Google Guice. Dependency injection is the main mechanism containers use to hand your objects what they need ([[Which inversion of control containers or frameworks do you know]]).

## What it actually does at runtime

Strip the magic and the container does four jobs. Instantiate: build objects according to their configuration (components, scopes). Configure: fill in settings - properties, qualifiers, profiles. Wire: satisfy declared dependencies by constructor, setter, or field injection, resolving the dependency graph - including singletons shared across the app or fresh instances per request. Manage lifecycle: startup callbacks, `@PostConstruct`-style init, destruction hooks, and container events. In Spring terms the container is the `ApplicationContext` - a `BeanFactory` plus events, i18n, `Environment`, and auto-registered post-processors ([[What is the difference between inversion of control and ApplicationContext]], [[What is the Spring inversion of control container]]).

```java
// What you declare...
@Service
class CheckoutService {
    private final PaymentGateway gateway;
    CheckoutService(PaymentGateway gateway) {   // "I need a PaymentGateway"
        this.gateway = gateway;
    }
}

// ...and what the container does (conceptually, once at startup):
PaymentGateway gateway = new StripeGateway(config);
CheckoutService checkout = new CheckoutService(gateway);   // injected
```

**Listing 1.** Conceptual. Your class declares a need; the container resolves it against registered implementations at startup. The constructor stays test-friendly - in a unit test you inject a fake by hand, no container required.

## The inversion, precisely

Without a container your code is the director: it news up collaborators, decides construction order, and owns the wiring - so it is hardwired to concrete choices. With a container the direction flips: you register components and declare needs, and the container drives construction and calls your code (including framework callbacks - the lifecycle events are the container calling YOU). Fowler's article separates the general phenomenon - frameworks invert control flow - from the specific container flavor, dependency injection, where the inverted control is specifically "where do my dependencies come from" ([[What is the difference between dependency injection and inversion of control]]).

> [!warning] "The container IS IoC" and "IoC = dependency injection" both flatten the concept
> IoC is the PRINCIPLE (control flow inverted, framework calls you); the container is one runtime that applies it to object wiring; injection is the technique the container uses for dependencies. A GUI framework inverts control without any container; `ctx.getBean(...)`-everywhere inverts nothing - it re-imports control through a service-locator-shaped door. The second trap: field injection hides dependencies from the constructor, so the class no longer states its requirements - the container still works, the design got quieter and worse ([[How can you apply dependency injection with a Spring bean]]).

> [!tip] Interview answer
> An IoC container builds, configures, wires, and manages your objects so the code declares needs instead of constructing collaborators - the framework drives, you get called. Spring's ApplicationContext, CDI, and Guice are the usual examples, and dependency injection is the mechanism they use. I mention the Hollywood-principle framing and that constructor injection keeps the whole thing testable without a container.
