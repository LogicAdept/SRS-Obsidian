<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #SRS

# What is the Factory Method pattern

> [!abstract] Short answer
> Factory Method is a creational pattern that puts a creation step behind a method in a superclass and lets subclasses decide which concrete class to instantiate. The client code asks the factory method for a product and works with its common interface, never with `new` on a concrete class.

## How the pattern works

The pattern replaces direct construction calls with calls to a special factory method. The objects are still created with `new`, but the call lives inside a method whose return type is declared as the common product interface. Subclasses override the factory method and return different concrete products, so the base class's business logic keeps working while the produced type changes. The constraint: subclasses may return different products only if those products share the interface that the factory method declares.

The textbook example is a logistics application that grew from road transport to shipping: the base class wants "something that can deliver", and each subclass supplies its own transport.

```java
interface Transport {
    void deliver();
}

abstract class Logistics {
    abstract Transport createTransport();   // the factory method

    void planDelivery() {                   // base logic is written against the interface
        Transport transport = createTransport();
        transport.deliver();
    }
}

class RoadLogistics extends Logistics {
    @Override
    Transport createTransport() {
        return new Truck();                 // Truck implements Transport
    }
}

class SeaLogistics extends Logistics {
    @Override
    Transport createTransport() {
        return new Ship();                  // Ship implements Transport
    }
}
```

**Listing 1.** Subclasses alter the product type by overriding the factory method; `planDelivery` never names a concrete transport class.

```d2
direction: right
base: "Logistics\ncreateTransport() : Transport\nplanDelivery()" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
road: "RoadLogistics\nreturns Truck" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
sea: "SeaLogistics\nreturns Ship" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
prod: "Transport\ndeliver()" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
road -> base: extends
sea -> base: extends
base -> prod: returns
```

**Fig. 1.** The base class binds only to the Transport interface; each subclass decides which concrete product flows through it.

## Where it sits among the creational patterns

Factory Method is the entry point of the creational family: designs often start with it and evolve toward Abstract Factory, Prototype, or Builder when they need more flexibility. It is a specialization of the Template Method pattern - the creation algorithm is the skeleton, the factory method is the overridable step - and it can itself serve as one step inside a larger template method. Collection classes use exactly this shape when subclasses return collection-compatible iterators. The broader catalogue context is in [[What are examples of creational design patterns]], the family comparison angle in [[What is the Abstract Factory pattern]], and the GRASP assignment logic behind "who creates" in [[What is the Creator principle in GRASP]].

> [!warning] Static creation helpers are not this pattern
> In Java, "factory method" commonly means any static creation helper - the methods in [[What are the collection factory methods List.of Set.of and Map.of]] are the famous example. Those are idiomatic static factories, but they are not the GoF Factory Method: the pattern is inheritance-based, meaning a subclass overrides an instance method to change the produced type. Answering the interview with "List.of is Factory Method" mixes two ideas that only share a name.

> [!tip] Interview answer
> Factory Method defines a creation method in a superclass and lets subclasses override it to decide which concrete product to return; the client and the base business logic work only with the product interface. It is inheritance-based creation - a specialization of Template Method - and designs typically start with it, later evolving to Abstract Factory or Builder when whole families or step-by-step construction enter the picture.
