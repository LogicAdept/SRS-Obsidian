<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS

# What is an observation in machine learning

> [!abstract] Short answer
> An observation (also a **sample**, **example**, or **row**) is one measurement unit of your dataset: a full record of feature values, and a target if the setting is supervised. Models are trained on a collection of observations, and every data-quality disease — duplicates, leakage, drift — is defined at the level of observations.

The unit matters because it defines what "n" means and what counts as independence. If you have 10,000 clicks from 40 users, you do not have 10,000 independent observations — you have 40 users who produced correlated rows. Metrics computed as if rows were independent will be overconfident.

## Observation, feature, target

One observation is a vector `xᵢ = (xᵢ1, ..., xᵢp)` of feature values plus optionally a label `yᵢ`. Features are the columns describing each observation: [[What is a feature or predictor]]. The value you want to predict is the target: [[What is a target variable in machine learning]]. Stacking all observation rows gives the design matrix `X` of shape `n × p`: [[What is a design matrix]].

```text
        feature1  feature2  feature3   target
obs 1 |    0.8       24      "RU"        1
obs 2 |    1.2       19      "DE"        0
obs 3 |    0.5       31      "RU"        1
        (each row = one observation; columns = features)
```

**Listing 1.** A dataset as a table: each row is one observation, each column one feature, the rightmost column the target.

## Why the unit is an interview question

Because splitting, cross-validation, and drift monitoring all assume the unit is right. If the same user appears in both train and test sets, your score measures memorization, not generalization — group-based splits exist precisely for this. In time series the observation unit hides temporal order; a random shuffle destroys the evaluation, see [[What is a train validation test split]].

> [!warning] Interview trap
> "More rows always means more information." Only up to the number of genuinely independent units. Duplicated or near-duplicated observations inflate the dataset without adding signal, and they leak across splits. Ask "what is one observation here?" before quoting any metric — the answer changes what the metric means.

> [!tip] Interview answer
> An observation is a single example the model learns from or predicts on — one row of features, plus a label in supervised settings. I would add that identifying the true unit matters: correlated rows from the same user or the same day are not independent, and that assumption underlies splits, cross-validation, and every reported metric.

