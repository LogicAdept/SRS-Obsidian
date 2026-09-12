<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What happens when you run kubectl run in Kubernetes

> [!abstract] Short answer
> Modern `kubectl run` creates **exactly one Pod** — nothing else. The name is misleading by history: before Kubernetes 1.18 it generated a Deployment with `--replicas`, and that behavior was removed so the command has one predictable meaning. Today the pod is POSTed to kube-apiserver as a plain Pod object, gets scheduled like any other, and if it dies it stays dead, because no controller owns it. Anything that needs replicas, self-healing, or rollouts is a job for a Deployment, not for `run`.

## The single-pod contract

`kubectl run demo --image=nginx` builds a Pod object ([[What is a Pod in Kubernetes]]) locally — container, default `restartPolicy: Always`, the image — and submits it. The API server validates and persists it, the scheduler binds it to a node, and the kubelet starts the container. That is the whole story: no ReplicaSet is watching, so a node failure or a killed container ends the object's lifecycle after the container restart policy is exhausted on that node — rescheduled nowhere. Flags make the pod slightly more usable (`--rm` to clean up on exit, `-it` for interactive terminals, `--env`, `--restart=Never` for batch-style one-shots), but none of them changes ownership. The removal of `--replicas` is verifiable on any modern client — the flag simply no longer exists ([[What is the difference between a Deployment and a ReplicaSet in Kubernetes]]).

```bash
./kubectl run demo --image=nginx --replicas=3
error: unknown flag: --replicas
./kubectl create deployment web --image=nginx:1.27 --replicas=3 --dry-run=client -o yaml
```

**Listing 1.** kubectl v1.37.0: `run` rejects `--replicas` at flag parsing — proof of the 1.18 change — while `create deployment` accepts it and generates the right object.

```d2
direction: right
run: "kubectl run\none Pod, no owner" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
api: "API server -> scheduler\n-> kubelet -> container" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
dead: "container dies\npod stays failed" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
dep: "kubectl create deployment\nDeployment owns ReplicaSet" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
heal: "ReplicaSet controller\nrecreates pods forever" {
  width: 270
  height: 90
  style.fill: "#e8f5e9"
}
run -> api
api -> dead
dep -> heal
```

**Fig. 1.** Ownership is the difference: a bare pod has no controller behind it, a Deployment's pods are recreated by its ReplicaSet as long as the object exists.

> [!warning] The old answer fails the interview
> If you say "kubectl run creates a Deployment", you are describing a pre-2018 cluster and an interviewer will probe deeper. The second trap is the inverse: using `run` for anything beyond a quick debug pod — it has no probes, no resource limits, no config, no scaling, nothing declarative to review in a PR. The third trap: `--restart=Never` plus `--rm` does not make `run` a Job — a Job has retries, completion tracking, and TTL cleanup; `run` has none of that.

> [!tip] Interview answer
> kubectl run creates a single unmanaged Pod — an API object with no controller behind it — so it is only good for quick, throwaway testing. The --replicas flag was removed in 1.18 exactly to make that unambiguous: replicas and self-healing mean a Deployment via create or apply, which brings the ReplicaSet controller into the picture. A bare pod that dies stays dead; a Deployment's pod gets recreated until you change the declared replica count.
