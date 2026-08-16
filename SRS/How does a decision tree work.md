<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How does a decision tree split?**

Greedy recursive splits maximizing information gain / Gini (class) or variance reduction (reg). Unbounded depth overfits. Insensitive to monotone scaling. Can't extrapolate below/above seen leaf averages. Feature importance via impurity decrease. Regularize: max_depth, min_samples_leaf, pruning.
