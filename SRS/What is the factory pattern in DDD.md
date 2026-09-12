<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the factory pattern in DDD?

> [!abstract] Short answer
> A DDD factory is anything whose job is to hand out a fully valid aggregate: creation factories build a new aggregate from scratch with every invariant already satisfied, and reconstitution factories rebuild an aggregate from stored state without re-running business decisions. The rule they enforce: at no point in its life does an aggregate exist in an invalid state - not even for the duration of its construction.

## Creation and reconstitution

Complex aggregates have intricate birth: an order needs an id, a currency, an initial status, consistent child structures, and a history entry. Spreading that over caller code means every caller can forget a step and produce a valid-looking invalid aggregate. A factory centralizes the birth. Two flavors exist and must not be confused. Creation makes new decisions - generates identity, sets initial state, records "created" - and is a genuine domain operation. Reconstitution makes no decisions: it replays stored state into the object graph exactly as saved, skipping invariants-checking logic that concerns business operations, because the stored state is presumed to have been valid when committed. Reconstitution is what a repository calls on load ([[What is the repository pattern in DDD]]).

Factories appear as static factory methods on the root (the lightest form), dedicated factory objects for aggregates whose construction needs other domain objects, and rebuild methods for the reconstitution flavor. The GoF factory patterns share the shape; the DDD motivation differs - not hiding a concrete class, but guaranteeing invariants at birth ([[What is the Factory Method pattern]]).

```java
static Order place(long id, String currency) {          // creation: makes decisions
    Order o = new Order(id, currency);
    o.history.add("created");
    return o;
}
static Order reconstitute(long id, String currency, List<String> history) {  // replay
    Order o = new Order(id, currency);
    o.history.addAll(history);
    return o;
}
// save + load roundtrip through a repository:
Order placed = Order.place(100, "EUR");
repo.add(placed);
Order loaded = repo.findById(100).orElseThrow();
System.out.println(loaded == placed);          // false
System.out.println(loaded.history());          // [created]
```

**Listing 1.** Verified on JDK 21.0.12.1: `place` and `reconstitute` are distinct paths - the loaded aggregate is a new object with the same recorded history, and the constructor stays private so no other birth route exists.

```d2
direction: right
caller: "Caller\napp service or repository" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
create: "Creation factory\nnew id, initial state,\ninvariants checked" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
recon: "Reconstitution factory\nstored state replayed\nno decisions" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
valid: "Valid aggregate\ninvariant holds from t0" {
  width: 240
  height: 80
  style.fill: "#f3e5f5"
}
caller -> create: "new use case"
caller -> recon: "load"
create -> valid
recon -> valid
```

**Fig. 1.** Both routes converge on the same guarantee: an aggregate that exists at all is an aggregate that is valid.

## Where the boundary sits

The factory owns assembly; the caller owns intent. An application service says "place an order for this customer" - the factory decides how a valid order begins life. Creation logic that depends on other aggregates (a draft order needs the customer's credit terms) belongs in a factory object rather than a static method, because it needs lookups - but the lookups stay behind the factory's interface, and the aggregate's constructor never becomes public "for flexibility". Private constructors plus static factories is the mechanical enforcement; the conceptual enforcement is that no code path can short-circuit validity.

> [!warning] Public setters are not a factory
> The anti-pattern: a public constructor producing an empty shell and a dozen setters the caller "fills in later". Between construction and the last setter, the aggregate is invalid - and any observer may see it that way. The same holds for reconstitution that silently reruns business rules: replaying "created" through the creation path would duplicate history entries and re-derive derived state. Creation and reconstitution are different doors, and both must stay open for exactly their own traffic ([[What are aggregate aggregate root entity and value object in DDD]]).

> [!tip] Interview answer
> A DDD factory guarantees aggregates are born valid: creation factories build new aggregates with all invariants satisfied, reconstitution factories rebuild them from stored state without re-running decisions. Private constructors plus factory methods enforce it mechanically. The repository uses the reconstitution door on load; the application service uses the creation door in use cases.

