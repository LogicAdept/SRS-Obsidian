<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**XGBoost vs LightGBM vs CatBoost?**

XGBoost: level-wise, exact/approx splits, classic default. LightGBM: leaf-wise, histogram, fast on large data, risk of over-deep leaves. CatBoost: ordered boosting, strong categorical handling, less target leakage on cats. All GBDT; pick by categoricals, speed, and CV, not brand loyalty.
