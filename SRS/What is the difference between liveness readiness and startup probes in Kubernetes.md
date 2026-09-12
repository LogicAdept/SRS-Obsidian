<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is the difference between liveness readiness and startup probes in Kubernetes

> [!abstract] Short answer
> Three probes, three reactions from the kubelet. **Liveness** answers "is the process alive?" — failure means the container is **restarted**. **Readiness** answers "should this pod receive traffic?" — failure removes it from Service endpoints but restarts nothing. **Startup** answers "is the app still booting?" — it gates the other two and gives slow-starting applications a grace window so liveness does not kill them mid-boot.

## The three contracts

The kubelet executes each probe against the container — `httpGet`, `tcpSocket`, `exec`, or `grpc` — on a schedule (default `periodSeconds: 10`, `timeoutSeconds: 1`, `failureThreshold: 3`) and reacts by the probe's role. Liveness failure trips the container's restart policy: the process dies and restarts, in-pod, forever if the cause persists. Readiness failure is purely a routing statement: the pod stays up, stays visible in `kubectl get pods`, but drops out of the endpoints of every Service selecting it — traffic stops until it passes again, which is what makes deployments, load spikes, and dependency brownouts survivable ([[How do you perform a rolling update and rollback in Kubernetes]] leans on exactly this). Startup probes are an ordering rule: while the startup probe has not succeeded once, liveness and readiness are simply not run; after `failureThreshold × periodSeconds` without success (30 × 2s-style budgets), the container is killed and the restart loop begins. The defaults matter: without a startup probe, a JVM app that needs 90 seconds to boot dies at its first liveness check — the pre-startup-probe workaround, an inflated `initialDelaySeconds`, still shows up in old YAML and is the interviewer's favorite archaeology question ([[How do you implement Kubernetes probes with Spring Boot]] maps them onto Actuator endpoints).

```yaml
startupProbe:
  httpGet: { path: /, port: 8080 }
  failureThreshold: 30
  periodSeconds: 2
readinessProbe:
  httpGet: { path: /, port: 8080 }
  periodSeconds: 5
livenessProbe:
  httpGet: { path: /, port: 8080 }
  periodSeconds: 10
  failureThreshold: 3
```

**Listing 1.** The canonical trio from the empirics manifest (`scripts/empirics/kubernetes/probe-pod.yaml`): one minute of startup budget (30 tries × 2s) before liveness ever fires, then a 10-second liveness cadence and a 5-second readiness cadence on the same endpoint.

```d2
direction: right
boot: "container starts" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
startup: "startup probe runs\nliveness/readiness paused" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
live: "liveness fails\ncontainer restarted" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
ready: "readiness fails\nremoved from endpoints only" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
ok: "all passing\ntraffic flows" {
  width: 210
  height: 90
  style.fill: "#e8f5e9"
}
boot -> startup
startup -> ok: "first success"
startup -> boot: "budget spent\nrestart"
ok -> live
ok -> ready
live -> ok: "recovers"
ready -> ok: "recovers"
```

**Fig. 1.** Same check types, different consequences: restart the container (liveness), withdraw from routing (readiness), or hold both back until boot completes (startup).

> [!warning] Liveness is not a health endpoint you visit once
> The recurring traps: a liveness probe checking **dependencies** — the database hiccups, every pod fails liveness, and the cluster restarts the entire application tier on top of a database problem (dependency checks belong to readiness, if anywhere). A probe heavier than `timeoutSeconds: 1` default can fail spuriously under load. And the inverse trap: no readiness probe at all, so a pod joins endpoints the instant its process listens — before caches warm or migrations finish.

> [!tip] Interview answer
> All three probes are kubelet checks with the same shapes — HTTP, TCP, exec, gRPC — but different reactions. Liveness failure restarts the container; readiness failure just pulls the pod from Service endpoints; startup gates the other two until it succeeds once, giving slow boots a kill-budget instead of the old initialDelaySeconds hack. Design rule: liveness must be dependency-free and cheap, readiness carries the dependency and warmup truth. Spring Boot ships dedicated actuator liveness and readiness endpoints for exactly this split.
