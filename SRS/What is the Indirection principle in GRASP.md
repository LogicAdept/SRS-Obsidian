<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Indirection principle in GRASP

> [!abstract] Short answer
> Indirection is a GRASP principle: avoid direct coupling between two elements by assigning the responsibility for mediating between them to an intermediate object. The intermediary decouples the sides, so each can change or be reused with less impact on the other.

## Where the intermediary goes

The problem it answers: where do you assign responsibility to avoid direct coupling between two or more things, while keeping reuse potential high? The solution: assign mediation to an intermediate object, which becomes the only element that knows both sides. The classic system-level example is MVC - a controller mediates between the model and its view, so the representation never depends on the data and the data never depends on how it is drawn.

The same move works at integration level. An order service that calls a legacy billing system directly is welded to that system's API; an adapter in between keeps the service bound only to a stable interface:

```java
interface BillingService {
    void invoice(Invoice invoice);
}

class LegacyBillingAdapter implements BillingService {
    private final LegacyBillingSystem legacy;

    LegacyBillingAdapter(LegacyBillingSystem legacy) {
        this.legacy = legacy;
    }

    public void invoice(Invoice invoice) {
        legacy.submitInvoice(invoice.number(), invoice.totalCents()); // old API stays behind the wall
    }
}

class OrderService {
    private final BillingService billing;

    OrderService(BillingService billing) {
        this.billing = billing;
    }

    void completeOrder(Invoice invoice) {
        billing.invoice(invoice); // knows BillingService, not the legacy system
    }
}
```

**Listing 1.** The adapter is the indirection: OrderService depends on the stable interface, and every quirk of the legacy API is contained in one replaceable class.

```d2
direction: right
direct: "Direct coupling\nOrderService -> LegacyBillingSystem" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
split: "Insert indirection" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
a: "OrderService\n-> BillingService" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
m: "LegacyBillingAdapter\nmediates" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
b: "LegacyBillingSystem\ncan change freely" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
direct -> split -> a -> m -> b
```

**Fig. 1.** One inserted element turns a welded pair into two halves that evolve independently, at the price of one more class to read.

## Indirection in familiar shapes

Most structural vocabulary in OO design is Indirection instantiated: adapters translate between incompatible interfaces, proxies stand in for their subjects, facades front subsystems, dependency injection containers sit between consumers and their services, and event buses mediate producers and consumers. The adapter case is drawn out in [[How would you explain the Adapter design pattern]], the proxy flavor in [[What is the difference between the Proxy and Decorator design patterns]], and the container-driven flavor in [[How would you explain dependency injection]]. All of them serve the same evaluative goal as [[What is the Low Coupling principle in GRASP]].

> [!warning] Indirection is not free and not automatically good
> Every mediator is one more hop to read, debug, configure, and name. A pass-through layer that forwards every call and still leaks the other side's types adds ceremony without removing coupling - the definition of useless indirection. The principle pays only when the mediation actually decouples: the intermediary must shield at least one side from the other's types and change rate, otherwise the hop is pure cost.

> [!tip] Interview answer
> Indirection says: when two elements should not couple directly, insert an intermediate object that mediates between them. MVC's controller between model and view, an adapter in front of a legacy system, a DI container between consumers and services - all one principle. It serves Low Coupling, but each layer costs readability, so the mediation must genuinely shield one side from the other; pass-through wrappers are ceremony, not design.
