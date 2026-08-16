<!--
reps: 0
priority: 0
-->
#Paradigms/Async #Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**@Async — что важно знать?**

Работает через прокси (как @Transactional) — не работает при self-invocation. Нужен @EnableAsync. Default executor может быть неподходящим — часто настраивают свой TaskExecutor.

**Чем @Async может удивить?**

Не работает self-invocation (как у @Transactional). Нужен @EnableAsync. Default executor может быть неподходящим — часто настраивают свой.
