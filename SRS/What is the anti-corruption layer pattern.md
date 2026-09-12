<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Refactoring #Methodologies/DDD #SRS

# What is the anti-corruption layer pattern

> [!abstract] Short answer
> An anti-corruption layer (ACL) is a translation boundary between two domain models: your new service's clean model on one side, a legacy monolith's or foreign system's model on the other, with the ACL converting between them so the legacy vocabulary never leaks in. From Evans's DDD, used in Richardson's refactoring-to-microservices work to keep a strangler-extracted service from inheriting the monolith's concepts.

## Mechanism: isolate, translate, own your language

The problem the pattern names is corruption: a new service integrating directly with the legacy system starts thinking in the legacy system's terms - its entity names, its status codes, its accidental complexities. Within a few sprints the "clean" service has legacy field names in its API, legacy state machines in its logic, and every future change must consider the legacy shapes. The ACL is a layer with two responsibilities: facade - present the legacy system's capabilities in your model's terms, hiding its API surface; adapter/translator - convert requests and responses between the two models, including semantic normalization (the legacy "CustomerRecord with status 7" becomes your "Customer with status ACTIVE"). Crucially, the ACL is owned by the new service's side: the legacy team changes nothing, and the translation knowledge lives in one place instead of being smeared across calling code. Conceptually the ACL protects a bounded context - which is why the pattern is DDD-native and pairs naturally with context mapping ([[What is a bounded context and how do you identify one]] for the boundary-finding mechanics).

```d2
direction: right
new: "New service
own ubiquitous language
Customer, ACTIVE" {style.fill: "#e8f5e9"}
acl: "Anti-corruption layer
facade + translator" {style.fill: "#ffe0b2"}
legacy: "Legacy monolith
CustomerRecord, status=7" {style.fill: "#ffcdd2"}
new -> acl: your model's calls
acl -> legacy: legacy API
legacy -> acl: legacy shapes
acl -> new: your model's types
```

**Fig. 1.** The ACL is the only place where the two vocabularies meet; both sides keep speaking their own language.

In Richardson's refactoring story the ACL is the companion of [[What is the strangler fig pattern and when do you use it]]: strangling moves traffic from monolith to new services incrementally, and the ACL keeps each extracted service clean while it still calls back into the monolith for the not-yet-migrated capabilities ([[How do you decompose a monolith into microservices]] is the overall playbook). The same pattern applies beyond modernization: any foreign system with a model you do not control - a partner's SOAP API, a purchased CRM - deserves an ACL if its model differs from yours.

## Costs and the honest boundary

An ACL is real code: mapping layers, mapping tests, and a maintenance tax every time the foreign system changes. For a small integration the tax can exceed the benefit - if the foreign model is already close to yours, a thin adapter suffices and calling it an ACL is ceremony. The pattern earns its cost when the models genuinely diverge and the integration is long-lived: then the one-time cost of translation buys permanent conceptual cleanliness - the new service evolves its model freely, and replacing the legacy system behind the ACL eventually becomes an implementation detail. That endgame is the interview-worthy point: an ACL is often temporary scaffolding; when the legacy system is gone, the ACL shrinks to an adapter or disappears.

> [!warning] A leaky ACL is worse than none
> The slow failure mode: convenience shortcuts leak legacy types through the layer - one method returns the legacy DTO "just this once", a status code passes through unconverted - and callers bind to them; now the corruption has a path around the wall and every subsequent leak is easier to justify. Enforce the boundary: the ACL's public surface speaks only your model's types, and the tests assert translations, not pass-throughs. Second trap: fat ACLs that silently absorb business rules - the moment the layer starts deciding things (defaults, eligibility), it is a service in disguise; business logic belongs in the domain, translation belongs in the ACL.

> [!tip] Interview answer
> An anti-corruption layer is a translation boundary that keeps a foreign model - a legacy monolith, a third-party system - from polluting my service's domain model: a facade in my vocabulary plus adapters that convert both directions, owned by my side. It is DDD context-mapping made concrete and the standard companion of the strangler-fig migration. It costs mapping code, so I use it where models truly diverge - and keep its surface strictly my-model-only.
