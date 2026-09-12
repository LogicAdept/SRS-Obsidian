<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Monolith #Patterns/Architecture/Microservices/ArchitecturalStyle #SRS

# What is monolithic architecture and when does it make sense

> [!abstract] Short answer
> Monolithic architecture: the application is one deployable unit containing all subdomains, working against one database - a Java WAR on Tomcat is the canonical example. All operations are local: ACID transactions, simple calls, one pipeline. It is the right first choice for most products; its costs - coordination-heavy teams, slow builds, one tech stack - grow with the size of the application and the number of teams, not with the code alone.

## Mechanism: one component, all subdomains, local everything

The definition is deployability, not code style: however modular the source tree, the application is built, tested and deployed as a single executable component over a single database. The trade has two force families. The dark energy forces push toward decomposition: simple components (small is understandable), team autonomy, fast deployment pipelines, multiple technology stacks, and segregating subdomains by characteristics - scaling, availability, security - independently. The dark matter forces push toward the monolith: simple interactions (a local call beats a distributed one), efficient interactions (no network round trips, no large transfers), ACID over BASE (a database transaction beats a saga), minimal runtime coupling and minimal design-time coupling. The monolith resolves the dark matter forces perfectly - everything is local: one transaction spans order and inventory trivially, refactoring crosses module borders freely, one pipeline builds one thing. What it cannot resolve is the dark energy set as scale grows: all teams share one codebase and one release train; the build and test loop slows with the codebase; the single tech stack fits every subdomain equally well or equally poorly; and a memory-hungry batch module forces the whole application to scale.

```d2
direction: right
app: "Monolithic application
all subdomains, one deployable" {style.fill: "#e8f5e9"}
ui: "UI" {style.fill: "#eceff1"}
ord: "Orders module" {style.fill: "#eceff1"}
inv: "Inventory module" {style.fill: "#eceff1"}
bil: "Billing module" {style.fill: "#eceff1"}
db: "One database" {style.fill: "#fff3e0"}
app -> ui
app -> ord
app -> inv
app -> bil
app -> db: single ACID transaction scope
```

**Fig. 1.** One deployable over one database: every interaction local, every transaction ACID - and every team in one build.

## When it makes sense - and the exit path

The honest engineering answer: by default. A new product with a small team gets to market faster with a well-modularized monolith - the architecture that maximizes simple interactions and ACID simplicity while the product's shape is still being discovered. Microservices are justified when the dark energy costs dominate: many teams tripping over each other in one release train, subdomains with genuinely divergent scaling or availability needs, and enough operational maturity to run distributed systems. Scale the decision to the organization, not to fashion. And the modern framing: the monolith is also the most common starting point of a migration, where [[What is the strangler fig pattern and when do you use it]] extracts services incrementally rather than in a big-bang rewrite - the monolith's modular internal structure determines how painful that extraction will be, so module boundaries deserve real care even in a monolith destined to stay one ([[What advantages do microservices have over a monolith]] is the comparison card from the other side).

> [!warning] Modular monolith or mud
> A monolith without enforced module boundaries is a distributed-systems-free path to the same pain: every module reaches into every database table, and extracting anything later means untangling decades of accidental coupling. If you choose the monolith, keep the modules honest - internal APIs, separate schemas, architecture tests that fail on cross-module imports. The opposite trap: microservices cosplaying as a monolith - a dozen services sharing one database and deploying in lockstep, which has the costs of both architectures and the benefits of neither.

> [!tip] Interview answer
> A monolith is one deployable unit holding all subdomains over one database - a WAR on Tomcat. Everything is local: ACID transactions, cheap calls, one pipeline, which is why it is my default for a new product with a small team. Its costs are organizational - one release train, one codebase, one stack - and they grow with team count, not code size. I keep modules strictly separated so that if we outgrow it, strangler-fig extraction stays feasible.
