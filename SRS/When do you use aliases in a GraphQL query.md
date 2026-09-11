<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Aliases rename a field **in the response** without changing what the server executes: `hero: character(id: "1000")` runs the `character` field but the result appears under key `hero`. You need an alias whenever the same field must appear twice in one selection set — response keys would otherwise collide — and they are equally useful to give a stable, UI-friendly key to a field with a long argument list.

## The rule and the mechanism

Selection-set keys must be unique within one object level: JSON objects cannot hold duplicate keys, so `{ character(id: "1") { name } character(id: "2") { name } }` is invalid — the second `character` would overwrite the first. Aliasing each occurrence (`first:`, `second:`) makes the document valid and the result unambiguous. Validation enforces this: two same-named fields with identical arguments merge, otherwise the document fails before execution ([[What is a GraphQL fragment]]).

```java
// graphql-java 26.1, schema with droid(id) and human(id):
// query: { hero: droid(id: "2000") { name }  person: human(id: "1000") { name } }
// {"data":{"hero":{"name":"C-3PO"},"person":{"name":"Luke"}}}
```

**Listing 1.** Verified on graphql-java 26.1: both fields ran with different arguments; the aliases gave each its own result key.

Aliases apply to any field, including root fields and meta fields, and compose with fragments and directives — an aliased field can carry its own `@include`, and fragments keep the alias they were spread with ([[What do the include skip and deprecated GraphQL directives do]]). Alias names follow GraphQL name rules (no dots, no quotes) and do not need to match any schema name, because they never reach the server's execution logic: the resolver still sees `character` ([[How does the GraphQL execution engine resolve a query]]).

> [!warning] Aliases change response keys, not the schema, and clients notice
> Two practical traps. First: renaming an alias is a client-side breaking change — normalization caches, typed clients, and UI bindings key on the response field name, so a casual alias edit can break a screen with no server change at all ([[Which GraphQL schema changes are breaking]]). Second: do not reach for aliases to "hide" server field names as a security measure; obfuscating `passwordHash` as `p` still executes the same resolver and still returns the data. Aliasing is a presentation concern, not an authorization boundary ([[How do you authenticate and authorize a GraphQL request]]).

Typical legitimate uses: fetching several entities of the same kind in one round trip (`first: user(id: "1"), second: user(id: "2")`); giving a stable contract name to a field whose server-side arguments churn; and discriminating parallel calls to the same field with different enum arguments in a single operation. The cost is negligible — aliases are resolved during document parsing and cost one map key at serialization ([[What are the four arguments passed to a GraphQL resolver]]).

```d2
direction: down
F1: "character(id: "1")" { width: 240; height: 55 }
F2: "character(id: "2")" { width: 240; height: 55 }
A1: "alias first:" { width: 170; height: 50 }
A2: "alias second:" { width: 180; height: 50 }
R: "response keys
first, second" { width: 240; height: 60 }
F1 -> A1
F2 -> A2
A1 -> R
A2 -> R
``
```

**Fig. 1.** Two executions of the same field need distinct response keys; aliases rename results without touching the schema or the resolvers.

> [!tip] Interview answer
> An alias renames a field in the response only: `alias: field(args)` keeps execution identical but changes the result key. It is mandatory when the same field appears twice in one selection set — response keys must be unique — and handy for stable client-facing names. Clients and caches key on the alias, so alias names are part of the client contract even though the server never sees them.

