<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# What is a confusion matrix

> [!abstract] Short answer
> The confusion matrix is the **2×2 table of prediction outcomes** for a binary classifier: true positives, false positives, false negatives, true negatives. Every standard classification metric — accuracy, precision, recall, specificity, F1 — is a ratio of its cells, so the matrix is the ground truth from which all threshold-dependent numbers derive.

The name is the point: the matrix shows **how the model confuses classes** — which direction the errors flow. Two models with identical accuracy can have opposite error profiles (one misses positives, one raises false alarms), and only the matrix distinguishes them.

## The table and its descendants

```text
                    predicted +     predicted -
actual +       |        TP         |        FN        |
actual -       |        FP         |        TN        |

precision = TP/(TP+FP)   recall = TP/(TP+FN)
accuracy  = (TP+TN)/all  specificity = TN/(TN+FP)
F1 = 2·precision·recall/(precision+recall)
```

**Listing 1.** The four cells and the metrics they generate; multiclass extends the table to N×N, where the diagonal is correct and off-diagonal cells show which classes collapse into which — [[How do you handle class imbalance]] starts by reading this table.

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_te, pred, labels=[1, 0])
print(cm)  # [[TP, FN], [FP, TN]] with labels=[1, 0]
```

**Listing 2.** One caveat lives in this call: scikit-learn's default `labels` ordering puts class 0 first — stating the layout (`labels=[1,0]` → TP top-left) prevents the classic misreading.

## The operating point lives here

The matrix is **threshold-dependent**: every threshold gives a different table, and metric curves (ROC, PR) are traces across those tables: [[What is ROC AUC]], [[When is PR AUC better than ROC AUC]]. In review, demand the matrix at the production threshold with class counts — not accuracy alone. Cost-sensitive reading is the grown-up version: multiply cells by the business cost of each error type and the "best" model may change; the precision/recall trade discussion carries that decision: [[What is the difference between precision and recall]].

> [!warning] Interview trap
> "Accuracy is computed from the confusion matrix, so it is as informative." Accuracy collapses the matrix to one number and drowns under imbalance — 99% accuracy on 1% positives by always predicting negative shows a matrix full of FNs and almost nothing else. Second trap: transposed layouts — FN and FP swap under different label conventions; always state the axes and label order before reading aloud.

> [!tip] Interview answer
> The confusion matrix tabulates TP, FP, FN, TN at a given threshold — the raw material every classification metric is derived from. I read it at the production threshold, check which error direction dominates, extend it to per-class tables for multiclass, and convert cells to business costs before declaring a model better; curves like ROC and PR are just the matrix swept across thresholds.

