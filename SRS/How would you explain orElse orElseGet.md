<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чём разница orElse и orElseGet?**

orElse(value) — eager: значение вычисляется ВСЕГДА, даже если Optional не пустой. orElseGet(Supplier) — lazy: вызывается только если Optional пустой. Если default-значение получается дорогим вызовом — использовать orElseGet. Optional<User> user = repo.findById(id);
