<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is the persistence context / L1 cache?**

Per persistence context (typically per @Transactional). Same id → same instance, dirty checking at flush. No L1 across transactions. Second-level cache is optional (shared, needs setup). clear()/saveAndFlush confusion is a common follow-up. save() vs persist() vs merge() still asked.
