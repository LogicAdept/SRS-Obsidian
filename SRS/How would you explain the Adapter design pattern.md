<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# How would you explain the Adapter design pattern

> [!abstract] Short answer
> Adapter is a structural pattern that lets objects with **incompatible interfaces collaborate**: the adapter implements the interface the client expects, wraps the service, and translates each call into the shape the service understands. It is also known as Wrapper.

## The mechanism

You reach for an Adapter when a useful class — usually third-party or legacy — cannot be changed and its interface does not fit the client code. The object adapter implements the client interface and holds the service in a field: the client calls the adapter through the familiar interface, and the adapter converts the arguments and forwards the call in the format and order the service expects; the wrapped object is not even aware of the adapter. There is also a class adapter, which inherits from both sides at once and adapts inside overridden methods — this needs multiple inheritance, so in Java the object adapter is the realistic form. A two-way adapter that translates in both directions is possible when both interfaces are known.

```java
interface JsonAnalytics { void feed(String json); }

class XmlService {                       // legacy, cannot change
    void consume(String xml) { /* ... */ }
}

class XmlToJsonAdapter implements JsonAnalytics {
    private final XmlService service;
    XmlToJsonAdapter(XmlService service) { this.service = service; }
    public void feed(String json) {
        service.consume(toXml(json));    // conversion lives here
    }
    private String toXml(String json) { return "<root/>"; }
}
```

**Listing 1.** Object adapter: the client depends on `JsonAnalytics`, the adapter converts and delegates, and the legacy `XmlService` stays untouched.

## Where it pays

Typical uses are gluing a third-party library into your code and wrapping legacy classes during a migration. Because clients work through the client interface, you can introduce new adapters or swap the wrapped service without touching client code — the Open/Closed benefit the catalog lists. The cost is extra classes: sometimes changing the service is simply cheaper than adapting it.

> [!warning] Adapter versus Decorator versus Facade
> Adapter gives an existing object a **different** interface; Decorator keeps the same interface and layers behavior; Facade simplifies access to an entire subsystem, while Adapter usually wraps a single object. The Decorator/Proxy contrast continues in [[What is the difference between the Proxy and Decorator design patterns]], and the structural set is surveyed in [[What are examples of structural design patterns]].

> [!tip] Interview answer
> Adapter makes incompatible interfaces work together: it implements the interface the client knows, wraps the service that cannot be changed, and translates each call. The object adapter uses composition and works in any language; the class adapter uses inheritance and needs multiple inheritance. Use it for third-party or legacy integration, and remember it changes the interface — unlike Decorator, which keeps it.
