<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# What is a train validation test split

> [!abstract] Short answer
> Three disjoint datasets with three jobs: **train** fits the model, **validation** selects among models and hyperparameters, **test** gives the final, untouched estimate of production performance. The split is the physical implementation of the promise "the model never saw what it is scored on".

The validation set is the working judge during development — it decides checkpoints, early stopping, architectures. Because you look at validation scores many times and act on them, validation performance drifts optimistic — that is exactly why test exists and must be touched once, at the end, ideally by an automated pipeline rather than a curious human: [[What is overfitting]] applies to your decisions, not only to gradient descent.

## How to split — the unit question

Random rows are only valid if rows are independent and identically distributed. They rarely are:

* **Grouped data** (multiple rows per user/patient/session) — split by group, or the same entity in train and test turns the score into memorization: [[What is an observation in machine learning]].
* **Temporal data** — split by time: train on the past, validate and test on the future; random shuffling leaks the future and overstates everything.
* **Imbalanced classes** — stratify so class ratios survive in all three sets: [[How do you handle class imbalance]].

```python
from sklearn.model_selection import train_test_split

X_tr, X_tmp, y_tr, y_tmp = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=0)
X_val, X_te, y_val, y_te = train_test_split(
    X_tmp, y_tmp, test_size=0.5, stratify=y_tmp, random_state=0)
# 70 / 15 / 15; when data is scarce, cross-validation replaces the middle loop
```

**Listing 1.** The canonical 70/15/15 via two stratified splits; with little data, the validation loop becomes cross-validation on the training portion: [[What is cross-validation]] — and the test set stays sealed either way.

## Discipline that keeps the numbers honest

Fit **all** preprocessing on train only, transform the others frozen — scalers, imputers, encoders, feature selection: [[What is data leakage in machine learning]]. The test set is consumed once per model generation; repeated "final" evaluations turn it into a second validation set and need a fresh replacement. Sizes: enough test rows that the metric's confidence interval is narrower than the differences you claim; with tiny data, report uncertainty rather than a third decimal.

> [!warning] Interview trap
> "Validation and test are interchangeable names." They are different jobs: validation is consumed continuously by selection and is therefore optimistic; test is the once-only estimate. Second trap: splitting time series randomly "for balance" — any metric from that split is fiction; the production gap will teach the lesson expensively.

> [!tip] Interview answer
> Train fits, validation selects, test certifies — and the split unit must respect the data: groups stay whole, time moves forward, classes stay stratified. All preprocessing is fitted on train and replayed frozen on the other sets. Validation gets consumed by my decisions, so test is sealed until the end; when data is scarce the selection loop becomes cross-validation, but a final untouched estimate never stops being mandatory.

