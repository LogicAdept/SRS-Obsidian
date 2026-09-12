<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# How do you handle missing data in machine learning

> [!abstract] Short answer
> First diagnose **why** values are missing — completely at random, depending on other features, or depending on the target — then choose: drop rows or columns only when the loss is small, impute with statistics or model-based methods, or use algorithms that handle missingness natively. The mechanism, not the tool, decides the strategy; and the missingness itself is often a feature.

MCAR (missing completely at random) tolerates simple deletion. MAR (missing given other observed features) tolerates imputation conditioned on those features. MNAR (missing because of the value or the target — e.g. income missing for high earners) is the dangerous one: naive handling biases the model, and the missingness indicator becomes genuine signal.

## The escalation ladder

1. **Understand the mechanism:** compare distributions of missingness across the target and features; a missing-rate that differs by class is informative, not noise.
2. **Simple statistical imputation:** median/mean for numeric, mode or "missing" category for categorical. Fast, robust baseline; shrinks variance.
3. **Model-based imputation:** KNN-imputer or iterative imputation (MICE-style, `sklearn.impute.IterativeImputer`) — predict missing cells from other cells; better when features are correlated.
4. **Missingness-aware models:** gradient boosting libraries (XGBoost/LightGBM/CatBoost) route missing values down a learned default branch; trees with `missing` support exist — see [[What is the difference between XGBoost LightGBM and CatBoost]].
5. **Flag it:** add `was_missing` boolean features when missingness could correlate with the target.

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

pre = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), num_cols),
    ("cat", SimpleImputer(strategy="constant", fill_value="missing"), cat_cols),
])
# plus: df["amount_was_missing"] = df["amount"].isna().astype(int)
```

**Listing 1.** A leakage-safe baseline: median for numerics, an explicit "missing" category for categoricals, and an indicator feature — all fitted inside the pipeline so imputation statistics come from training folds only.

## The two cardinal rules

Fit imputers on training data only and apply them frozen at validation/serving time — an imputer fitted on the full dataset leaks future statistics. And deletion decisions must respect the missingness mechanism: dropping MNAR rows silently removes a subpopulation. Everything must be replayed identically in production — the pipeline discipline of [[What is MLOps]] — and the split rules of [[What is a train validation test split]] apply to imputation fitting too.

> [!warning] Interview trap
> "Just fill with the mean." It distorts correlations, shrinks variance, and is actively wrong under MNAR — plus a mean imputer fitted on train+test is leakage. Another trap: filling numeric NaN with 0 when 0 is a real value (zero spend vs no record are different facts); the missingness indicator separates them.

> [!tip] Interview answer
> I first classify the missingness mechanism, because MCAR, MAR, and MNAR need different treatment. My default ladder: median and explicit-missing-category imputation with a missingness flag, model-based imputation when features are correlated, and boosting models with native missing handling when available. The two disciplines are fitting imputers inside the training folds only and keeping the same transform frozen in production.

