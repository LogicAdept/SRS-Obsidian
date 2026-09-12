<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker/Compose #SRS

# How does depends_on work in Docker Compose

> [!abstract] Short answer
> `depends_on` controls **start and stop order**, not readiness. Compose starts dependency containers before dependents, but "started" only means the container is running — a Postgres that is still initializing has already satisfied plain `depends_on`. Real readiness requires a `healthcheck` on the dependency plus `condition: service_healthy`.

## Order is not readiness

The classic failure: app starts, connects to `db:5432`, gets connection refused, crashes — because Compose kept its end of the deal (db container running) while the database inside was still in recovery. The fix is declaring what "ready" means:

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres:18
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Listing 1.** Three conditions exist: `service_started` (default — container running), `service_healthy` (dependency's healthcheck green), and `service_completed_successfully` (a one-shot job finished with 0). Configuration shape per the Compose reference — not executed here.

```d2
direction: right
db: "db\npostgres:18" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
hc: "healthcheck\npg_isready every 10s" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
w: "web\ndepends_on: service_healthy" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
db -> hc -> w: "starts only when healthy"
```

**Fig. 1.** The readiness chain: the healthcheck defines healthy, the condition gates the dependent on it.

Compose also stops in dependency order, so shutdowns walk the graph the reverse way. `restart: true` on a dependency makes Compose restart it if it dies while a dependent is running — a lifecycle nicety plain `depends_on` never had.

> [!warning] depends_on is not a readiness probe, and healthchecks are not liveness probes
> Two levels of the same trap. Inside Compose, `depends_on` without a condition only sequences container creation — the app-level retry/backoff for the DB connection is still your job for the "ready but then overloaded" window. And a Compose `healthcheck` is a *startup gate* here, not continuous supervision: in Kubernetes that role belongs to probes ([[What is the difference between liveness readiness and startup probes in Kubernetes]]) — and there `depends_on` does not exist at all; ordering is replaced by init containers and retry loops ([[What is Kubernetes]] frames the platform difference).

> [!tip] Interview answer
> **depends_on sequences start/stop; it does not wait for readiness. To gate on actual readiness you define a healthcheck on the dependency and set condition: service_healthy; service_completed_successfully gates on one-shot jobs. Without a condition you only know the container is running — connection retries remain the app's responsibility.**

