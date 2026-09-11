<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> The GraphQL flavor of N+1: a list field resolves N parents, and each parent's nested field runs its own resolver that fetches from the store — N parents produce **N additional fetches** (plus the original one). The selection structure makes this the default behavior, because nested fields execute per returned object, independently. The cure is batching: collect the N keys at one execution level and fetch them in a single call — which is exactly what DataLoader automates.

## Why the execution model produces it

The engine walks the selection tree per object: for each `Post` in `posts`, the `author` field's resolver runs with that post as source. If `author` does `store.getUser(post.authorId)`, ten posts cost ten independent user lookups — even though the engine resolved them "in parallel", the store sees ten queries ([[How does the GraphQL execution engine resolve a query]]). A REST handler would have written one JOIN; the GraphQL layer split the work into per-field resolvers, which is the price of composability ([[What is over-fetching and under-fetching compared with REST]]).

```java
// graphql-java 26.1: 4 posts, naive per-parent author fetch:
// posts resolver returns p1(u1), p2(u2), p3(u1), p4(u3);
// each author resolver would call store.getUser(authorId) -> 4 store calls.
// With DataLoader (next card), the whole execution produces ONE batch call:
// BATCH CALL keys=[u1, u2, u3]   <- 4 parents, 3 distinct keys, 1 fetch
```

**Listing 1.** Verified on graphql-java 26.1. The batch call received every key collected during the level — deduplicated and order-preserving — turning 4 fetches into 1 ([[How does DataLoader batch GraphQL resolver calls]]).

```d2
direction: down
P: "posts: [p1, p2, p3, p4]" { width: 250; height: 55 }
N: "naive: author resolver per post" { width: 310; height: 60 }
S1: "4 store lookups" { width: 190; height: 50 }
B: "batched: keys collected per level" { width: 310; height: 60 }
S2: "1 store call\nkeys=[u1,u2,u3]" { width: 220; height: 60 }
P -> N -> S1
P -> B -> S2
```

**Fig. 1.** Same schema, same operation: the naive per-parent walk multiplies fetches; batching collapses one execution level into a single keyed call.

> [!warning] N+1 has relatives that batching does not fix
> First: **HTTP-layer N+1** — clients issuing one operation per resource slice recreate the pattern at the network level; server batching cannot help ([[What is over-fetching and under-fetching compared with REST]]). Second: **depth-N+1** — `friends { friends { friends } }` repeats the problem per level; each level needs its own batched loader, and unbounded depth turns a fixed cost into an attacker-controlled one ([[How do you limit nested query depth in GraphQL]]). Third: the false economy of "solving" it with one giant root resolver that prefetches everything — that reintroduces over-fetching *inside* the server and defeats lazy selection ([[What is GraphQL execution context]]).

Interview framing matters: N+1 is not a GraphQL bug — it is the standard cost of moving join logic from a planner into application code, and the ecosystem's answer (per-request batching, `@BatchMapping` in Spring) is mature. What *is* unforgivable is discovering it in production load tests: field-usage analytics and tracing per resolver make the multiplication visible early ([[What is query complexity analysis in GraphQL]]).

> [!tip] Interview answer
> GraphQL N+1: a list field resolves N parents and each nested field's resolver fetches per parent — N extra store calls per level. It follows from per-object field execution, not from a bug. Fix it with batching: collect keys at one level and fetch once — DataLoader does this per request; deduplication and ordering come free. Watch list-plus-nesting depth and per-client HTTP N+1, which batching alone does not cover.

