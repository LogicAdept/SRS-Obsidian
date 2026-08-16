<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**JOIN FETCH vs @EntityGraph?**

JOIN FETCH in JPQL loads associations in one query (watch cartesian product on multiple collections). @EntityGraph (named or ad-hoc) declares fetch plan without stuffing JPQL; works with findBy methods. Both must run inside a transaction if you still navigate more lazies later.
