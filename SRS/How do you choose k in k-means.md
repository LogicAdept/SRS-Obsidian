<!--
reps: 0
priority: 0
-->
#MachineLearning/Unsupervised #SRS

# How do you choose k in k-means

> [!abstract] Short answer
> There is **no single statistical answer — k is a modeling decision** supported by diagnostics: the elbow of the inertia curve, silhouette scores, gap statistics, and stability across resamples — and, decisively, whether the resulting segments are actionable for the use case. The metrics prune silly values; the business decides among the survivors.

## The standard diagnostics

* **Elbow (inertia):** within-cluster sum of squares always decreases with k; pick the bend where adding a cluster stops buying much. Cheap, universal, and annoyingly subjective near smooth curves.
* **Silhouette:** for each point, `s = (b − a) / max(a, b)` with `a` = mean intra-cluster distance, `b` = mean distance to the nearest other cluster; ranges −1 to 1. Higher means compact, well-separated clusters; per-cluster silhouettes also reveal junk clusters, not just junk k.
* **Gap statistic:** compares inertia to its expectation under a null reference distribution — more principled, more compute.
* **Stability:** cluster resampled or bootstrapped data and measure how consistently segments reappear (e.g. adjusted Rand index across runs); an unstable k is not a real structure.

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

for k in range(2, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xs)
    sil = silhouette_score(Xs, km.labels_)
    print(k, km.inertia_, round(sil, 3))
```

**Listing 1.** Sweep k and record inertia plus silhouette; read the elbow, prefer the silhouette peak, then check the survivors' stability.

## The part metrics cannot do

Metrics encode geometry, not meaning. A k of 6 with a slightly worse silhouette may be right if six segments map to six real marketing treatments; a k of 4 may be right because only four action strategies exist regardless of geometry. Cluster profiling — means of key features per cluster, sizes, business names — is the deciding step; if two clusters have no distinguishable treatment, they are one segment operationally. The same honest-evaluation mindset as supervised model selection: [[What is the bias-variance tradeoff]] has no direct analog here, but [[What is cross-validation]]-style stability checks do.

> [!warning] Interview trap
> "The elbow method finds the right k." It finds a kink in a curve you must still interpret; on smooth data there is no elbow at all. Second trap: "silhouette decides everything" — silhouette rewards compact convex clusters, which is also k-means's own bias; it will happily endorse geometrically pretty segments that mean nothing to the business. And never report k selected with the same metric you then use to claim cluster quality — selection bias applies in clustering too.

> [!tip] Interview answer
> I treat k as a decision with diagnostics: inertia elbow and silhouette sweep to prune the range, stability across resamples to reject noise, then profiling and business actionability to choose among survivors. Metrics bound the search, they do not make the call — a segment you cannot act on is not a segment, and I would rather deliver four usable clusters than seven geometrically perfect ones.

