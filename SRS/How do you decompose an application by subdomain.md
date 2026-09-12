<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceBoundaries #SRS

# How do you decompose an application by subdomain

> [!abstract] Short answer
> Decompose by subdomain: apply Domain-Driven Design, split the business problem into subdomains - core (the differentiating part), supporting and generic - and define one service per subdomain. Richardson lists it as the sibling of [[How do you decompose an application by business capability]]; both aim at cohesive, loosely coupled services, but subdomains come from modeling the problem space, capabilities from business-architecture analysis.

## Mechanism: subdomain analysis to service cut

DDD classifies subdomains by business value. The core subdomain is where the business differentiates - for an e-commerce platform that is typically recommendation and pricing; implement it yourself, keep the best people, evolve it fast. Supporting subdomains matter but do not differentiate - order fulfillment workflows; build them lean. Generic subdomains are solved problems everyone needs - authentication, email sending, billing - buy them off the shelf where possible. The service cut then follows the model: each service owns one subdomain's ubiquitous language, its domain model and its data. A term like "Order" can mean slightly different things in different services, and that is by design - each subdomain's model stays internally consistent.

The subtle point interviewers probe: subdomain versus bounded context. A subdomain is a part of the problem; a bounded context is a part of the solution where a model holds. In a clean greenfield design they align one-to-one - one context per subdomain - and that alignment is exactly what makes the service decomposition healthy. For the concept-level contrast see [[What is the difference between a bounded context and a subdomain]]; for how to detect contexts in an existing codebase see [[What is a bounded context and how do you identify one]].

```d2
direction: right
business: "Business problem" {style.fill: "#eceff1"}
core: "Core subdomain
pricing + recommendations
build in-house" {style.fill: "#ffcdd2"}
sup: "Supporting subdomain
order fulfillment
build lean" {style.fill: "#fff3e0"}
gen: "Generic subdomains
auth, email, billing
buy / adopt" {style.fill: "#e8f5e9"}
svc1: "Pricing service" {style.fill: "#ffcdd2"}
svc2: "Fulfillment service" {style.fill: "#fff3e0"}
business -> core
business -> sup
business -> gen
core -> svc1: one service
sup -> svc2: one service
```

**Fig. 1.** Subdomain classification drives both the service cut and the build-vs-buy decision per service.

## Why the classification pays off

The classification is an effort-allocation map, not just naming. Services for core subdomains get architectural investment: their own data model, room for rich invariants, fast release cadence. Services for generic subdomains should be as thin as possible around an off-the-shelf product, because maintaining a homegrown identity provider is a tax with no differentiation payoff. This directly answers the interview follow-up "how do you decide what deserves to be a service and what does not": anything core or supporting that needs model integrity of its own becomes a service; generic concerns become products or shared platforms, which is also how Richardson's chassis idea relates ([[What is the microservice chassis pattern]] covers the shared runtime plumbing).

In legacy systems subdomains are implicit, tangled inside one model. The decomposition exercise starts by teasing the languages apart - what the sales team calls a customer is not what billing calls a customer - and the boundaries between languages are the future service seams. That is also the bridge to refactoring work: seams found this way are where [[What is the strangler fig pattern and when do you use it]] gradually extracts services.

> [!warning] Subdomains are not modules
> A subdomain is not "a package of code" - it is a region of the problem with its own language and consistency rules. Two common traps: cutting services along technical layers instead of subdomains (a "data service" belongs to no subdomain and changes for every reason), and forcing one model to serve two subdomains (the shared Order entity becomes a god object nobody can change safely). If two teams keep colliding in one service, you almost always find two subdomains hiding inside it.

> [!tip] Interview answer
> I run DDD strategic design: classify subdomains into core, supporting and generic, then draw one service per subdomain so each service owns its model, its language and its data. Core gets the investment, generic gets bought. Subdomain is the problem-side view, bounded context the solution side - in a healthy design one context per subdomain, and that alignment is the service boundary.
