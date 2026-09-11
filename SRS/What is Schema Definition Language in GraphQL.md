<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> SDL — Schema Definition Language — is the declarative syntax of GraphQL used to **describe types** rather than to fetch data. A `query` document asks for data; an SDL document defines what *can* be asked for: `type`, `input`, `enum`, `interface`, `union`, `scalar`, and `schema` definitions. It is the human-readable form of the schema that servers parse and that teams treat as the API contract.

## Where SDL shows up

Server frameworks parse SDL into a type registry and then bind resolvers to it. The same text serves other roles: code generators turn SDL into typed client models; schema-registry systems store and diff successive SDL versions to detect breaking changes; federated gateways compose subgraph SDL into one supergraph schema. Because the syntax is identical everywhere, "the schema" is usually shipped and reviewed as an SDL file ([[What is a GraphQL schema]]).

```graphql
directive @deprecated(
  reason: String = "No longer supported"
) on FIELD_DEFINITION | ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION | ENUM_VALUE

type Query {
  character(id: ID!): Character
}

type Character {
  id: ID!
  name: String!
  homePlanet: String @deprecated(reason: "Use origin instead")
}

interface Node { id: ID! }

union SearchResult = Character | Episode

input CharacterFilter { name: String! }

enum Episode { NEWHOPE EMPIRE JEDI }
```

**Listing 1.** The SDL vocabulary: object types with arguments and wrappers, an interface, a union, an input object, an enum, and a directive definition with locations. Built-in directives such as `@deprecated` are defined in SDL too.

## How SDL relates to runtime types

SDL is a **description**, not the implementation. A server parses SDL into in-memory type objects (in graphql-java a `TypeDefinitionRegistry`), then merges it with runtime wiring that supplies resolvers and type resolvers for interfaces and unions; only then does an executable schema exist ([[What is the difference between schema-first and code-first GraphQL]]). Two consequences matter in practice. First, SDL says nothing about storage or transport — the same SDL may sit over SQL, a cache, or another HTTP call. Second, SDL has no behavior: a field marked non-null in SDL is only a declaration; the *runtime* enforces it through null bubbling when a resolver actually returns null ([[How does null bubbling work when a GraphQL field is null]]).

> [!warning] SDL is not a query, and a query is not SDL
> Interviewers like the mixup. A request document can contain anonymous shorthand (`{ hero { name } }`) only for queries; SDL files contain no selection sets at all. If you catch yourself writing `type Query` inside a request or writing `{ characters { id } }` inside a schema file, you have swapped the two roles ([[What is the difference between a GraphQL query a mutation and a subscription]]).

There is one syntax family rather than two: request documents and SDL share the same lexer and value literals (ints, floats, strings, booleans, enum names), so tooling can parse both with one grammar. That is why fragments, variables, and directives have the same shape in both worlds ([[What is a GraphQL fragment]]).

```d2
direction: right
sdl: "SDL document
type, input, enum, union" { width: 250; height: 80 }
wiring: "Runtime wiring
resolvers, type resolvers" { width: 250; height: 80 }
schema: "Executable schema
validate + execute" { width: 250; height: 80 }
sdl -> schema: "parsed"
wiring -> schema: "merged"
```

**Fig. 1.** SDL describes, wiring implements; only their merge yields the executable schema that validates and runs requests.

> [!tip] Interview answer
> SDL is the definition language of GraphQL: `type`, `input`, `enum`, `interface`, `union`, `scalar`, and directive declarations describing the API surface. Servers parse it, merge runtime wiring into it, and get an executable schema; registries and generators diff it or produce typed clients. Queries and SDL share one grammar, but a query selects data while SDL declares what exists — the distinction is the role, not the syntax.

