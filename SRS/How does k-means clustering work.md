<!--
reps: 0
priority: 0
-->
#MachineLearning/Unsupervised #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How does k-means work?**

Assign points to nearest of k centroids, recompute means, repeat (minimize within-cluster SS). Needs k, spherical clusters, scale-sensitive. Init: k-means++. Elbow / silhouette for k. Mini-batch for scale. Not for arbitrary shapes → DBSCAN. Unsupervised; don't confuse with k-NN.
