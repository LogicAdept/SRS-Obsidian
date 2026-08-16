<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is an observation (example, row)?**

One training/serving instance: a feature vector x (and y if labeled). IID assumption is often false (users, time). Split by group/time to avoid leakage across observations of the same entity.
