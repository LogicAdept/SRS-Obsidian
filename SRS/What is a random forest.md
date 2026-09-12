<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS

# What is a random forest

> [!abstract] Short answer
> A random forest is a **bag of decorrelated decision trees**: each tree is trained on a bootstrap resample of the rows, and at every split only a random subset of features is considered. Predictions average (regression) or vote (classification). The double randomization cuts the variance of individual trees dramatically while keeping their low bias.

The recipe is pure bagging plus feature subsampling — the feature randomness is what separates it from plain bagging: two trees see different candidate features at each split, so their errors decorrelate and the average cancels more noise: [[What is the difference between bagging and boosting]].

## Mechanics and the free lunch

scikit-learn defaults: `n_estimators=100`, bootstrap on, `max_features="sqrt"` for classification (`1.0` for regression), unlimited depth with `min_samples_leaf=1` — trees are grown deep on purpose: strong, overfit members whose averaged variance is small. Bootstrap leaves ~37% of rows out of each tree's sample (**out-of-bag**, OOB); those rows serve as a built-in validation set — `oob_score=True` gives an honest generalization estimate without a separate split, though it is not a replacement for a proper held-out test: [[What is a train validation test split]].

```python
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(
    n_estimators=300, max_features="sqrt",
    min_samples_leaf=1, oob_score=True, n_jobs=-1, random_state=0,
).fit(X_tr, y_tr)
print("OOB accuracy:", clf.oob_score_)
```

**Listing 1.** More trees never hurt accuracy (only latency and memory) — the ensemble's risk does not grow with M, unlike boosting; feature importance (impurity-based or permutation) comes free from the structure.

## Strengths, costs, and where boosting overtakes it

Strengths: robust default on tabular data, noise-tolerant, hard to overfit through tuning mistakes, parallelizable, gives OOB and importances. Costs: less accurate than well-tuned gradient boosting on many benchmarks — [[What is gradient boosting]]; large memory (hundreds of deep trees); no extrapolation; impurity importances mislead on correlated or high-cardinality features — use permutation importance. Interpretability of a single rule path survives per-tree, but the forest as a whole is a black box compared to one tree: [[How does a decision tree work]].

> [!warning] Interview trap
> "Random forest does not overfit." It overfits far less than a single tree and does not degrade with more trees, but each member still memorizes its bootstrap — noisy labels, leaked features, and correlated rows all pass straight through to the ensemble. Leaked features are the classic: the forest will happily score 0.95 OOB on a leak — [[What is data leakage in machine learning]].

> [!tip] Interview answer
> A random forest averages many deep trees, each fit on a bootstrap sample with a random feature subset at every split — the bagging-plus-decorrelation recipe that attacks variance. I would mention OOB scoring as a free validation signal, sqrt-of-features for classification as the classic setting, its robustness as the tabular default, and that tuned gradient boosting usually beats it in accuracy while demanding more careful regularization.

