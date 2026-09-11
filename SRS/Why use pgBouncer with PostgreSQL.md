<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# Why use pgBouncer with PostgreSQL?

> [!abstract] Short answer
> Because every PostgreSQL connection is a backend process with its own memory ([[What is the difference between a process and a connection in PostgreSQL]]), thousands of application connections exhaust RAM and scheduler capacity long before they exhaust CPU. pgBouncer is a lightweight pooler (~2 kB per client connection) that multiplexes many clients over few real server connections — session, transaction, or statement pooling — and adds online restart without dropping clients.

## Pooling modes

| Mode | Server connection held | Breaks |
|---|---|---|
| session | whole client session | nothing (least effective) |
| transaction | one transaction only | session features: SET, LISTEN/NOTIFY, session advisory locks, (pre-1.21) prepared statements |
| statement | single statement | multi-statement transactions entirely |

```d2
apps: "Hundreds of app connections" {width: 320; height: 70}
pb: "pgBouncer\nauth, pool per db/user,\n~2 kB per client" {width: 300; height: 90}
srv: "PostgreSQL\nmax_connections backends\n tens, not thousands" {width: 340; height: 90}
apps -> pb -> srv: "multiplexed"
```

**Fig. 1.** The multiplexer sits on the wire; the database sees a stable, small backend count.

## What transaction pooling costs you

Session state is bound to a server process ([[What is LISTEN NOTIFY in PostgreSQL]] — LISTEN needs a dedicated connection; [[What are advisory locks in PostgreSQL]] — session-level locks break; SET/GUCs leak across users). The adaptations: per-transaction SET LOCAL, transaction-level advisory locks, application-side statement caching against the pooler (pgBouncer gained protocol-level prepared statement support in 1.21 with max_prepared_statements). None of this is exotic — it is the standard cost of the throughput win.

## Operational settings that matter

- `default_pool_size` / `max_client_conn`: the real concurrency budget is server-side connections, not clients.
- `server_reset_query` (session mode) restores clean state per client handover; transaction mode relies on server_reset_query_always and DISCARD ALL discipline being unneeded.
- `pool_mode = transaction` is the default recommendation for OLTP fleets; session mode for services needing session features.
- PgBouncer also smooths failovers: clients point at the pooler; the pooler's target moves ([[What is the difference between streaming and logical replication in PostgreSQL]] — promotion day).

The application-side view of pooling (why pools exist in JDBC drivers too) is in [[What are database connection pools for]]; the deeper connection-cost mechanics in [[What are shared_buffers and work_mem in PostgreSQL]].

> [!warning] A pooler is not a license to keep connections open forever
> pgBouncer makes idle clients cheap, but an application holding a transaction open across a user think still pins a server backend and the vacuum horizon ([[Why do long-running transactions hurt PostgreSQL]]). Pooling fixes connection count; transaction hygiene fixes holding time — both are required, and neither substitutes for the other.

> [!tip] Interview answer
> PostgreSQL pays a process per connection, so connection storms eat memory and max_connections. pgBouncer multiplexes hundreds of clients over tens of backends at about 2 kB per client. Transaction mode gives the best ratio but breaks session state — SET, LISTEN, session advisory locks — so code adapts with per-transaction state or dedicated sessions where needed.
