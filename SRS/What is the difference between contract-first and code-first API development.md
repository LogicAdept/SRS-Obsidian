<!--
reps: 0
priority: 0
-->
#API/Contracts #API/OpenAPI #SRS

# What is the difference between contract-first and code-first API development

> [!abstract] Short answer
> Contract-first writes the interface (OpenAPI document) first and generates or validates code against it; code-first writes the implementation and derives the contract from it (annotations, reflection). Contract-first makes the interface the source of truth and drift mechanically detectable; code-first optimizes iteration speed and leaks the risk of the contract being whatever the code grew into.

## Two directions of truth

Contract-first: the OpenAPI (or gRPC proto) document is authored, reviewed, and versioned as the artifact; server stubs, client SDKs, and mocks are generated from it, and CI keeps implementation honest (generated interfaces to implement, or contract tests to replay). Consumers see the agreed document, not your last deploy. Code-first: you write controllers and DTOs; tooling (springdoc, Swagger core) derives the OpenAPI at runtime — convenient, always in sync with the code, and exactly as considered as the code. The trade is who owns truth: contract-first puts it in the reviewed document (with drift as a test failure), code-first puts it in the implementation (with drift impossible but design review late and accidental exposure likely — an internal field name becomes the public JSON key because nobody planned the surface). Hybrid flows are common: code-first with spec-check-in — generate, review, pin, and diff the artifact in CI ([[What is API-first design]] is the process that makes contract-first organizational; [[What is OpenAPI and how does Swagger relate to it]] for the artifact format).

```d2
cf: contract-first {
  spec: OpenAPI doc (authored)
  gen: generated stubs + SDKs + mocks
  impl: implements against stubs
  ci: CI: contract tests on drift
  spec -> gen -> impl
  impl -> ci -> spec
}
cl: code-first {
  code: controllers + DTOs
  derive: springdoc derives spec
  pub: spec = what code grew
  code -> derive -> pub
}
cf.spec: source of truth
cl.code: source of truth
```

**Fig. 1.** The arrow of truth: contract-first flows from a reviewed document to code; code-first flows from code to whatever document the tooling can extract.

## Choosing per boundary

Contract-first fits public APIs, partner interfaces, and microservice boundaries — places where consumers exist before the implementation and negotiation must happen early; costs are authoring discipline and codegen friction. Code-first fits internal endpoints with fast iteration and small consumer circles, exploratory work, and teams whose spec tooling is weak; its cost is that review shifts after the fact and the contract inherits implementation accidents (leaky entities, field names as serialized). The interview follow-up "how do you prevent drift" is the real test: contract-first answers with generated interfaces or contract tests in CI; code-first answers with publishing the derived spec and diffing it — both are mechanical, and "we review carefully" is the wrong answer ([[What changes are breaking for a REST API]] because diffs catch exactly those; [[What are the key principles of good API design]] for consistency enforcement). SOAP's history is instructive: WSDL-first versus code-first was the same debate twenty years ago ([[What is WSDL used for]]).

```text
contract-first: openapi.yaml (reviewed) -> openapi-generator -> stubs, SDK, mocks
                CI: contract tests replay spec against implementation
code-first    : @RestController code -> springdoc derives openapi.json at runtime
                CI: publish derived spec, diff for accidental changes
```

**Listing 1.** Both flows end with an artifact; the difference is which side is authored first and which side is the truth (conceptual).

> [!warning] Code-first's spec is a photograph, not a plan
> A derived OpenAPI documents what exists — including the pagination inconsistency, the entity leak, and the two error shapes. Treating a generated document as evidence of design means no design happened; the review that contract-first forces has merely moved to your consumers' bug tracker.

> [!tip] Interview answer
> Contract-first authors the interface as the artifact — OpenAPI first, then stubs, SDKs, mocks generated from it, and CI contract tests to catch drift. Code-first implements and derives the spec with tooling like springdoc — fast, always in sync, but the contract is whatever the code grew. I go contract-first at public and cross-team boundaries, code-first for internal iteration, and in both cases I make drift a build failure, not a review hope.
