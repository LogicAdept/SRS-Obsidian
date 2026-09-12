<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is etcd in Kubernetes

> [!abstract] Short answer
> etcd is the **consistent, highly-available key-value store** that holds all cluster state — every object the API server accepts (pods, secrets, Deployments) lives in it. Only kube-apiserver reads and writes it. It is a distributed system built on the Raft consensus algorithm, so an etcd cluster of 3 or 5 members survives member failures while keeping a quorum, and every write is committed by that quorum before being acknowledged. Lose etcd and the cluster loses its memory: the API server serves nothing, controllers cannot reconcile, pods keep running but nothing new can be decided.

## What it stores and how it is accessed

The API server maps every object to a key under `/registry/` — a pod becomes `/registry/pods/default/web`, a secret `/registry/secrets/default/db-cred`. Clients never touch etcd directly: kubectl, controllers, and the kubelet all go through kube-apiserver, which serializes access, enforces RBAC and schema validation, and exposes watch streams so controllers learn about changes instead of polling. Watch is what makes the whole architecture event-driven: a controller registers interest in a resource type, etcd streams every change since a resource version, and the reconcile loop reacts. This is also why a healthy etcd is a latency budget question — every API call becomes an etcd round trip, and slow disks show up as slow kubectl ([[What are the main components of the Kubernetes architecture]]).

## Quorum, HA topologies, backups

Raft requires a majority to commit: 3 members tolerate 1 failure, 5 members tolerate 2 — an even number adds risk without adding tolerance, so clusters run odd sizes. Kubernetes ships two standard topologies: **stacked** (etcd members on the control-plane nodes, simpler, default for kubeadm) and **external** (separate machines, isolates control-plane load from storage load). The interview-critical operational fact is the backup story: etcd has a native snapshot command, and restoring means restoring the whole cluster — the snapshot contains RBAC rules, secrets, everything — so it must be encrypted in transit and at rest, and a restored control plane needs its certificate data consistent ([[How does Kubernetes achieve high availability]]).

```bash
./etcdctl endpoint health
./etcdctl put /registry/pods/default/web '{"phase":"Running"}'
./etcdctl snapshot save /tmp/etcd-demo.snapshot
./etcdctl snapshot status /tmp/etcd-demo.snapshot -w table
# ... cluster lost: restore the snapshot into a fresh data dir, restart etcd ...
./etcdctl snapshot restore /tmp/etcd-demo.snapshot --data-dir /tmp/etcd-demo-data --name demo
./etcdctl get /registry/pods/default/web
```

**Listing 1.** Single-member etcd v3.5.21 driven locally: keys under a registry-like prefix, then the full backup-and-restore cycle — snapshot, wipe the data dir, restore, and the key is back.

```
127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.132689ms
OK
Snapshot saved at /tmp/etcd-demo.snapshot
+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| af96e094 |        3 |          8 |      29 kB |
+----------+----------+------------+------------+
/registry/pods/default/web
{"phase":"Running"}
```

```d2
direction: right
api: "kube-apiserver\nsole etcd client" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
w: "write request\npod created" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
leader: "leader member\nappends to Raft log" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
quorum: "quorum ack\n3 of 5 members" {
  width: 210
  height: 90
  style.fill: "#e8f5e9"
}
ack: "write acknowledged\nwatchers notified" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
down: "lost quorum?\nno commits at all" {
  width: 230
  height: 90
  style.fill: "#ffebee"
}
api -> w -> leader -> quorum -> ack
quorum -> down: "2 of 5 down"
```

**Fig. 1.** Consistency over availability: without a Raft majority etcd refuses all writes rather than risking split-brain — the cluster freezes, it does not fork.

> [!warning] Etcd is not a database for your application
> Interview traps: etcd stores cluster *metadata*, not app data — putting 10 GB of records in it is a design smell; it has a default 2 GB backend quota (2.1 GB seen in real logs) and etcd slowness under load is usually disk latency. Another trap: restoring a snapshot on a *running* cluster does nothing useful — you restore into fresh members, and you must take snapshots regularly because no controller replicates etcd content elsewhere. And secrets sit in etcd in plain form unless encryption at rest is enabled ([[How do you secure a Kubernetes cluster]]).

> [!tip] Interview answer
> etcd is a Raft-based, strongly consistent distributed key-value store where the API server keeps every object of the cluster — nothing else writes to it, clients only ever see it through kube-apiserver and its watch streams. Production runs 3 or 5 members — quorum of 2-of-3 or 3-of-5 tolerates 1 or 2 failures, and losing quorum halts writes, not forking state. Operations care about disk latency, the 2 GB quota, snapshots for disaster recovery, and enabling encryption at rest because secrets are stored there.
