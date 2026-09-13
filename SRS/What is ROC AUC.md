<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# What is ROC AUC

> [!abstract] Short answer
> ROC AUC is the **area under the curve of true-positive rate versus false-positive rate** as the decision threshold sweeps. It answers: "if I draw one positive and one negative example at random, how often does the model score the positive higher?" — 0.5 is coin-flipping, 1.0 is perfect ranking.

The probabilistic reading is the interview gold: AUC is threshold-free ranking quality. It does not care where you put the threshold or how the classes are scored — only that positives outrank negatives. That is both its strength (comparability across thresholds) and its blindness (no operating point, no calibration).

## Reading the curve

TPR = recall = TP/(TP+FN); FPR = FP/(FP+TN) — note the denominators: TPR conditions on actual positives, FPR on actual negatives. The diagonal is chance; the curve bows toward the top-left for better models. AUC is a **global summary**; two models with the same AUC can have very different curves — one better at low FPR, which is the region that usually matters in practice.

```python
from sklearn.metrics import roc_auc_score, roc_curve

probs = clf.predict_proba(X_te)[:, 1]
print(roc_auc_score(y_te, probs))          # ranking quality, threshold-free
fpr, tpr, thr = roc_curve(y_te, probs)     # pick an operating point from here
```

**Listing 1.** AUC for reporting, `roc_curve` for choosing the actual threshold — the metric ranks, the business picks the point.

## When AUC misleads

With heavy class imbalance, FPR's denominator (huge negatives) hides false-alarm volume: an FPR of 1% on a million negatives is ten thousand false alarms — the PR view exposes this: [[When is PR AUC better than ROC AUC]]. AUC also ignores calibration: a model can rank perfectly and still output probabilities that are all doubled — for probability-sensitive decisions you need calibration metrics (Brier score, reliability curves). And AUC is insensitive to the cost asymmetry between error types — the precision/recall framing carries that: [[What is the difference between precision and recall]]. Evaluation split discipline: [[What is a train validation test split]].

> [!warning] Interview trap
> "AUC 0.9 means the model is 90% accurate." No — accuracy is threshold-dependent and class-mix-dependent; AUC is a ranking score with a coin-flip baseline of 0.5, not a percentage of correct answers. Second trap: comparing AUC across datasets with different class ratios — the same model can show different AUC when the negative pool changes.

> [!tip] Interview answer
> ROC AUC is the area under TPR-versus-FPR across thresholds, equivalently the probability that a random positive outranks a random negative — a threshold-free measure of ranking quality. I would state the 0.5 baseline, its blindness to calibration and to error costs, and that under heavy imbalance I report PR AUC alongside, then choose the operating point on the curve against business costs.

