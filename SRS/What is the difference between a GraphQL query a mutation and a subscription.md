<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> The three operation types differ in intent and execution guarantees. A **query** reads data: root fields may run in parallel and the document may omit the `query` keyword only here. A **mutation** writes data: it requires the `mutation` keyword, and its root fields execute **serially, in document order**. A **subscription** opens a long-lived stream: the root field's resolver returns a source event stream, and each event is executed like a query. Validation, arguments, fragments, and variables work identically across all three.

## One grammar, three execution contracts

The schema declares which root type backs which operation (`Query`, `Mutation`, `Subscription` by default; only `Query` is mandatory). The client picks the operation type by keyword — or by omission for queries, which is legal shorthand solely for reads. Everything below the root behaves the same: selection sets, fragments, aliases, directives ([[What is a GraphQL fragment]]). The differences are all at the root: concurrency for queries, ordered serial execution for mutations, and a source stream that feeds repeated executions for subscriptions ([[How do GraphQL subscriptions work over WebSockets]]).

```java
// graphql-java 26.1: mutation with two root fields, aliased c and d:
// mutation M($in: PostInput!) { c: createPost(input: $in) { id title }  d: deletePost(id: "p1") }
// console: RUN createPost title=Hello tags=[api]
//          RUN deletePost id=p1          <- document order, strictly serial
// result: {"data":{"c":{"id":"p42","title":"Hello"},"d":true}}
```

**Listing 1.** Verified on graphql-java 26.1: root mutation fields ran one after another in document order — the guarantee the spec adds for side-effecting operations.

```d2
direction: right
Q: "query\nroot fields in parallel" { width: 250; height: 70 }
M: "mutation\nroot fields serial,\nin document order" { width: 240; height: 80 }
S: "subscription\nstream of events,\neach executed as a query" { width: 250; height: 80 }
J: "JSON-ish transport\nPOST /graphql" { width: 230; height: 65 }
W: "WebSocket / SSE" { width: 200; height: 55 }
Q -> J
M -> J
S -> W
```

**Fig. 1.** Reads and writes usually ride request/response transports; subscriptions need a long-lived channel — an operational, not linguistic, difference.

> [!warning] Serial mutations are a convenience, not a transaction
> Serial root execution prevents *this operation's* root fields from racing each other — it does not give you database transactions across them, does not isolate them from other clients' mutations, and does not stop *nested* selections of different root fields from interleaving. Two clients issuing the same mutation concurrently still race server-side; idempotency and transactional boundaries remain your job ([[What is idempotency in HTTP and in messaging]]). And a "query" that secretly writes is a convention violation, not a language error — the spec's wording is about expectations, so servers that cache query results aggressively will misbehave ([[Why is HTTP caching harder with GraphQL than REST]]).

Subscriptions invert the lifecycle: the operation does not return once; the transport holds the request open, the root resolver subscribes to a source stream, and per event the engine re-runs the selection set — so each payload is shaped like a query response and errors per event land in that event's `errors` ([[Why does GraphQL often return HTTP 200 when a field errors]]).

> [!tip] Interview answer
> Query reads data and may run root fields in parallel — and is the only operation allowed to omit its keyword. Mutation writes: root fields execute serially in document order, which orders side effects but is not a transaction. Subscription holds a long-lived stream open: the root resolver returns an event source, and each event executes the selection set like a query. Below the root, all three share the same grammar and rules.

