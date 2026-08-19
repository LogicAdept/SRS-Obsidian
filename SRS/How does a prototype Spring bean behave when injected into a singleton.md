<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What happens if you inject a Prototype bean into a Singleton?**

Источник: https://habr.com/ru/articles/967632/

Подводный камень: Spring создаст только один экземпляр Prototype при создании Singleton, а не новый каждый раз.

**Prototype captured by singleton — fix?**

Resolved once. ObjectProvider, @Lookup, or scoped proxy for a new instance per use.
