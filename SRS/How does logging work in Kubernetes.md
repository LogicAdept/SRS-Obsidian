<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How does logging work in Kubernetes

> [!abstract] Short answer
> The cluster-native contract is deliberately thin: container stdout and stderr are captured by the container runtime to files **on the node**, and `kubectl logs` reads them — that is all Kubernetes guarantees, and logs vanish with the pod and the node. Anything beyond one node, one lifecycle — search, retention, cross-node correlation — is your architecture: a **node-level agent** (usually a DaemonSet) tails the log files and ships them to a store (Elasticsearch/OpenSearch, Loki, a cloud service). Sidecar-based shipping exists for special cases; application-side shipping directly to a sink is the fallback.

## The node is the log unit

The kubelet tells the runtime to write each container's streams into `/var/log/containers`-adjacent files with rotation (size-capped, typically 10 MiB × 5 files via kubelet config — old files simply fall off). `kubectl logs` is a node-local read; `--previous` reads the dead-but-recently-alive attempt ([[How do you debug a Pod that fails to start]] — that flag is the single most useful log tool). Because storage is per-node and per-lifecycle, rescheduling or node loss orphans logs — the reason the standard answer to "how do you get central logs" is a **node agent**: Fluent Bit / Fluentd / Vector as a DaemonSet ([[What is a DaemonSet in Kubernetes]]), reading the runtime's files directly, enriching each line with pod/namespace/labels metadata from the API, and shipping onward. The node-file design has a real virtue: the agent is completely decoupled from the app — no SDK, no config per service — and one agent's resource bill serves the whole node.

The Java nuance everyone trips on: your framework logs *structured, multi-line* records — a stack trace is many physical lines. The agent sees raw lines, so multi-line reassembly (or JSON-per-line logging from the app, e.g. Logback/Log4j2 encoders) must happen somewhere deliberate, or dashboards count stack traces as a thousand error events ([[How do you view logs of a running Java process]] is the single-host version of the same problem).

```d2
direction: right
c1: "pod A container" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
c2: "pod B container" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
files: "runtime log files\non the node, rotated" {
  width: 270
  height: 90
  style.fill: "#e3f2fd"
}
kubectl: "kubectl logs\nnode-local read" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
agent: "DaemonSet agent\nenrich + ship" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
store: "central store\nLoki / Elasticsearch" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
c1 -> files
c2 -> files
files -> kubectl
files -> agent -> store
```

**Fig. 1.** One file set, two consumers: kubectl serves humans at the node; the node agent serves the central store — neither touches the application.

> [!warning] kubectl logs is not a logging strategy
> The traps: treating `kubectl logs` as retention — rotation silently eats history, and deleted pods take their logs with them permanently. Appending to files *inside* the container "because log4j is configured that way" — Kubernetes captures streams, not files, so that output exists nowhere (unless you also tail it to stdout). Relying on timestamps across nodes without clock discipline. And multi-line stack traces shredded into events — the dashboards lie quietly. System component logs (`kube-system`) follow the same node-file mechanics and are often the actual clue.

> [!tip] Interview answer
> Kubernetes itself only does node-local capture: the runtime writes container stdout and stderr to rotated files on the node, and kubectl logs reads them — with --previous for the last dead attempt; nothing more survives pod or node death. Central logging is an architecture: a DaemonSet agent per node tails those files, enriches lines with pod metadata from the API, and ships to Loki or Elasticsearch; sidecar shippers and app-direct shipping are the exceptions. Java-specifically, ship JSON-per-line or configure multi-line handling, or every stack trace becomes a thousand log events.
