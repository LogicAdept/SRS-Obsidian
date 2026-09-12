<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# When is PR AUC better than ROC AUC

> [!abstract] Short answer
> When the positive class is **rare** or false positives are expensive: PR AUC (area under precision-recall curve) focuses on the positive class only, so it stays informative where ROC AUC inflates. With 1% positives, a model can post ROC AUC 0.9 while its precision at useful recalls is garbage — the PR curve shows that immediately.

The arithmetic: ROC's FPR divides by the huge negative pool, so sweeping the threshold left adds few visible FPR points even while adding thousands of absolute false positives. Precision divides by everything flagged — its denominator feels every extra false alarm. Under imbalance, ROC is stable and flattering; PR is honest and punishing.

## The mechanics of the difference

* **ROC AUC** mixes both classes in its rates (TPR vs FPR) — baseline at 0.5 regardless of class ratio; class prevalence barely moves it.
* **PR AUC** involves no true-negative term — baseline sits near the prevalence (0.01 for 1% positives); a "good" PR AUC of 0.4 on rare positives can be excellent.
* Therefore: **PR AUC values are not comparable across datasets with different prevalence** — compare models within the same data, not PR numbers across problems.

```python
from sklearn.metrics import average_precision_score, roc_auc_score

probs = clf.predict_proba(X_te)[:, 1]
print(roc_auc_score(y_te, probs), average_precision_score(y_te, probs))
# imbalanced case: ROC 0.93 / AP 0.31 is a common, honest pairing
```

**Listing 1.** `average_precision_score` is sklearn's PR-AUC-style summary; when the two numbers diverge this much, the ROC figure is the flattering one.

## The decision rule

Fraud, click-through, defect detection, disease screening — positives rare and alarms costly → report PR AUC (plus precision/recall at the operating point: [[What is the difference between precision and recall]]). Balanced classes or ranking tasks where both error types matter symmetrically → ROC AUC is fine and more stable. Either way the operating threshold comes from the curve against business cost, not from the metric's single number; the confusion-matrix grounding is in [[What is a confusion matrix]], the split discipline in [[What is a train validation test split]].

> [!warning] Interview trap
> "PR AUC is always better than ROC AUC." It is more informative under imbalance, but noisier with tiny positive counts (the curve jitters with few positives) and its values shift with prevalence — ROC remains the better cross-prevalence ranking summary. Second trap: quoting PR AUC without stating prevalence — the same number means different things at 1% and 20% positives.

> [!tip] Interview answer
> PR AUC wins when positives are rare and false alarms are costly, because precision absorbs every extra false positive while ROC's FPR hides them in the huge negative base rate. I would report both under imbalance, read PR AUC against the prevalence baseline, and never compare PR numbers across datasets with different class ratios — then set the threshold on the curve against business cost.

