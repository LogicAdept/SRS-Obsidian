<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**Why does @Transactional fail on a self-invocation from @PostConstruct?**

Источник: https://habr.com/ru/articles/967632/

Spring создаёт прокси для @Transactional. Вызов processPayment() из init() того же класса идёт мимо прокси — interceptor не срабатывает.
BeanPostProcessors применяются до @PostConstruct, но внутренний this-вызов всё равно без прокси. Обходы: вынести метод в другой бин; self-injection через @Lazy; ApplicationContext.getBean(...). Предпочтительнее отдельный бин.

**Self-invocation and REQUIRES_NEW?**

this.method() skips the proxy; inner @Transactional including REQUIRES_NEW is ignored. Split beans or self-inject @Lazy.
