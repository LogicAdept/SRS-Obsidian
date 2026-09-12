<!--
reps: 0
priority: 0
-->
#MachineLearning/Unsupervised #SRS

# What is unsupervised learning

> [!abstract] Short answer
> Unsupervised learning finds **structure in unlabeled data**: no `y` is provided, so the algorithm invents its own objective — compact clusters, low-variance directions, dense regions — and reports the structure it found. Typical outputs are clusters, reduced-dimension representations, or anomaly scores.

Because there is no ground-truth label, there is no single "accuracy". Evaluation is intrinsic (inertia, silhouette), downstream (does the new representation help a supervised task?), or business-level. This is the defining property that separates it from supervised learning, where labels anchor the loss.

## The three workhorse patterns

* **Clustering** groups rows by similarity: k-means partitions by distance to centroids, DBSCAN follows density and marks outliers as noise — mechanics in [[How does k-means clustering work]] and [[How does DBSCAN work]].
* **Dimensionality reduction** projects data into fewer dimensions while keeping the informative variance: [[What is PCA]] is the linear baseline, t-SNE and UMAP are non-linear visualization tools.
* **Anomaly and density modeling** scores how unusual a row is: Gaussian mixtures, isolation forests, one-class SVMs.

```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

Xs = StandardScaler().fit_transform(X)     # scale first: distances drive everything
Z = PCA(n_components=10).fit_transform(Xs) # compress, keep most variance
km = KMeans(n_clusters=5, n_init=10, random_state=0).fit(Z)
labels = km.labels_                        # structure found, no labels were given
```

**Listing 1.** The usual unsupervised pipeline: standardize, reduce, cluster. Scaling is not cosmetic — k-means minimizes Euclidean distances, so raw units would decide the clustering.

## Where it is used honestly

Customer segmentation, topic discovery, compression, feature pretraining, and outlier detection before a supervised model ever sees the data. Embeddings learned by deep networks are also unsupervised (self-supervised, precisely): the labels are manufactured from the input itself, then [[What is an embedding]] vectors feed supervised heads.

> [!warning] Interview trap
> "Unsupervised learning finds the true natural classes in the data." There is no such guarantee — every algorithm imposes its own geometry. k-means finds convex blobs because it minimizes Euclidean inertia; if your real groups are elongated or non-convex, it will slice them wrongly and still report a low inertia. Structure found is algorithm-relative, and choosing `k` is a human decision: [[How do you choose k in k-means]].

> [!tip] Interview answer
> Unsupervised learning works without labels — clustering, dimensionality reduction, and anomaly detection are the big three. I would stress that evaluation is indirect because there is no ground truth, that preprocessing like scaling changes results dramatically for distance-based methods, and that in practice I validate the structure by whether it improves a downstream task or is actionable for the business.

