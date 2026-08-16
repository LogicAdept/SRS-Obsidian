<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**save vs persist vs merge?**

Spring Data save(): persist if new, merge if detached — merge copies state and can surprise you (lost updates, extra SELECTs). persist() only for new managed entities. saveAll is not always one batch; need jdbc.batch_size and order_inserts. Interviewers use this after N+1.
