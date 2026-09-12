<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Controller principle in GRASP

> [!abstract] Short answer
> Controller is a GRASP principle that assigns input system events to a non-UI object: either a use case controller that handles the events of one use case, or a facade controller that represents the whole system. The controller receives the event and delegates the work - it coordinates, it does not compute.

## Where the controller sits in the design

The controller is the first object beyond the UI layer that receives and coordinates a system operation. It comes in two forms. A use case controller owns all system events of one use case, and may serve a small cluster of related use cases - a single UserController covering Create User and Delete User instead of two separate classes. A facade controller represents the overall system or a root object and routes every incoming event; it fits small systems or when use cases are too thin to warrant their own controllers.

When the architecture separates an application or service layer from the domain layer, the controller belongs to that application layer. It forwards requests to domain objects - register, sale, order - and returns their results, keeping no pricing, storage, or business rules of its own.

```java
class CheckoutController {                    // application layer, use case controller
    private final Register register;

    CheckoutController(Register register) {
        this.register = register;
    }

    Sale placeOrder(Cart cart) {
        Sale sale = register.createSale();    // coordinates the use case...
        for (CartLine line : cart.lines()) {
            sale.addLine(line.product(), line.quantity());
        }
        return sale;                          // ...and delegates; no pricing logic here
    }
}
```

**Listing 1.** The controller receives the placeOrder system event, walks it through the domain objects, and stays free of domain rules itself.

```d2
direction: right
ui: "UI layer\nform, button, HTTP handler" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
ctrl: "Controller\nuse case or facade" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
domain: "Domain objects\nRegister, Sale, Order" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
ui -> ctrl: system event
ctrl -> domain: delegates work
domain -> ctrl: results
ctrl -> ui: response
```

**Fig. 1.** Every system event flows through the controller, but the controller only routes and coordinates; the domain objects do the actual work.

## The two classic violations

The first violation is the fat controller: an object that receives a system event and then runs domain logic itself - computing totals, executing SQL, deciding prices. It violates the very principle it is named after, grows with every use case, and cannot be reused outside its one entry point. Such grab-bag classes are a recognized [[What is an antipattern]].

The second is confusing GRASP Controller with a web framework controller. Spring's @RestController classes are web-layer adapters that translate HTTP into application calls; the framework's front dispatcher is actually the object playing the GRASP facade controller role for the whole system. The mapping is visible in [[What is the Front Controller pattern in Spring MVC]] and in the broader picture of [[What design patterns does the Spring Framework use]].

> [!warning] Two common interview traps
> First, "controller" in GRASP must delegate; a class that receives the event and executes domain logic itself is a fat controller, no matter what its name says. Second, do not equate GRASP Controller with Spring controller annotations - one is a responsibility-assignment principle for system events, the other is a concrete web-layer mechanism; compare them via [[What is the difference between Repository Component Controller and Service annotations]].

> [!tip] Interview answer
> Controller assigns each input system event to a non-UI object: a use case controller per use case, or a facade controller for the whole system. The controller is the first object past the UI, it coordinates by delegating to domain objects, and it lives in the application layer. If it starts doing domain work itself, it has become a fat controller and broken its own principle.
