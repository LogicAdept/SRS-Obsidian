<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**MSE vs MAE vs RMSE vs R²?**

MAE: median-ish, robust to outliers. MSE/RMSE: penalize large errors, same units as y for RMSE. R²: fraction of variance explained, can be negative. MAPE: unstable near zero. Pick by business (absolute $ vs relative %). Log-transform skewed targets.
