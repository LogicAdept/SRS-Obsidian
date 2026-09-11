<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Variables turn a request's dynamic parts into a separate JSON payload: the document stays a **constant string** with declared placeholders (`query D($id: ID!) { droid(id: $id) { name } }`), and `variables` travel beside it. Clients get one cacheable document per operation, safe escaping for free, and no string interpolation against the query language — which is both the security and the performance argument.

## How the mechanism works

The document declares each variable with its input type; non-null variables must be present and nullability is checked against the type. Values are supplied out of band (the `variables` member of the request payload) and substituted where an input value is expected — arguments, defaults for skipped directives, nested input-object fields. `operationName` selects among multiple named operations in one document. Nothing about variables is transport-specific: HTTP POST with `{query, variables, operationName}` is the usual shape ([[What is GraphQL introspection]]).

```java
// graphql-java 26.1:
String doc = "query DroidById($id: ID!) { droid(id: $id) { name } }";
ExecutionInput in = ExecutionInput.newExecutionInput()
        .query(doc)
        .variables(java.util.Map.of("id", "2000"))
        .build();
// {"data":{"droid":{"name":"C-3PO"}}}
```

**Listing 1.** Verified on graphql-java 26.1: one static document, the value supplied via the variables map, result identical to an inline literal.

> [!warning] Variables are not an injection shield — and not a license for dynamic strings
> Unlike SQL, GraphQL documents are not string-concatenated into a database command; injection lives one layer down, in what a resolver does with the value, so a resolver that builds SQL from `$id` without parameters is still injectable ([[What is the N plus 1 problem in GraphQL]]). The real anti-pattern is the inverse: building the *document* by string templating (`"{ droid(id: \"" + id + "\") ... }"`) instead of using variables. That breaks document caching and persisted-query hashes, and hand-escaped strings are how accidental query-language injection happens ([[What are persisted queries in GraphQL]]).

Why this matters operationally: with inlined values every distinct user input produces a distinct document, so server-side caches keyed by document text collapse — variable use keeps the document identical across callers. Clients (Apollo, Relay) exploit this: normalized caches and persisted queries store the document once and send hashes plus variables. Typed clients also generate variable types from the schema, so a wrong variable shape fails client-side before the request ([[What is the difference between schema-first and code-first GraphQL]]).

Rules worth reciting: variable types must be input types; a `ID!` variable cannot be null or missing (unless the argument has a default); and omitting a nullable variable that an optional argument references passes null through explicitly. Custom scalar variables go through `parseValue` — the JSON-side coercion — while inline literals go through `parseLiteral`, and a custom scalar that implements only one of them breaks one syntax silently ([[What are GraphQL scalar types]]).

```d2
direction: right
D: "Static document\nquery D($id: ID!)" { width: 240; height: 70 }
P: "Payload\nvariables: {id}" { width: 200; height: 60 }
S: "Server" { width: 180; height: 55 }
D -> S: "same bytes every time"
P -> S: "values only"
```

**Fig. 1.** The document stays byte-identical across callers while values travel separately — the precondition for document caches and persisted queries.

> [!tip] Interview answer
> Variables separate the constant document from the changing values: declared with input types, validated against them, supplied as JSON. Benefits: one cacheable/persistable document, no string-building against the query language, generated client types, and free correct escaping. They are not a SQL-injection fix — resolver-level parameterization still is — but they eliminate document-level interpolation bugs and make document caches and persisted queries work.

