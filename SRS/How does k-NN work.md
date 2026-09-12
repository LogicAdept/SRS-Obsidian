<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# How does k-NN work

> [!abstract] Short answer
> k-nearest neighbors is **lazy learning**: it stores the training set and, at prediction time, finds the `k` closest observations to the query (by a distance metric) and returns their majority class — or their average for regression. There is no training phase; the "model" is the data, which is why scaling and metric choice are the entire game.

k-NN is the non-parametric baseline: decision boundaries flex to local data density. Small `k` → wiggly, noise-sensitive boundaries; large `k` → smooth boundaries biased toward the majority class. Odd `k` avoids tie votes in binary problems; class-weighted variants damp imbalance — related metric traps in [[How do you handle class imbalance]].

## Mechanics and the real costs

Prediction cost is the catch: finding neighbors is `O(n·p)` per query with brute force — index structures (KD-tree, ball tree) help at low dimensionality but degrade as `p` grows (curse of dimensionality: distances concentrate, "nearest" stops meaning anything). Standardizing features is mandatory — otherwise the largest-scale feature silently owns the distance: [[What is a design matrix]] preprocessing discipline.

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

clf = make_pipeline(
    StandardScaler(),                        # distances must be fair
    KNeighborsClassifier(n_neighbors=7, weights="distance"),
).fit(X_tr, y_tr)                            # fit() just stores the data
```

**Listing 1.** k-NN with distance-weighted votes: closer neighbors count more, and the scaler lives inside the pipeline so serving replays it exactly.

## When to reach for it

Small data with meaningful geometry, baseline recommendations and similarity lookups, anomaly detection by neighbor distance. Avoid it for high-dimensional sparse data, strict-latency serving (every query pays a search cost), and huge training sets — approximate neighbor search (ANN indexes) exists precisely to cut that cost. The accuracy-vs-`k` trade-off is the model's only real tuning knob — a miniature version of the capacity story in [[What is the bias-variance tradeoff]] — and it is selected honestly by cross-validation: [[What is cross-validation]].

> [!warning] Interview trap
> "k-NN has no hyperparameters except k." Also the distance metric (Euclidean, Manhattan, cosine), the weighting scheme, and the index structure — and they matter more than `k` in practice. The deeper trap: "no training phase means no overfitting" — wrong; tiny `k` on noisy data overfits gloriously, it just does the fitting at query time.

> [!tip] Interview answer
> k-NN classifies by voting among the k closest training points under a distance metric — no training, all cost at query time. I would stress feature scaling, the curse of dimensionality killing distance meaning, the k trade-off between bias and variance, and that in production the per-query search cost and approximate indexes are the real engineering concerns.

