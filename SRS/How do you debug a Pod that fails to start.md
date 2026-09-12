<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How do you debug a Pod that fails to start

> [!abstract] Short answer
> Read the pod status, and the status names the failure class: **Pending** — the scheduler cannot place it (no capacity, unsatisfiable affinity, taints, PVC not bound); **ImagePullBackOff** — the image cannot be fetched (name wrong, no auth, rate limit, no network); **CrashLoopBackOff** — the container starts and dies repeatedly (app bug, bad config, OOMKilled); **OOMKilled** — memory limit exceeded. The tooling order is `kubectl describe pod` (events tell the story) → `kubectl logs --previous` (the dead container's stdout) → `kubectl exec` for the living ones, with `kubectl get events --sort-by=.lastTimestamp` as the cluster-wide timeline.

## Pending: the scheduler said no

A pod stuck in Pending was accepted by the API server but never bound. `kubectl describe pod` surfaces the exact sentence: `Insufficient cpu` (requests exceed any node's allocatable — lower requests or add nodes), `node(s) had untolerated taint` (control-plane taints or a drained node), `node(s) didn't match Pod's node affinity/selector`, or an unbound PersistentVolumeClaim ([[What are PersistentVolumes PersistentVolumeClaims and StorageClasses in Kubernetes]] — storage topology is a scheduling input). Pending with a cluster autoscaler installed often just means "wait for the node" ([[How does Kubernetes scheduling work]] is the decision machinery behind the message).

## ImagePullBackOff and CrashLoopBackOff: different layers lie differently

ImagePullBackOff is a registry-layer failure: the kubelet's pull attempts fail with exponential backoff, and `describe` prints the precise cause — `manifest unknown` (tag wrong), `unauthorized` (pull secret missing — `imagePullSecrets`), `toomanyrequests` (Docker Hub rate limits) — the message names the layer, so do not debug the app when the name is wrong. CrashLoopBackOff is the app *starting and dying*: the container runs, exits non-zero, kubelet restarts it with backoff (10s, 20s, 40s... capped at 5 minutes — that is the loop you watch). The money command is `kubectl logs pod -c container --previous` — the output of the *dead* attempt; pair it with `describe`'s exit code: 1 (app error), 137 (SIGKILL — OOMKilled if reason agrees, otherwise an external kill), 126/127 (command/exec problems), 0 (container "completed" — a wrong ENTRYPOINT story for a server). Config errors land here too — a bad env value, missing ConfigMap key (optional keys are empty, required missing ones block container start with CreateContainerConfigError). A `startupProbe` failing its budget produces this loop without any app log line — check probe config before blaming the code ([[What is the difference between liveness readiness and startup probes in Kubernetes]]).

```d2
direction: right
p: "pod not behaving" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
desc: "kubectl describe pod\nread events + exit code" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
pend: "Pending\ncapacity, taints, affinity, PVC" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
pull: "ImagePullBackOff\nname, auth, rate limit" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
loop: "CrashLoopBackOff\nlogs --previous, exit 137 = OOM" {
  width: 330
  height: 90
  style.fill: "#ffebee"
}
ok: "Running but odd\nexec, logs, port-forward" {
  width: 270
  height: 90
  style.fill: "#e8f5e9"
}
p -> desc
desc -> pend
desc -> pull
desc -> loop
desc -> ok
```

**Fig. 1.** The triage tree: the status word picks the layer — scheduler, registry, or container runtime — and each layer has its own one-command tell.

> [!warning] The status is a summary, not a diagnosis
> The traps: `CrashLoopBackOff` hides *why* — people debug the backoff instead of reading the previous container's logs; `restartPolicy: Always` masks a config bug by looping forever. Exit 137 without the OOMKilled reason is a kill, not a crash — check who sent the signal ([[What is the PID 1 problem in Docker containers]] is the container-runtime twin of this confusion). And `kubectl logs` on a pod whose container never started returns nothing — that is not "no logs", that is the wrong layer; `describe` events are the only witness.

> [!tip] Interview answer
> I triage by status word. Pending means the scheduler refused: describe shows the exact sentence — insufficient CPU, taints, affinity, unbound PVC. ImagePullBackOff is registry-side: wrong tag, missing pull secret, rate limit — describe quotes the pull error. CrashLoopBackOff means the container runs and dies: logs with --previous for the dead attempt's output, describe for the exit code — 137 means OOMKilled, 1 is app error, 0 means it exited like a batch job. describe, logs --previous, exec, and events cover ninety percent; the status is a class, the events are the diagnosis.
