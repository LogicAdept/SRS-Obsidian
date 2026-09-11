<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> GraphQL's versioning philosophy: **no URL-level versions** — the schema evolves additively within one contract. You add fields and types, `@deprecated` the old ones with a reason, monitor field usage, and remove once telemetry shows zero callers. Breaking changes are not forbidden but demand coordination; the ecosystem's substitute for versioned endpoints is a **schema registry** that diffs each release and classifies every change as safe or breaking before it ships.

## The additive workflow, end to end

The mechanics: ship the new field alongside the old (`fullName` next to `name`), mark the old one `@deprecated(reason: "Use fullName")` — introspection exposes the flag so tooling flags usages ([[What do the include skip and deprecated GraphQL directives do]]) — then read actual usage: per-field analytics and registry checks tell you which *registered clients* still select the deprecated field. Removal is a contract negotiation, not a code change: announce, migrate, verify zero traffic, delete ([[What is GraphQL introspection]]).

```graphql
type Character {
  id: ID!
  name: String! @deprecated(reason: "Use fullName — removal planned for Q3")
  fullName: String!
  origin: String
  homePlanet: String @deprecated(reason: "Use origin")
}
```

**Listing 1.** The additive step: both names live in the schema, the old one self-documents its replacement and removal horizon; clients migrate at their own pace ([[Which GraphQL schema changes are breaking]]).

```d2
direction: down
Add: "add new field" { width: 200; height: 55 }
Dep: "@deprecated on old field\n(reason visible in introspection)" { width: 340; height: 70 }
Mon: "usage analytics +\nregistry diff each release" { width: 300; height: 70 }
Rm: "remove old field\nwhen usage hits zero" { width: 250; height: 60 }
Add -> Dep -> Mon -> Rm
```

**Fig. 1.** The lifecycle is a pipeline, not a version bump: introduce, mark, observe, retire.

> [!warning] "No versions" does not mean "no breaking changes"
> Three corrections. First: the claim is that GraphQL *reduces the need* for versioned endpoints by making most changes additive — field additions, new types, new optional arguments — but **removals, renames, type narrowing, and argument tightening** are as breaking as they would be anywhere; the registry's job is to catch them pre-merge ([[Which GraphQL schema changes are breaking]]). Second: deprecated does **not** mean dead — nothing enforces migration; without usage telemetry and a removal date in the reason string, deprecation markers accumulate forever ([[What is GraphQL introspection]]). Third: version pressure does not disappear — it moves into client release coordination, which persisted-query registries make tractable by tying hashes to client builds ([[What are persisted queries in GraphQL]]).

Operational layer: schema registries (Apollo Graph Manager-style, or self-hosted) diff proposed schemas against production, gate CI on breaking-change detection, and store per-release snapshots; gateways roll out composition only after checks pass ([[What is the difference between GraphQL federation and schema stitching]]). For genuinely incompatible redesigns — new auth model, changed value semantics — teams still choose parallel schema endpoints (a `v2` URL) rather than contorting one schema; additive evolution covers the 90% case, not the 100% ([[When should you not use GraphQL]]).

> [!tip] Interview answer
> GraphQL evolves the schema instead of versioning URLs: add fields, deprecate old ones with a reason, watch field-usage analytics, and remove when usage is zero. Registries diff every release and classify changes as additive or breaking before merge — because removals, renames, and type narrowing still break clients. True redesigns may still warrant a separate schema; the discipline is usage-driven retirement, not version strings.

