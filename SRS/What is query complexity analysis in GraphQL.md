<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Query complexity analysis estimates **how much work a document can cause** before executing it: each field carries a weight, list fields multiply by their `first`/`limit` arguments, and the engine sums the tree — rejecting operations above a configured budget (often returning the estimated cost so clients can adapt). It complements depth limiting: depth counts nesting blindly, complexity prices breadth, fan-out, and argument-driven multiplication — the actual shape of GraphQL work.

## The pricing model

A complexity function walks the AST with schema knowledge. Baseline rules that model reality: object fields add their own weight plus their children's; **list fields multiply the subtree cost** by the requested page size (`first: 100` on `friends` means up to 100 executions of everything nested below); fields known to hit expensive backends get custom weights; introspection selections get their own (non-trivial) price ([[What is GraphQL introspection]]). The budget is a server knob: reject outright, or degrade gracefully with a `cost` in extensions and strict throttles above thresholds ([[Why is rate limiting harder in GraphQL than REST]]).

```graphql
# cost = 3 (user) + 3 * first? { friends } subtree
# { user { friends(first: 50) { friends(first: 50) { name } } } }
# naive model: user(3) + friends(50 x (3 + friends(50 x 1))) -> thousands of units
# the multiplication, not the nesting, is what makes the document expensive
```

**Listing 1.** The pricing intuition: two-level fan-out at 50 turns a four-field document into a workload costing thousands of field resolutions — the case depth limits alone miss ([[What is the N plus 1 problem in GraphQL]]).

```d2
direction: down
Doc: "document AST" { width: 190; height: 55 }
W: "walk with schema:\nweights + list multipliers" { width: 300; height: 65 }
S: "sum vs budget" { shape: oval; width: 180; height: 50 }
Ok: "execute" { width: 130; height: 50 }
Rej: "reject with cost\n(before any resolver)" { width: 280; height: 65 }
Doc -> W -> S
S -> Ok: "under"
S -> Rej: "over"
```

**Fig. 1.** Static analysis before execution: the estimate comes from the AST and schema alone, so rejection costs the server nothing.

> [!warning] Estimates are estimates — and budgets are policy, not physics
> First: the calculator cannot know data-dependent cost — a resolver's real price varies with arguments, hot caches, and store behavior; weights are calibrated approximations, so tune them against field-level metrics rather than trusting defaults ([[What is GraphQL execution context]]). Second: complexity checks are **bypassable in spirit** — a client splitting one huge document into ten small ones defeats per-request budgets unless you also rate-limit by token and monitor per-user cost over time ([[Why is rate limiting harder in GraphQL than REST]]). Third: do not conflate complexity with depth: a flat document selecting 200 scalar fields is cheap per field but heavy in serialization, while depth-3 with wide fan-out can be catastrophic — mature setups run both limits plus timeouts and pagination caps ([[How do you limit nested query depth in GraphQL]]).

Tooling note: graphql-java ships `MaxQueryComplexityInstrumentation` alongside its depth counterpart, both AST-based and pre-execution; persisted-query deployments get the strongest variant — allowlisted documents with **known** costs — which converts analysis from a gate into a build-time check ([[What are persisted queries in GraphQL]]).

> [!tip] Interview answer
> Complexity analysis prices a document statically: field weights, list multipliers by requested page size, subtree sums — reject over budget before executing. It catches breadth and fan-out that depth limits miss, though estimates need calibration against real resolver costs, and per-request budgets must be paired with token-level throttles. graphql-java ships MaxQueryComplexity instrumentation; persisted queries make costs known at deploy time.

