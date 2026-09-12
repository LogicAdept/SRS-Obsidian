<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceCollaboration #Patterns/DistributedSystems #SRS

# What is the command-side replica pattern

> [!abstract] Short answer
> The command-side replica pattern — from the Service collaboration group of the microservices.io catalogue — tells a service that handles commands to keep a local, queryable replica of the data owned by another service, maintained by subscribing to that owner's domain events. Writes still go to the owner; the replica only serves reads and validations performed while handling a command. It removes synchronous calls from the command path at the price of eventual consistency and duplicated storage.

## Problem: the command path needs someone else's data

Handling a command rarely touches only one service's tables. An Order Service must validate that a menu item exists and is available — but the menu belongs to the Kitchen Service. An order total may be capped by a credit limit that the Customer Service owns. The naive options are both bad. A synchronous [[What is the remote procedure invocation pattern between microservices]] call turns the command handler into a distributed transaction coordinator: the order service is now temporarily coupled to the availability and latency of its dependencies, exactly what decomposition tried to avoid. A [[What is the shared database pattern in microservices]] restores the coupling at the schema level. [[Why is two-phase commit a poor fit for microservices]] explains why spanning the write across services is not an option either.

## Solution: replicate for reads, delegate the writes

The command service subscribes to the owner's change stream — domain events published via [[What is the domain event pattern in microservices]], typically produced with [[How would you explain the transactional outbox pattern]] or [[How would you explain the event sourcing pattern]] — and materializes a private replica of just the fields it needs: open menu items, credit limits, active promotions. Command handling reads the local replica; any real mutation is sent to the owning service, which remains the single source of truth. Richardson frames this inside the same family as [[What is CQRS]]: a command-side replica is CQRS applied locally, keeping the queryable view inside the service that commands, while [[What is the API composition pattern in microservices]] instead joins other services' data at query time.

```d2
direction: right
owner: "Menu Service (owner)" {
  db: "menu table" {shape: cylinder}
}
cmd: "Order Service (command side)" {
  replica: "menu replica" {shape: cylinder; style.fill: "#fff3e0"}
  handler: "CreateOrder handler"
}
owner.db -> events: "MenuChanged events" {style.stroke: "#1565c0"}
events: "event broker" {shape: queue}
events -> cmd.replica: "project"
handler -> cmd.replica: "validate locally"
handler -> owner: "CreateOrder command"
```

**Fig. 1.** The replica is projected from the owner's events and used only on the read/validate path; mutations still flow to the owner.

## Forces and costs

The pattern trades freshness for autonomy. The replica is eventually consistent: a menu item removed seconds ago may still validate an order until the next event lands. Storage is duplicated, and every consumed field widens the implicit contract between the services — a schema change in the owner's events breaks the projection. The replica must stay private to the consuming service; if other services start reading it, a shadow "shared database" appears with no owner.

> [!warning]
> Decisions made on stale replica data are the classic production incident: a retired menu item keeps accepting orders until the deletion event is processed. Guard the command handler with owner-side revalidation for irreversible actions, and treat the replica as a cache with an explicit projection, never as a second writeable copy.

> [!tip] Interview answer
> Command-side replica: the service that handles commands keeps a local read model of another service's data, kept fresh by its domain events, while the writes stay with the owner. It cuts synchronous calls from the command path — the same family as CQRS and the opposite trade-off to API composition — and its price is eventual consistency, so irreversible commands still need owner-side validation.
