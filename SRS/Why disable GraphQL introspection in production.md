<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Because introspection publishes your **complete attack surface** — every type, field, argument, and deprecated path — to anyone who asks, and production callers usually do not need it. Disabling it at the edge removes cheap reconnaissance, shrinks the payload of information leaks, and costs little when clients already hold generated types. It is a hygiene control, not an authorization mechanism: access still has to be enforced per field, and internal tooling needs an authenticated path with introspection kept on.

## What attackers get from an open introspection endpoint

An introspection dump converts blind probing into a targeted map: hidden admin mutations, deprecated-but-alive fields, internal naming that hints at backend structure, argument surfaces for injection testing, and object types that reveal relationships for IDOR attempts ([[What is GraphQL introspection]]). Combined with per-field error differences, an open introspection endpoint accelerates authorization probing from guesswork to checklist ([[How do you authenticate and authorize a GraphQL request]]). Public APIs with unbounded documents add a second angle: the full `__schema` tree is itself an expensive response, and repeated large introspection selections are a work-generation vector under weak rate limiting ([[Why is rate limiting harder in GraphQL than REST]]).

```d2
direction: down
Q: "{ __schema { ... } }" { width: 220; height: 55 }
M: "Complete type map:\nfields, args, deprecated" { width: 290; height: 65 }
P: "Production client" { width: 230; height: 55 }
A: "Anonymous probing" { width: 220; height: 55 }
R: "registered docs / codegen\nintrospection not needed" { width: 320; height: 70 }
D: "disable at edge\nfor unauthenticated traffic" { width: 300; height: 65 }
M -> P: "unnecessary"
M -> A: "free map"
P -> R
A -> D
```

**Fig. 1.** First-party clients build documents from codegen, not live introspection; anonymous probing is the only consumer that truly needs it — so the edge can refuse it.

```graphql
# The reconnaissance selection the edge refuses for unauthenticated traffic:
# { __schema { types { name fields { name args { name } } } } }
# expected for anonymous callers: a transport-level rejection (or empty result),
# while authenticated internal tooling keeps full introspection.
```

**Listing 1.** Not an execution concern — the query validates — but a policy decision at the gateway: introspection is gated, not destroyed.
> [!warning] "Introspection off" is not a security architecture
> The mandatory corrections. First: authorization lives in resolvers and policies; a server with introspection disabled but field-level auth missing is wide open — you only hid the map, not the doors ([[How do you authenticate and authorize a GraphQL request]]). Second: first-party clients rarely need runtime introspection (documents are built and typed at build time, persisted queries carry hashes), but *developer* tooling does — so teams usually gate introspection by auth or environment rather than hard-disable it everywhere ([[What are persisted queries in GraphQL]]). Third: hiding the schema is not obscurity worth much — leaked SDL, client bundles, and gateway configs expose contracts anyway; treat introspection state as one layer among many ([[What is GraphQL introspection]]).

Operationally: gateways may keep introspection internal-only; schema registries snapshot it in CI; and production monitoring should alert on introspection selections from unauthenticated traffic as a signal of probing ([[Why is HTTP caching harder with GraphQL than REST]]).

> [!tip] Interview answer
> An open introspection endpoint hands out the full field map — admin fields, deprecated leftovers, internal naming — making reconnaissance targeted instead of blind, and large `__schema` selections are themselves a cost vector. First-party clients hold typed documents already, so the edge can disable or auth-gate introspection in production. But it is hygiene, not authorization: field-level enforcement does the real work.

