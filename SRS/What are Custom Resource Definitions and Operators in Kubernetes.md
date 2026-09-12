<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What are Custom Resource Definitions and Operators in Kubernetes

> [!abstract] Short answer
> A **Custom Resource Definition (CRD)** extends the Kubernetes API with your own object kind: apply a CRD and the API server immediately serves, validates, stores, and watches `kind: MyThing` — with RBAC, kubectl support, and versioning included. A **custom controller** watches those objects and reconciles them like built-in controllers do. An **Operator** is the pattern of packaging a CRD with a controller that encodes operational knowledge — deploy, scale, back up, upgrade a specific piece of software (PostgreSQL, Kafka, Prometheus) — so the cluster manages it declaratively. CRD is the data model; the controller is the behavior; the Operator is the application of both to operating software.

## CRD: adding kinds to the API

The API server is a generic object engine: built-in kinds (Pod, Deployment) and custom kinds share one machinery. A CRD declares the kind's group/version, scope (namespaced or cluster), and an OpenAPI schema for validation — after that, `kubectl get databases` works, etcd stores the objects ([[What is etcd in Kubernetes]]), RBAC guards them ([[What is RBAC in Kubernetes]]), and watch streams notify anyone. What a CRD deliberately does *not* include is behavior: create a CRD alone and its objects are inert records — data without a driver. Aggregated APIs (`APIService`) are the heavier alternative — a real API server extension behind the same endpoint — used when you need your own storage or semantics; CRDs cover the overwhelming majority of extension needs.

## Operators: operational knowledge as a controller

A controller closes the loop: watch objects of the kind, compare desired `spec` with observed state, act, repeat — the same reconciliation loop every built-in controller runs. The Operator pattern applies this to *operating software*: the `PostgresCluster` object says "3 replicas, backups daily, version 17.2"; the operator provisions StatefulSets, headless Services, PVCs, manages failover, runs backups, performs version upgrades step by step — turntable knowledge that used to live in runbooks becomes code that runs continuously ([[What is a StatefulSet in Kubernetes and when do you need one]] — operators are the reason running databases on Kubernetes became defensible). The interview-grade trade-offs: operators are always-on controllers — their bugs are cluster incidents; CRD APIs are forever (versioning and conversion are obligations, not options); and writing an operator is justified when the operational knowledge is deep and recurring — consume existing ones (Prometheus, cert-manager, strimzi) before writing your own.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.demo.io
spec:
  group: demo.io
  scope: Namespaced
  names: { kind: Database, plural: databases }
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                replicas: { type: integer, minimum: 1 }
                version: { type: string }
```

**Listing 1.** A minimal CRD: from this moment, `kubectl apply` of `kind: Database` objects validates `replicas` and `version` at admission — but nothing is created anywhere until a controller watches the kind.

```d2
direction: right
user: "kubectl apply\nkind: Database" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
api: "API server + CRD\nvalidates, stores, watches" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
ctrl: "operator controller\nreconcile loop" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
real: "creates real objects\nStatefulSet, PVC, backup Jobs" {
  width: 330
  height: 100
  style.fill: "#e8f5e9"
}
user -> api -> ctrl -> real
```

**Fig. 1.** CRD supplies the vocabulary, the operator supplies the verbs: the object is the wish, the controller is the muscle.

> [!warning] A CRD without a controller is a spreadsheet
> The traps: shipping a CRD and expecting objects to do anything — no controller, no behavior; the API server validates but never acts. Treating CRD versions as documentation — deprecating a served version without a conversion plan breaks consumers. Running an operator with cluster-wide RBAC and unreviewed upgrades — it is privileged code ([[How do you secure a Kubernetes cluster]]). And hand-editing operator-owned sub-objects: the reconcile loop reverts you — the same drift fight as with Deployments ([[What is the difference between kubectl apply and kubectl create]]), one level up.

> [!tip] Interview answer
> A CRD adds a new object kind to the API server — group, scope, OpenAPI schema — and the platform gives it storage, validation, RBAC, kubectl, and watches for free, but no behavior. A custom controller watches that kind and reconciles it like built-ins; an Operator packages CRD plus controller to run software: it provisions the StatefulSets and PVCs, handles failover, backups, upgrades — runbook knowledge turned into always-running code. CRD is the data model, controller is the behavior, Operator is the pattern; prefer consuming mature operators before writing your own, and remember their bugs are cluster incidents.
