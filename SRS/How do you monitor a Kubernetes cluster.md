<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How do you monitor a Kubernetes cluster

> [!abstract] Short answer
> Monitoring splits into layers: **node and container metrics** (cAdvisor inside the kubelet exposes per-container CPU, memory, network; metrics-server scrapes and serves them to the platform — that is what powers `kubectl top` and the HPA), **cluster-state metrics** (kube-state-metrics renders object truth — desired vs available replicas, pod restarts, PVC status — as metrics), and the **control plane itself** (API server latency and errors, scheduler throughput, etcd disk latency and quorum health). The standard stack: **Prometheus** pulls all of it, Grafana visualizes, Alertmanager routes; `kubectl get events` and `kubectl describe` remain the zero-setup triage tools.

## Metrics plumbing: who measures what

The measurement chain explains the capabilities: the kubelet embeds cAdvisor, which reads cgroups for real usage — every container's CPU seconds, working-set memory, network counters ([[How do resource requests and limits work in Kubernetes]] — usage is also what eviction decisions read). **metrics-server** aggregates that per node and serves the Metrics API in-cluster: cheap, ephemeral (no history), enough for `kubectl top` and autoscaling. Prometheus is the retention and query layer: it scrapes metrics endpoints — kubelet, node-exporter DaemonSets for host stats, kube-state-metrics for object state, control-plane components' own `/metrics` — and keeps history your alerts and dashboards need ([[What is a DaemonSet in Kubernetes]] — node exporters are the textbook DaemonSet). kube-state-metrics deserves the interview mention: it converts the *API object state* (Deployment desired 3, ready 2) into metrics — information no cgroup can see. Control-plane monitoring is what separates senior answers: etcd fsync latency and leader changes, apiserver p99 and 5xx rates, scheduler queue depth — the failure modes that explain "everything is slow" before "everything is down".

Events and logs complete the picture: the Events API records scheduling, probe, and lifecycle transitions ([[How do you debug a Pod that fails to start]]), and node logs ship via the logging stack ([[How does logging work in Kubernetes]]).

```d2
direction: right
kubelet: "kubelet + cAdvisor\ncontainer usage (cgroups)" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
ms: "metrics-server\nkubectl top, HPA" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
ksm: "kube-state-metrics\nobject state as metrics" {
  width: 290
  height: 90
  style.fill: "#e3f2fd"
}
prom: "Prometheus\nscrape + store + alert" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
graf: "Grafana / Alertmanager" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
cp: "control plane metrics\napiserver, etcd, scheduler" {
  width: 290
  height: 90
  style.fill: "#ffebee"
}
kubelet -> ms
kubelet -> prom
ksm -> prom
cp -> prom
prom -> graf
```

**Fig. 1.** Two consumption paths from one measurement plane: metrics-server serves the platform's internal consumers; Prometheus serves humans and history.

> [!warning] Metrics are not SLOs and metrics-server is not Prometheus
> The traps: `kubectl top` shows *requests-relative* usage snapshots — treating it as a capacity history misleads, because metrics-server keeps no history at all. Monitoring pods but not the control plane — etcd latency degradation masquerades as "flaky deploys" for weeks. Alerts on raw CPU instead of the service's latency and error rate — the dashboard is green while the users are not. And node pressure (memory, disk) as an afterthought — kubelet eviction is a monitoring event you want before it fires ([[How do you monitor a Kubernetes cluster]] and its alerting both read the same sources).

> [!tip] Interview answer
> Layered: cAdvisor inside each kubelet reads cgroup usage; metrics-server aggregates it for kubectl top and the HPA; kube-state-metrics exposes object state — desired versus ready, restarts, claims; node-exporter covers host metrics; control-plane components expose their own endpoints, with etcd and apiserver latency being the early-warning tier. Prometheus scrapes and stores all of it, Grafana visualizes, Alertmanager routes — and events plus describe remain the fastest triage. The senior part is knowing metrics-server has no history, and that SLO-shaped alerts beat CPU-shaped alerts.
