<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Records в Java — что это?**

Java 14+: компактный immutable data-класс. record User(String name, int age) {} — автоматически: конструктор, getters (name(), age()), equals, hashCode, toString. Нельзя наследовать (implicitly final). Можно реализовывать интерфейсы. Идеально для DTO в тестах.
