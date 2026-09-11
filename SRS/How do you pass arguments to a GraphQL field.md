<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Every field can declare typed **arguments** in the schema — scalars, enums, input objects, or lists of those, optionally with defaults — and the client supplies values inline (`character(id: "1000")`) or through variables (`character(id: $id)`). Validation checks names and types before execution; at runtime the resolver reads them from its args parameter (`env.getArgument("id")` in graphql-java).

## Declaration, supply, consumption

Declaration side: an argument has a name, an input type, and an optional default. Only **input types** are legal — scalars, enums, and input objects composed of them; arbitrary object types with circular fields are rejected, which is exactly why mutations take `input PostInput!` instead of a result type ([[Why do GraphQL mutations use input types instead of object types]]). Non-null (`ID!`) makes the argument required unless it has a default.

```graphql
type Query {
  character(id: ID!): Character
  characters(episode: Episode = NEWHOPE, minId: Int): [Character!]!
}
```

**Listing 1.** A required `ID!` argument, an enum argument with a default, and an optional nullable `Int`.

Runtime side: the engine coerces literals and variables to the declared types, applies defaults for omitted arguments, and hands the map to the resolver. In graphql-java a resolver reads `env.getArgument("minId")` — an absent optional argument is `null`, an SDL enum arrives as its name string by default, and `env.getArgumentOrDefault("first", 2)` supplies a runtime fallback ([[What is the typename meta field in GraphQL]]). Arguments are per-field, so one selection can fan out different values to sibling fields — the standard mechanism for reuse ([[How does the GraphQL execution engine resolve a query]]).

```java
// resolver for "characters(episode: Episode = NEWHOPE, minId: Int)" on graphql-java 26.1:
Object ep = env.getArgument("episode");   // enum name as String, e.g. "NEWHOPE"
Integer minId = env.getArgument("minId"); // null when the client omitted it
// query { characters(minId: 999) { id } }  ->  resolver saw: episode=NEWHOPE minId=999
// {"data":{"characters":[{"id":"1000"},{"id":"1002"}]}}
```

**Listing 2.** Verified on graphql-java 26.1: the SDL default applied, the optional argument arrived as null, values reached the resolver as a typed map.

> [!warning] Argument errors are validation errors, not resolver errors
> A missing required argument fails before any code runs: executing `{ character { name } }` yields `{"errors":[{"message":"Validation error (MissingFieldArgument@[character]) : Missing field argument 'id'","locations":[{"line":1,"column":3}],"extensions":{"classification":"ValidationError"}}]}` — note the classification and that there is no `data` key. The same early rejection applies to wrong literal types and enum values outside the declared set. Resolvers should therefore treat argument **validity** as guaranteed by the schema, and argument **authorization/consistency** (can this caller ask for this id?) as their own job ([[How do you authenticate and authorize a GraphQL request]]).

Two syntax details worth precision. Inline values are written in GraphQL literal syntax — strings in double quotes, enums bare, objects as `{field: value}` field-literals of the input type. And argument values may reference variables anywhere an input value is expected, which keeps documents static and cacheable ([[Why prefer GraphQL variables over inlined values]]).

```d2
direction: down
Doc: "query { character(id: "1000") }" {
  width: 340; height: 60
}
V: "Validation: name, input type,
required, enum set" {
  width: 320; height: 70
}
Co: "Coercion + defaults" {
  width: 250; height: 60
}
R: "Resolver args map
env.getArgument(...)" {
  width: 300; height: 70
}
Doc -> V
V -> Co: "ok"
Co -> R
V -> Err: "unknown/wrong" { width: 250; height: 55 }
Err: "ValidationError,
nothing executes" { width: 250; height: 60 }
```

**Fig. 1.** Arguments flow from the document through validation and coercion into the resolver's args map; invalid arguments abort before execution.

> [!tip] Interview answer
> Arguments are declared per field in SDL with input types and optional defaults; clients pass literals or variables; validation coerces and checks them before execution; resolvers read them from the args/environment — absent optional ones as null, enums as names unless custom coercion. Required-but-missing is a ValidationError before any resolver runs, and only input types (scalars, enums, input objects) are legal argument types.

