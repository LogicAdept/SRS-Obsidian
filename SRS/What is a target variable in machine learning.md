<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is a target variable in machine learning

> [!abstract] Short answer
> The target variable (label, dependent variable, `y`) is **the quantity a supervised model is trained to predict**. It fixes the problem type — continuous target means regression, categorical means classification — and everything downstream, from the loss to the metrics, is chosen relative to it.

The target is the definition of success. If the target measures the wrong thing (a proxy instead of the real business outcome), a well-fit model will faithfully optimize the wrong objective. Deciding what `y` is, and how honestly it is measured, is a modeling decision, not a detail.

## Target type drives the pipeline

* **Continuous** (price, duration, demand) — regression; losses like squared error; metrics like MAE and R² — see [[What regression metrics do you use in machine learning]].
* **Binary** (churn yes/no) — classification; cross-entropy loss; precision/recall and ROC AUC — see [[What is the difference between precision and recall]] and [[What is ROC AUC]].
* **Multiclass / multilabel** — softmax or per-label heads; macro vs micro averaging decisions appear.
* **Ordinal, count, time-to-event** — need specialized losses; treating them naively as plain regression is a common modeling bug.

```python
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression().fit(X, y_churn)     # y_churn: binary target
# predicting y_price instead would be a different model family:
# LinearRegression().fit(X, y_price)
```

**Listing 1.** The same feature matrix `X` with a different target becomes a different problem; the target choice selects loss and metrics.

## Where targets go wrong

Mislabeled and ambiguous labels inject noise the model cannot think around. Targets measured with delay (a chargeback 60 days later) force careful snapshotting or you train on answers you will not have. Proxy targets — clicks instead of satisfaction — invite reward hacking. And a target that is trivially available at scoring time is not a target, it is leakage: [[What is data leakage in machine learning]].

> [!warning] Interview trap
> "The target is just the column we predict." The leak version of this attitude is a career classic: anything correlated with `y` because it was recorded after or from `y` must not be a feature. Also watch class imbalance: a 99/1 target makes accuracy a nearly meaningless headline metric — see [[How do you handle class imbalance]].

> [!tip] Interview answer
> The target variable is what supervised training optimizes toward, and its type determines problem class, loss, and metrics. I would emphasize that choosing the target is where business goal becomes math, that proxy or delayed targets need explicit handling, and that target-related leakage is the fastest way to produce a model that looks great offline and fails in production.

