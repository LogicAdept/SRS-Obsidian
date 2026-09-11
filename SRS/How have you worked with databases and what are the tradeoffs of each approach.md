<!--
reps: 0
priority: 0
-->
#Career/Experience #SystemDesign/Tradeoffs #SRS

# How have you worked with databases and what are the tradeoffs of each approach

> [!abstract] Short answer
> This interview question is answered with a structured personal inventory: the database families you have actually used (relational, document, key-value, analytical), one concrete system per family (workload, scale, why that engine), and the tradeoffs you personally hit — consistency versus availability, schema discipline versus flexibility, joins versus denormalization. The winning shape is specific stories with numbers and decisions, not a feature-list comparison recited from a blog.

## Structuring the answer: inventory, story, tradeoff

First, the inventory in one breath: engines grouped by family with your depth honestly stated (relational: PostgreSQL/MySQL daily driver; document: MongoDB on one project; key-value: Redis as cache/session tier; analytical: ClickHouse for events). Second, one story per family with its numbers — "orders service on PostgreSQL: ~2k writes/s peak, p95 40 ms, we hit a JOIN wall on the reporting queries and built a denormalized read table refreshed via outbox events" carries more signal than any taxonomy. Third, the tradeoffs told as decisions you made and their aftermath — that is what the interviewer is actually probing: whether you have felt the consequences, not whether you can recite them. The tradeoff map to draw from: relational gives transactions, joins and constraints at the cost of schema migrations and vertical-first scaling ([[What are the ACID properties of database transactions]], [[How do NoSQL databases scale compared with SQL databases]]); document gives shape-flexible aggregates at the cost of cross-document joins moving to code ([[How would you explain tradeoffs among relational document and other database types]]); key-value gives speed at the cost of query expressiveness; analytical engines give scan throughput at the cost of point-update cost. [[When should you use NoSQL and when should you use SQL]] is the general decision card — your job here is to attach personal evidence to it.

```text
answer skeleton (~90 seconds):
1 inventory : "mostly PostgreSQL/MySQL, Redis for cache/session,
               MongoDB once, ClickHouse for analytics"
2 one story : workload + scale + one decision per engine
3 tradeoffs : "we chose X for Y, it cost us Z, here is what I'd do again"
4 takeaway  : "my default is relational until a measured reason says otherwise"
```

**Listing 1.** The 90-second shape: inventory, story, tradeoff, default.

## The follow-ups to be ready for

Interviewers dig one level past the story: "why that engine over the obvious alternative?" (need the rejected option and its reason — not fashion), "what went wrong?" (a real failure: a migration, a lock storm, a cache stampede — [[What difficulties arise when working with caching]], [[How do you identify slow or non-performant SQL queries]] are the technical depths behind the common ones), "how did you handle schema changes?" (migrations, backwards compatibility, [[How do you alter a table in a relational database]]-level mechanics), and "what would you do differently?" (the reflective close — naming a tradeoff you would now take the other side of is a credibility gain, not a weakness). The preparation discipline: before the interview, write down for each engine one workload, one number, one decision, one regret. [[What architecture did you use on past projects]] is the sibling question at the architecture level — the same story-first discipline applies, and the two answers should not contradict each other.

> [!warning] A feature list is not experience
> Reciting engine capabilities ("MongoDB is document-oriented, Redis is in-memory") answers a question nobody asked and signals none. Every claim needs a project attached; every tradeoff needs a consequence you lived with — otherwise the answer reads as documentation, not experience.

> [!tip] Interview answer
> I structure it as inventory, stories, tradeoffs: relational as my daily driver with concrete scale numbers, Redis for cache/session tiers, one honest project each for document and analytical engines — then the tradeoffs I personally hit (JOIN walls, migration pain, cache staleness) and what I decided. My stated default: relational until a measured reason says otherwise.
