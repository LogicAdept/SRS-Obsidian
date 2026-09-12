<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceBoundaries #SRS

# How do you decompose an application by business capability

> [!abstract] Short answer
> Decompose by business capability: define one service per capability - something the business does to generate value, like Order Management, Inventory Management or Delivery Management. Capabilities come from business architecture analysis (org structure, processes, high-level domain model), they are stable while technologies churn, and they naturally group strongly related functions behind one API. Richardson presents it as one of the two primary decomposition patterns for microservices, alongside [[How do you decompose an application by subdomain]].

## Why capabilities are the cutting line

A business capability answers "what does this part of the business do", not "what code implements it". Order Management is responsible for orders; Customer Management for customers; Inventory Management for stock. Two object-oriented principles carry over almost verbatim to services. The Single Responsibility Principle: a class should have one reason to change - a service should implement a small set of strongly related functions so most changes touch one service. The Common Closure Principle: classes that change together should live together - a business rule change should require editing one service, not four. When requirements spread across services, every change becomes a cross-team coordination exercise, and that is exactly the slowdown microservices were supposed to remove.

Capabilities are relatively stable even when the business reorganizes around them: an online store keeps doing product catalog management, inventory, order management and delivery regardless of which framework version renders the web UI. That stability is the architectural payoff - the service boundaries survive technology migrations, and teams organize around durable business ownership instead of transient technical layers. Richardson's guideline for size: a service must be small enough for a two-pizza team (6-10 people) to own, test and deploy autonomously.

```d2
direction: right
store: "Online store" {style.fill: "#eceff1"}
catalog: "Product catalog
management" {style.fill: "#e8f5e9"}
inventory: "Inventory
management" {style.fill: "#e8f5e9"}
orders: "Order
management" {style.fill: "#e8f5e9"}
delivery: "Delivery
management" {style.fill: "#e8f5e9"}
store -> catalog: capability
store -> inventory: capability
store -> orders: capability
store -> delivery: capability
catalog -> inventory: stock levels (API)
orders -> inventory: reserve (API)
```

**Fig. 1.** Each box is a business capability turned into a service; arrows are explicit APIs, not shared databases.

## How to find the capabilities

Start from three sources: the organization structure (groups often map to capability groups, with the Conway's-law caveat that org reality may need re-shaping rather than blind copying), the high-level domain model (capabilities frequently correspond to domain objects like Order, Customer, Shipment), and the business processes (each major step chain hints at a capability). The identification is iterative: sketch a capability hierarchy, cut services, then check the two failure modes - services that change together but are split (merge candidates) and one capability smeared across services (boundary in the wrong place). For the DDD vocabulary version of the same exercise see [[What is a bounded context and how do you identify one]]; the capability view and the subdomain view usually converge on similar cuts from opposite directions - business function versus model consistency.

> [!warning] Capabilities are not layers
> The classic mistake is cutting along technical lines - "web service", "business-logic service", "data-access service" - and calling them capabilities. A change to ordering then edits three services owned by three teams. Capabilities are vertical slices: each service owns its function end to end, including its UI-facing API and its data. A second trap: copying the org chart one-to-one gives you services sized like departments, not like two-pizza teams - decompose by what the business does, then align teams to services, not the reverse.

> [!tip] Interview answer
> I decompose by business capability: one service per thing the business does - order management, inventory, delivery. It follows SRP and Common Closure Principle at the architecture level - related functions live together, most changes touch one service and one team. Capabilities are stable while tech stacks change, so boundaries survive refactors. The alternative view is DDD subdomains, and in a good design both converge on the same cut.
