<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral/Observer #SRS

# What is Observer

> [!abstract] Short answer
> Observer is a behavioral pattern — also known as Event-Subscriber or Listener — that defines a **subscription mechanism**: a publisher keeps a list of subscribers and notifies each of them when an event happens, so the objects it affects can react without the publisher knowing their concrete classes.

## The mechanism

The object with interesting state — the publisher, or subject in the older GoF naming — maintains two things: a container of subscribers and public methods to add and remove them. All subscribers implement one interface declaring a notification method, typically a single `update`, and the publisher only ever talks to that interface. When the event occurs, the publisher walks the list and calls `update` on each subscriber, optionally passing event context as arguments — or passing itself, so the subscriber pulls whatever data it needs. The list is live: subscribers join and leave at runtime, which is the whole point compared to a hardcoded call list. The Java toolkit has shipped this for decades as `PropertyChangeListener` support on beans, and message brokers generalize it across processes; inside Spring, [[How does ApplicationContext publish events]] is the framework-shaped version of the same idea.

```java
interface Listener { void update(String event); }

class Store {
    private final List<Listener> listeners = new ArrayList<>();
    void subscribe(Listener l) { listeners.add(l); }
    void unsubscribe(Listener l) { listeners.remove(l); }
    void newArrival(String product) {
        for (Listener l : listeners) l.update(product);
    }
}
```

**Listing 1.** The full pattern in miniature: a subscription list, add and remove, and a notification loop over the shared interface.

## The costs the catalog names

The official con list is short but real: subscribers are notified in **random order** — the contract gives no sequencing guarantee, so code relying on listener A running before listener B is broken by design. And the pattern's flexibility turns into a leak risk: a subscriber that forgets to unsubscribe stays reachable through the publisher's list and can never be collected, the classic lapsed-listener problem in GUI applications.

> [!warning] The interview trap is the order guarantee
> Presenting the notification loop as "listeners run in registration order" is the common lie; an `ArrayList` happens to preserve insertion order, but the pattern itself promises nothing. The modern evolution of the same idea — push streams with completion and error signals — is covered in [[What roles do Observable and Observer play in reactive programming]].

> [!tip] Interview answer
> Observer defines a one-to-many subscription: the publisher keeps a list of subscribers behind a common interface, supports subscribe and unsubscribe at runtime, and notifies them on events, passing context or itself. It decouples publishers from subscriber classes, but notification order is unspecified and forgotten unsubscribes leak listeners.
