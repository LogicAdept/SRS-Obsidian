<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# What regression metrics do you use in machine learning

> [!abstract] Short answer
> The standard set: **MAE** (mean absolute error — robust, in target units, median-seeking), **RMSE** (root mean squared error — outlier-sensitive, mean-seeking, in target units), **R²** (variance explained, scale-free, comparable across problems), plus **MAPE/sMAPE** for relative-error business cases and quantile losses when the decision needs a percentile. The choice encodes which errors hurt.

Each metric implies a different notion of "best": minimizing MAE fits the conditional median; minimizing MSE fits the conditional mean; quantile loss fits the requested quantile. Reporting one number without saying this is how regression models get chosen against the business's actual interest.

## The roster

* **MAE** = mean |y − ŷ| — linear in error; one huge miss counts as its size, not its square; robust to outliers, less smooth as a loss.
* **RMSE** = √mean (y − ŷ)² — punishes large errors disproportionately; the right headline when big misses are genuinely worse; dominated by outliers when they are noise — the loss-perspective is in [[What is mean squared error]].
* **R²** = 1 − SSE/SST — "how much better than predicting the mean"; 0.9 can be awful in domains where 0.99 is the floor; can be negative on test data — a honest smell of disaster.
* **MAPE** — percentage error; interpretable, but explodes near zero targets and is asymmetric; sMAPE damps some of that.
* **Quantile/pinball loss** — when the deliverable is "90th percentile demand", not the mean.

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_te, pred)
rmse = mean_squared_error(y_te, pred, squared=False)
r2 = r2_score(y_te, pred)
print(f"MAE {mae:.3f}  RMSE {rmse:.3f}  R2 {r2:.3f}")
```

**Listing 1.** Report at least MAE and RMSE together: their ratio (RMSE/MAE) is itself a quick outlier-sensitivity diagnostic — a big ratio says a few points dominate.

## How to choose honestly

Start from the decision: inventory planning punishes large misses (RMSE or quantile at high percentile), delivery ETA tolerates outliers (MAE), finance needs relative error (MAPE with zero-guards). Then report two, not one — a central metric plus an outlier diagnostic — and always on the same held-out protocol: [[What is a train validation test split]], [[What is cross-validation]] for the selection loop. Metric shopping across many splits is selection bias, same as any other: [[What is data leakage in machine learning]].

> [!warning] Interview trap
> "RMSE is always better than MAE because it is smoother." Smoother as a loss, yes — but as a metric it manufactures outlier drama; with heavy-tailed targets RMSE mostly reports your anomalies. Second trap: "R² 0.95 means the model is production-ready" — R² says nothing about absolute error magnitude or about the tails where the business risk usually lives; ask for MAE in target units and a quantile view.

> [!tip] Interview answer
> My default is MAE plus RMSE with R² as context: MAE for robust interpretability in target units, RMSE when large misses cost more, R² for scale-free comparison — and quantile loss when the decision needs percentiles. I would add that each metric optimizes a different conditional statistic — median, mean, or quantile — so the metric must mirror the business cost, and the RMSE/MAE ratio is my quick outlier check.

