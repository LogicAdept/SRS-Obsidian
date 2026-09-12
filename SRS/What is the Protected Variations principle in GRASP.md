<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Protected Variations principle in GRASP

> [!abstract] Short answer
> Protected Variations is a GRASP principle: identify points of predicted variation or instability and assign responsibilities to create a stable interface around them. The rest of the design then depends on that interface, and the variation churns safely behind it through polymorphic implementations.

## How protection is built

The problem it answers: how do you design objects, subsystems, and systems so that variations or instability in some elements do not have an undesirable impact on other elements? The procedure has three moves. First, name the point of predicted variation - an external provider, a storage engine, a regulation, a hardware detail. Second, design a stable interface around that point of instability. Third, implement the variants polymorphically behind the interface, so clients bind only to the stable side.

```java
interface PaymentGateway {
    PaymentReceipt charge(PaymentRequest request);
}

class StripeGateway implements PaymentGateway {
    public PaymentReceipt charge(PaymentRequest request) {
        // vendor SDK calls, retries, idempotency keys - all vendor-specific
        return PaymentReceipt.approved(request.orderId());
    }
}

class SandboxGateway implements PaymentGateway {
    public PaymentReceipt charge(PaymentRequest request) {
        return PaymentReceipt.approved(request.orderId()); // deterministic test double
    }
}

class CheckoutService {
    private final PaymentGateway gateway;

    CheckoutService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    PaymentReceipt checkout(Cart cart) {
        return gateway.charge(PaymentRequest.of(cart)); // stable side of the wall
    }
}
```

**Listing 1.** Provider-specific logic stays inside the implementations; swapping providers, adding one, or faking one for tests touches only the wiring, not the checkout flow.

```d2
direction: right
core: "Stable core\nCheckoutService" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
wall: "Stable interface\nPaymentGateway" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
s1: "StripeGateway\nvolatile" {
  width: 190
  height: 70
  style.fill: "#ffebee"
}
s2: "SandboxGateway\nvolatile" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}
core -> wall: depends on
wall -> s1: implements
wall -> s2: implements
```

**Fig. 1.** The interface is a wall: variation on one side, clients that never feel it on the other.

## The principle behind the patterns

Protected Variations is the most general of the nine GRASP principles: many GoF structures - Strategy, Adapter, Observer, Facade - can be read as concrete applications of this one idea, each protecting a different kind of variation point. It is also the responsibility-level statement of the open-closed idea: clients stay closed to modification because new behavior arrives as new implementations behind the stable interface, which is the connection drawn in [[How would you explain the open closed principle in SOLID]]. The Strategy shape is the most common realization, compared in [[What is the Strategy pattern used for]], and the general machinery it leans on is [[What is polymorphism]].

> [!warning] Protect only predicted variation
> Wrapping everything "just in case" produces speculative layers, configuration bloat, and pass-through interfaces nobody needs - the same trap catalogued in [[What are downsides of design patterns]]. The principle triggers on points of predicted variation, where change is realistic and its impact would spread. And the protection is only as good as the interface: if vendor types leak through the wall, the coupling you claimed to remove is still there, just wearing a disguise.

> [!tip] Interview answer
> Protected Variations says: find where change is predicted to happen, and wrap that point behind a stable interface with polymorphic implementations, so instability stays contained. A payment gateway interface in front of vendor SDKs is the textbook case. It is the most general GRASP principle - many GoF patterns are just concrete applications of it - and it maps onto the open-closed principle, but it must be triggered by realistic predicted variation, not by speculation.
