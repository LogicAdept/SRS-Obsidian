<!--
reps: 0
priority: 0
-->
#SystemDesign/Tradeoffs #Methodologies/Principles/YAGNI #SRS

# What is overengineering and how does it affect enterprise software

> [!abstract] Short answer
> Overengineering is building more capability, abstraction, generality or infrastructure than the requirements and their foreseeable growth justify — microservices for a CRUD app, framework-of-frameworks for three endpoints, config for requirements nobody stated. In enterprise software it taxes everything that comes after: slower delivery, more failure modes, harder onboarding, and maintenance of machinery whose owning justification is gone. Its antidote is YAGNI with a price tag: build the simple thing that meets measured requirements, and leave documented seams for the growth that actually appears.

## What it looks like and what it costs

Overengineering has recognizable shapes: speculative generality (interfaces with one implementation "in case", parameterization nobody uses), premature distribution (services split by fashion, paying network, consistency and ops costs for a monolith-sized problem — the CQRS/microservice cautions in [[Which kinds of projects benefit most from CQRS]] and [[What is the difference between a stateful service and a stateless service]] apply), infrastructure before load (sharding, multi-region, deep cache hieropies before the traffic exists — [[What problem does database sharding solve]] is a cost to pay when measured), and gold-plating (layers of config, abstraction and pipeline around features whose behavior could be a function). The enterprise costs compound: every abstraction is code that must be understood, tested and maintained even while unused; delivery slows because trivial changes traverse ceremony; reliability suffers because more moving parts fail more ways ([[What difficulties arise when working with caching]]-style failure modes multiply); and onboarding steepens — new developers learn the architecture before the business. The subtlest cost is decision debt: speculative structures encode guessed requirements, and guesses age badly — the abstraction built "for flexibility" constrains the actual flexible change when it arrives.

```text
symptoms:
- interface with 1 impl, added "in case"
- N services for M << N business capabilities
- config surface >> feature surface
- change requires touching 5 layers to add a column
cost: slower delivery, more failure modes, onboarding tax, decision debt
antidote: YAGNI + measured requirements + documented seams
```

**Listing 1.** The symptom list, the cost, and the counter-policy.

## The counter-policy and the honest tradeoff

YAGNI ("you aren't gonna need it") is the discipline: implement for the requirements you have; when a new requirement arrives, refactor then — with tests and version control, refactoring later is cheaper than maintaining speculation now. But the enterprise-grade version is not "always dumbest": some flexibility is purchased deliberately — the skill is paying for extensibility only at seams with evidence: measured growth curves (load heading toward the vertical-scaling ceiling of [[How do NoSQL databases scale compared with SQL databases]]), contractual volatility (a vendor swap planned — [[How do you design a system against vendor lock-in]]'s exit-plan pricing), or organizational scaling (team boundaries demanding service borders). The counter-policy that survives enterprise reality: start simple, measure, extract abstractions when the second real case appears (rule of three), and document the seams you deliberately left simple — a README line saying "this is intentionally a monolith table scan; shard when X" is architecture, not debt. [[What are coupling and cohesion and how do they affect maintainability]] gives the quality bar the simple version must still meet: simple does not mean coupled mud — the simplest design that keeps boundaries clean is the one that refactors cheaply later.

> [!warning] Speculative flexibility constrains the real change
> The abstraction added "for later" hard-codes today's guess about what later needs — and the actual later usually differs. Removing a wrong abstraction costs more than never writing it; premature structure is not neutral, it is a bet placed against your future requirements.

> [!tip] Interview answer
> Overengineering is capability beyond justified requirements — speculative interfaces, premature microservices and infrastructure, gold-plating. It taxes delivery, reliability and onboarding in enterprise settings. My counter is YAGNI with evidence: build the simple clean-boundary version, measure, and pay for extensibility only at seams with real growth signals — refactoring later is cheaper than maintaining guesses.
