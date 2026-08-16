<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How do you handle missing values?**

First: why missing (MCAR/MAR/MNAR). Simple: drop if rare; median/mode impute. Better: indicator of missingness + impute; iterative/KNN impute. Trees tolerate NaNs better than linear models. Don't impute with test statistics. Domain: 'missing' can be a feature.
