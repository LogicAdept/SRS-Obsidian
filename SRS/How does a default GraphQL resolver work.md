<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> A field without an explicit resolver does not fail — the server's **default resolver** runs. In graphql-java that is `PropertyDataFetcher`: it takes the parent object and reads the property whose name matches the field (map key, record component, or getter). If the parent is a map with that key, or the POJO has that property, the value is used; a missing property resolves to null. Explicit resolvers are needed only where the default lookup cannot compute the field.

## Lookup rules and the value contract

The default resolver's contract, in order: null parent yields null; map parent yields `map.get(fieldName)`; bean/record parent yields the property or accessor matching the field name. This is why well-shaped source objects make wiring almost empty — you wire root fetchers that load aggregates, and nested plain-object fields resolve themselves ([[How does the GraphQL execution engine resolve a query]]).

```java
// graphql-java 26.1: only "user" is wired; "name" and "handle" use the default resolver.
Map<String, Object> user = new LinkedHashMap<>();
user.put("name", "Leia Organa");   // "handle" intentionally absent
// query { user { name handle } } ->
// {"data":{"user":{"name":"Leia Organa","handle":null}}}
```

**Listing 1.** Verified on graphql-java 26.1. The missing map key silently became `"handle":null` — the default resolver's null for an absent property.

```d2
direction: down
P: "Parent value" { width: 200; height: 55 }
D: "Default resolver\nPropertyDataFetcher" { width: 280; height: 65 }
M: "Map: key lookup" { width: 230; height: 55 }
B: "Bean/record: accessor" { width: 240; height: 55 }
N: "missing property -> null" { width: 250; height: 55 }
P -> D
D -> M
D -> B
M -> N: "no key"
B -> N: "no accessor"
```

**Fig. 1.** The default resolver is name-driven: same field name, three outcomes — value from map, value from accessor, or null.

> [!warning] Silent nulls are the price of name matching
> The convenience cuts both ways: a typo between a schema field name and a source property (`handle` vs `nick`) produces a permanent `null` in responses with **no error and no log** — the resolver worked exactly as designed. Against a non-null field type, the same typo detonates as a null-bubbling error instead ([[How does null bubbling work when a GraphQL field is null]]). Guardrails: render the schema against a sample source object in tests, or make fields non-null where absence is truly impossible, so mistakes surface loudly ([[What is the difference between GraphQL list and non-null modifiers]]).

Another subtlety: the default resolver also applies to argument-free scalar fields on the root? No — root fields always need fetchers, because there is no meaningful parent to read from; in graphql-java an unwired root field fails schema construction or resolves null depending on wiring completeness. Frameworks built on graphql-java vary the surface, not the core: Spring for GraphQL's `@SchemaMapping` methods *are* the explicit resolvers, and its property resolution falls back to the same default mechanism ([[How would you explain Spring for GraphQL]]).

When to reach for an explicit resolver despite the default: computed fields, permission checks, joins to another store, and anything that reads arguments — the default resolver knows nothing about `args` or `context` beyond the parent ([[What are the four arguments passed to a GraphQL resolver]]).

> [!tip] Interview answer
> The default resolver resolves a field from its parent by name: maps by key, beans/records by accessor, missing property as null, null parent as null. It is why minimal wiring still works — but mismatches fail silently as nulls unless the field is non-null, where they become loud bubbling errors. Explicit resolvers are for computed values, arguments, context, or cross-store joins.

