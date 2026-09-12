<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is a StatefulSet in Kubernetes and when do you need one

> [!abstract] Short answer
> A StatefulSet manages pods that need a **stable identity**: each replica gets a fixed, never-recycled name (`db-0`, `db-1`, `db-2`), stable DNS names through a **required headless Service**, ordered creation and termination, and its own PersistentVolumeClaim that follows the pod across rescheduling. Use it for databases, message brokers, and clustered stateful software where "replica number 1" must remain the same member with the same disk; use a Deployment for anything stateless.

## What "sticky identity" actually buys

Three guarantees from the docs, each with a concrete consequence. First, stable, unique network identity: pod names and their per-pod DNS records survive rescheduling, so `db-1.db-headless.ns.svc.cluster.local` always finds the same member — that is how most quorum-based systems (PostgreSQL with Patroni, Kafka, ZooKeeper-style ensembles, etcd itself) bootstrap and rejoin peers. Second, ordered, graceful deployment and scaling: replicas start in index order and terminate in reverse order, which matters for systems where a new member must join before the next one does, or where a leader should be the last to die. Third, stable storage: each pod's PVC is bound to its identity, so `db-1`'s volume reattaches to whatever node `db-1` lands on — data does not live in the pod, it lives in the claim ([[What are PersistentVolumes PersistentVolumeClaims and StorageClasses in Kubernetes]]).

The price of all this: StatefulSets are slower to scale and heal by design — ordered transitions and no parallel chaos — and pods are not recreated when only deleted without scale-down semantics. If an app needs none of identity, ordering, or per-replica storage, the docs say it plainly: use a stateless workload object ([[What is the difference between a Deployment and a ReplicaSet in Kubernetes]]).

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: db-headless
  replicas: 3
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
        - name: postgres
          image: postgres:17
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

**Listing 1.** The canonical skeleton: `serviceName` points at the headless Service, and `volumeClaimTemplates` mints one PVC per replica — `data-db-0`, `data-db-1`, `data-db-2` — instead of sharing one volume.

```d2
direction: right
headless: "headless Service\nno cluster IP" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
s0: "db-0\nDNS + PVC data-db-0" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
s1: "db-1\nDNS + PVC data-db-1" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
s2: "db-2\nDNS + PVC data-db-2" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
order: "start 0,1,2\nstop 2,1,0" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
headless -> s0
headless -> s1
headless -> s2
s0 -> order
s1 -> order
s2 -> order
```

**Fig. 1.** Identity, not load balancing: the headless Service returns per-pod DNS records instead of one virtual IP, and ordering is a StatefulSet guarantee, not a Service one.

> [!warning] Traps: headless Service, deletion semantics, "just use StatefulSet"
> A StatefulSet without its headless Service does not give you per-pod DNS — you must create the Service yourself. Deleting the StatefulSet does not delete the PVCs by default: recreating it reattaches old data, sometimes exactly what you did not want. And bolting StatefulSet onto a stateless app costs you parallel scaling and fast healing for nothing — the mirror trap of putting a database in a Deployment and losing its identity on every reschedule.

> [!tip] Interview answer
> StatefulSet is the workload controller for pods with identity: stable ordinal names that survive rescheduling, per-pod DNS through a required headless Service, ordered start and reverse-order termination, and a per-replica PVC from volumeClaimTemplates that reattaches wherever the pod lands. That combination is what clustered databases and brokers need to form quorums and keep member disks. If your app is stateless and order-free, a Deployment is strictly better — faster scaling, faster healing, no ceremony.
