<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**self-invocation.**

this.method() минует прокси → @Transactional/@Async/@Cacheable не работают. Решения: вынести метод в другой бин (рекомендуемый), инжектить self через @Lazy или ObjectProvider, использовать AspectJ compile-time weaving.
