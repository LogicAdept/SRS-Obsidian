<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Lazy vs Eager загрузка.**

Lazy — связь подгружается только при обращении (прокси). Eager — сразу в SELECT. Default для @OneToMany и @ManyToMany — Lazy, для @ManyToOne и @OneToOne — Eager.

**Что лучше — Lazy или Eager?**

Lazy. Eager почти всегда плохо — Hibernate тянет лишнее, и часто это даёт N+1 в неожиданном месте. Правило: ставь Lazy везде, а конкретный JOIN FETCH делай в запросах, где данные действительно нужны.
