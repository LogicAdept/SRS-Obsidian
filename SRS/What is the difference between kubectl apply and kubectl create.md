<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is the difference between kubectl apply and kubectl create

> [!abstract] Short answer
> `kubectl create` is **imperative**: it reads what you gave it right now and POSTs a new object — and fails if the object already exists. `kubectl apply` is **declarative**: it takes a config file as the long-lived source of truth, compares it against the live object and the last-applied annotation, and then either creates the object or computes a patch that converges the live one toward the file. In day-to-day terms: `create` is a one-shot command, `apply` is how configuration is managed in Git and CI.

## The mechanism under apply

What makes `apply` more than "create if missing" is the three-way merge. The client remembers what it last applied — historically the `kubectl.kubernetes.io/last-applied-configuration` annotation, today field managers with `managedFields` on the object — and when the file changes, it diffs three versions: the file, the live object, and the last applied record. Fields you removed from the file get cleaned up, fields other actors changed are left alone, fields the file sets are enforced. That is why `apply` is safe to run repeatedly and from many pipelines, while blindly re-running imperative commands is not — `create` would 409 on the second run, and `replace` would clobber fields it does not know about ([[What are the main components of the Kubernetes architecture]] — the API server enforces all of it).

The modern evolution is **server-side apply** (`--server-side`): the API server itself does the merge and tracks field ownership per manager, which fixes client-side annotation size limits and makes conflicts between two writers an explicit, resolvable error instead of a silent last-write-wins.

## Imperative commands still have a place

`kubectl create deployment web --image=nginx:1.27`, `create secret`, `create cronjob` — generators that build an object inline — are ideal for scratch work, demos, and bootstrapping, and `kubectl ... --dry-run=client -o yaml` turns them into the starting point for the declarative file you commit next. The mature workflow is: generate once, edit the manifest, and from then on only `apply` (or Kustomize/Helm rendering to `apply`) touches the cluster ([[What is Helm and what problem does it solve]] is the packaged evolution of the same idea).

```bash
./kubectl kustomize
```

**Listing 1.** The declarative endgame on kubectl v1.37.0: from one committed manifest, `kustomize` renders the exact objects to apply — replicas overridden to 5, every name prefixed, the image pinned — the rendered output, not a sequence of commands, is the source of truth.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-web
spec:
  replicas: 5
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - image: nginx:1.27
        name: nginx
        ports:
        - containerPort: 80
```

```d2
direction: right
create: "kubectl create\nPOST the object\nfails if it exists" {
  width: 240
  height: 110
  style.fill: "#e3f2fd"
}
apply: "kubectl apply\ndiff file vs live vs last-applied" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
patch: "create or\nthree-way patch" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
live: "live object converges\nidempotent on re-run" {
  width: 270
  height: 90
  style.fill: "#e8f5e9"
}
create -> live: "one shot"
apply -> patch -> live
```

**Fig. 1.** `create` is a statement; `apply` is a policy — the same file applied again changes nothing, which is what makes it CI-safe.

> [!warning] Mixing styles drifts the cluster
> The trap interviewers listen for: managing an object with `apply` while someone edits it with `kubectl scale` or `edit` — the next apply silently reverts that change, because the file is the source of truth. The inverse bites too: `apply` does not delete objects you removed from a directory unless you pass `--prune`, so deleted manifests leave orphan resources running. And `replace` is not `apply`: it needs the full object and drops fields it was not given.

> [!tip] Interview answer
> kubectl create is imperative — it POSTs a freshly generated object and errors if it exists. kubectl apply is declarative — it stores what it applied, diffs your file against the live object and that record, and produces a converging patch, so it is idempotent and pipeline-friendly. Deletions and multi-writer safety are the sharp edges: apply never prunes without a flag, and server-side apply moves the merge into the API server with per-field ownership. In practice: generate with create, live on apply.
