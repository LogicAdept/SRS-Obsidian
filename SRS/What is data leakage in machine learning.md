<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS

# What is data leakage in machine learning

> [!abstract] Short answer
> Data leakage is **information from outside the legitimate training moment reaching the model or the evaluation** — features that encode the answer (target leakage) or evaluation data that influenced fitting (train-test contamination). Its signature: offline metrics are excellent and production is mysteriously mediocre. It is the most expensive silent bug in ML.

Target leakage means a feature that would not exist at prediction time but correlates with the label — the refund amount when predicting refunds, post-outcome aggregates, the timestamp of the event you predict. Contamination means the test set influenced training directly (fitting preprocessing on the full dataset) or indirectly (tuning on test, duplicated rows across splits, temporal overlap).

## The classic catalog

* **Post-outcome features:** anything computed with knowledge that the event happened — refunds, cancellations, diagnoses after admission.
* **Future information via joins:** aggregations over windows that extend past the prediction snapshot; the fix is point-in-time correctness — every feature value must be computable from data existing strictly before the prediction moment.
* **Preprocessing on the full dataset:** scalers, imputers, encoders, feature selectors fitted on train+test — statistics of the test rows leak into training: [[What is a design matrix]].
* **Split violations:** same user in train and test ([[What is an observation in machine learning]]), random shuffles on temporal data, resampling before splitting: [[How do you handle class imbalance]].
* **Selection leakage:** hyperparameters and features chosen by test-set performance — the test set becomes a training set: [[What is hyperparameter tuning]].

```python
# WRONG:  scaler.fit(X)  then split
# RIGHT:  fit on train, transform both
scaler.fit(X_tr)
X_tr_s, X_te_s = scaler.transform(X_tr), scaler.transform(X_te)
# or let the pipeline enforce it:
from sklearn.pipeline import make_pipeline
pipe = make_pipeline(scaler, clf).fit(X_tr, y_tr)
```

**Listing 1.** The mechanical half of prevention: fit transformations on training folds only — pipelines make the correct order the only order.

## Detection and culture

Treat a too-good score as evidence, not victory: if a simple model beats domain baselines by an implausible margin, hunt the leak before celebrating. Audit features with the question "would this exist at scoring time, computed only from the past?"; temporal backtesting ("train on month 1, predict month 2") exposes both target leakage and split violations. In production, the complement of leakage is train/serve skew — the same feature must be computed identically offline and online: [[What is MLOps]], [[How do you monitor a model in production]].

> [!warning] Interview trap
> "Leakage only happens to careless juniors." The devastating cases are institutional: a shared feature store that quietly backfills today's aggregates onto historical rows, an id column that encodes time, a deduplication that ran before the split. Second trap: "we use pipelines, so we are safe" — pipelines fix preprocessing order, not temporal snapshots, not target-derived features, not group splits.

> [!tip] Interview answer
> Leakage is answer information reaching the model or the evaluation: post-outcome features, future-window aggregates, preprocessing fitted on all data, split violations, or tuning on test. I prevent it with point-in-time feature correctness, fitted-on-train-only transformations via pipelines, group and time-aware splits, and a sealed test set. My strongest signal is a suspiciously excellent offline score — I audit for leaks before I believe it.

