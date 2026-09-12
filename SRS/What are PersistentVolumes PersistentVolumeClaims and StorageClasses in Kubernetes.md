<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What are PersistentVolumes PersistentVolumeClaims and StorageClasses in Kubernetes

> [!abstract] Short answer
> Kubernetes splits storage into a supply side and a demand side. A **PersistentVolume (PV)** is a piece of real storage (NFS, cloud disk, Ceph) registered into the cluster. A **PersistentVolumeClaim (PVC)** is a user's request for storage of a size and access mode — the pod mounts the claim, never the volume. A **StorageClass** is the template that makes **dynamic provisioning** work: when a claim names a class, the class's provisioner (a CSI driver) creates a matching PV on demand. The PVC is the contract that lets pods be rescheduled without losing their data ([[What is a StatefulSet in Kubernetes and when do you need one]] — per-replica claims are minted from `volumeClaimTemplates`).

## The three-object dance

Admins (or drivers) supply: a PV carries capacity, `accessModes` — `ReadWriteOnce` (single node), `ReadOnlyMany`, `ReadWriteMany` (multi-node, needs a backing system that truly supports it: NFS, CephFS, EFS — not a block disk) — and a `reclaimPolicy`: `Retain` keeps the volume and its data after the claim is gone (manual cleanup), `Delete` destroys the backing storage with the claim (the default for dynamically provisioned volumes). Users demand: a PVC states size, access modes, and — the binding linchpin — a `storageClassName`. Empty class name means static binding only; an omitted field defaults to the cluster's default class and *will* trigger dynamic provisioning. Once bound, PVC-to-PV is one-to-one: capacity may be resizable, the pairing is not. Pods consume claims via `volumes: persistentVolumeClaim` mounts; the kubelet and CSI node plugin handle attach and mount on whichever node the pod lands on — the mechanism that makes "db-1's disk follows db-1" true.

Access modes deserve the interview care: RWO is per-*node*, not per-pod (two pods on one node can share an RWO volume); asking RWO pods onto different nodes needs RWX storage or a redesign. And topology is real: a disk provisioned in zone A cannot follow a pod to zone B — the scheduler treats the claim's topology as a constraint ([[How does Kubernetes scheduling work]]).

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  storageClassName: fast-ssd
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 10Gi
```

**Listing 1.** The demand side: a 10 Gi RWO claim against the `fast-ssd` class — no PV is mentioned, because the class's CSI provisioner creates one; StatefulSet `volumeClaimTemplates` stamp exactly this per replica.

```d2
direction: right
pvc: "PVC data\n10Gi, RWO, class fast-ssd" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
sc: "StorageClass fast-ssd\nprovisioner: CSI driver" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
pv: "PV\ncreated dynamically, bound 1:1" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
disk: "real storage\ncloud disk / NFS / Ceph" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
pod: "pod mounts the claim\nnot the volume" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
pvc -> sc: "class name triggers"
sc -> pv: "dynamic provisioning"
pv -> disk
pod -> pvc
```

**Fig. 1.** Users never see disks: claims name a class, the class manufactures volumes, pods mount claims — supply and demand meet at the binding.

> [!warning] Deleting a PVC can delete your data
> The trap with teeth: reclaim policy `Delete` means `kubectl delete pvc` destroys the backing disk — for dynamically provisioned storage that is the default, so "cleanup scripts" have deleted databases. `Retain` is the safety setting, at the cost of manual reclamation. The others: RWO misread as per-pod (it is per-node); RWX assumed available when the storage class cannot deliver it; and zone-topology mismatches that leave pods Pending with a bound-but-unreachable claim. Pod-local volumes — `emptyDir`, `hostPath` — are *not* this system: they die with the node or the pod ([[What is a Pod in Kubernetes]]).

> [!tip] Interview answer
> PersistentVolumes are the supply — actual storage registered with capacity, access modes, and a reclaim policy; PersistentVolumeClaims are the demand — a size, access modes, and a StorageClass name; StorageClasses bring the CSI provisioner that dynamically manufactures matching PVs. Pods mount claims, one-to-one binding, RWO means single-node not single-pod, RWX needs shared filesystems, and Delete reclaim policy really deletes backing storage. This split is what gives StatefulSets portable per-replica disks: the claim follows the pod, the volume follows the claim.
