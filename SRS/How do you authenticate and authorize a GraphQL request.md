<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> **Authentication** (who is calling) happens at the transport boundary before execution: parse the HTTP request's credentials (session cookie, bearer token, mTLS), validate them, and place the principal into the **execution context**. **Authorization** (what may this caller do) happens per operation — ideally per field or per type — inside resolvers or directive-based rules, because GraphQL's granularity is fields, not routes. The single most common mistake is treating "the endpoint is authenticated" as sufficient.

## Transport auth, field-level authorization

Authentication is unchanged from any HTTP API: middleware validates credentials and rejects or attaches the user. The GraphQL-specific part is *where* the principal lives afterwards: in the per-request context object every resolver can read — never in global state, never re-derived per field ([[What is GraphQL execution context]]).

Authorization is where GraphQL differs structurally from REST: one endpoint means one URL-level policy cannot express per-field access. The checks belong at the finest boundary the data flows through:

- **Field-level resolvers**: each sensitive field's resolver reads the context and fails the field if the caller lacks rights — producing a field error rather than aborting siblings ([[What does the GraphQL errors array contain]]).
- **Directive/decorator enforcement**: declare intent in the schema (`@auth(role: "hr")` style) and enforce centrally via wiring — declarative, auditable, testable ([[What do the include skip and deprecated GraphQL directives do]]).
- **Business-layer checks**: the most robust point — resolvers call domain services that already enforce rights, so no GraphQL-specific path can bypass them.

```java
// graphql-java 26.1: context carries role; the sensitive field's resolver enforces it.
DataFetcher<Object> salary = env -> {
    Map<String, Object> ctx = env.getContext();
    if (!"hr".equals(ctx.get("role"))) {
        throw GraphqlErrorException.newErrorException()
                .message("salary requires role=hr")
                .extensions(Map.of("code", "FORBIDDEN")).build();
    }
    return "120000 USD";
};
// anonymous: 200 + {"errors":[{"path":["salary"],"extensions":{"code":"FORBIDDEN",...}}],"data":null}
// hr role:   {"data":{"publicInfo":"public","salary":"120000 USD"}}
```

**Listing 1.** Verified on graphql-java 26.1. The same document from two callers: the unauthorized one gets a field-scoped FORBIDDEN error; the sibling field still resolved — authorization granularity is per field ([[How does null bubbling work when a GraphQL field is null]]).

```d2
direction: down
H: "HTTP request\ncredentials" { width: 220; height: 60 }
A: "Authenticate at boundary\n-> context.principal" { width: 300; height: 65 }
R: "Resolvers execute" { width: 220; height: 55 }
Z: "Authorize per field/type\ncontext + policy" { width: 300; height: 65 }
H -> A
A -> R
R -> Z
```

**Fig. 1.** Two different questions at two different layers: authentication once at the boundary, authorization at every data boundary the schema exposes.

> [!warning] Introspection-visible fields are not authorized fields
> The classic GraphQL auth bugs: hiding a field from the schema is not protection — the schema is documentation, not policy, and an unauthorized caller can still select anything exposed unless resolvers enforce ([[What is GraphQL introspection]]); relying on "the gateway authenticated the user" while any field reads raw data; and leaking object existence through error differences (404 vs FORBIDDEN probes) ([[Why disable GraphQL introspection in production]]). Also mind object-level authorization: field checks do not automatically cover lists — a `friends` resolver returning entities the caller may not read needs an object-level rule, the GraphQL flavor of IDOR ([[How do you paginate a GraphQL list]]).

> [!tip] Interview answer
> Authenticate once at the transport — validate credentials and put the principal into the request context. Authorize at GraphQL's real granularity: per field or per type, in resolvers, via declarative directives, or best in the business layer behind them. Schema visibility is not authorization; field errors let siblings survive denial; and list fields need object-level checks to avoid IDOR.

