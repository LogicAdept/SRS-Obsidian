<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Introspection is GraphQL's self-description mechanism: the schema is itself queryable through the meta fields `__schema` and `__type` on the query root. A special introspection query returns every type, field, argument, deprecation state, and directive — which is how IDEs autocomplete, clients generate typed code, and documentation renders. It is a normal part of every compliant schema, selected like any other fields.

## What it exposes and who consumes it

The entry points are two meta fields available **only on the query root**: `__schema` (the whole type system: query/mutation/subscription roots, all types, directives) and `__type(name:)` (one type by name). Inside, everything a tool needs: field lists with argument types, wrapper composition (list/non-null), enum values, implemented interfaces, `isDeprecated` plus deprecation reasons ([[What is the typename meta field in GraphQL]]). Note what introspection does **not** expose: runtime data — only the contract; and resolver wiring — only declared types ([[What is Schema Definition Language in GraphQL]]).

```java
// graphql-java 26.1, schema with union SearchResult = Movie | Person:
// { __schema { queryType { name } } __type(name: "Movie") { fields { name } } }
// {"data":{"__schema":{"queryType":{"name":"Query"}},
//          "__type":{"fields":[{"name":"title"}]}}}
```

**Listing 1.** Verified on graphql-java 26.1: the query root's name and one type's field list pulled from the live schema — no out-of-band description needed.

The consumers, in practice: **tooling** — IDEs (GraphiQL and playgrounds render docs and autocomplete purely from introspection), client code generators, schema registries and diff tools that classify changes as breaking ([[Which GraphQL schema changes are breaking]]); **client libraries** — normalized caches and typed documents are built from schema knowledge; **federation** — gateways compose subgraph schemas by fetching their SDL/introspection at build or boot time ([[What is the difference between GraphQL federation and schema stitching]]).

```d2
direction: down
D: "{ __schema { ... } }" { width: 240; height: 55 }
S: "Live schema" { width: 180; height: 50 }
T: "Docs, autocomplete\nIDEs / playgrounds" { width: 260; height: 65 }
C: "Typed clients, caches" { width: 240; height: 60 }
R: "Registries, diff,\nfederation composition" { width: 280; height: 70 }
D -> S
S -> T
S -> C
S -> R
```

**Fig. 1.** One mechanism, three consumer classes: developer tooling, client libraries, and schema-governance infrastructure all read the same self-description.

> [!warning] Introspection is a data surface, not just documentation
> The security nuance behind "disable introspection in production": the introspection query reveals the **complete attack surface** — every field, argument, and deprecated path, including internal or admin fragments someone forgot to hide. It converts blind probing into targeted probing; combined with field-level error differences it accelerates authorization testing ([[How do you authenticate and authorize a GraphQL request]]). But disabling it is weak defense: it breaks legitimate tooling, and gateways or generated clients usually already hold the schema — treat it as attack-surface reduction at the edge, not as an authorization control ([[Why disable GraphQL introspection in production]]). Cost-wise, introspection queries can be large and expensive; unbounded `__schema` selection is itself a work-generation vector under rate limiting ([[Why is rate limiting harder in GraphQL than REST]]).

Interview precision: introspection is specified via the same meta-field machinery as `__typename` (double-underscore names are reserved), and it reads the schema as **currently deployed** — deprecated fields included — which is exactly why schema registries snapshot it per release ([[How do you version a GraphQL schema]]).

> [!tip] Interview answer
> Introspection is the schema querying itself: `__schema` and `__type` on the query root expose every type, field, argument, and deprecation. Tooling — autocompletion, codegen, schema diffing, federation composition — is built entirely on it. It reveals the API's full surface but not runtime data; production often restricts it as attack-surface hygiene, while registries and gateways legitimately rely on it.

