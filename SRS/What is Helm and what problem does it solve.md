<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Helm #DevOps/Tools/Kubernetes #SRS

# What is Helm and what problem does it solve

> [!abstract] Short answer
> Helm is the **package manager for Kubernetes**: a **chart** bundles an application's manifests as templates with sane defaults, a **values file** overrides those defaults per environment, and Helm renders the combination and installs, upgrades, or removes the result as a named **release** with history. The problem it solves: raw YAML does not parameterize — five environments, ten services, and version discipline quickly become copy-paste drift; Helm adds templates, defaults, versioned releases, and rollback to that.

## Charts, values, releases

A chart is a directory: `Chart.yaml` (name, version, appVersion — the packaging metadata), `templates/` with Go-templated manifests, and `values.yaml` — the documented default surface. Deployment becomes `helm install myapp ./chart --set image.tag=1.42 --values prod.yaml`: the template engine merges defaults and overrides and emits plain Kubernetes objects, which are then applied *as a release*. The release record is the value-add over raw `apply`: Helm stores what it installed and in which version, so `helm upgrade` diffs and applies changes coherently across all the chart's objects, and `helm rollback myapp 7` returns the whole release to a prior revision — multi-object rollback that raw manifests never had ([[What is the difference between kubectl apply and kubectl create]] — Helm layers release semantics on the same API). Charts compose: subcharts let a platform chart depend on, say, PostgreSQL as a library, and public repositories (Artifact Hub) distribute third-party charts the way registries distribute images — `helm repo add`, `helm search`, `helm pull`.

The honest boundary: Helm templates are text — the YAML a chart renders is whatever the template logic produces, and broken values surface as broken YAML; Kustomize is the competing philosophy (patches over complete manifests, no templating), and many shops run both — Helm for third-party software, Kustomize for in-house overlays.

```bash
./kubectl kustomize
```

**Listing 1.** The parameterization need, shown with its non-Helm cousin on kubectl v1.37.0: one committed base manifest transformed by declared overrides — `demo-` prefix, replicas 5, image pinned to 1.27. Helm's charts do this job with richer templating plus release tracking and rollback.

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
chart: "chart\ntemplates + Chart.yaml" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
values: "values.yaml\nenv overrides" {
  width: 210
  height: 90
  style.fill: "#fff3e0"
}
render: "helm template\nplain manifests" {
  width: 210
  height: 90
  style.fill: "#fff3e0"
}
rel: "release v8\nversioned install record" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
undo: "helm rollback\nwhole release to v7" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
chart -> render
values -> render
render -> rel -> undo
```

**Fig. 1.** Two inputs, one rendering, one versioned release — the release record is what enables whole-application rollback rather than file-by-file archaeology.

> [!warning] Templates fail at render time, and secrets do not belong in values
> The traps: a typo deep in a values file can render invalid YAML — Helm is only as typed as its templates; `helm lint` and `helm template` are the pre-flight ([[What do admission controllers do in Kubernetes]] — policy enforcement still happens at the server). Secrets committed as plain-text values leak exactly where Git does; use external secret operators or encrypted values. And `helm upgrade` with an accidentally changed selector or label scheme can orphan or strand workloads — the three-way merge of Helm upgrades has its own drift stories when people `kubectl edit` behind Helm's back ([[What is the difference between kubectl apply and kubectl create]]).

> [!tip] Interview answer
> Helm is Kubernetes' package manager: a chart is templated manifests with default values, environments override values, and installing renders a release that Helm tracks with version history. You get parameterization across environments, curated third-party charts from public repos, coherent upgrades across many objects, and release-level rollback — the packaging layer raw YAML lacks. The sharp edges: template rendering is string-typed, secrets must not ride in values, and out-of-band kubectl edits fight the release record.
