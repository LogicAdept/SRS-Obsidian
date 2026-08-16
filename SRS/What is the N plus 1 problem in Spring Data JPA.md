<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is the N+1 problem and how do you fix it?**

Load a list of N parents (1 query), then each lazy collection/association triggers another query (N). Symptoms: slow endpoint, many identical SELECTs in logs. Fixes: JOIN FETCH / entity graph, @BatchSize, DTO projection / @Query constructor expression, batch fetching. Don't blindly switch to EAGER. Don't return entities from controllers (Jackson + OSIV makes N+1 worse).
