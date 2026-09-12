<!--
reps: 0
priority: 0
-->
#MachineLearning/Unsupervised #SRS

# How does k-means clustering work

> [!abstract] Short answer
> k-means partitions data into **k clusters by alternating two steps**: assign every point to its nearest centroid, then move each centroid to the mean of its assigned points. Repeat until assignments stabilize. It minimizes within-cluster squared distance (inertia) — which mathematically bakes in an assumption of roughly spherical, similarly sized clusters.

Lloyd's algorithm: initialize k centroids (k-means++ spreads them probabilistically far apart — the standard fix for bad random starts), assign, update, iterate to convergence. The objective is non-convex, so the result is a local optimum depending on initialization — hence `n_init` restarts; scikit-learn's default moved to `n_init="auto"` in 1.4 (previously 10).

## The loop

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

Xs = StandardScaler().fit_transform(X)   # means are Euclidean: scale first
km = KMeans(n_clusters=5, n_init=10, init="k-means++", random_state=0)
labels = km.fit_predict(Xs)
print(km.inertia_)                        # within-cluster sum of squares
```

**Listing 1.** The production call: scale, k-means++ initialization, several restarts, and inertia as the convergence statistic. Scaling is not cosmetic — unscaled features dominate the mean step.

```d2
direction: right
init: "init k centroids\n(k-means++)" { width: 170; height: 80 }
a: "assign each point\nto nearest centroid" { width: 200; height: 80 }
u: "move centroid\nto cluster mean" { width: 190; height: 80 }
s: "assignments stable?" { width: 170; height: 70 }
out: "labels + centroids" { width: 180; height: 70 }
init -> a -> u -> s
s -> a: "no" { style.stroke: "#b71c1c" }
s -> out: "yes"
```

**Fig. 1.** The assign–update loop converges to a local optimum of inertia; restarts guard against a bad basin.

## What it is good and bad at

Good: fast (linear in n per iteration), scalable, the default first clustering tool, and a legitimate compression/quantization method (centroid IDs as features). Bad: convex-blob geometry only — elongated, nested, or density-varying clusters get butchered (that is DBSCAN territory: [[How does DBSCAN work]]); sensitive to outliers (means get dragged — medians motivate k-medoids); requires k upfront: [[How do you choose k in k-means]]; and every run may give a different partition — check stability across restarts before presenting "the" segmentation.

> [!warning] Interview trap
> "k-means always converges to the best clustering." It converges to a local optimum of inertia, and inertia itself is a proxy nobody actually cares about — the business wants meaningful segments. Second trap: forgetting that k-means **requires numeric features** (means of one-hot columns are meaningless) and scaling — the preprocessing sins here are the most common real-world bug, see [[What is feature engineering]].

> [!tip] Interview answer
> k-means alternates assigning points to the nearest centroid and recomputing centroids as means, minimizing within-cluster squared distance; k-means++ initialization and multiple restarts handle its local-optima problem. I would stress scaling, the spherical-cluster assumption and its failure modes, choosing k by elbow/silhouette plus business judgment, and DBSCAN as the alternative when clusters are non-convex or noise matters.

