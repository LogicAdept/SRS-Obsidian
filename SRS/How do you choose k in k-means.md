<!--
reps: 0
priority: 0
-->
#MachineLearning/Unsupervised #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How do you choose the number of clusters?**

Elbow of inertia, silhouette, domain k, stability across inits. No true k if clusters overlap. For business, interpretability beats a slightly better silhouette. Try several seeds (k-means++).
