<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> **Schema stitching** merges multiple schemas at runtime by type names — the client queries one merged schema; matching types are combined, and hand-written resolvers delegate between them. **Federation** (Apollo's architecture, now the de-facto standard) is a **build-time composition contract**: each subgraph declares ownership of entity fields (`@key`), a router composes the supergraph from subgraph SDL, and the **gateway/router** plans and executes queries across subgraphs, passing entity representations. Stitching is a merge technique; federation is an ownership architecture.

## The structural difference

Stitching's raw material is **whole schemas**: `stitchSchemas({ schemas: [...] })` unites them; conflicts are resolved by convention or extension delegation. It works well for aggregating stable schemas but gives the merged graph no notion of *who owns what* — cross-service references are ad hoc delegation functions ([[What is GraphQL introspection]]).

Federation's raw material is **partial ownership**: each subgraph defines its own types and **extends** entities owned elsewhere — `type Product @key(fields: "upc")` in the products subgraph, while reviews extends `Product` with just `upc` plus its own fields. Composition (build time) verifies the supergraph is valid: no conflicting field definitions, keys declared and resolvable. At runtime the **router** plans the query: fetch entities from the owning subgraph, then distribute `_entities` requests carrying *representations* (type name + key fields) to subgraphs that extend them ([[How does a federated GraphQL gateway plan a query]]).

```graphql
# subgraph "reviews": it does not own Product; it extends it.
type Product @key(fields: "upc") {
  upc: String!            # key field only — resolvable, not owned
  reviews: [Review]!      # owned by reviews
}
# the gateway plans { product(upc) { name reviews { body } } } as:
#   products subgraph -> Product.name
#   reviews  subgraph -> _entities(representations: [{__typename: "Product", upc}]) -> reviews
```

**Listing 1.** Ownership by fields, coordination by key fields and representations — the mechanism stitching lacks entirely ([[What is the typename meta field in GraphQL]]).

```d2
direction: down
A: "stitching\nmerge by type names at runtime" { width: 340; height: 70 }
B: "federation\ncompose from owned subgraphs at build time" { width: 350; height: 70 }
R: "router plans + executes\n@key / _entities protocol" { width: 330; height: 70 }
A -> B: "superset + contract"
B -> R
```

**Fig. 1.** Stitching merges schemas; federation composes ownership and adds the router protocol that makes cross-subgraph entity traversal deterministic.

> [!warning] The choice is organizational before it is technical
> First: stitching's flexibility is its failure mode — no ownership model means two teams can define the same type differently and the merge invents semantics; federation's composition **fails the build** on conflicts, which is the feature ([[How do you version a GraphQL schema]]). Second: federation is not cost-free — subgraphs must speak the `_service`/`_entities` contract (libraries exist for Java via Spring for GraphQL federation support), and the router is critical infrastructure ([[How would you explain Spring for GraphQL]]). Third: "stitching is dead" overstates it — merging heterogeneous or third-party schemas where you cannot enforce subgraph contracts remains stitching territory; Apollo itself evolved stitching-era tooling into federation because the ownership problem needed a protocol, not a merge utility ([[When should you not use GraphQL]]).

Migration note: teams routinely start with one monolithic schema, split into subgraphs when team boundaries demand independent deploys, and adopt federation at that point — the trigger is organizational scale, not query complexity.

> [!tip] Interview answer
> Stitching unites schemas by type names at runtime with delegated resolvers — an aggregation technique. Federation is an ownership architecture: subgraphs own fields, extend entities via @key, composition validates the supergraph at build time, and a router plans queries, passing entity representations through _entities. Choose stitching for merging schemas you don't control; federation when multiple teams need independent, verifiable ownership of one graph.

