<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why is gradient boosting called gradient?**

Each new tree is trained on the negative gradient of the loss w.r.t. current predictions (residuals for MSE). Shrinkage (learning rate) × many trees. Early stopping on val. XGBoost/LightGBM/CatBoost are the production implementations. Yes, you can overfit boosting; bagging less so.
