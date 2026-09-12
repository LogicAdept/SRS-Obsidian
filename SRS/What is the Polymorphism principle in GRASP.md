<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Polymorphism principle in GRASP

> [!abstract] Short answer
> The Polymorphism principle of GRASP says: when behavior varies by type, assign the varying behavior - using polymorphic operations - to the types for which it varies. The client calls one operation name; dynamic dispatch selects the right variant, so the client never branches on type.

## What the principle assigns where

The problem it answers: how do you handle alternatives based on type, and how do you build pluggable components? The solution: when related alternatives or behaviors vary by type, give the same operation name to the services of different objects and let each type implement its own version. The client depends only on the shared name - the interface - and the dispatch mechanism picks the variant. In this context polymorphism means exactly "giving the same name to services in different objects", which is narrower than the programming-language sense of the word.

```java
interface DiscountPolicy {
    Money discountFor(Sale sale);
}

class NoDiscount implements DiscountPolicy {
    public Money discountFor(Sale sale) {
        return new Money(0);
    }
}

class BulkDiscount implements DiscountPolicy {
    private final int minQuantity;
    private final int percentOff;

    BulkDiscount(int minQuantity, int percentOff) {
        this.minQuantity = minQuantity;
        this.percentOff = percentOff;
    }

    public Money discountFor(Sale sale) {
        boolean bulk = sale.lines().stream().anyMatch(l -> l.quantity() >= minQuantity);
        return bulk ? sale.total().percent(percentOff) : new Money(0);
    }
}

class Checkout {
    Money payable(Sale sale, DiscountPolicy policy) {
        return sale.total().minus(policy.discountFor(sale)); // no instanceof, no switch on type
    }
}
```

**Listing 1.** The variation lives inside the types that vary - each policy implements discountFor - and the checkout calls the operation without knowing which variant is behind it.

```d2
direction: right
client: "Checkout\npayable(sale, policy)" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
op: "DiscountPolicy\ndiscountFor(Sale)" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
v1: "NoDiscount\nreturns zero" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
v2: "BulkDiscount\npercent off" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
client -> op: calls one name
op -> v1: dispatch
op -> v2: dispatch
```

**Fig. 1.** The client binds to one operation name; adding a new variant type touches none of the client's branching, because there is no branching to touch.

## Where the language feature ends and the principle begins

The principle is a responsibility rule, not the language feature: it tells you where type-varying behavior belongs, while dynamic dispatch is merely how the JVM implements the call. The mechanics of that implementation are the territory of [[What is polymorphism]] and [[How would you explain dynamic runtime polymorphism in Java]], and the general survey of the feature lives in [[What kinds of polymorphism do you know]]. The same shape - one interface, interchangeable type-driven behaviors - is what the GoF Strategy structure formalizes; the relation is drawn in [[What is the Strategy pattern used for]] and [[What is the difference between the Strategy and State design patterns]].

> [!warning] Do not build hierarchies for variations that are not type-driven
> When the variation is a table of rates, a config value, or a numeric threshold, a polymorphic hierarchy is over-engineering: data handles it with less machinery. Class explosion - one subclass per value combination - is the classic abuse. The principle triggers only when related behaviors genuinely vary by type; when in doubt, weigh it against the cautionary notes in [[What are downsides of design patterns]].

> [!tip] Interview answer
> GRASP Polymorphism means: when behavior varies by type, push that variation into polymorphic operations of the varying types instead of branching on type in client code. The client calls one operation name and dispatch does the rest, which is what makes components pluggable. It is the responsibility-assignment ground that patterns like Strategy stand on - but it only applies when the variation is genuinely type-driven, not when a table or config value would do.
