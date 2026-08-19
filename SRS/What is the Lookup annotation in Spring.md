<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Lookup` is method injection for a **prototype** dependency into a **singleton**. Constructor or setter injection would capture one prototype instance when the singleton is created.

You declare a stub method on the singleton that returns the prototype type and annotate it with `@Lookup`. The body can return `null`; the container subclasses the bean and overrides the method so each call creates a new prototype instance.

```java
@Component
public class Car {
    @Lookup
    public Passenger createPassenger() {
        return null;
    }
    public String drive(String name) {
        Passenger passenger = createPassenger();
        passenger.setName(name);
        return "car with " + passenger.getName();
    }
}
```

Related fixes for the same gotcha: `ObjectProvider.getObject()` each call, or a scoped proxy.

> [!warning] Unverified traps from the dump
> - The stub method must be overridable (not `private` / `final`); CGLIB subclassing replaces it.
> - Lookup happens on each method call, not at container startup.
