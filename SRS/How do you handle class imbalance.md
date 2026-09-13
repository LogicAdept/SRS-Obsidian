<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# How do you handle class imbalance

> [!abstract] Short answer
> Imbalance breaks the **default objectives and default metrics**, not the math: accuracy becomes meaningless (predict-all-negative scores 99% at 1% positives). Handle it with the right metric (PR-based: [[When is PR AUC better than ROC AUC]]), loss reweighting or resampling so the minority class matters, threshold tuning to the business cost, and algorithms with native imbalance support — in that order of preference.

## The toolbox, in order of preference

1. **Fix the metric first:** precision/recall at the operating point, PR AUC, and per-class confusion matrices: [[What is a confusion matrix]]. No model change fixes a wrong ruler.
2. **Class weights in the loss:** `class_weight="balanced"` in scikit-learn, pos_weight in focal/BCE losses — upweight minority errors without touching the data distribution; usually the cleanest lever.
3. **Resampling if weights are unavailable:** oversample the minority (SMOTE-style synthesis has interpolation pathologies — prefer simple random over- or under-sampling as a baseline) — applied **inside the training folds only**: [[What is cross-validation]].
4. **Threshold tuning:** train normally, then move the decision threshold along the PR curve to the cost-optimal point — often the highest-leverage, most forgotten step: [[What is the difference between precision and recall]].
5. **Native support:** boosting libraries expose scale_pos_weight and balanced growth options — [[What is the difference between XGBoost LightGBM and CatBoost]]; anomaly-detection framing (isolation forests, one-class) when positives are essentially absent.

```python
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(class_weight="balanced", max_iter=1000).fit(X_tr, y_tr)
probs = clf.predict_proba(X_te)[:, 1]
# then pick the threshold from the PR curve against business cost — not 0.5
```

**Listing 1.** Reweight, score by probabilities, and choose the threshold deliberately — the three-step imbalance posture that beats exotic sampling tricks in most reviews.

## What actually goes wrong

Fitting the resampled or reweighted model and then reporting **accuracy** — the metric change is the whole game. Applying SMOTE before the train/test split — synthetic copies of test-adjacent rows leak: [[What is data leakage in machine learning]]. Treating extreme imbalance (1:100 000) as a classification problem at all — it is often anomaly detection or ranking. And confusing imbalance with insufficient signal: if the minority class has too few *examples*, no reweighting conjures information — collect more minority data.

> [!warning] Interview trap
> "Always SMOTE." Synthetic interpolation can fabricate implausible points in categorical or sparse spaces and inflates scores when done pre-split; class weights plus threshold tuning beat it in most real pipelines. Second trap: "the model is biased against the minority class" — often the model is fine and the threshold is default 0.5; check the PR curve before touching the training procedure.

> [!tip] Interview answer
> I fix the metric first — PR-based, at an explicitly chosen threshold — then reweight the loss (class weights or pos_weight), resample only inside training folds if needed, and use learners with native imbalance support. For extreme rarity I reframe as anomaly detection. The two sins I watch for are accuracy as a headline and any resampling done before the split.

