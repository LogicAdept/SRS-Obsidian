<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is the difference between a process and a connection in PostgreSQL?

> [!abstract] Short answer
> A connection is a client's TCP or Unix-socket session to the server; a process is the server-side backend (forked from `postgres`) that serves exactly that one connection for its whole lifetime. PostgreSQL has no shared multi-threaded gateway: one connection costs one operating-system process with its own memory, so connections are the expensive resource that poolers multiplex.

## The process-per-connection model

The `postgres` server process listens for clients; on each new connection it forks a fresh backend process. From then on the client talks to that backend until disconnect. Each backend carries private memory: work areas for sorts and hashes (work_mem), catalog caches, and execution state — megabytes before any query runs. `max_connections` (default 100) is a hard ceiling on backends, plus fixed auxiliary processes (checkpointer, background writer, WAL writers, autovacuum workers).

```d2
postmaster: "postgres (postmaster)\nlistens, forks" {width: 260; height: 80}
b1: "Backend process\nconnection 1" {width: 220; height: 70}
b2: "Backend process\nconnection 2" {width: 220; height: 70}
b3: "Backend process\nconnection N (max 100)" {width: 250; height: 70}
postmaster -> b1: "fork per connection"
postmaster -> b2
postmaster -> b3
```

**Fig. 1.** There is no thread pool inside PostgreSQL: concurrency equals the number of backend processes, and each one is isolated.

## What one backend carries

Besides executing queries, each backend holds catalog caches (schema, type and operator lookups), private work areas for sorts and hashes ([[What are shared_buffers and work_mem in PostgreSQL]]), and session state: GUC settings, prepared statements, LISTEN registrations, advisory locks. Fixed auxiliary processes (checkpointer, background writer, WAL writers, autovacuum workers) add to the process count regardless of client load. This footprint is why an idle connection is never free, and why storms of them degrade latency before CPU saturates.

Compare the model honestly with thread-per-connection or shared-worker engines: process isolation is crash-safe and simple to reason about — one misbehaving backend cannot corrupt another's memory — and the scheduling reality changes only when pooling changes the multiplexing ([[What are database connection pools for]] covers the application-side equivalent). The design is a deliberate trade of memory for robustness, not an oversight to be fixed by raising max_connections.

## Why the distinction matters in production

- Memory math: dozens of concurrent complex sorts multiply work_mem across backends ([[What are shared_buffers and work_mem in PostgreSQL]]); "100 connections, each 4 MB work_mem, several sort nodes each" is how OOMs happen.
- Context switching and scheduler overhead grow with thousands of processes; queries themselves are not the only cost.
- Session state (SET, LISTEN, prepared statements, advisory locks) lives in that one process, which is why [[What is LISTEN NOTIFY in PostgreSQL]] and session advisory locks ([[What are advisory locks in PostgreSQL]]) break under transaction-pooling.
- The standard fix is a pooler ([[Why use pgBouncer with PostgreSQL]]): many client connections multiplexed over few server connections. The related existing card [[What are database connection pools for]] covers the application side.

> [!warning] Raising max_connections is the classic wrong fix
> "Too many connections — raise max_connections to 1000" multiplies backend memory and scheduler load and usually makes latency worse. The durable fix is pooling plus shorter transactions; only then tune the limit upward modestly.

> [!tip] Interview answer
> In PostgreSQL a connection maps one-to-one to a forked backend process with its own memory — there is no shared server thread. That makes connections expensive: memory per process, scheduler pressure at scale, and session state pinned to one process. Poolers like pgBouncer multiplex many client connections over few backends, in transaction or session mode.
