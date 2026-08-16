<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чём разница JPA и Hibernate?**

JPA (Java Persistence API) — спецификация (интерфейсы и аннотации в пакете javax.persistence / jakarta.persistence). Hibernate — конкретная реализация. Альтернативы: EclipseLink, OpenJPA. Через JPA можно писать переносимый код, но в реальности почти всегда используют Hibernate-специфичные функции (например, @JoinFormula).
