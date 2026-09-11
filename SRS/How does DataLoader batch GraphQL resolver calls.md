<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> DataLoader batches and memoizes loads within one request: resolvers call `load(key)`, which **queues** the request and returns a promise; after the execution level finishes, DataLoader collects all queued keys and calls your **batch function once** with the distinct keys. The batch function must return values **in the same order as the keys**. Results are memoized per request — repeated keys resolve from cache without new work. One loader instance per request keeps the cache from leaking across users.

## The dispatch cycle, step by step

During a level, every `author` resolver calls `userLoader.load(post.authorId())` — nothing hits the store yet; each call registers a pending promise. When the level completes, the engine's dispatch hook flushes the queue: the batch function receives `[u1, u2, u3]`, fetches them in one query (an `IN (...)`, a `mget`, a mass lookup), and returns them positionally; DataLoader then completes each waiting promise. Children of those results resume, and the next level batches again ([[What is the N plus 1 problem in GraphQL]]).

```java
// graphql-java 26.1 + java-dataloader: one batch replaces per-parent fetches.
BatchLoader<String, User> batchLoader = keys -> {          // keys=[u1, u2, u3]
    List<User> ordered = new ArrayList<>();
    for (String k : keys) ordered.add(new User(k, USERS.get(k)));  // positional!
    return CompletableFuture.completedFuture(ordered);
};
DataLoader<String, User> userLoader = DataLoaderFactory.newDataLoader(batchLoader);
DataLoaderRegistry registry = new DataLoaderRegistry().register("userLoader", userLoader);
// author resolver: env.getDataLoader("userLoader").load(p.authorId());
// result of { posts { id author { name } } } for posts p1(u1) p2(u2) p3(u1) p4(u3):
// BATCH CALL keys=[u1, u2, u3]
// {"data":{"posts":[{"id":"p1","author":{"name":"Luke"}},{"id":"p2","author":{"name":"Leia"}},
//                    {"id":"p3","author":{"name":"Luke"}},{"id":"p4","author":{"name":"Han"}}]}}
```

**Listing 1.** Verified on graphql-java 26.1: four parents, one batch call, `u1` appearing once — queue, dispatch, positional results, memoized repeat.

```d2
direction: down
L: "load(u1) load(u2) load(u1) load(u3)\npromises queued" { width: 330; height: 70 }
D: "level ends -> dispatch" { width: 220; height: 55 }
B: "batch fn([u1,u2,u3])\none store call" { width: 250; height: 65 }
M: "memoize + complete promises\nchildren resume" { width: 290; height: 65 }
L -> D
D -> B
B -> M
```

**Fig. 1.** Queue at load time, dispatch at level end, one store call, positional completion — the whole batching cycle per execution level.

> [!warning] Two bugs account for most DataLoader incidents
> First: **order violation** — the batch function must return results matching key order; returning them sorted by id silently attaches wrong users to wrong posts, because positions, not keys, drive completion. If your store cannot promise order, reorder in code. Second: **cache lifetime** — a loader created once per *application* memoizes user A's ids for user B: per-request construction (or explicit per-request cache clearing) is mandatory in multi-tenant contexts ([[What is GraphQL execution context]]). A subtler third: batching only aligns **within a level** — deeply unbalanced resolvers that block before calling `load` shrink batches or serialize dispatch; keep resolvers thin and let the engine fan out ([[Why do GraphQL mutations run serially while queries can run in parallel]]).

Where dispatch happens: modern graphql-java integrates dispatch into execution — you supply the registry on the `ExecutionInput`; older setups used a dispatcher instrumentation. Spring for GraphQL wires it declaratively: `BatchLoaderRegistry` registrations become named loaders reachable from `@SchemaMapping` methods, with context propagation included ([[How would you explain Spring for GraphQL]]). Transport-level batching (arrays of operations in one POST) is a different optimization — it cuts HTTP overhead, not store calls ([[What are persisted queries in GraphQL]]).

> [!tip] Interview answer
> DataLoader turns per-field loads into per-level batches: load() queues keys and returns promises; at level end the batch function gets distinct keys once, must return values positionally, and each promise completes; repeats are memoized. Create the loader per request so caches never leak between users. In graphql-java you pass a DataLoaderRegistry on the execution input; Spring wires it via BatchLoaderRegistry.

