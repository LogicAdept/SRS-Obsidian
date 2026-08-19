<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Scope: prototype в singleton.**

Prototype-бин создастся один раз при инжекте. Решение: Provider<T>, ObjectFactory<T>, @Lookup.
