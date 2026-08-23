<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# How do Spring Data repository domain events work?

> [!abstract] Short answer
> Spring Data publishes **domain events** from aggregate roots on repository `save`/`delete` calls that receive the entity instance. The root exposes events with `@DomainEvents` and clears them with `@AfterDomainEventPublication`. Spring Data REST adds a separate HTTP lifecycle API with `@HandleBeforeSave` and similar handlers.

## Aggregate domain events (Spring Data Commons)

Repository-managed entities are treated as aggregate roots. When business logic mutates state, the root records events (often via `AbstractAggregateRoot.registerEvent`). On a repository call that passes the aggregate instance, Spring Data invokes the `@DomainEvents` method, publishes each returned event through the Spring `ApplicationEventPublisher`, then calls `@AfterDomainEventPublication` so you can clear the pending list.

```java
@Entity
class Order extends AbstractAggregateRoot<Order> {

  void ship() {
    this.status = Status.SHIPPED;
    registerEvent(new OrderShipped(this.id));
  }

  // Optional if you extend AbstractAggregateRoot — it already exposes domainEvents()
}
```

**Listing 1.** Collect events inside the aggregate; publication is tied to repository persistence, not to arbitrary setters.

Triggered repository methods (Spring Data Commons docs): `save`, `saveAll`, `delete`, `deleteAll`, `deleteAllInBatch`, `deleteInBatch`. **`deleteById` is excluded** — the implementation may issue a query without loading the aggregate, so there is no instance to read events from.

```java
@DomainEvents
Collection<Object> domainEvents() {
  return events;
}

@AfterDomainEventPublication
void clearDomainEvents() {
  events.clear();
}
```

**Listing 2.** Manual event exposure when you do not extend `AbstractAggregateRoot`; return one event or a collection, no parameters.

```d2
direction: right
repo: "repository.save(order)\nor delete(order)" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
expose: "@DomainEvents\nreturn pending events" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
pub: "ApplicationEventPublisher\npublish each event" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
clear: "@AfterDomainEventPublication\nclear list" {
  width: 260
  height: 80
  style.fill: "#f3e5f5"
}

repo -> expose -> pub -> clear
```

**Fig. 1.** Domain events flow through the repository proxy around save/delete of the aggregate instance.

## Spring Data REST lifecycle handlers (different API)

When entities are exposed over HTTP, Spring Data REST fires **repository events** around REST-driven persistence. Register a `@RepositoryEventHandler` bean with methods such as `@HandleBeforeCreate`, `@HandleAfterSave`, or `@HandleBeforeDelete`, or extend `AbstractRepositoryEventListener` and override `onBeforeSave` / `onAfterDelete`. These hooks run in the REST export pipeline — validation, side effects, messaging — and are **not** the same as `@DomainEvents` on the entity.

> [!warning] Two event systems, two triggers
> `@DomainEvents` fires around **repository** save/delete of an aggregate instance and publishes Spring application events. REST `@HandleBeforeSave` runs when Spring Data REST processes an HTTP create/update/delete. Setting a field on a detached entity publishes nothing until `save` runs. `deleteById` may skip domain-event publication entirely.

See [[What is Spring Data Commons]], [[What is Spring Data REST]], and [[How can you customize Spring Data REST endpoints]].

> [!tip] Interview answer
> Domain events live on the aggregate: collect them during business methods, expose them with `@DomainEvents`, and clear after publication. Spring Data publishes them when you call repository save or delete methods that take the entity. Spring Data REST’s `@HandleBeforeSave` handlers are a separate HTTP lifecycle layer — useful, but not the same mechanism.
