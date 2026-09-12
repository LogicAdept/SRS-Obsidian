<!--
reps: 0
priority: 0
-->
#MachineLearning/Unsupervised #SRS

# How does DBSCAN work

> [!abstract] Short answer
> DBSCAN (Density-Based Spatial Clustering of Applications with Noise) grows clusters from **dense regions**: a point is core if at least `min_samples` neighbors lie within radius `eps`; core points connected through overlapping neighborhoods form clusters, and everything else is labeled **noise**. It finds arbitrarily shaped clusters and needs no `k` — the two properties k-means lacks.

## The algorithm

Pick an unvisited point. If its `eps`-neighborhood holds `min_samples` points, it becomes a core point and a cluster starts; all its density-reachable neighbors join, and the process expands through their neighborhoods (border points have few neighbors but fall inside some core's radius). Points neither core nor border are noise. Implementation-wise: neighborhood queries via spatial index (ball tree / KD-tree), `O(n log n)` typical, degrading in high dimensions.

```python
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

Xs = StandardScaler().fit_transform(X)
db = DBSCAN(eps=0.5, min_samples=5, metric="euclidean")
labels = db.fit_predict(Xs)
print(set(labels))            # {-1} means: everything marked noise — tune eps
```

**Listing 1.** `eps` and `min_samples` are the whole model; label −1 is noise. If everything is −1 or one giant cluster, the density parameters are wrong for the scaled data.

## Choosing eps and min_samples

The standard heuristic: plot the distance to the `min_samples`-th nearest neighbor for all points sorted ascending — the knee of that curve is a sane `eps`. `min_samples` encodes "how dense is dense"; 5–10 is a common start, higher for noisy data. Both parameters interact with scaling — distances on unscaled data are meaningless, the same discipline as [[How does k-means clustering work]]. Unlike k, the cluster **count** emerges from the data — there is no [[How do you choose k in k-means]] dilemma, but parameter sensitivity replaces it.

```d2
direction: right
core: "core point\n>= min_samples neighbors\nwithin eps" { width: 230; height: 90 }
reach: "density-reachable\nexpands the cluster" { width: 200; height: 80 }
border: "border point\nin a core's eps,\nnot core itself" { width: 210; height: 90 }
noise: "noise (-1)\nin no core's radius" { width: 180; height: 80 }
core -> reach; reach -> core { style.stroke: "#1565c0" }
core -> border
noise
```

**Fig. 1.** Points are core, border, or noise; clusters are connected sets of density-reachable core points with their borders attached.

## Strengths and the failure surface

Strengths: arbitrary cluster shapes (moons, rings), explicit noise detection — a free anomaly signal, no preset cluster count. Failures: **varying densities** break a single global `eps` (dense and sparse clusters cannot both be served); high-dimensional data makes distances concentrate and `eps` tuning miserable — dimensionality reduction first ([[What is PCA]]); and border-point assignments are order-dependent in edge cases. For segment-style business data with roughly convex clusters, k-means remains simpler; DBSCAN is the tool when shape and noise are the story.

> [!warning] Interview trap
> "DBSCAN needs no parameters." It needs no k, but `eps` and `min_samples` are more delicate than k — one global density radius is a strong assumption. Second trap: treating noise labels as errors to be eliminated; the −1 points are the method's honest answer about sparse regions and are often the most interesting rows in fraud and monitoring contexts.

> [!tip] Interview answer
> DBSCAN builds clusters from density: core points with min_samples neighbors inside eps expand through density-reachable neighbors, borders attach, and sparse points become noise. I would mention the k-th-distance knee plot for choosing eps, its strengths — arbitrary shapes, noise detection, no preset k — and its limits: varying densities and high dimensions. Scaling the data first is mandatory, same as any distance-based method.

