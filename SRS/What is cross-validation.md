<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# What is cross-validation

> [!abstract] Short answer
> Cross-validation estimates generalization by **rotating the holdout**: split the training data into K folds, train on K−1, evaluate on the held-out fold, repeat so every fold serves once as the test, and average the scores. It buys a lower-variance estimate than a single split at K times the training cost.

The point is statistical: one 80/20 split gives one number with unknown variance — a lucky or unlucky split changes conclusions. Five-fold CV averages five such estimates and lets you see their spread. It is the standard engine for model selection and hyperparameter search — the tuning loop of [[What is hyperparameter tuning]] — because it reuses data efficiently when data is the scarce resource.

## The variants that matter

* **K-fold** — the plain rotation; K=5 or 10 is convention.
* **Stratified K-fold** — preserves class ratios in every fold; the default for classification, mandatory under imbalance: [[How do you handle class imbalance]].
* **GroupKFold / Leave-one-group-out** — whole groups (users, patients, sessions) held out together; the cure for correlated rows leaking across folds.
* **Time-series split** — folds walk forward in time; training must never see the future — random folds on temporal data are a leakage scandal waiting to happen: [[What is a train validation test split]].
* **Nested CV** — an inner loop for hyperparameter selection inside an outer loop for the honest estimate; the rigorous answer to "how good is the model selected this way".

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(RandomForestClassifier(n_estimators=200),
                         X_tr, y_tr, cv=cv, scoring="roc_auc")
print(scores.mean(), scores.std())
```

**Listing 1.** Report mean and standard deviation: the std is the split-sensitivity signal — large variance means small data or unstable modeling, not a good model.

## The leakage surface

Every data-dependent transformation must live **inside** the fold loop: scaling, imputation, feature selection, target encoding — fitted on the K−1 folds, applied to the held-out one; pipelines exist to enforce this mechanically. The final model after selection is refit on all training data; CV numbers then describe the *procedure*, not one fitted artifact — the distinction interviewers probe: [[What is overfitting]] applies to hyperparameter choices too, and preprocessing leakage is the classic silent score inflator: [[What is data leakage in machine learning]].

> [!warning] Interview trap
> "Cross-validation prevents overfitting." It detects and estimates — it does not prevent; selecting hyperparameters by CV on the same data can still overfit the folds, which is what nested CV addresses. Second trap: CV on time-ordered data with random shuffles — future information floods training folds; the honest estimate collapses, and the production surprise is total.

> [!tip] Interview answer
> Cross-validation rotates the holdout: train on K−1 folds, test on the last, average — a lower-variance generalization estimate than one split, at K times the cost. I use stratified folds for classification, group folds for clustered data, forward-chaining for time series, and keep every fitted transformation inside the loop via pipelines. I would add that CV estimates the procedure, the final model is refit on all training data, and nested CV is the answer when selection bias must be measured.

