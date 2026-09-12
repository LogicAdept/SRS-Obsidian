<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS

# What is the difference between XGBoost LightGBM and CatBoost

> [!abstract] Short answer
> All three are **industrial gradient-boosted-tree implementations** sharing the regularized, second-order objective; they differ in speed engineering, growth strategy, and — most visibly — categorical-feature handling. XGBoost: the reference implementation, exact and regularized. LightGBM: histogram binning plus leaf-wise growth, fastest on large data. CatBoost: ordered target statistics and ordered boosting, built for heavy categorical data and honest training.

## What they actually share

All three fit shallow trees to loss gradients with shrinkage, row/column subsampling, L1/L2 penalties on leaf weights, and early stopping — the objective is `loss + Ω(tree)` where Ω penalizes leaf count and leaf magnitudes, with second-order (Hessian) optimization: [[What is gradient boosting]]. Defaults differ, philosophy does not.

## The real differences

* **Binning and growth.** LightGBM histogram-bins features (GOSS/EFB tricks included) and grows **leaf-wise** — best-first by max gain — giving lower loss per tree but overfitting on small data without `num_leaves` control. XGBoost grows **level-wise** by default (hist mode available), CatBoost grows symmetric (oblivious) trees — same split per level, fast inference.
* **Categoricals.** XGBoost historically one-hot (native support added recently, still young). LightGBM offers Fisher-style native splits on category values. CatBoost's signature: **target statistics with permutations** — each row's encoding of a category uses only preceding rows (ordered target encoding), plus ordered boosting to fight the prediction-shift bias; this makes naive target-encoding leakage much less likely — the leakage topic in [[What is data leakage in machine learning]].
* **Scale and ecosystem.** LightGBM wins raw speed/memory on millions of rows; XGBoost has the deepest integration surface and distributed options; CatBoost excels out-of-the-box on categorical-heavy tabular problems with sensible defaults.

```python
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

xgb = XGBClassifier(n_estimators=500, learning_rate=0.05, max_depth=6,
                    subsample=0.8, colsample_bytree=0.8,
                    eval_metric="logloss", early_stopping_rounds=50)
lgbm = LGBMClassifier(n_estimators=1000, learning_rate=0.05, num_leaves=63)
cat = CatBoostClassifier(iterations=1000, learning_rate=0.05,
                         depth=6, cat_features=cat_cols, verbose=0)
```

**Listing 1.** The same recipe expressed three times; note `cat_features` — CatBoost takes raw category columns and handles the encoding internally.

> [!warning] Interview trap
> "LightGBM's leaf-wise growth is strictly better." It reaches lower loss per tree on big data, but on small datasets it overfits fast unless `num_leaves`/`min_data_in_leaf` are tightened — level-wise is the conservative default. Second trap: "native categorical handling means no leakage worry" — LightGBM's native splits still need care with rare categories and its target statistics settings; CatBoost's ordered scheme is the most defensively engineered, not a license to ignore validation discipline: [[What is a train validation test split]].

> [!tip] Interview answer
> All three implement regularized second-order gradient boosting; the differences are engineering and defaults. XGBoost is the mature reference with level-wise growth, LightGBM histogram-bins and grows leaf-wise for speed on large data, CatBoost uses ordered target statistics and symmetric trees, making it the safest on categorical-heavy data. In practice I pick by data size, categorical share, and ecosystem needs — and tune num_leaves, depth, and early stopping per library.

