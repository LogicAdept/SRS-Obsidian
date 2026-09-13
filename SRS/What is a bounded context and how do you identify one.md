<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is a bounded context and how do you identify one?

> [!abstract] Short answer
> A bounded context is the explicit edge inside which one domain model and its vocabulary are consistent. Inside the boundary, every term has one meaning and every invariant is enforced by one model; across the boundary, the same word can mean something different. You identify bounded contexts during domain analysis: cluster the domain into subdomains by business capability and language, look for places where terms shift meaning, and check team and integration seams. Each bounded context maps to the model of a specific subdomain and, in a microservice system, commonly to one service.

## The mechanism: one model per boundary

The reason boundaries exist is that a single model cannot stay consistent across a whole enterprise. "Account" means a bank ledger in Billing, a login in Identity, and a marketing profile in CRM. If all three share one `Account` class, each team's new requirement bends the others' model. A bounded context solves this by scoping the model: each context has its own `Account`, its own rules, and its own persistence, and contexts translate at their edges when they talk. This is why the bounded context is the natural unit of deployment in a microservice system: both are answers to the same question - where does one model end.

```d2
direction: right
sales: "Sales context" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
ship: "Shipping context" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
bill: "Billing context" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
s1: "Customer = buyer\nof record" {
  width: 200
  height: 60
}
s2: "Customer = delivery\naddress owner" {
  width: 200
  height: 60
}
s3: "Customer = invoice\npayer" {
  width: 200
  height: 60
}
sales -> s1
ship -> s2
bill -> s3
```

**Fig. 1.** Same word, three models. Each context defines its own Customer; integration happens between contexts, not in a shared class - and the named relationship patterns for that integration live on the context map ([[What is context mapping in DDD]]).

## How you actually find them

Practical heuristics for the analysis: list the business functions, group closely related ones, separate what is core to the business from what merely supports it, and map dependencies between the groups. Event storming does the same thing bottom-up: the team walks through domain events and finds the spots where the flow changes ownership or vocabulary. Two smells refine the cut: if two candidate contexts constantly collaborate, they are probably one context (the failure mode goes by the name Inappropriate Intimacy), and a context that must call another to answer any request is not autonomous. Language shifts, team ownership, and transaction boundaries usually agree on the same line; when they disagree, the language shift wins. Applied to decomposition, one context becomes one service - [[How do you decompose an application by subdomain]].

> [!tip] Interview answer
> A bounded context is the scope in which a domain model and its terms are valid and consistent. I find them by decomposing the domain into [[What is the difference between a bounded context and a subdomain|subdomains]], watching where the same word changes meaning ([[What is ubiquitous language and why does it matter|ubiquitous language]]), and checking cohesion, team ownership, and transaction seams. Each context keeps its own model and translates at the edges, which is why bounded contexts map so naturally onto [[What is microservices|microservice]] boundaries.
