<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices #Patterns/Architecture/Monolith #SRS

# What is the strangler fig pattern and when do you use it

> [!abstract] Short answer
> The strangler fig pattern — Fowler's name, after the vine that gradually grows around and replaces its host tree — migrates a system by building the new application around the legacy one and shifting functionality incrementally, route by route or feature by feature, until the old system is gone. Richardson's microservices.io applies it as the standard answer to "how do you migrate a monolith to microservices" without a big-bang rewrite.

## The mechanism: a facade decides where each request goes

Three components make the migration safe. A interception facade (load balancer, gateway or proxy) sits in front of the legacy system and routes each request either to the legacy application or to the new services ([[What is the API gateway pattern in microservices]] is a natural host for this routing table). New functionality grows as separate services behind the facade — including genuinely new features, which demonstrate value early without touching the monolith. Migration is incremental and reversible: move one route, watch it in production, move the next; a rollback is a routing change, not a deployment. The result context Richardson describes: eventually the monolith serves nothing and can be retired ("decommissioned"), or the migration stops deliberately when remaining strangling costs more than it returns.

```d2
direction: down
user: "Clients" {style.fill: "#eceff1"}
facade: "Facade / gateway
route table" {style.fill: "#fff3e0"}
orders: "Orders service (new)" {style.fill: "#e8f5e9"}
users: "Users service (new)" {style.fill: "#e8f5e9"}
legacy: "Legacy monolith
/report, /admin..." {style.fill: "#eceff1"}
user -> facade
facade -> orders: /orders/* migrated
facade -> users: /users/* migrated
facade -> legacy: everything else
```

**Fig. 1.** Progressive cutover: migrated routes hit new services; everything else still reaches the monolith. Rollback is a routing edit.

```java
String route(String path) {
    if (migratedToOrders.contains(path)) return next.orders(path);
    if (migratedToUsers.contains(path)) return next.users(path);
    return legacy.handle(path);                 // everything else still hits the monolith
}
```

**Listing 1.** Verified on JDK 21 (G05_StranglerRouting in empirics): with no routes migrated all paths answer `legacy:...`; after migrating `/orders/7` and `/users/3` they answer `orders-svc:...` and `users-svc:...` while `/reports/2026` stays legacy (out/G05_StranglerRouting.txt).

## The hard parts the pattern doesn't remove

Shared data: the monolith's database is the real knot — extracted services either read the monolith's schema (keeping coupling, see [[What is the shared database pattern in microservices]]) or the migration must carve data ownership out route by route, with sync in the transition ([[How would you explain the transactional outbox pattern]] and CDC are the standard bridges). Session and identity: auth state must work across both worlds during migration. Semantic drift: two implementations of one feature must not diverge while both serve traffic — freeze the legacy feature when its route migrates. And the discipline risk: migrations stalled at 80% become permanent architecture; the pattern needs an owner who either finishes the strangling or declares the monolith's residual core a legitimate service boundary ([[How do you decompose a monolith into microservices]] defines the target).

> [!warning] The facade is now critical infrastructure
> Every request passes through the routing layer, so it must be as available as the system it fronts, observable per route, and versioned like a product — an undocumented route table is a hidden monolith of its own. And "temporary" dual-running has a real cost curve: two systems to monitor, secure and keep in sync for the whole migration window.

> [!tip] Interview answer
> Strangler fig means incremental replacement: put a routing facade in front of the monolith, build new features and extracted capabilities as services behind it, migrate routes one by one with reversibility at every step, and retire the monolith when nothing routes to it. The hard parts are shared data, sessions during dual-running and preventing feature drift — rollback is cheap (a routing change) which is exactly why this beats a big-bang rewrite.
