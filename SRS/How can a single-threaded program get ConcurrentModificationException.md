<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Fail-fast vs fail-safe итераторы.**

Fail-fast (HashMap, ArrayList) кидают ConcurrentModificationException при изменении коллекции. Fail-safe (ConcurrentHashMap, CopyOnWriteArrayList) работают со снимком.
